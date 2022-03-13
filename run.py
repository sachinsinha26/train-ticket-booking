#!flask/bin/python
from app import app

# Override production settings.
app.config['SERVER_NAME'] = 'localhost:5000'
app.config['TESTING'] = True
app.config['FLASKS3_OVERRIDE_TESTING'] = False
app.config['FLASK_ASSETS_USE_S3'] = False

if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)
