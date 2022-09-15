# import logging
# import socket
# from codeitsuisse import app
# logger = logging.getLogger(__name__)

# @app.route('/', methods=['GET'])
# def default_route():
#     return "Python Template"


# logger = logging.getLogger()
# handler = logging.StreamHandler()
# formatter = logging.Formatter(
#         '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)



# if __name__ == "__main__":
#     logging.info("Starting application ...")
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.bind(('localhost', 0))
#     port = sock.getsockname()[1]
#     sock.close()
#     app.run(port=5000)
from flask import Flask, jsonify, request
from codeitsuisse import app

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route('/add')
def add():
    num1 = int(request.args.get('num1'));
    num2 = int(request.args.get('num2'));

    return f"{num1} + {num2} = {num1 + num2}"

#if __name__ == "__main__":
    #app.run(debug=True);
    #app.run(host="0.0.0.0", port=int("1234"), debug=True)
