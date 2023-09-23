
import binascii
import random

from shannon_fano import compress,shannon_fano
from linear_coding import encode
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

# Get stats
stats = shannon_fano(file)

# Compress file
compressed_file = compress(file,stats)

print(stats)
print(len(compressed_file))
print(compressed_file)

# Add 0s to the end of file to make it divisible by 4
padding = 0
while len(compressed_file) % 4 != 0:
    compressed_file += '0'
    padding += 1 

print(len(compressed_file))
print(compressed_file)

# Encoding
encoded_file = encode(compressed_file)

print(len(encoded_file))
print(encoded_file)

# Add errors
errors_encoded = addErrors(encoded_file,userError)
print(len(errors_encoded))
print(errors_encoded)

# Count errors
errors = countErrors(encoded_file,errors_encoded)
print(errors)

# Entropy
ent = calc_ent(file)

# Turn to base64
encoded_file = binascii.b2a_base64(encoded_file.encode('utf-8')).decode('utf-8')
print(encoded_file)
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