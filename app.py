from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/disambiguate.json', methods=['POST'])
def disambiguate():
    print("Received : %s" % request.form["text"])
    dummy_data = """[\
{"begin" : 10, "end" : 15, "url" : "https://en.wikipedia.org/wiki/Bar"},
{"begin" : 18, "end" : 30, "url" : "https://en.wikipedia.org/wiki/Plant"}]"""
    return dummy_data

if __name__ == '__main__':
    app.run(host='0.0.0.0')
