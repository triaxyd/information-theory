#Triantafyllos Xydis

import binascii
import random
import shannon_fano
import linear_coding
import entropy
import hashlib
import requests


# Calculate SHA256
def calcSHA256(file):
    sha256 = hashlib.sha256(file.encode('utf-8')).hexdigest()
    return sha256


# Add errors
def addErrors(encoded,errors_percentage):
    # Turn encoded to list
    encoded_list = [int(bit) for bit in encoded]

    # Add errors
    total_bits = len(encoded_list)
    num_errors = int(total_bits * errors_percentage / 100)
    error_positions = random.sample(range(total_bits), num_errors)
    
    # Flip bits in error positions
    for pos in error_positions:
        encoded_list[pos] = 1 - encoded_list[pos]
    
    # Turn list to string
    error_encoded = ''.join(str(bit) for bit in encoded_list)
    return error_encoded


# Count errors
def countErrors(encoded,erros_encoded):
    errors = 0
    for i in range(len(encoded)):
        if encoded[i] != erros_encoded[i]:
            errors += 1
    return errors


# Choose file and error length
while(True):
    try:
        userChoice = int(input("\n\t***\n\t1.myfile.txt\n\t2.myfile2.txt\n\t***\nChoose File:"))
        if userChoice == 1:
            chosenFile = "myfile.txt"
        elif userChoice == 2:
            chosenFile = "myfile2.txt"
        else:
            raise ValueError
        userError =  float(input("Error length (%): "))
        if userError>=0 and userError<=100:
            break
        raise ValueError
    except ValueError:
        print("Wrong input try again")

# Read file
file = open(chosenFile, 'r', encoding='utf-8').read()

# Get the SHA256 of the file
sha256 = calcSHA256(file)

# Compress file
compressed_file = shannon_fano.shannon_fano(file)

# Get Generator matrix
G = linear_coding.getGeneratorMatrix()

# Encode file
encoded = linear_coding.encode_hamming(compressed_file,G)

# Add errors
errors_encoded = addErrors(encoded,userError)

# Turn encoded to base64
encoded_base64 = binascii.b2a_base64(errors_encoded.encode('utf-8'))

# Parameters (turn matrix to list for JSON)
parameters = G.tolist()

# Errors
errors = countErrors(encoded,errors_encoded)

# Entropy
ent = entropy.calc_ent(file)

print("Message with errors:",errors_encoded)
print("Message after encoding:",encoded)
print("Message after compression:",compressed_file)


# Send JSON to server
message = { 'encoded-message': encoded_base64.decode('utf-8'),
            'compression-algorithm':'shannon-fano',
            'encoding':'linear',
            'parameters': parameters,
            'errors': errors,
            'SHA256':sha256,
            'entropy':ent
        }

response = requests.post('http://localhost:7500/upload', json=message)

# Check the response from the server
print("Status code:",response.status_code)
print("Message from server:",response.text)