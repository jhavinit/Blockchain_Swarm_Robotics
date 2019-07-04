import serial

Serial = serial.Serial("/dev/pts/20",9600)
receive=serial.Serial("/dev/pts/22",9600)

Serial.write("Hi there arduino")
print(receive.read())

