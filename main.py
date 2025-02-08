import cv2
import numpy as np
import pyinputplus as pyip
import math
import tkinter as tk
from tkinter import filedialog as fd

DELIMITER = '=='
CHOICES = ['Int', 'String']

def file_selection():
    file_path = fd.askopenfilename()
    return file_path

def fetch_image():
    root = tk.Tk()
    root.withdraw()

    file_path = file_selection()
    return file_path

                
#Ensures data is converted from native to binary.
def data_to_binary(data):
    if isinstance(data, str):
        return ''.join(format(ord(char), '08b') for char in data) #Converts string
    elif isinstance(data, int): #Converts int
        return format(data, '08b')
    elif isinstance(data, bytes): #Converts bytes
        return ''.join(format(byte, '08b') for byte in data)
    elif isinstance(data, np.ndarray): #Converts numpy arrays
        return [format(i, '08b') for i in data]
    else:
        raise TypeError("Type not supoprted womp womp")

#Gets the message to be hidden. Either integer or string accepted.
def fetch_message():
    option = pyip.inputMenu(CHOICES, numbered=True) 
    if option == CHOICES[0]:
        return int(input("Enter int value: "))
    if option == CHOICES[1]:
        return input("Enter value: ")

def size_check(image, data): #Ensures selected image is large enough to contain all the data
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print(f'Max bytes to encode {n_bytes}')
    if len(data) > n_bytes:
        raise ValueError('Insufficient bytes. Require larger image or less data!')
    return True

def data_encoding(image, data): #Encodes data in image using lSB 
    data += DELIMITER
    data_index = 0
    bin_data = data_to_binary(data) #Converting data to bin
    data_len = len(bin_data)

    for row in image: #Iterating through pixels
        for pixel in row:
            r,g,b = data_to_binary(pixel) #Alters the int values in an array that represent pixels to binary representations
            if data_index < data_len: #changing least signifciant pixel of the red, green, and blue values. 

                pixel[0] = int(r[:-1] + bin_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[1] = int(g[:-1] + bin_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[2] = int(b[:-1] + bin_data[data_index], 2)
                data_index += 1
            if data_index >= data_len:
                break
    return image

def decoder(image):
    print('Decoding...')
    binary_data = ''
    for row in image:
        for pixel in row:
            r,g,b=data_to_binary(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-len(DELIMITER):] == DELIMITER:
            break
    return decoded_data[:-len(DELIMITER)]


if __name__=='__main__':
    IMAGE = fetch_image()
    IMAGE = cv2.imread(IMAGE)
    data = fetch_message()
    datab = data_to_binary(data)
    print(f'OG Data: {data} New Data: {datab}')
    size_check(IMAGE, datab)
    print(f'Data:{data}<->{datab}\n#Bytes: {math.ceil(len(str(datab))/8)}')
    cv2.imwrite('encode.png', data_encoding(IMAGE, datab))
    enc_im = cv2.imread('encode.png')
    decoded_data = decoder(enc_im)
    print(f'Decoded message: {decoded_data}')
    if decoded_data == datab:
        print("Yipee")
    else:
        print("Saddness envelopes me")