# This script connects to the Pylontech US2000B Plus
# and read the charge status, voltage, current, and temperature
# it stores the data in a .csv file with the actual date

import serial, csv, time, numpy, struct, sys, re, datetime


def exit_fail(pylontech):
    try:
        pylontech.close()
    except: pass
    raise
    print 'FAILURE DETECTED.'
    exit()


def exit_clean(pylontech):
    try:
        pylontech.close()
    except: pass
    print 'CLEAN EXIT.'
    exit()



def connect():
    pylontech = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)
    #pylontech = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)
    return pylontech


def get_data(rec, data_writer, pylontech):
    # reads the data from the battery pack
    pylontech.write('pwr\r')
    time.sleep(0.5)
    data = pylontech.read(2200)
    # print repr(battery.read(1000))

    #name = ['Volt', 'Curr', 'Tempr', 'Tlow', 'Thigh', 'Vlow', 'Vhigh', 'Base.St', 'Volt.St', 'Curr.St', 'Temp.St','Coulomb', 'Time']

    numbers = re.findall(r'\d+',data)


    if rec:
        data_writer.writerow({'Time': str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute), \
                                'Volt1':str(numbers[1]), 'Current1': str(numbers[2]), 'Charge1': str(numbers[8]), 'Temp1':str(numbers[3]), \
                                'Volt2':str( numbers[16]), 'Current2': str(numbers[17]), 'Charge2': str(numbers[23]), 'Temp2':str(numbers[18]), \
                                'Volt3': str(numbers[31]), 'Current3': str(numbers[32]), 'Charge3': str(numbers[38]),'Temp3': str(numbers[33]), \
                                'Volt4': str(numbers[46]), 'Current4': str(numbers[47]), 'Charge4': str(numbers[53]),'Temp4': str(numbers[48]) \
                                           })
        csvfile.flush()

    #print data

    print ('Charge status A %s, B %s, C %s, D %s ' % (numbers[8], numbers[23], numbers[38], numbers[53]))

    return


#START OF MAIN:

if __name__ == '__main__':
    from optparse import OptionParser


    p = OptionParser()
    p.set_usage('BMSv1.py [options]')
    p.set_description(__doc__)
    p.add_option('-p', '--path', dest='path', type='str',default='/home/pollak/PycharmProjects/BMS/Log',
        help='Specify the link where the log files should be saved to. Default is ~/BMS/Log')
    p.add_option('-d', '--display', dest='display',action='store_true',
        help='Defines if the battery values are displayed. Default is False')
    opts, args = p.parse_args(sys.argv[1:])


    #if args==[]:
    #    print 'Please specify a ROACH board. Run with the -h flag to see all options.\nExiting.'
    #    exit()
    #else:
    #    roach = args[0]
    #if opts.boffile != '':
    #    bitstream = opts.boffile

try:

    print('BMS vers.: 1 ')

    # Connect to battery module
    pylontech = serial.Serial('/dev/ttyr00', 115200, timeout=0.05)



    # ---------------------------------------------------------------------------#
    # Readout configuration
    rec = True

    if rec:
        filename = str(opts.path) +'/'+ str(datetime.date.today()) +'.csv'
        date = str(datetime.date.today())
        csvfile = open(filename, mode='w+')
        name = ['Time', 'Volt1', 'Current1','Charge1','Temp1','Volt2', 'Current2','Charge2','Temp2','Volt3', 'Current3','Charge3','Temp3','Volt4', 'Current4','Charge4','Temp4']
        data_writer = csv.DictWriter(csvfile, fieldnames=name)
        data_writer.writeheader()

    # ---------------------------------------------------------------------------#



    try:
        while True:
            get_data(rec, data_writer, pylontech)
            time.sleep(30)
            if date != str(datetime.date.today()):
                filename = str(opts.path) + '/' + str(datetime.date.today()) + '.csv'
                date = str(datetime.date.today())
                csvfile = open(filename, mode='w+')
                name = ['Time', 'Volt1', 'Current1','Charge1','Temp1','Volt2', 'Current2','Charge2','Temp2','Volt3', 'Current3','Charge3','Temp3','Volt4', 'Current4','Charge4','Temp4']
                data_writer = csv.DictWriter(csvfile, fieldnames=name)
                data_writer.writeheader()
    except KeyboardInterrupt:
        print('interrupted!')
    # Read BMS data







except KeyboardInterrupt:
    exit_clean(pylontech)
except:
    exit_fail(pylontech)

exit_clean()
