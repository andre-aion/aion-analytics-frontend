from flask import Flask

from app import app

app = Flask(__name__)
app.config.from_object('config')


app.run(host='0.0.0.0', port=8080, debug=True)

