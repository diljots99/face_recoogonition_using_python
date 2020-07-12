from flask import Flask, render_template, Response
app = Flask(__name__)

@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')

if __name__ == '__main__':
    # defining server ip address and port
    app.run(port='5000', debug=True)