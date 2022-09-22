import serial, time

def equipment_serials(comport0, comport1, baud):
    try:
        ser = serial.Serial(comport1, int(baud), timeout=60)
    except Exception as e:
        ser = serial.Serial(comport0, int(baud), timeout=60)
    return ser

def test_loudspeaker(ser):
    up = bytearray.fromhex("02 06 00 04 00 02 49 F9")
    # up = bytearray.fromhex("01 06 00 05 00 00 99 CB")
    try:
        ser.write(up)
    except Exception as e:
        print(e)

def test_hik(battery_serials):
    battery_code = bytearray.fromhex('01 03 01 01 00 01 D4 36')
    try:
        battery_serials.write(battery_code)
    except Exception as e:
        print(e)
        print("*******************0")
        power = 0
        return power

    time.sleep(0.1)
    len_return_data = battery_serials.inWaiting()
    print(len_return_data)

    if len_return_data != 0:
        try:
            return_data = battery_serials.read(len_return_data)
            return_data_right = str()
            for recv_part in return_data:
                return_data_right += "0x%02x" % recv_part
            return_data_right = return_data_right[2:].split("0x")[:]
            power = int(str(return_data_right[3] + return_data_right[4]), 16) * 10
        except Exception as e:
            power = int(1)
        return power
    else:
        print("*************************1")
        power = int(0)
        return power

ser = equipment_serials("/dev/ttyUSB0", "/dev/ttyUSB1", 9600)
#test_loudspeaker(ser)
power = test_hik(ser)
print(power)

