
import numpy as np
import datetime
import re
def main():

    BMS_array = [[0 for i in range(5)] for j in range(2)]
    N_MODULES=1
    with open('pylontech') as f:
        contents = f.read()
        print(contents)


    rec_int = re.findall(r'\w+', contents)
    # Writes values into BMS_array and returns it.
    if N_MODULES == 1:
        BMS_array[0][0] = str(rec_int[38])  # SOC
        BMS_array[0][1] = str(rec_int[27])  # Voltage
        BMS_array[0][2] = str(rec_int[28])  # Current
        BMS_array[0][3] = str(rec_int[29])  # Temperature
        BMS_array[0][4] = str(rec_int[34])  # Battery Status


    tmp_time = str(datetime.datetime.now().date())+' '+str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute)+':'+str(datetime.datetime.now().second)

    print (BMS_array[0, 3])










if __name__ == '__main__':
    main()
