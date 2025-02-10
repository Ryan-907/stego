import cv2
import tkinter as tk
from tkinter import filedialog as fd
import numpy as np
import LSb
import DCT
#Constants
FILETYPES = [("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff;*.webp"),
    ("PNG Files", "*.png"),
    ("JPEG Files", "*.jpg;*.jpeg")]

DELIMITER = '=='

METHODS = ['Least Significant Bit', 'Discrete Cosine Transform']



def fetch_image():
    selection = fd.askopenfilename(filetypes=FILETYPES)
    return selection

def fetch_message():
    root = tk.Tk()
    root.title("Enter Message")

    tk.Label(root, text="Enter message:").pack(pady=5)

    entry = tk.Entry(root)
    entry.pack(pady=5)
    entry.focus()

    input_var = tk.StringVar()

    entry.bind("<Return>", lambda event: (input_var.set(entry.get()), root.destroy()))

    root.wait_window()

    return input_var.get()

def data_to_binary(data):
    if isinstance(data, str):
        bin_data = ''.join(format(ord(char), '08b') for char in data)
        return bin_data
    elif isinstance(data, int): #Converts int
        bin_data = format(data, '08b')
        return bin_data 
    elif isinstance(data, bytes): #Converts bytes
        bin_data = ''.join(format(byte, '08b') for byte in data)
        return bin_data 
    elif isinstance(data, np.ndarray): #Converts numpy arrays
        bin_data = [format(i, '08b') for i in data]
        return bin_data 
    else:
        raise TypeError("Type not supoprted womp womp")

def stego_method():
    root = tk.Tk()
    root.title('Select stego method')

    method = tk.StringVar()
    method.set(METHODS[0])

    tk.OptionMenu(root, method, *METHODS).pack()

    root.bind("<Return>", lambda event: root.destroy())

    root.mainloop()

    return method.get()

def lsb(image, bin_data):
    valid_size = LSb.size_check(image, bin_data)
    if valid_size:
        encoded = LSb.data_encoding(image, bin_data)
        return encoded
    else:
        raise ValueError('Something wrong happened')
    


if __name__=='__main__':
    #Image Handling
    image = fetch_image()
    image = cv2.imread(image)
    image = cv2.resize(image, (800,400))
    cv2.imshow('Selected Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #Message Handling
    msg = fetch_message()
    msg_bin = data_to_binary(msg) + data_to_binary(DELIMITER)
    method = stego_method()
    if method == METHODS[0]:
        stego_image = lsb(image, msg_bin)
        cv2.imwrite("LSBEncoded.png", stego_image)

    elif method == METHODS[1]:
        image = DCT.gray_scale(image)  
        image = DCT.size_adjust(image)  
        height, width = image.shape  

        blocks = DCT.blocking(image)  
        dct_blocks = DCT.apply_dct(blocks)  
        encoded_blocks = DCT.encode_message(dct_blocks, msg_bin) s
        idct_blocks = DCT.invert_dct(encoded_blocks)  
        recon_img = DCT.reassemble_image(idct_blocks, height, width) 

        cv2.imwrite('encode_dct.png', recon_img) 
        cv2.imshow('DCT Encoded', recon_img)  
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(DCT.decode_dct(encoded_blocks, data_to_binary(DELIMITER)))

    else:
        raise TypeError('Unsupported method')


    

    
   