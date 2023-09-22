#Triantafyllos Xydis

import binascii
import random
import shannon_fano
import linear_coding
import requests

from entropy import calc_ent
from hashlib import sha256



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
print("CLIENT STARTED\n")
# Choose error length
while(True):
    try:
        userError =  float(input("Choose error length (0-100): "))
        if userError>=0 and userError<=100:
            break
        raise ValueError
    except ValueError:
        print("Wrong input try again")


chosenFile = "myfile.txt"
# Read file
file = open(chosenFile, 'r', encoding='utf-8').read()

# Get the SHA256 of the file
sha256_file = sha256(file.encode('utf-8')).hexdigest()

# Compress file
compressed_file , stats = shannon_fano.shannon_fano(file)

# Encoding


# Entropy
ent = calc_ent(file)

# Send JSON to server
message = { 'encoded-message': 0,
            'compression-algorithm':'shannon-fano',
            'encoding':'linear',
            'parameters': 0,
            'errors': 0,
            'SHA256':sha256_file,
            'entropy':ent
        }

response = requests.post('http://localhost:7500/upload', json=message)

# Check the response from the server

print("\nMessage from server:",response.text)
print("Status code:",response.status_code)
print("\nCLIENT TERMINATED\n")
print("\n**********\n")