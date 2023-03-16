import serial
import time


def link_arduino():
    try:
        ser = serial.Serial('COM3', 9600)
        comm = True
        time.sleep(2)
        print("\nSERIAL COMM ONLINE")
        return ser, comm
    except serial.serialutil.SerialException:
        ser = None
        comm = False
        print("\nUnable to reach Arduino, continuing without serial communication")
        return ser, comm


def comm_data(serial_port, ACK, azimuth, elevation):
    # construct the data packet
    data_packet = f"{ACK},{azimuth},{elevation}\n"

    # try to establish a handshake with the Arduino
    handshake_successful = False
    while not handshake_successful:
        try:
            # send SYN packet
            serial_port.write(data_packet.encode())

            # wait for SYN-ACK packet
            syn_ack_packet = serial_port.readline().decode('utf-8')

            # check if SYN-ACK packet is correct
            if syn_ack_packet == data_packet:
                # send ACK packet
                serial_port.write(f"{ACK}".encode())
                print("Azimuth: ", azimuth)
                print("Elevation: ", elevation)
                time.sleep(1)
                handshake_successful = True
            else:
                # re-send SYN packet
                print("Handshake failed. Retrying...")
                time.sleep(1)

        except Exception as e:
            print(f"Error occurred during serial communication: {e}")
            return

    return
