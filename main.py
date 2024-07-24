import serial
from serial.tools import list_ports
import threading

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
    global stop_communication
    while True:
        data = input("Enter data to send: ")
        if data == '$quit()':
            stop_communication = True
            break
        ser.write(data.encode())  # Send data to Arduino

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
