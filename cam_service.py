# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 14:56:56 2020

@author: PAVA
"""
import os
import socket
import urllib.request
import cv2
import numpy as np
import time
import imutils
from imutils.video import VideoStream
from operator import itemgetter
from pyzbar import pyzbar
from datetime import datetime
from config import (cam_IP,
                    username,
                    password,
                    path_write,
                    separator)
cam = None

# Pripojenie na kameru
def connect_to_camera():
    print("Connecting to camera.")
    cam = cv2.VideoCapture()
    try:
        if cam.open("rtsp://{}:{}@{}/Streaming/channels/2/".format(username,password,cam_IP)):
            print('Camera connected successfully.')
            return cam
    except Exception as e:
        print(e)
    print('Connection was not successfull.')
    return None

# Kontrola pripojenia kamery
def check_camera_connection(camera_object):
    if camera_object is None or not camera_object.isOpened():
        return False
    else:
        return True

# Zápis chýb do logu
def f_handle_exception(e):
    log = open('log.txt','a+')
    if os.stat(r"log.txt").st_size > 500000000:
        log.truncate(0)
    log_date = datetime.now()
    log.write("{} {} \n\n".format(log_date,e))
    log.close()
    return 0

# Zapis barcodov do súboru
def write_data_into_file(barcodes_in_order):
    w_file = open(path_write,'a+')
    w_file.truncate(0)
    w_file.write(separator.join(barcodes_in_order))
    w_file.close()
    return 0

while True:
    if not check_camera_connection(cam):
        cam = connect_to_camera()
        time.sleep(5)
    else:
        try:
            _, image = cam.read()
            barcodes = pyzbar.decode(image) # Najde barkody
            barcodes_in_order=[] 
            for barcode in barcodes:
                (x,y,w,h) = barcode.rect
                points = np.zeros((4,2),dtype = int)
                
                # Zapise body pre aktualny barcode
                points[3,0] , points[3,1] = barcode[3][0][0] ,barcode[3][0][1]
                points[2,0] , points[2,1] = barcode[3][1][0] ,barcode[3][1][1]
                points[1,0] , points[1,1] = barcode[3][2][0] ,barcode[3][2][1]
                points[0,0] , points[0,1] = barcode[3][3][0] ,barcode[3][3][1]
            
                # Obkreslenie barcodu
                cv2.line(image,tuple(points[0,0:2]),tuple(points[1,0:2]),(0,0,255),5)
                cv2.line(image,tuple(points[1,0:2]),tuple(points[2,0:2]),(0,0,255),5)
                cv2.line(image,tuple(points[2,0:2]),tuple(points[3,0:2]),(0,0,255),5)
                cv2.line(image,tuple(points[3,0:2]),tuple(points[0,0:2]),(0,0,255),5)

                # Najdenie max a min pre x a y pre crop obrazku
                y_max = (np.amax(points[:,1]), np.amin(points[:,1]))
                x_max = (np.amax(points[:,0]), np.amin(points[:,0]))
                
                # Precita data z barkodu
                barcodeData = barcode.data.decode("utf-8")
                barcodes_in_order.append([y_max[0],x_max[0],barcodeData])
            
            if barcodes_in_order:
                barcodes_in_order = sorted(barcodes_in_order, key=itemgetter(0))
                barcodes_in_order = [x for x[2] in barcodes_in_order]
                write_time = str(datetime.now())
                barcodes_in_order.insert(0,write_time)
                write_data_into_file(barcodes_in_order)
        
        except Exception as e:
            f_handle_exception(e)
            
            