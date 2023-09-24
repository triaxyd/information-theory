
import base64
import binascii
import os

from PIL import Image, ImageDraw, ImageFont , UnidentifiedImageError
from linear_coding import decode
from shannon_fano import decompress
from entropy import calc_ent
from hashlib import sha256
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    print("\n**********\nPROCESSING NEW FILE...\n")
    received_json = request.get_json()
    encoded_message = received_json['encoded-message']
    compression_algorithm = received_json['compression-algorithm']
    encoding = received_json['encoding']
    parameters = received_json['parameters']

    stats = parameters[0]
    padding = parameters[1]
    message_type = parameters[2]

    errors = received_json['errors']
    received_sha256 = received_json['SHA256']
    entropy = received_json['entropy']
    
    # Decode base64 message to binary
    message = binascii.a2b_base64(encoded_message).decode('utf-8')

    # Decode Hamming
    decoded , errors_fixed = decode(message)

    # Remove padding
    decoded = decoded[0:len(decoded)-padding]
    
    # Decompress file
    decompressed_file = decompress(decoded,stats)

    # Calculate SHA256
    sha256_server = sha256(decompressed_file.encode('utf-8')).hexdigest()

    # Calculate entropy
    ent = calc_ent(decompressed_file)

    # Round entropy to 5 decimal places
    ent = round(ent,5)
    entropy = round(entropy,5)

    # If the message is text then print it
    if message_type == 1:
        print("\n*FINAL MESSAGE:\n ", decompressed_file)
    else:
        # The message is image
        try:
            # Turn base64 string to image and show it
            imgdata = base64.b64decode(decompressed_file)
            filename = 'finalimage.jpg'

            # If the file exists then delete it
            if os.path.exists(filename):
                os.remove(filename)

            with open(filename, 'wb') as f:
                f.write(imgdata)

            # Show image and add caption to image
            img = Image.open(filename)

            # Add caption as a text overlay
            caption = "SERVER IMAGE"
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default() 

            # Position of the text
            position = (10, 10)  
            draw.text(position, caption, font=font, fill="white")

            # Show image
            img.show()
            # Remove the image from saved files
            if os.path.exists(filename):
                os.remove(filename)
            

        except UnidentifiedImageError:
            # Remove the image from saved files
            if os.path.exists(filename):
                os.remove(filename)
            print("The file could not be shown because of corruption.")

    print("\nRESULT FOR FILE: ", received_sha256 , "\n")
    print("Compression algorithm: ", compression_algorithm)
    print("Encoding: ", encoding)
    print("Errors received: ", errors)
    print("Errors fixed: ", errors_fixed)
    print("Entropy: ", ent)
    print("SHA256: ", sha256_server)
    print("\n\n**********\n")

    if received_sha256 == sha256_server and entropy == ent:
        return jsonify({'message': 'FILE RECEIVED SUCCESSFULLY!',
                        'errors': errors_fixed,
                        'entropy': ent,
                        'SHA256': sha256_server
        }) , 200
    else:
        return jsonify({'message': 'THE FILE WAS CORRUPTED DURING TRANSMISSION!',
                        'errors': errors,
                        'fixedErrors': errors_fixed,
                        'entropy': ent,
                        'originalEntropy': entropy,
                        'originalSHA256': received_sha256,
                        'SHA256': sha256_server
        }), 400

if __name__ == '__main__':
    app.run(port=7500, debug=True)