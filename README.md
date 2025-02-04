Authors: Ryan Thornton, Maren White, and Gavin Maybach

## **Working Title:** Steganography Research for Capstone Project

### **Summary**

This GitHub repository represents our team's work in the field of **Steganography**. This field encompasses all methods of hiding data in **plain sight**. Our current focus is the implications of **image steganography** in the realm of **cybersecurity**.

---

# **Code Explanation**

## **Lines 1-4**

```python
import cv2
import numpy as np
import pyinputplus as pyip
import math
```

`cv2` and `numpy` enable us to work with images—`cv2` allows loading and viewing images, while `numpy` permits matrix operations on the image.

`pyinputplus` simplifies input handling, and `math` is used for basic mathematical operations.

---

## **Lines 6-11**

```python
DELIMITER = '====='
CHOICES = ['Int', 'String']
IMAGE = 'test.png'
if not IMAGE:
    IMAGE = input("Enter path to image: ")

IMAGE = cv2.imread(IMAGE)
```

Here, we set a **default image path** (`test.png`). If this is removed, the user is prompted to enter an image path. `cv2.imread()` is used to load the image.

- `DELIMITER` is appended to the end of the data (used later in the code) so the **decoder function** knows when the message ends.
- `CHOICES` defines the acceptable data types for encoding (currently **integer** or **string**).

---

## **Lines 14-24**

```python
def data_to_binary(data):
    if isinstance(data, str):
        return ''.join(format(ord(char), '08b') for char in data)  # Converts string
    elif isinstance(data, int):  # Converts int
        return bin(data)
    elif isinstance(data, bytes):  # Converts bytes
        return ''.join(format(byte, '08b') for byte in data)
    elif isinstance(data, np.ndarray):  # Converts numpy arrays
        return [format(i, '08b') for i in data]
    else:
        raise TypeError("Type not supported womp womp")
```

This function converts input data into **binary format** based on its type:

- **Strings**: Each character is converted to its **8-bit ASCII representation**.
- **Integers**: Converted to binary using `bin()`.
- **Bytes**: Each byte is represented in **8-bit binary**.
- **NumPy Arrays**: Pixel values are converted into their **binary equivalents**.

**Example:** Converting 'hello' to binary:

```python
>>> data_to_binary('hello')
'0110100001100101011011000110110001101111'
```

---

## **Lines 27-32**

```python
def fetch_message():
    option = pyip.inputMenu(CHOICES, numbered=True)
    if option == CHOICES[0]:
        return int(input("Enter int value: "))
    if option == CHOICES[1]:
        return input("Enter value: ")
```

This function prompts the user to select between an **integer or string input**, ensuring only supported data types are used.

---

## **Lines 34-39**

```python
def size_check(image, data):
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print(f'Max bytes to encode: {n_bytes}')
    if len(data) > n_bytes:
        raise ValueError('Insufficient bytes. Use a larger image or reduce the data size!')
    return True
```

This function **ensures that the image has sufficient capacity** to store the message:

- It calculates the **maximum bytes available** for encoding.
- If the message size **exceeds the image’s capacity**, an error is raised.

---

## **Lines 41-62**

```python
def data_encoding(image, data):
    data += DELIMITER
    data_index = 0
    bin_data = data_to_binary(data)  # Converting data to binary
    data_len = len(bin_data)

    for row in image:  # Iterate through pixels
        for pixel in row:
            r, g, b = data_to_binary(pixel)  # Convert pixel values to binary
            if data_index < data_len:  # Modify LSB
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
```

### **How Encoding Works:**

- The **data and delimiter** are converted to binary.
- Iterates through **each pixel** and **modifies the least significant bit (LSB)** of the **red, green, and blue channels**.
- The message is encoded **bit-by-bit** until the entire data is hidden.

---

## **Lines 64-80** (Decoding the Message)

```python
def decoder(image):
    print('Decoding...')
    binary_data = ''
    for row in image:
        for pixel in row:
            r, g, b = data_to_binary(pixel)
            binary_data += r[-1]  # Extract LSBs
            binary_data += g[-1]
            binary_data += b[-1]
    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]

    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-len(DELIMITER):] == DELIMITER:
            break
    return decoded_data[:-len(DELIMITER)]
```

### **How Decoding Works:**

- Extracts the **LSB from each color channel**.
- Reconstructs the **binary data**.
- Splits it into **8-bit segments** and converts them to characters.
- Stops when the **delimiter is detected**, ensuring **only the hidden message is retrieved**.

---

## **Main Execution (Lines 83-97)**

```python
if __name__ == '__main__':
    data = fetch_message()
    datab = data_to_binary(data)
    print(f'Original Data: {data}, Binary: {datab}')
    size_check(IMAGE, datab)
    cv2.imwrite('encode.png', data_encoding(IMAGE, datab))
    enc_im = cv2.imread('encode.png')
    decoded_data = decoder(enc_im)
    print(f'Decoded Message: {decoded_data}')
    if decoded_data == data:
        print("Yipee")
    else:
        print("Sadness envelopes me")
```

This is the **main script execution**:

1. Fetches user input.
2. Converts it to binary and checks if it fits inside the image.
3. **Encodes** the data into the image and saves it.
4. **Decodes** the image to retrieve the hidden message.
5. **Verifies the output**, printing `"Yipee"` if successful or `"Sadness envelopes me"` if not.

---

### **Final Notes**

This implementation successfully demonstrates **LSB-based steganography**, ensuring data is embedded **without noticeable changes** to the image. Further refinements could explore **error correction** or **compression methods** for larger messages.

# TO-DO:
    - [ ] Add to read me explainign DCT
    - [ ] Get deeper understanding of DCT math
    - [ ] Look into GAN based stego 
    - [ ] See about ensuring images are changed less, as they seem to be ruined afterwards. Perhaps file type