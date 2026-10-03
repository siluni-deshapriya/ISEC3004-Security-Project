import logging
from flask import Flask, request, render_template

#creating the web application object; __name__ tells Flask where this file is
app = Flask(__name__)

# send logs to app.log; record INFO level and above
logging.basicConfig(filename="app.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

logging.getLogger("werkzeug").setLevel(logging.ERROR)

#fake user
USERS = {"admin":"admin"}

@app.route("/")#homepage
def home():
        #load and send templates/login.html to the browse
        return render_template("login.html")

# handle POST requests sent to "/login"
@app.route("/login", methods=["POST"])
def login():
        #reading the fields from the form.    
        username = request.form.get("username","")
        password = request.form.get("password","")

        #password validation.
        if USERS.get(username)==password:
            logging.info("Successful login for user: %s",username)
            #css for the success ful login
            return """

<link rel="stylesheet" href="/static/style.css">
<div style="text-align:center; margin-top:60px;">
  <h2>Welcome to the patient portal</h2>
  <p>You are now logged in.</p>
</div>
"""
        #this is the VULNERABILITY- because this allows the raw username written to the log without sanitizing.
        logging.warning("Failed login for user: %s",username)
        #css for the failed login
        return """

<link rel="stylesheet" href="/static/style.css">
<div style="text-align:center; margin-top:60px;">
  <h2>Invalid credentials</h2>
  <p>Please try again.</p>
</div>
"""

# only run this if the file is executed directly
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)







