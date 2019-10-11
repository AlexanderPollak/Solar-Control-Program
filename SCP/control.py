""" This module contains classes and functions to control the solar system based on the detected BMS parameter and
settings defined in this class.

**Description:**

    This module implements the required functions to enable and disable the Schneider XW+ inverter based on the
    detected BMS parameters. It uses functions from both, pylontech_com and conext_com modules. It will allow the
    user to enable the readout and write program specific parameters.
    The main functions implemented are:
        1. control_system()
        2. set_low_SoC_cutout()
        3. set_operational_mode()


The main class in this module ("Control") allows the user to
run the control system.


"""
from threading import Thread
from pylontech_com import *
from conext_com import *
from data_log import *



# EMBEDDING Controller_Thread CLASS ----------------------------------------------------

class Controller_Thread(threading.Thread):


    def __init__(self,group=None,target=None,name=None,verbose=None,N_MODULES=1, UDP_IP ="127.0.0.1", UDP_PORT1 = 5005):

        threading.Thread.__init__(self,group=group,target=target,name=name,verbose=verbose)

        self._stopevent =threading.Event()# used to stop the socket loop.
        """communication parameter battery"""
        self.N_MODULES=N_MODULES
        self.UDP_IP=UDP_IP
        self.UDP_PORT1=UDP_PORT1
        """communication parameter conext"""
        self._conext_port=0

        """inverter parameter while running the control loop"""
        self.__low_battery_voltage_operation               =46#Default value for low battery voltage
        self.__low_battery_voltage_hysteresis_operation    =3  #Default value for low battery voltage hysteresis


    def initialise(self):
        """This function initilises the settings for the control loop"""

        print self._inverter.read_Inverter_Status()


        


    def run(self):
        """Main control loop"""

        inverter = XW()
        if not inverter.is_connected():
            return False
        self._inverter = inverter





        BMS = US2000B()
        BMS.open()
        self._port = BMS._port

        for i in range(1,10):
            if BMS.is_connected():
                break
            time.sleep(1)
            if i == 5:
                BMS.initialise()
            if i == 10:
                print "ERROR, no connection could be established!"
                return
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            while not self._stopevent.isSet():

                self._port.write('pwr\r')
                time.sleep(0.5)
                rec_str = self._port.read(2200)
                rec_int = re.findall(r'\d+', rec_str)
                #Writes values into SOC_array and returns it.
                if self.N_MODULES == 1:
                    MESSAGE = "SoC"+"\t"+"N=1"+"\t"+"A="+str(rec_int[8])

                elif self.N_MODULES == 2:
                    MESSAGE = "SoC"+"\t"+"N=2"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])

                elif self.N_MODULES == 3:
                    MESSAGE = "SoC"+"\t"+"N=3"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])

                elif self.N_MODULES == 4:
                    MESSAGE = "SoC"+"\t"+"N=4"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])

                elif self.N_MODULES == 5:
                    MESSAGE = "SoC"+"\t"+"N=5"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])+"\t"+"E="+str(rec_int[68])

                elif self.N_MODULES == 6:
                    MESSAGE = "SoC"+"\t"+"N=6"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])+"\t"+"E="+str(rec_int[68])+"\t"+"F="+str(rec_int[83])

                elif self.N_MODULES == 7:
                    MESSAGE = "SoC"+"\t"+"N=7"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])+"\t"+"E="+str(rec_int[68])+"\t"+"F="+str(rec_int[83])+"\t"+"G="+str(rec_int[98])

                elif self.N_MODULES == 8:
                    MESSAGE = "SoC"+"\t"+"N=8"+"\t"+"A="+str(rec_int[8])+"\t"+"B="+str(rec_int[23])+"\t"+"C="+str(rec_int[38])+"\t"+"D="+str(rec_int[53])+"\t"+"E="+str(rec_int[68])+"\t"+"F="+str(rec_int[83])+"\t"+"G="+str(rec_int[98])+"\t"+"H="+str(rec_int[113])

                else:
                    print"ERROR number of modules not recognised please specify a number between 1 and 8"
                    sock.close()
                    return
                sock.sendto(MESSAGE, (self.UDP_IP, self.UDP_PORT1))
                sock.sendto(MESSAGE, (self.UDP_IP, self.UDP_PORT2))
                sock.sendto(MESSAGE, (self.UDP_IP, self.UDP_PORT3))
                time.sleep(5)
        except Exception:
            sock.close()
            print"ERROR no communication possible, check if the connection has been opened with open()"
            return

    def join(self, timeout=None):
        """Stop the thread"""
        self._stopevent.set()
        threading.Thread.join(self, timeout)



# EMBEDDING SystemControl CLASS ----------------------------------------------------

class SystemControl():
    """This class implements the serial connection functions """

    def __init__(self):
        ''' Constructor for this class. '''

        self.__low_SoC_default_summer                           =22   #Default value for low SoC
        self.__low_SoC_default_winter                           =40  # Default value for low SoC

        self.__low_battery_voltage_default_summer               =46.7 #Default value for low battery voltage
        self.__low_battery_voltage_hysteresis_default_summer    =2.2  #Default value for low battery voltage hysteresis

        self.__low_battery_voltage_default_winter               =47.5  # Default value for low battery voltage
        self.__low_battery_voltage_hysteresis_default_winter    = 3.0  # Default value for low battery voltage hysteresis

        self.__operational_mode_default



    def __del__(self):
        ''' Destructor for this class. '''











