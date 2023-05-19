import serial
from queue import Queue
import matplotlib.pyplot as plt



ser = serial.Serial('COM3', 9600)

q = Queue()

st = True
i = 0
while st:
    # ser.write(bytes(bytearray([0x54,0x72,0x78,0x20,0x4D,0x6F,0x64,0x65])))
    # # ser.write(bytes(bytearray([48])))
    # ser.write('\n\r'.encode())
    l = ser.read(10)
    i += 1
    print(i)
    q.put(l)
    if i == 10239:
        st = False
        i = 0
ser.close()
result = []

for i in range(10239):
    result.append(q.get())

plt.figure()
plt.plot(result)
plt.show()