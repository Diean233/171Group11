from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    date = request.form.get('date')
    print("The date received is", date)

    pred = "the predicted date you chose is: " + date
    return render_template('index.html', prediction=pred)

if __name__ == '__main__':
    app.run(port=3000, debug=True)