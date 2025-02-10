import cv2
import numpy as np
import scipy.fftpack
  
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

def encode_message(dct_blocks, bin_msg):
    data_index = 0

    for dct_block in dct_blocks:
        if data_index >= len(bin_msg):
            break

        u, v = 4, 4

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

def decode_dct(dct_blocks, bin_delimiter):
    bin_msg = ''

    for dct_block in dct_blocks:
        u, v = 4, 4  # Ensure this matches encoding
        coeff = int(dct_block[u, v])  # Extract modified coefficient
        bin_msg += str(coeff & 1)  # Extract the least significant bit (LSB)

        # Stop reading if the delimiter is detected
        if bin_msg.endswith(bin_delimiter):
            break  

    # Convert binary message back to text (excluding delimiter)
    bin_msg = bin_msg[:-len(bin_delimiter)]  # Remove delimiter before conversion
    msg_chars = [chr(int(bin_msg[i:i+8], 2)) for i in range(0, len(bin_msg), 8)]

    return ''.join(msg_chars)  # Return the decoded message
