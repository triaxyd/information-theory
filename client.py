
import os
import binascii
import requests
import base64

from PIL import Image
from hashlib import sha256
from shannon_fano import compress,shannon_fano
from linear_coding import encode
from entropy import calc_ent



# Add errors
def addErrors(encoded,errors_percentage):
    # Turn encoded to list
    encoded_list = [int(bit) for bit in encoded]

    # Add errors
    total_bits = len(encoded_list)

    num_errors = int(total_bits * errors_percentage / 100)

    # Get random positions for errors and try to spread them evenly
    # 2 Different ways to do it, 1 random and 1 evenly

    #error_positions = random.sample(range(total_bits), num_errors)
    error_positions = []
    for i in range(num_errors):
        error_positions.append(int(i * total_bits / num_errors))

    
    # Flip bits in error positions
    for pos in error_positions:
        encoded_list[pos] = 1 - encoded_list[pos]
    
    # Turn list to string
    error_encoded = ''.join(str(bit) for bit in encoded_list)
    return error_encoded



# Count errors
def countErrors(encoded,errors_encoded):
    errors = 0
    for i in range(len(encoded)):
        if encoded[i] != errors_encoded[i]:
            errors += 1
    return errors



print("\n**********\n")
# Choose error length
while(True):
    try:
        userOption = int(input("Choose file (1)text (2)image: "))
        if not(userOption==1 or userOption==2):
            raise ValueError
    
        userError =  float(input("Choose error length (0-100): "))
        if userError>=0 and userError<=100:
            break
        raise ValueError
    except ValueError:
        print("Wrong input try again")


if userOption == 1:
    chosenFile = "myfile.txt"
    file = open(chosenFile, 'r', encoding='utf-8').read()
else:
    chosenFile = "dog.png"
    if os.path.exists(chosenFile):
        print(f"File '{chosenFile}' exists.")
    else:
        print(f"File '{chosenFile}' does not exist.")
        exit()
    
    # Open image
    with open(chosenFile,'rb') as image:
        base64_image = base64.b64encode(image.read())
        file = base64_image.decode('utf-8')

    

img = Image.open(chosenFile)
img.show()
# Get the SHA256 of the file
sha256_file = sha256(file.encode('utf-8')).hexdigest()

# Get stats
stats = shannon_fano(file)

# Compress file
compressed_file = compress(file,stats)

# Add 0s to the end of file to make it divisible by 4
padding = 0
while len(compressed_file) % 4 != 0:
    compressed_file += '0'
    padding += 1 


# Encoding
encoded_file = encode(compressed_file)

# Add errors
errors_encoded = addErrors(encoded_file,userError)

# Count errors
errors = countErrors(encoded_file,errors_encoded)

# Entropy
ent = calc_ent(file)

# Turn to base64
encoded_file = binascii.b2a_base64(errors_encoded.encode('utf-8')).decode('utf-8')

parameters = [stats,padding]

# Send JSON to server
message = { 'encoded-message': encoded_file,
            'compression-algorithm':'shannon-fano',
            'encoding':'linear',
            'parameters': parameters,
            'errors': errors,
            'SHA256':sha256_file,
            'entropy':ent
        }

response = requests.post('http://localhost:7500/upload', json=message)

# Check the response from the server
print("\nMessage from server:",response.text)
print("Status code:",response.status_code)
print("\nCLIENT TERMINATED\n")
print("\n**********\n")