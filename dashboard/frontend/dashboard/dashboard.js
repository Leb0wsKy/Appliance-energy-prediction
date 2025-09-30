let globalChart, refrigerationChart, climatisationChart, informatiqueChart, barChart, pieChart;
let lastIndex = -1;
const API_URL = "http://localhost:5000/api/measurements";
const userId = "68d8592d6cd53946712b109b";
document.addEventListener("DOMContentLoaded", () => {
    const isLoggedIn = localStorage.getItem("loggedIn");
    if (!isLoggedIn) {
        window.location.href = "../login_register/login.html";
        return;
    }

    document.getElementById("userName").textContent = localStorage.getItem("userName") || "admin";
    document.getElementById("userEmail").textContent = localStorage.getItem("userEmail") || "admin@domain.com";

    loadCharts();
});
const ctxGlobal = document.getElementById("globalChart").getContext("2d");
const ctxRefrigeration = document.getElementById("fridgeChart").getContext("2d");
const ctxClimatisation = document.getElementById("climatisationChart").getContext("2d");
const ctxInformatique = document.getElementById("informatiqueChart").getContext("2d");
const ctxBar = document.getElementById("barChart").getContext("2d");
const ctxPie = document.getElementById("pieChart").getContext("2d");
const userName = localStorage.getItem("userName") || "admin";
const userEmail = localStorage.getItem("userEmail") || "admin@domain.com";
document.getElementById("userName").textContent = userName;
document.getElementById("userEmail").textContent = userEmail;

const TOTAL_API_URL = `http://localhost:5000/api/total-consumption/${userId}`;

const totalDiv = document.getElementById("totalConsumption"); 
const pricingDiv = document.getElementById("pricing"); 

async function updateTotalConsumption() {
    try {
        const res = await fetch(TOTAL_API_URL);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        
        const data = await res.json();
        const totalKWh = data.totalConsumption_kWh;
        console.log("Total consumption data:", totalKWh);

        totalDiv.textContent = `${totalKWh.toFixed(2)} kWh`;
        const tranches = [
            { max: 200, price: 176 },  
            { max: 300, price: 218 },  
            { max: 500, price: 341 },  
            { max: Infinity, price: 414 }
        ];

        const redevanceKVA = 700; 
        const surtaxeMunicipale = 5; 
        const fte = 5; 
        const tva = totalKWh > 300 ? 0.13 : 0.07;

        let remainingKWh = totalKWh;
        let priceHT = 0;

        for (const tranche of tranches) {
            const trancheKWh = Math.min(remainingKWh, tranche.max);
            if (trancheKWh <= 0) continue;

            priceHT += trancheKWh * (tranche.price + surtaxeMunicipale + fte) / 1000; 
            remainingKWh -= trancheKWh;
        }

        priceHT += redevanceKVA / 1000;

        const priceTTC = priceHT * (1 + tva);

        if (pricingDiv) {
            pricingDiv.textContent = ` ${priceTTC.toFixed(2)} TND`;
        }

    } catch (err) {
        console.error("Erreur fetch total consumption:", err);
        totalDiv.textContent = "Erreur lors de la récupération de la consommation totale.";
        if (pricingDiv) {
            pricingDiv.textContent = "Erreur estimation prix.";
        }
    }
}


updateTotalConsumption();

setInterval(updateTotalConsumption, 5000);

