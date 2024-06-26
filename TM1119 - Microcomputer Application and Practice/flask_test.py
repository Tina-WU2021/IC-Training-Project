# Importing the flask module
from flask import Flask
 
# Create a flask object named app
app = Flask(__name__)
 
# Once you enter the IP address of Raspberry Pi in the browser, below code will run.
@app.route("/")
def main():
    return "Hello, Welcome to IoT Starters"
 
#if code is run from terminal
if __name__ == "__main__":
    # Server will listen to port 80 and will report any errors.
   app.run(host='0.0.0.0', port=80, debug=True)