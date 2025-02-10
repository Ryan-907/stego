from main import data_to_binary

CHOICES = ['Int', 'String']
                

def size_check(image, bin_data): #Ensures selected image is large enough to contain all the data
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print(f'Max bytes to encode {n_bytes}')
    if len(bin_data) > n_bytes:
        raise ValueError('Insufficient bytes. Require larger image or less data!')
    return True

def data_encoding(image, bin_data): #Encodes data in image using lSB 
    data_index = 0
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

def decoder(image, DELIMITER):
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

