# Define the pins for the HX711
hx711_pin = [27,17]
# Define the output path for the data
OUTPUTPATH = 'Data.csv'
# Define the time format
TIMEFORMAT = '%Y/%m/%d %H:%M:%S'
# Define the zero value for the scale
zero = 447836
# Define the ratio for the scale
ratio = 502.98
# Define the number of replicates for reading data from HX711
rep = 3
# Define the labels of the parameters
labels = ['Time','weight']

# Import necessary libraries
import time
import os
import csv
import numpy as np
from datetime import datetime

class write_out:
    'write out data to csv file'
    def __init__(self, output_path = './data/adc1.csv', parameters = []):
        # Initialize output path and parameters
        self.output_path = output_path
        # Create a list of headers with 'Time' as the first column
        self.headers_list = parameters
        # Sort the headers list
        self.headers_list_sort = self.headers_list.sort()
        # Check if the output file exists
        check_file = os.path.exists(self.output_path)
        # If the file does not exist, create it and write the headers
        if check_file == False:
            with open(self.output_path, 'a', newline= '') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.headers_list)
        # If the file exists, check if the headers are correct
        else:
            with open(self.output_path, 'r', newline= '') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)
                headers_sort = headers.sort()
                # If the headers are correct, print a message
                if headers_sort == self.headers_list_sort:
                    print('headers already exist')
                # If the headers are not correct, raise an error
                else:
                    raise TypeError('parameters_list is not correct')
        
    def write_data(self, data = []):
        # Write data to the output file
        self.data = data
        with open(self.output_path, 'a', newline= '') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = self.headers_list)
            writer.writerow(self.data)

class read_HX711:
    'read data from HX711'
    def __init__(self, dout_pin=14, pd_sck_pin=15, offset=-92200, ratio=58.05):
        # Import necessary libraries and set up GPIO pins for HX711
        import RPi.GPIO as GPIO  # import GPIO
        GPIO.setmode(GPIO.BCM)
        from hx711 import HX711
        import numpy as np
        # Initialize HX711 with given parameters and set scale offset and ratio
        self.dout_pin = dout_pin
        self.pd_sck_pin = pd_sck_pin
        self.scale_offset = offset
        self.scale_ratio = ratio
        self.hx = HX711(dout_pin, pd_sck_pin)
        self.hx.set_scale_ratio(self.scale_ratio)
        self.hx.set_offset(self.scale_offset)

    def get_value(self):
        # Get a single value from HX711 and round it to an integer value.
        try:
            value = np.around(self.hx.get_weight_mean(1))
        except:
            # If an error occurs, try again.
            pass
        # If value is not False (i.e. reading was successful), return it.
        if value != False:
            return value
        # If value is False (i.e. reading was unsuccessful), try again.
        else:
            return self.get_value()

    def read_hx711(self, replicate = 3):
        # Read multiple values from HX711 and calculate mean and standard deviation.
        self.scale_value = []
        for i in range (replicate):
            self.scale_value.append(self.get_value())
            time.sleep (0.05)
        self.scale_value_std = np.std(self.scale_value)
        self.scale_value_mean = np.around(np.mean(self.scale_value))
        
         # If standard deviation is greater than 10, try again.
        if self.scale_value_std > 10:
            return self.read_hx711()
        return self.scale_value_mean
    
# Create an instance of read_HX711 class with given parameters.
hx711 = read_HX711(hx711_pin[0], hx711_pin[1], zero, ratio)
# Create an instance of write_out class with given parameters.
datawriter = write_out(OUTPUTPATH, parameters = labels)

# Main loop to continuously read data from HX711 and write it to output file.
while __name__ == '__main__':
    try:
        # Create a dictionary to store data.
        data = {}
        # Get the current time and store it in the dictionary.
        time_now = datetime.now().strftime(TIMEFORMAT)
        # Read data from HX711 and store it in the dictionary.
        data['weight'] = hx711.read_hx711(replicate = rep)
        data['Time'] = time_now
        # Write data to output file.
        datawriter.write_data(data)
        # Print data to console.
        print (data)
        time.sleep(1 - time.time() % 1)
    except:
        # If an error occurs, wait for 5 second and try again.
        time.sleep(5)
        pass
