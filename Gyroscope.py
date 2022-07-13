import smbus  # import SMBus module of I2C
from time import sleep  # import
import math
from screen import write_text



# some MPU6050 Registers and their Address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
Device_Address_MPU = 0x68  # MPU6050 device address


def MPU_Init():
    # write to sample rate register
    bus.write_byte_data(Device_Address_MPU, SMPLRT_DIV, 7)

    # Write to power management register
    bus.write_byte_data(Device_Address_MPU, PWR_MGMT_1, 1)

    # Write to Configuration register
    bus.write_byte_data(Device_Address_MPU, CONFIG, 0)

    # Write to Gyro configuration register
    bus.write_byte_data(Device_Address_MPU, GYRO_CONFIG, 24)

    # Write to interrupt enable register
    bus.write_byte_data(Device_Address_MPU, INT_ENABLE, 1)


def read_raw_data_MPU(addr):
    # Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address_MPU, addr)
    low = bus.read_byte_data(Device_Address_MPU, addr + 1)

    # concatenate higher and lower value
    value = ((high << 8) | low)

    # to get signed value from mpu6050
    if (value > 32768):
        value = value - 65536
    return value

#odczyt zmiany położenia kątowego modelu w osi x i osi y
def read_turn():
    Gx_current = 0
    Gy_current = 0
    stop = False
    text = ""

    for i in range(40):

        # Read Gyroscope raw value
        gyro_x = read_raw_data_MPU(GYRO_XOUT_H)
        gyro_y = read_raw_data_MPU(GYRO_YOUT_H)
        gyro_z = read_raw_data_MPU(GYRO_ZOUT_H)

        # Full scale range +/- 250 degree/C as per sensitivity scale factor
        Gx = gyro_x / 131.0
        Gy = gyro_y / 131.0
        Gz = gyro_z / 131.0

        #aktualizacja maksymalnego dokonanego wychylenia w danej osi
        Gx_current = Gx_current + Gx
        Gy_current = Gy_current + Gy

        #pomocnicze printy do podglądu na żywo na komputerze:
        # print("Gx=%.2f" % Gx, u'\u00b0' + "/s", "\tGy=%.2f" % Gy, u'\u00b0' + "/s", "\tGz=%.2f" % Gz, u'\u00b0' + "/s")
        #print("Gx_curr:", int(Gx_current), "Gy_curr:", int(Gy_current))

        #Warunki określające położenie
        if (Gx >= 50) or (Gx_current >= 50):
            text = "Down"
            stop = True
        elif (Gx <= -50) or (Gx_current <= -50):
            text = "Up"
            stop = True
        elif (Gy >= 50) or (Gy_current >= 50):
            text = "Right"
            stop = True
        elif (Gy <= -50) or (Gy_current <= -50):
            text = "Left"
            stop = True
        else:
            text = "Nothing"

        if stop == False:
            sleep(0.1)
        else:
            break
    # koniec petli
    return text

#Main code
bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards

MPU_Init()
