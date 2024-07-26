import serial
from serial.tools import list_ports
import threading
import time
import NMEA0183

comPort = "COM3"
try:
    ser = serial.Serial(comPort, 9600)  # Open serial port
except serial.SerialException:
    print(f'{comPort} not available')

    ports = list(list_ports.comports())
    if ports:
        print("Available ports:")
        for port in ports:
            print(f"\t{port.description}")
    else:
        print("No serial ports found.")
    
    quit()

stop_communication = False

def send_user_input_to_arduino():
    nmea = NMEA0183.NMEA()

    coords = [
        [51.22521374836571, 33.19309502652848],
        [51.22534517983234, 33.193290961423074],
        [51.2257806501225, 33.19382045193892],
        [51.22582859155405, 33.19387148716936],
        [51.2259124889391, 33.19396717822644],
        [51.22600437637579, 33.194082007494934],
        [51.22614020964186, 33.194215974974846],
        [51.22630001298017, 33.19440097771017],
        [51.22652373670881, 33.1946880508814],
        [51.22667954366612, 33.19491133002455]
    ]

    global stop_communication
    for i in range(0, 16):
        index = i
        if i >= len(coords):
            index = i % len(coords)
            
        time.sleep(1)
        message = nmea.generate_gprmc('102340.000', coords[index][0], coords[index][1], 10.2, 23.5, '200724', 13.4)
        print(message)
        ser.write(message.encode())  # Send data to Arduino

    time.sleep(2)
    stop_communication = True

def receive_from_ser():
    while True:
        if stop_communication:
            break
        if ser.in_waiting > 0:
            response = ser.readline().decode('utf-8').rstrip()
            print("Arduino response:", response)

receiving_thread = threading.Thread(target=receive_from_ser)
receiving_thread.start()

sending_thread = threading.Thread(target=send_user_input_to_arduino)
sending_thread.start()

sending_thread.join()
receiving_thread.join()
