# recording.py
# import the necessary packages
import picamera
import os
import datetime as dt
from subprocess import call
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

def piRecord():  
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

# MAIN goes here





# Accelerometer code goes here
