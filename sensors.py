import random as rnd
import datetime
import time
from threading import Thread
from file_manager import FileMngr
"""
SENSOR READING DATA
***
This code generates parameters of PyFloraPot, which are then transfered to the main app
***
Pot parameters:
   vwc (as Volumetric Water Content, VWC), 
        range from 20 to 50% 
   pH, typical range 4 to 10,
        3-5.5  acidic soil, 5.5-8 optimal range, 8-9 alkaline soil, 9 strongly alkaline soil
   sal, as EC (mS/cm or dS/m), range from 0 to 16
        0-2 non-saline, 2-4 very sparingly saline, 4-8 sparingly saline, 8-16 medium saline, 16> very saline
   lux (with LDR, photoresistor) - stronger light less resistance (range 10 to 1000 and more (digital))
        <10 pitch black, <200 dark, <500 low light, <800 medium light, <1000 strong light
"""
sensor_thread = None
recording = False
class Sensor():
    def __init__(self):
        self.filemngr = FileMngr()

    def read_db(self):
        from database import DBHandler
        self.db = DBHandler()
        self.pots = self.db.read_pot_tbl()

    def read_sensors(self, pot_id): 
        vwc = rnd.gauss(35,10) 
        ph = rnd.gauss(7,2)
        sal = rnd.triangular(0,16,3)
        lux = rnd.triangular(10,1000,900)
        return vwc,ph,sal,lux
    
    def read_sensors_cont(self, pot_id, f_vwc,f_ph,f_sal,f_lux): 
        """reads previous line and assigns new values with up to 10% difference with a random walk trend"""
        treshold = 0.6
        rng = rnd.gauss(0.1,0.1) #10% +/- 5%
        def random_walk(f_val):
            prob = rnd.random()
            step = rnd.uniform(0,f_val*rng)
            if prob > treshold:
                return f_val+step
            else:
                return f_val-step
        f_vals = [f_vwc,f_ph,f_sal,f_lux]
        val_list = [random_walk(f_val) for f_val in f_vals]
        return tuple(val_list)

    def sensor_data_manager(self):
        """sets a data storage file. Running this will erase current data!"""
        self.read_db()
        for pot in self.pots:
            file_path = f"PyFloraPots/pot_data_id_{pot.id_number}.csv"
            file_writer = FileMngr.openFileForWriting(self.filemngr, file_path)
            file_writer.write(f"datetime,vwc,ph,sal,lux\n")
            file_writer.close()
    
    def sensor_data_store_first_val(self):
        """read and stores first row of values"""
        self.read_db()
        datetimestamp = datetime.datetime.now()
        for pot in self.pots:
            file_path = f"PyFloraPots/pot_data_id_{pot.id_number}.csv"
            vwc,ph,sal,lux = self.read_sensors(pot.id_number)
            FileMngr.writeToFilePath(self.filemngr, file_path, f"{datetimestamp},{vwc},{ph},{sal},{lux}\n")

    def define_interval(self, interval=5):
        global inter
        inter = interval

    def sensor_data_recorder(self):
        """data generation and storage in file. Run in gui, otherwise it will run indefinitely"""
        while True:
            time.sleep(inter)
            datetimestamp = datetime.datetime.now()
            for pot in self.pots:
                file_path = f"PyFloraPots/pot_data_id_{pot.id_number}.csv"
                file_line = FileMngr.openFileForReading(self.filemngr, file_path).readlines()[1]
                f_vwc,f_ph,f_sal,f_lux = map(float, file_line.split(sep=',')[1:])
                vwc,ph,sal,lux = self.read_sensors_cont(pot.id_number,f_vwc,f_ph,f_sal,f_lux)
                FileMngr.writeToFilePath(self.filemngr, file_path, f"{datetimestamp},{vwc},{ph},{sal},{lux}\n")
            if recording == False:
                print('Sensor data recording stopped!')
                break
                
    def start_recording(self):
        global sensor_thread, recording
        self.sensor_data_store_first_val()
        if sensor_thread is None or not sensor_thread.is_alive():
            recording = True
            sensor_thread = Thread(target=self.sensor_data_recorder)
            sensor_thread.start()
            print('Sensor data recording started!')
    
    def stop_recording(self):
        global recording
        recording = False

# if __name__ == '__main__':
#     sensor_app = Sensor()
    #sensor_app.read_db()
    #sensor_app.sensor_data_manager()
    #sensor_app.sensor_data_store_first_val()
    #sensor_app.sensor_data_recorder()

    #TESTING RANDOM WALK ALGORITHM
    # f_vwc,f_ph,f_sal,f_lux = 30,7,2,500
    # for i in range(100):
    #     vwc,ph,sal,lux = sensor_app.read_sensors_cont(1,f_vwc,f_ph,f_sal,f_lux)
    #     f_vwc,f_ph,f_sal,f_lux = vwc,ph,sal,lux
    #     print(vwc,ph,sal,lux)