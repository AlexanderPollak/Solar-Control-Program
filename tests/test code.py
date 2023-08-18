
import numpy as np
import datetime
def main():

    BMS_ARRAY = np.zeros((5, 4))

    tmp_n_modules = len(BMS_ARRAY)
    tmp_time = str(datetime.datetime.now().date())+' '+str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute)+':'+str(datetime.datetime.now().second)

    print (tmp_time)










if __name__ == '__main__':
    main()
