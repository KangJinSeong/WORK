import serial
import RPi.GPIO as GPIO
class UART_HAT:
    def __init__(self):
        self.PICO_baudreate = 9600
        self.PICO_PORT = '/dev/ttyAMA2'
        self.PICO_UART = serial.Serial(self.PICO_PORT, self.PICO_baudreate)
        self.PICO_EN = 17   #Pin 11 , J22 CONN


        self.FPGA_baudreate = 115200
        self.FPGA_PORT = '/dev/ttyAMA1'
        self.FPGA_UART = serial.Serial(self.FPGA_PORT, self.FPGA_baudreate)
        self.FPGA_EN = 22   #Pin 15

        self.FPGA_Version = ''.join([chr(i) for i in [0x3E,0x35,0x40,0x30,0x0D]])
        self.FPGA_Temp = ''.join([chr(i) for i in [0x3E,0x35,0x54,0x30,0x0D]])
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PICO_EN, GPIO.OUT)
        GPIO.setup(self.FPGA_EN, GPIO.OUT)
        GPIO.output(self.PICO_EN, False)
        GPIO.output(self.FPGA_EN, False)
        GPIO.setwarnings(False)

    def PICO_Dat_analysis(self):
        data = self.PICO_UART.readline()
        Data = data.decode()
        return Data

    def FPGA_ECO_Dat_analysis(self):

        data = self.FPGA_UART.read(5)
        Data = data.decode()
        return Data
    
    def FPGA_Dat_analysis(self):
        data = self.FPGA_UART.readline()
        Data = data.decode()
        return Data
    def FPGA_Put_Version(self):
        GPIO.output(self.FPGA_EN, True)
        self.FPGA_UART.write(self.FPGA_Version.encode())
        GPIO.output(self.FPGA_EN, False)
    def FPGA_Put_Temp(self):
        GPIO.output(self.FPGA_EN, True)
        self.FPGA_UART.write(self.FPGA_Temp.encode())
        GPIO.output(self.FPGA_EN, False)
    def FPGA_Put_TX(self, FPGA_TX):
        GPIO.output(self.FPGA_EN, True)
        self.FPGA_UART.write(str(FPGA_TX).encode())
        GPIO.output(self.FPGA_EN, False)      

    def main(self):
        # self.FPGA_Put_Version()
        # FPGA_Data = []
        # for i in range(2):
        #     FPGA_Data.append(self.FPGA_Dat_analysis())
        # print(FPGA_Data)
        # self.FPGA_Put_Temp()
        # data = self.FPGA_Dat_analysis()
        # print(data)
        A= ''.join([chr(i) for i in [0x3E,0x35,0x53,int(hex(ord(str(1))),16),0x0D]])
        print(A)
        self.FPGA_Put_TX(A)
        data = self.FPGA_ECO_Dat_analysis()
        print(data)
        # data = self.PICO_Dat_analysis() # DSPEN,TRXEN,TRXCSEN,DC12VMNT,MNTIN,BDTEMP,ENVTEMP,Depth,FPGAWORKING
        # print(data)


if __name__ == "__main__":
    A = UART_HAT()

    A.main()