#Triantafylos Xydis


import shannon_fano
import linear_coding

import numpy as np
import binascii

from entropy import calc_ent
from hashlib import sha256
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Processing file...")
    received_json = request.get_json()
    encoded_message = received_json['encoded-message']
    compression_algorithm = received_json['compression-algorithm']
    encoding = received_json['encoding']
    parameters = received_json['parameters']

    # Generator matrix is at the first position of the parameters array
    G = np.asmatrix(parameters[0])
    # Stats are at the second position of the parameters array
    stats = parameters[1]

    errors = received_json['errors']
    received_sha256 = received_json['SHA256']
    entropy = received_json['entropy']

    # Decode base64
    message = binascii.a2b_base64(encoded_message).decode('utf-8')

    # Decode file
    decoded , errors_fixed = linear_coding.decode_hamming(message,G)


    # Decompress file
    decompressed_file = shannon_fano.decompress(decoded,stats)

    # Calculate SHA256
    sha256_server = sha256(decompressed_file.encode('utf-8')).hexdigest()

    # Calculate entropy
    ent = calc_ent(decompressed_file)

    # Round entropy to 5 decimal places
    ent = round(ent,5)
    entropy = round(entropy,5)

    print("**********\n")
    print("RESULT FOR FILE: ", received_sha256 , "\n")
    print("Compression algorithm: ", compression_algorithm)
    print("Encoding: ", encoding)
    print("Errors received: ", errors)
    print("Errors fixed: ", errors_fixed)
    print("Entropy: ", ent)
    print("SHA256: ", sha256_server)
    print("\n\n**********\n")


    if received_sha256 == sha256_server and entropy == ent:
        return jsonify({'message': 'File received successfully!',
                        'errors': errors_fixed,
                        'entropy': ent,
                        'SHA256': sha256_server
        })
    else:
        return jsonify({'message': 'File corrupted!',
                        'errors': errors_fixed,
                        'entropy': ent,
                        'originalEntropy': entropy,
                        'originalSHA256': received_sha256,
                        'SHA256': sha256_server
        }), 400

if __name__ == '__main__':
    app.run(port=7500, debug=True)