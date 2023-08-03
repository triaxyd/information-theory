#Triantafyllos Xydis

import numpy as np

# Hamming (7,4) code

def getGeneratorMatrix():
    G = np.array([[1, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 1, 1, 0],
                [0, 0, 1, 0, 1, 0, 1],
                [0, 0, 0, 1, 0, 1, 1]])
    # Turn to matrix
    G = np.asmatrix(G)
    return G


def encode_hamming(file, G):
    # Add padding
    while len(file) % 4 != 0:
        file += "0"

    # Divide file into 4-bit words
    words = [file[i:i + 4] for i in range(0, len(file), 4)]

    # Encode each word
    codewords = []
    for word in words:
        row_vector = np.array([int(bit) for bit in word])
        codeword_vector = np.dot(row_vector, G) % 2
        codeword_str = ''.join(str(bit) for bit in codeword_vector.flat)
        codewords.append(codeword_str)

    # Join codewords and return the encoded message as a string
    encoded = ''.join(codewords)
    return encoded


def decode_hamming(message, G):
    # Get parity matrix from generator matrix
    P = G[:, 4:]

    # Parity check matrix is the transpose of the parity matrix and the identity matrix
    H = np.hstack((P.transpose(), np.identity(3)))

    # Divide message into 7-bit words
    words = [message[i:i + 7] for i in range(0, len(message), 7)]
    
    # For each word calculate the syndrome 
    decoded = []
    for word in words:
        # Convert word to vector
        word_vector = np.array([int(bit) for bit in word])
        print(word_vector)

        # Calculate syndrome which is dot product of parity check matrix and transposed word vector
        S = np.dot(H, word_vector.transpose()) % 2
        print(S)
        
































'''
from sage.all import *


# Hamming (7,4) code


def getGeneratorMatrix():
    C = codes.HammingCode(GF(2), 3)
    G = C.generator_matrix()
    print(C)
    return G


def encode_message(file,G):
    # Add padding
    while (len(file) % 4 != 0):
        file += "0"

    # Divide file into 4-bit words
    words = [file[i:i+4] for i in range(0, len(file), 4)]
    
    # Encode each word
    codewords = []
    for word in words:
        row_vector = vector(GF(2), [int(bit) for bit in word])
        codeword_vector = row_vector * G
        codeword = ''.join(str(bit) for bit in codeword_vector)
        codewords.append(codeword)

    # Join codewords
    encoded = ''.join(codewords)
    return encoded


def decode_message(message, G):
    # Get parity matrix from generator matrix
    P = G[:, 4:]

    # Parity check matrix is the transpose of the parity matrix and the identity matrix
    H = P.transpose().augment(identity_matrix(3))

    # Divide message into 7-bit words
    words = [message[i:i+7] for i in range(0, len(message), 7)]

    # Decode each word
    decoded = []
    for word in words:
        # Convert word to vector
        #word_vector = vector(GF(2), [int(bit) for bit in word])
        print(word)
'''