async function loadCharts() {
    try {
        const res = await fetch(`${API_URL}?userId=${userId}`);
        const data = await res.json();
        if (!data.length) return;

        const labels = data.map(m => new Date(m.timestamp).toLocaleTimeString());
        const globalValues = data.map(m => m.globalConsumption);
        const refrigerationValues = data.map(m => m.measurements.Refrigeration);
        const climatisationValues = data.map(m => m.measurements.Climatisation);
        const informatiqueValues = data.map(m => m.measurements.AppareilInformatique);

        globalChart = new Chart(ctxGlobal, {
            type: "line",
            data: { labels, datasets:[{label:"Global Consumption", data:globalValues, borderColor:"blue", backgroundColor:"rgba(0,0,255,0.2)", fill:true, tension:0.4}]},
            options:{ responsive:true, scales:{ x:{ title:{ display:true, text:"Timestamp" } } } }
        });

        refrigerationChart = new Chart(ctxRefrigeration, {
            type: "line",
            data: { labels, datasets:[{label:"EBE", data:refrigerationValues, borderColor:"red", backgroundColor:"rgba(255,0,0,0.2)", fill:true, tension:0.4}]},
            options:{ responsive:true, scales:{ x:{ title:{ display:true, text:"Timestamp" } } } }
        });

        climatisationChart = new Chart(ctxClimatisation, {
            type: "line",
            data: { labels, datasets:[{label:"B2E", data:climatisationValues, borderColor:"green", backgroundColor:"rgba(0,255,0,0.2)", fill:true, tension:0.4}]},
            options:{ responsive:true, scales:{ x:{ title:{ display:true, text:"Timestamp" } } } }
        });

        informatiqueChart = new Chart(ctxInformatique, {
            type: "line",
            data: { labels, datasets:[{label:"TVE", data:informatiqueValues, borderColor:"orange", backgroundColor:"rgba(255,165,0,0.2)", fill:true, tension:0.4}]},
            options:{ responsive:true, scales:{ x:{ title:{ display:true, text:"Timestamp" } } } }
        });

        const last = data[data.length - 1];

        barChart = new Chart(ctxBar, {
            type:"bar",
            data:{
                labels:["EBE","B2E","TVE"],
                datasets:[{label:"Current Consumption", data:[last.measurements.Refrigeration, last.measurements.Climatisation, last.measurements.AppareilInformatique], backgroundColor:["red","green","orange"]}]
            },
            options:{ responsive:true, scales:{ y:{ beginAtZero:true } } }
        });

        pieChart = new Chart(ctxPie, {
            type:"pie",
            data:{
                labels:["EBE","B2E","TVE"],
                datasets:[{data:[last.measurements.Refrigeration, last.measurements.Climatisation, last.measurements.AppareilInformatique], backgroundColor:["red","green","orange"]}]
            },
            options:{ responsive:true }
        });

        lastIndex = data.length - 1;

    } catch(err) {
        console.error("Erreur fetch measurements:", err);
    }
}

async function addNewPoint() {
    try {
        const res = await fetch(`${API_URL}?userId=${userId}`);
        const data = await res.json();
        if (!data.length) return;

        const currentIndex = data.length - 1;
        if (currentIndex > lastIndex) {
            const newPoint = data[currentIndex];
            const label = new Date(newPoint.timestamp).toLocaleTimeString();

            globalChart.data.labels.push(label);
            globalChart.data.datasets[0].data.push(newPoint.globalConsumption);
            globalChart.update();

            refrigerationChart.data.labels.push(label);
            refrigerationChart.data.datasets[0].data.push(newPoint.measurements.Refrigeration);
            refrigerationChart.update();

            climatisationChart.data.labels.push(label);
            climatisationChart.data.datasets[0].data.push(newPoint.measurements.Climatisation);
            climatisationChart.update();

            informatiqueChart.data.labels.push(label);
            informatiqueChart.data.datasets[0].data.push(newPoint.measurements.AppareilInformatique);
            informatiqueChart.update();

            barChart.data.datasets[0].data = [
                newPoint.measurements.Refrigeration,
                newPoint.measurements.Climatisation,
                newPoint.measurements.AppareilInformatique
            ];
            barChart.update();

            pieChart.data.datasets[0].data = [
                newPoint.measurements.Refrigeration,
                newPoint.measurements.Climatisation,
                newPoint.measurements.AppareilInformatique
            ];
            pieChart.update();

            lastIndex = currentIndex;
        }
    } catch(err) {
        console.error("Erreur fetch new point:", err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadCharts();
    setInterval(addNewPoint, 5000);
});
