#Triantafyllos Xydis

#!/usr/bin/env sage -python

import shannon_fano
import linear_encoding
import entropy

import requests
import cv2
import hashlib
from PIL import Image
from io import BytesIO
import numpy as np



while(True):
    try:
        userChoice = int(input("\n\t***\n\t1.cat.jpg\n\t2.windows.jpg\n\t3.myfile.txt\n\t***\nChoose File:"))
        if userChoice == 1:
            raise ValueError
            continue
        elif userChoice == 2:
            continue
            chosenFile = "windows.jpg"
        elif userChoice == 3:
            chosenFile = "myfile.txt"
        else:
            raise ValueError
        userError =  int(input("Error length (%): "))
        if userError>=0 and userError<=100:
            break
        raise ValueError
    except ValueError:
        print("Wrong input try again")

'''
img = Image.open(chosenFile)
pixels = list(img.getdata())
print(pixels)
'''




# Read file

with open('myfile.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()
    compressed = shannon_fano.shannon_fano(file_content)
    encoded = linear_encoding.encode(compressed)
    parameters = 0
    errors = 0
    ent = entropy.calc_ent(file_content)
    #sha256 = hashlib.sha256(encoded).hexdigest()
    sha256 = 0
    #send json to the server
    message = { 'encoded-message': compressed,
                'compression-algorithm':'fano-shannon',
                'encoding':'linear',
                'parameters':0,
                'errors':0,
                'SHA256':sha256,
                'entropy':ent
            }
    response = requests.post('http://localhost:7500/upload', json=message)

# Check the response from the server
print("Status code:",response.status_code)
print("Message from server:",response.text)