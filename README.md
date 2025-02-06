# **Steganography Research for Capstone Project**

### **Authors:** Ryan Thornton, Maren White, Gavin Maybach

## **Project Overview**

This repository contains our research and implementation of **image-based steganography** for our capstone project. We explore two primary methods for hiding messages within images: **Least Significant Bit (LSB) Steganography** and **Discrete Cosine Transform (DCT) Steganography**. Our objective is to evaluate the effectiveness and detectability of these techniques in a **cybersecurity** context.

---

## **Code Explanation**

### **1. Least Significant Bit (LSB) Method**

LSB steganography embeds secret data by modifying the **least significant bit** of each pixel in an image. This ensures minimal perceptual change while effectively storing the message.

#### **Key Functions & Workflow**

1. **Binary Conversion (`data_to_binary`)**  
    Converts data (string, integer, bytes, numpy array) into binary format for encoding.
    
    ```python
    def data_to_binary(data):
        if isinstance(data, str):
            return ''.join(format(ord(char), '08b') for char in data)
        elif isinstance(data, int):
            return bin(data)[2:]
        elif isinstance(data, bytes):
            return ''.join(format(byte, '08b') for byte in data)
        elif isinstance(data, np.ndarray):
            return [format(i, '08b') for i in data]
        else:
            raise TypeError("Unsupported data type")
    ```
    
2. **Encoding (`data_encoding`)**
    
    - Converts the message into binary.
    - Iterates through image pixels, modifying the least significant bit of the **red, green, and blue (RGB) channels**.
    - Stops encoding when the **delimiter** (`=====`) is reached.
    
    ```python
    def data_encoding(image, data):
        data += DELIMITER  # Append delimiter to signal end
        bin_data = data_to_binary(data)
        data_index = 0
        data_len = len(bin_data)
    
        for row in image:
            for pixel in row:
                for channel in range(3):  # Modify RGB channels
                    if data_index < data_len:
                        pixel[channel] = int(format(pixel[channel], '08b')[:-1] + bin_data[data_index], 2)
                        data_index += 1
                    if data_index >= data_len:
                        break
        return image
    ```
    
3. **Decoding (`decoder`)**
    
    - Extracts the **least significant bits** from the image.
    - Reconstructs the message **bit-by-bit**.
    - Stops decoding when the **delimiter** is detected.
    
    ```python
    def decoder(image):
        binary_data = ''
        for row in image:
            for pixel in row:
                for channel in range(3):
                    binary_data += format(pixel[channel], '08b')[-1]  # Extract LSB
        
        all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
        decoded_data = ''.join(chr(int(byte, 2)) for byte in all_bytes)
        return decoded_data.split(DELIMITER)[0]
    ```
    

---

### **2. Discrete Cosine Transform (DCT) Method**

DCT-based steganography embeds data by modifying frequency components of an image rather than its pixel values. This approach is less detectable in compressed images (e.g., JPEGs).

#### **Mathematical Foundation of DCT**

The Discrete Cosine Transform (DCT) is a **Fourier-related transform** that represents an image as a sum of **cosine functions oscillating at different frequencies**. The transformation is defined as:

$$
C(u, v) = \frac{1}{4} \sum_{x=0}^{7} \sum_{y=0}^{7} f(x,y) \cos \left[ \frac{(2x+1)u \pi}{16} \right] \cos \left[ \frac{(2y+1)v \pi}{16} \right]

$$
Where:

- **f(x, y)** represents the pixel intensity at coordinate **(x, y)**
- **C(u, v)** is the transformed frequency domain representation
- **u, v** represent the spatial frequency components

DCT works by concentrating the **most important image information into the lowest frequency components**, which allows for subtle modifications in the high-frequency coefficients without noticeable visual degradation.

#### **Key Functions & Workflow**

4. **Apply DCT (`apply_dct`)**
    
    - Converts image blocks into **frequency domain representation**.
    - Uses **scipy.fftpack.dct** for **2D transformation**.
    
    ```python
    def apply_dct(blocks):
        return np.array([scipy.fftpack.dct(scipy.fftpack.dct(block.T, norm='ortho').T, norm='ortho') for block in blocks])
    ```
    
5. **Encoding (`encode_message`)**
    
    - Converts message to binary.
    - Modifies **low-frequency DCT coefficients**, typically at **u=1, v=2**, as they are less visually significant.
    
    ```python
    def encode_message(dct_blocks, message):
        bin_msg = data_to_binary(message) + DELIMITER
        data_index = 0
        
        for dct_block in dct_blocks:
            if data_index >= len(bin_msg):
                break
            u, v = 1, 2  # Frequency location for modification
            dct_block[u,v] = (dct_block[u,v] & ~1) | int(bin_msg[data_index])
            data_index += 1
        return dct_blocks
    ```
    

---

## **Future Work & Improvements**

### **To-Do List:**

- [x]  Expand the **mathematical explanation** of DCT and how different frequency coefficients affect image perception.
- [ ]  Research **GAN-based steganography**.
- [ ]  Reduce image distortion after encoding.
- [ ]  Implement error correction techniques for message retrieval.

---

### **Final Thoughts**

This project demonstrates how **steganography techniques** can be applied to **hide messages in images** using different encoding strategies. While LSB-based methods provide **high capacity**, they are more detectable. DCT-based methods offer **better robustness** but require **higher computational cost**. Further research will explore **GAN-based approaches** for improved undetectability.