#Triantafylos Xydis

from flask import Flask, request , jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    received_json = request.get_json()
    encoded_message = received_json['encoded-message']
    compression_algorithm = received_json['compression-algorithm']
    encoding = received_json['encoding']
    parameters = received_json['parameters']
    errors = received_json['errors']
    sha256 = received_json['SHA256']
    entropy = received_json['entropy']


    print (f'Encoded Message:{encoded_message}\nCompression Algorithm:{compression_algorithm}\nEncoding:{encoding}\nParameters:{parameters}\nErrors:{errors}\nSHA256:{sha256}\nEntropy:{entropy}')
    response = {
        'status':'success',
        'message':'Message received'
    }
    print(received_json)
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=7500, debug=True)