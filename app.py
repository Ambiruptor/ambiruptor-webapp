from flask import Flask, render_template, request
from utils import format_correction_corpus
from utils import disambiguation

import json


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/ambiruptor')
def ambiruptor():
    return render_template('ambiruptor.html')


@app.route('/disambiguate.json', methods=['POST'])
def disambiguate():
    disamb = disambiguation(request.form["text"])
    return disamb


@app.route('/check-disambiguate.json', methods=['POST'])
def check_disambigation():
    # print("Received : %s" % request.form["text"])
    print("Received : %s" % request.form["disamb"])
    return request.form["disamb"]


@app.route('/submit-corrections.json', methods=['POST'])
def submit_corrections():
    text = request.form["text"]
    disamb = request.form["disambiguation"]
    corrections = json.loads(request.form["sense_indices"])
    corpus = format_correction_corpus(text, disamb, corrections)
    with open('corpus/corrections.dump', 'a') as f:
        try:
            f.write(str(corpus))
            f.write("\n")
        except BaseException as e:
            print(e)
    return "Success!"
    # TODO think how to save them nicely

if __name__ == '__main__':
    app.run(host='0.0.0.0')
