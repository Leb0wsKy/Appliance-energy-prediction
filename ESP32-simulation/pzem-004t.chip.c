#include "wokwi-api.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef struct {
  uart_dev_t uart0;
} chip_state_t;

void send_data(chip_state_t *chip);

uint16_t calculate_crc(uint8_t *data, uint8_t length) {
    uint16_t crc = 0xFFFF;
    for (int pos = 0; pos < length; pos++) {
        crc ^= (uint16_t)data[pos];
        for (int i = 8; i != 0; i--) {
            if ((crc & 0x0001) != 0) {
                crc >>= 1;
                crc ^= 0xA001;
            } else {
                crc >>= 1;
            }
        }
    }
    return crc;
}

void chip_init(void) {
    static chip_state_t chip;
    const uart_config_t uart_config = {
        .tx = pin_init("TX", INPUT_PULLUP),
        .rx = pin_init("RX", INPUT),
        .baud_rate = 9600,
        .write_done = NULL,
        .user_data = &chip,
    };
    chip.uart0 = uart_init(&uart_config);

    send_data(&chip);
}

void send_data(chip_state_t *chip) {
    uint8_t data[25];
    int idx = 0;

    // Header
    data[idx++] = 0x01;  // Address
    data[idx++] = 0x04;  // Function code
    data[idx++] = 0x14;  // Byte count

    // Simulated data: voltage, current, power, energy, frequency, pf
    uint16_t simulated_values[] = {235, 5, 1175, 123, 50, 99};
    for (int i = 0; i < 6; i++) {
        data[idx++] = simulated_values[i] >> 8;
        data[idx++] = simulated_values[i] & 0xFF;
    }

    // Calculate CRC
    uint16_t crc = calculate_crc(data, idx);
    data[idx++] = crc & 0xFF;
    data[idx++] = crc >> 8;

    uart_write(chip->uart0, data, idx);
    printf("Data packet sent\n");
}
