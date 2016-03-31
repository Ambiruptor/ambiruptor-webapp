from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/disambiguate.json', methods=['POST'])
def disambiguate():
    print("Received : %s" % request.form["text"])
    dummy_data = """[\
        {
            "begin" : 10,
            "end" : 15,
            "sense" : "Bar (place)",
            "url" : "https://en.wikipedia.org/wiki/Bar"
        },
        {
            "begin" : 18,
            "end" : 30,
            "sense" : "Plant (green)",
            "url" : "https://en.wikipedia.org/wiki/Plant"
        }
    ]"""
    return dummy_data


@app.route('/check-disambiguate.json', methods=['POST'])
def check_disambigation():
    print("Received : %s" % request.form["text"])
    dummy_data = """[\
        {
            "begin" : 10,
            "end" : 15,
            "sense" : "Bar (place)",
            "all_senses" : ["Bar (place)", "Bar (fish)", "Bar (chocolate)"],
            "url" : "https://en.wikipedia.org/wiki/Bar"
        },
        {
            "begin" : 18,
            "end" : 30,
            "sense" : "Plant (green)",
            "all_senses" : ["Plant (green)", "Plant (factory)", "Plant (person)"],
            "url" : "https://en.wikipedia.org/wiki/Plant"
        }
    ]"""
    return dummy_data


@app.route('/submit-corrections.json', methods=['POST'])
def submit_corrections():
    print("Received corrections to text:\n %s\n" % request.form["text"])
    print("Disambiguation: %s" % request.form["disambiguation"])
    print("Correct senses indices: %s" % request.form["sense_indices"])
    return "Success!"
    # TODO think how to save them nicely

if __name__ == '__main__':
    app.run(host='0.0.0.0')
