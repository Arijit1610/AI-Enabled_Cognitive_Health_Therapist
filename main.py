from flask import Flask, render_template
app = Flask(__name__)
#route for home page
@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html')
app.run(debug=True) 