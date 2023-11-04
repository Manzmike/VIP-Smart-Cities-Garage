#include <stdio.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <unistd.h>

#define SENSOR1_ADDR 0x70  // Replace with the actual address of your sensor
#define SENSOR2_ADDR 0x71  // Replace with the actual address of your sensor

int main() {
    int file;
    char *bus = "/dev/i2c-1"; // I2C bus 1
    if ((file = open(bus, O_RDWR)) < 0) {
        printf("Failed to open the bus.\n");
        return 1;
    }

    int addresses[] = {SENSOR1_ADDR, SENSOR2_ADDR};
    int num_sensors = 2;
    
    for(int i = 0; i < num_sensors; i++) {
        int addr = addresses[i];
        if (ioctl(file, I2C_SLAVE, addr) < 0) {
            printf("Failed to acquire bus access and/or talk to sensor.\n");
            return 1;
        }
        
        char buf[2] = {0};
        if (read(file, buf, 2) != 2) {
            printf("Failed to read from the sensor.\n");
        } else {
            int distance = (buf[0] << 8) + buf[1];
            printf("Sensor %d Distance: %d cm\n", i, distance);
        }
    }

    close(file);
    return 0;
}
