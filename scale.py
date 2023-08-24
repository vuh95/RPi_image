hx711_pin = [17,27]
OUTPUTPATH = './data/Data.csv'
TIMEFORMAT = '%Y/%m/%d %H:%M:%S'

import time
import os
import csv
import numpy as np
from datetime import datetime

class write_out:
    'write out data to csv file'
    def __init__(self, output_path = './data/adc1.csv', parameters = []):
        self.output_path = output_path
        self.parameters = parameters
        self.headers_list = ['Time']
        self.headers_list = self.headers_list + self.parameters
        self.headers_list_sort = self.headers_list.sort()
        check_file = os.path.exists(self.output_path)
        if check_file == False:
            with open(self.output_path, 'a', newline= '') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.headers_list)
        else:
            with open(self.output_path, 'r', newline= '') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)
                headers_sort = headers.sort()
                if headers_sort == self.headers_list_sort:
                    print('headers already exist')
                else:
                    raise TypeError('parameters_list is not correct')
        
    def write_data(self, data = []):
        self.data = data
        with open(self.output_path, 'a', newline= '') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = self.headers_list)
            writer.writerow(self.data)
    
    def update_temp_file(self, output_path,data = []):
        self.data = data
        with open(TEMP_OUTPUTPATH, 'a', newline= '') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = self.headers_list)
            writer.writerow(self.data)

class read_HX711:
    'read data from HX711'
    def __init__(self, dout_pin=14, pd_sck_pin=15, offset=-92200, ratio=58.05):
        import RPi.GPIO as GPIO  # import GPIO
        GPIO.setmode(GPIO.BCM)
        from hx711 import HX711
        import numpy as np
        self.dout_pin = dout_pin
        self.pd_sck_pin = pd_sck_pin
        self.scale_offset = -81000
        self.scale_ratio = 58.2
        self.hx = HX711(dout_pin, pd_sck_pin)
        self.hx.set_scale_ratio(self.scale_ratio)
        self.hx.set_offset(self.scale_offset)

    def get_hx_value(self):
        self.value = np.around(self.hx.get_weight_mean(1))
        if self.value != False:
            return self.value
        else:
            return self.get_hx_value()

    def read_hx711(self, replicate = 3, label = "weight"):
        self.label = label
        self.time_now = datetime.now().strftime(TIMEFORMAT)
        self.out_value = {}
        self.scale_value = []
        for i in range (replicate):
            self.scale_value.append(self.get_hx_value())
            time.sleep (0.15)
        self.scale_value_std = np.std(self.scale_value)
        self.scale_value_mean = np.around(np.mean(self.scale_value))
        if self.scale_value_std > 10:
            return self.read_hx711()
        self.out_value['Time'] = self.time_now
        self.out_value[f"{self.label}"] = self.scale_value_mean
        return self.out_value
    
hx711 = read_HX711(hx711_pin[0], hx711_pin[1])
datawriter = write_out(OUTPUTPATH, 'weight')

while __name__ == '__main__':
    try:
        data = hx711.read_hx711()
        datawriter.write_data(data)
        print (data)
        time.sleep(10 - time.time() % 10)
    except:
        pass