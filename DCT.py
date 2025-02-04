import cv2
import numpy as np
import scipy.fftpack
import pyinputplus as pyip


image = 'stock.jpeg'
image = cv2.imread(image)
DELIMITER = '1111'
CHOICES = ['Int', 'String']

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

def fetch_message():
    option = pyip.inputMenu(CHOICES, numbered=True) 
    if option == CHOICES[0]:
        return int(input("Enter int value: "))
    if option == CHOICES[1]:
        return input("Enter value: ")
    
def gray_scale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    return gray_image

def size_adjust(image):
    height, width = image.shape
    if height % 8 != 0:
        new_height = height + (8 - height % 8)
    else:
        new_height = height
    if width % 8 != 0:
        new_width = width + (8 - width % 8)
    else:
        new_width = width

    pad_image = np.zeros((new_height, new_width), dtype=np.uint8)
    pad_image[:height, :width] = image

    return pad_image

def blocking(scaled_gray_image):
    blocks = []
    for i in range(0, scaled_gray_image.shape[0], 8):
        for j in range(0, scaled_gray_image.shape[1], 8):
            block = scaled_gray_image[i:i+8, j:j+8]
            blocks.append(block)

    return blocks

def apply_dct(blocks):
    dct_blocks = np.array([scipy.fftpack.dct(scipy.fftpack.dct(block.T, norm='ortho').T, norm='ortho') for block in blocks])
    return dct_blocks

def encode_message(dct_blocks, message):

    bin_msg=data_to_binary(message) + DELIMITER
    data_index = 0

    for dct_block in dct_blocks:
        if data_index >= len(bin_msg):
            break

        u, v = 1, 2

        coeff = int(dct_block[u,v])
        coeff = (coeff & ~1) | int(bin_msg[data_index])
        dct_block[u,v] = coeff
        
        data_index +=1

    return dct_blocks

def invert_dct(dct_blocks):
    return np.array([scipy.fftpack.idct(scipy.fftpack.idct(block.T, norm='ortho').T, norm='ortho')
        for block in dct_blocks])

def reassemble_image(blocks, height, width):
    recon = np.zeros((height, width), dtype=np.float32)
    block_index = 0

    for i in range(0, height, 8):
        for j in range(0, width, 8):
            recon[i:i+8, j:j+8] = blocks[block_index]
            block_index += 1

    return np.clip(recon, 0 , 255).astype(np.uint8)

def decode_dct(dct_blocks):
    bin_msg = ''

    for dct_block in dct_blocks:
        u,v = 1,2
        coeff = int(dct_block[u,v])
        bin_msg += str(coeff & 1)

        if bin_msg.endswith(DELIMITER):
            break
    msg_char = [chr(int(bin_msg[i:i+8], 2)) for i in range(0, len(bin_msg)-8, 8)]

    return ''.join(msg_char)

    

if __name__=='__main__':

    msg = fetch_message()
    bin_msg = data_to_binary(msg)
    #cv2.imshow('og', image)
    #cv2.waitKey(0)

    gray = gray_scale(image)
    #cv2.imshow("gray image", gray)
    #cv2.waitKey(0)

    scale_image = size_adjust(gray)
    #cv2.imshow('new size', scale_image)
    #cv2.waitKey(0)

    blocked_image = blocking(scale_image)
    height, width = scale_image.shape

    dct_result = apply_dct(blocked_image)

    encoded = encode_message(dct_result, bin_msg)
    recon_img = reassemble_image(encoded, height, width)

    cv2.imwrite('encode_dct.png', recon_img)
    cv2.imshow('dct encoded', recon_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(decode_dct(encoded))

    invert_dct(encoded)



