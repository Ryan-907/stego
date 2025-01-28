import cv2
import numpy as np

#Ensures data is converted from native to binary, if it is not binary already (usually will not be)
def data_to_binary(data):
    if isinstance(data, str):
        return ''.join(format(ord(char), '08b') for char in data)
    elif isinstance(data, int) or isinstance(data, np.unit8):
        return format(data, '08b')
    elif isinstance(data, bytes):
        return ''.join(format(byte, '08b') for byte in data)
    elif isinstance(data, np.ndarray):
        return [format(i, '08b') for i in data]
    else:
        raise TypeError("Type not supoprted womp womp")
    
d = data_to_binary(8)
print(d)