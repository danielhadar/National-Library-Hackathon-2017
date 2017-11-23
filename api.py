from flask import Flask, request
from flask_jsonpify import jsonpify

import socket

from main import process_image

def get_ip_address():
    """ get ip-address of interface being used """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

IP = get_ip_address()

app = Flask(__name__)

@app.route('/photo', methods=['GET'])
def hello_world():
    image_url = request.args.get('image_url', 'no image was sent')
#    print image_url
    call_code(image_url)
#    print "finished"
    return jsonpify(processed_image="http://34.239.198.2/final_image.png")

def call_code(image_url):
    process_image(image_url, True, True, False, False)

if __name__ == '__main__':
    app.run(host=IP, port=5000, debug=False)
