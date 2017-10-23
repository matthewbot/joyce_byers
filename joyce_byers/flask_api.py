from flask import Flask

app = Flask('joyce_byers')

@app.route('/')
def hello_world():
	return 'Hello world'