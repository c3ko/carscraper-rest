from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/multi/<int:num>', methods=['GET'])
def get_mult10(num):
    return jsonify({'result': num * 10 })
if __name__ == '__main__':
    app.run(debug=True)