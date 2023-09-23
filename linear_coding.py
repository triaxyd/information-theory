
import numpy as np

# Hamming code (7,4)

def create_G():
    # Create G (generator matrix)
    # Identity matrix represents the data bits
    I = np.identity(4)

    # Turn I to a matrix of ints
    I = I.astype(int)

    # Create empty P matrix
    P = np.zeros((4,3))

    # Go through all rows of the identity matrix
    for i in range(4):
        # Get the bits of each column and store them in d1,d2,d3,d4
        d1 = I[i][0]
        d2 = I[i][1]
        d3 = I[i][2]
        d4 = I[i][3]

        # Calculate parity bits
        p1 = d1 ^ d2 ^ d4
        p2 = d1 ^ d3 ^ d4
        p3 = d2 ^ d3 ^ d4

        # Store the parity bits in the P matrix
        P[i][0] = p1
        P[i][1] = p2
        P[i][2] = p3
    
    # Create G matrix
    G = np.concatenate((I,P),axis=1)

    # Turn G to a matrix of ints
    G = G.astype(int)
    return G


def create_H():
    # Create H , the parity check matrix
    # H is the transpose of the right part of G
    G = create_G()
    P = np.transpose(G[:,4:])

    # Add the identity matrix to the left part of H
    H = np.concatenate((P,np.identity(3)),axis=1)

    # Turn H to a matrix of ints
    H = H.astype(int)
    return H


def encode(bits):
    encoded_messsage = ""

    # Create generator matrix G
    G = create_G()
    
    # Split the bits into 4 bit words
    words = [bits[i:i+4] for i in range(0, len(bits), 4)]

    # Encode each word
    for word in words: 
        # Turn word to a list of ints
        word = [int(bit) for bit in word]

        # Multiply word with G
        encoded_word = np.dot(word,G)

        # Mod 2 the result
        encoded_word = np.mod(encoded_word,2)

        # Turn the result to a string
        encoded_word = ''.join(str(bit) for bit in encoded_word)

        # Add the encoded word to the encoded message
        encoded_messsage = encoded_messsage + encoded_word
    
    return encoded_messsage



def decode(bits):
    # Create parity check matrix H
    H = create_H()
    
    # S = r * H^T and S = e * H^T
    # r = received word

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
    # Each row of Syndromes (3 bits) corresponds to the error vector of the same row in error_vectors(7 bits)
    Syndromes = np.asmatrix(Syndromes)

    # Divide message into 7-bit words
    codewords = [bits[i:i + 7] for i in range(0, len(bits), 7)]
    
    # For each word calculate the syndrome 
    decoded = []
    sum_errors_corrected = 0
    for codeword in codewords:
        # Convert word to vector
        word_vector = np.array([int(bit) for bit in codeword])

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
            decoded.append(codeword[0:4])
            continue

        # If the syndrome is not zero then find the error with the help of the Syndromes matrix
        # Find the row of the error in the Syndromes matrix
        error_row = np.where((Syndromes == S_vector).all(axis=1))[0][0]

        # We know the error vector is the same row in the error_vectors matrix
        error_vector = error_vectors[error_row]

        # XOR the error vector with the received word to get the corrected word
        corrected_word = np.bitwise_xor(word_vector, error_vector)

        # Turn the corrected word to a string
        corrected_word = ''.join(str(bit) for bit in corrected_word)
        
        # Remove the parity bits from the corrected word
        corrected_word = corrected_word[0:4]

        # Add the corrected word to the decoded message
        decoded.append(corrected_word)
        sum_errors_corrected += 1
        
    # Join decoded words
    decoded = ''.join(decoded)
    return decoded , sum_errors_corrected

    
    

