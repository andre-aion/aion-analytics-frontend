from app import app

if __name__ == '__main__':
    app.run()

"""
run server
- gunicorn -b 0.0.0.0:5005 --workers=5 wsgi

to register changes
- sudo systemctl restart analytics-frontend

"""