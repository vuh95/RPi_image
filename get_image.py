import os
from datetime import datetime

def get_image():
    time= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_path = f"image_{time}"
    os.system(f'libcamera-still -o {output_path}')
    print (f'{output_path} saved')

if __name__ == '__main__':
    get_image()
    