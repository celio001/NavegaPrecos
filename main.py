from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def ola():
    return render_template('lista.html')


app.run()

if __name__ == "__main__":
    app.run(debug=True)