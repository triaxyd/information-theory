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

    # S = r * H^T and S = e * H^T

    # Get parity matrix from generator matrix
    P = G[:, 4:]

    # Parity check matrix is the transpose of the parity matrix and the identity matrix
    H = np.hstack((P.transpose(), np.identity(3)))

    # Get the error vector e
    error_vectors = np.identity(7, dtype=int)
    error_vectors = np.vstack((np.zeros(7, dtype=int), error_vectors))
    
    # For each row of error_vectors calculate the syndrome and add it to a new matrix called Syndromes
    Syndromes = []
    for row in error_vectors:
        S_vector = np.dot(row, H.transpose()) % 2
        # Turn S values to int and then to string
        S_vector = ''.join(str(int(bit)) for bit in S_vector.flat)
        # Turn syndrome to vector
        S_vector = np.array([int(bit) for bit in S_vector])
        Syndromes.append(S_vector)

    # Turn Syndromes to matrix
    Syndromes = np.asmatrix(Syndromes)
    # Each row of Syndromes (3 bits) corresponds to the error vector of the same row in error_vectors(7 bits)


    # Divide message into 7-bit words
    words = [message[i:i + 7] for i in range(0, len(message), 7)]
    
    # For each word calculate the syndrome 
    decoded = []
    sum_errors_corrected = 0
    for word in words:
        # Convert word to vector
        word_vector = np.array([int(bit) for bit in word])

        # Calculate syndrome which is dot product of parity check matrix and transposed word vector
        S = np.dot(H, word_vector.transpose()) % 2

        # Turn S values to int and then to string
        S = ''.join(str(int(bit)) for bit in S.flat)
        
        # Turn syndrome to vector
        S_vector = np.array([int(bit) for bit in S])

        # If the syndrome is zero then there is no error
        # If the syndrome is not zero then there is an error
        # The position of the row is the position of the error

        if np.array_equal(S_vector, np.zeros(3, dtype=int)):
            decoded.append(word[0:4])
            continue

        # Find the position of the error
        for i in range(len(Syndromes)):
            # Turn Syndromes[i] to vector
            syndrome_pos = np.array(Syndromes[i])[0]
            if np.array_equal(S_vector, syndrome_pos):
                # The correct word is the word with the error bit flipped, so we xor the word with the error vector
                correct_word = np.bitwise_xor(word_vector, error_vectors[i])
                
                # Turn correct word to string
                correct_word = ''.join(str(bit) for bit in correct_word)

                # Add the corrected word to the decoded message
                decoded.append(correct_word[0:4])
                sum_errors_corrected += 1
                break
            

    # Join decoded words
    decoded = ''.join(decoded)
    return decoded , sum_errors_corrected