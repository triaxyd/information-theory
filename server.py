#Triantafylos Xydis

import binascii

import shannon_fano
import linear_coding

import numpy as np

from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    received_json = request.get_json()
    print("**********\n")
    print("SERVER RECEIVED\n\n",received_json)
    print("\n**********")
    encoded_message = received_json['encoded-message']
    compression_algorithm = received_json['compression-algorithm']
    encoding = received_json['encoding']
    parameters = received_json['parameters']

    #Get Generator matrix from parameters
    G = np.asmatrix(parameters)

    errors = received_json['errors']
    sha256 = received_json['SHA256']
    entropy = received_json['entropy']

    # Decode base64
    message = binascii.a2b_base64(encoded_message).decode('utf-8')

    # Decode file
    decoded = linear_coding.decode_hamming(message,G)

    # Decompress file
    #decompressed_file = shannon_fano.decompress(decoded)





    response = {
        'status':'success',
        'message':'Message received'
    }
    #print (f'Encoded Message:{encoded_message}\nCompression Algorithm:{compression_algorithm}\nEncoding:{encoding}\nParameters:{parameters}\nErrors:{errors}\nSHA256:{sha256}\nEntropy:{entropy}')
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=7500, debug=True)