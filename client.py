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
    # Spead errors evenly (this version goes up to 14.287% errors)
    # The random version goes up to ~0.5% errors
    
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


# Get Generator matrix
G = linear_coding.getGeneratorMatrix()

# Encode file
encoded = linear_coding.encode_hamming(compressed_file,G)

# Add errors
errors_encoded = addErrors(encoded,userError)

# Turn encoded to base64
encoded_base64 = binascii.b2a_base64(errors_encoded.encode('utf-8'))

# Parameters will be a 2D array that contains the generator matrix and the stats
parameters = [G.tolist(),stats]

# Errors
errors = countErrors(encoded,errors_encoded)

# Entropy
ent = calc_ent(file)

# Send JSON to server
message = { 'encoded-message': encoded_base64.decode('utf-8'),
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