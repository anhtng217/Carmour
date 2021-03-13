# recording.py
# import the necessary packages
import picamera
import os
import datetime as dt
import smbus
from time import sleep
from subprocess import call
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

#camera set up and recording method
def piRecord():
    print("Camera recording.")
    """
    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1080)     # set video resolution
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = dt.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
        camera.start_recording('/home/pi/Desktop/footage.h264') # record video
    
        # Display timestamps in the video
        start = dt.datetime.now()
        while (dt.datetime.now() - start).seconds <20:
            camera.annotate_text = dt.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
            camera.wait_recording(0.2)            
        camera.stop_recording()                
        
        print('Footage recored and saved. Begin to upload to database')
            # convert file to mp4 file type
            #convertVid = "MP4Box -add video.h264 video.mp4"  
            #call ([convertVid], shell=True)
        
        #os.remove("video.h264")   # remove extension .h264
    """
    """
    #upload to Youtube
    CLIENT_SECRET_FILE = 'Client_Secret1.json'
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    request_body = {
        'snippet': {
            'title': 'Camera Footage',
            'description': 'Recorded footage from cameras'
            },
        'status': {
            'privacyStatus': 'private',
            'selfDeclaredMadeForKids': False,
            },
        'notifySubscribers': False
        }
    
    mediaFile = MediaFileUpload('/home/pi/Desktop/footage.h264')
    
    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()
    
    service.thumbnails().set(
        videoId = response_upload.get('id'),
        media_body = MediaFileUpload('Carmour Logo.jpg')).execute()
    
    print('Footage successfully uploaded to database!')
    """
    #sleep(5)
#accelerometer
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    
    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    
    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
    
    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    
    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)

    #concatenate higher and lower value
    value = ((high << 8) | low)
    
    #to get signed value from mpu6050
    if(value > 32768):
            value = value - 65536
    return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print ("Reading Data from Gyroscope and Accelerometer")


#MAIN
while True:
    Ax = read_raw_data(ACCEL_XOUT_H)/16384
    Ay = read_raw_data(ACCEL_YOUT_H)/16384
    Az = read_raw_data(ACCEL_ZOUT_H)/16384
    
    Gx = read_raw_data(GYRO_XOUT_H)/131
    Gy = read_raw_data(GYRO_YOUT_H)/131
    Gz = read_raw_data(GYRO_ZOUT_H)/131
    print ("Ax=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)
    print ("Gx=%.2f dps" %Gx, "\tGy=%.2f dps" %Gy, "\tGz=%.2f dps" %Gz)
    if (Ax > 1.1 or Ax < -1.1) or (Ay > 1 or Ay < -1) or (Az > 1 or Az < -1) or (Gx > 1 or Gx < -1) or (Gy > 1 or Gy < -1) or (Gz > 1 or Gz < -1):
        piRecord()
    else:
        print("The system is normal.")
    sleep(1)
    
    
        