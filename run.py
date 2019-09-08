from flask import Flask

app = Flask(__name__)
app.config.from_object('config')


app.run(host='0.0.0.0', debug=True)

# run using v
# fabmanager run --port 5005

# sudo systemctl start analytics-frontend
# sudo systemctl stop analytics-frontend

