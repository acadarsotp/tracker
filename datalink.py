import serial


def link_arduino():
    try:
        ser = serial.Serial('COM6', 9600)
        comm = True
        return ser, comm
    except serial.serialutil.SerialException:
        ser = None
        comm = False
        print("\nUnable to reach Arduino, continuing without serial communication")
        return ser, comm
