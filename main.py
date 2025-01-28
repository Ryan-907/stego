import cv2
import numpy as np
import pyinputplus as pyip
import math

CHOICES = ['Int', 'String']
IMAGE = 'test.png' #Stock image. Remove to enable image entry in cli.
if not IMAGE:
    IMAGE = input("Enter path to image: ")

#Ensures data is converted from native to binary.
def data_to_binary(data):
    if isinstance(data, str):
        return ''.join(format(ord(char), '08b') for char in data) #Converts string
    elif isinstance(data, int): #Converts int
        return bin(data)
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

def size_check(image_name, data): #Ensures selected image is large enough to contain all the data
    image = cv2.imread(image_name)
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print(f'Max bytes to encode {n_bytes}')
    if len(data) > n_bytes:
        raise ValueError('Insufficient bytes. Require larger image or less data!')
    return True

def data_encoding(image, data):
    pass


if __name__=='__main__':

    data = fetch_message()
    datab = data_to_binary(data)
    size_check(IMAGE, datab)
    print(f'Data:{data}<->{datab}\n#Bytes: {math.ceil(len(str(datab))/8)}')



#Size checker. Ensures size of image can hanld encoded data