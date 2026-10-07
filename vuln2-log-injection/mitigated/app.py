import os
import logging
from flask import Flask, request, render_template
import re 
#creating the web application object; __name__ tells Flask where this file is
app = Flask(__name__)



#Mitigation 01 : Inpuit vadidation 
# This only allows a safe expected character set for usernames (letters, digits, dot, unserscore, hyphen, 1- 32 chars). This rejects CR(\r), LF(\n) and any other unxepected
# character before the value is ver used anywhere including a log statement.

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9._-]{1,32}$")

def sanitize_for_log(value: str) -> str:
        
    """Sanitize a string for safe logging."""
        # Mitigation 02 : Sanitization
        # This replaces any CR or LF characters with a safe placeholder. This prevents log injection attacks.

    return value.replace("\r", "\\r").replace("\n", "\\n")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "app.log")

# send logs to app.log; record INFO level and above
logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
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


#Mitigation - reject anything outside the expected username format before it is used anywhere including logging.
        if not USERNAME_PATTERN.match(username):
                logging.warning("failed login attempt with invalid username format (Input rejected)")
                return """
<link rel= stylesheet" href="/static/style.css">
<div style="text-align:center; margin-top:60px;">
        <h2>Invalid credentials</h2>
        <p>Please try again.</p>
</div>
""",400

        
        #password validation.
        if USERS.get(username)==password:
                #Mitigation - sanitize before logging
            logging.info("Successful login for user: %s", sanitize_for_log(username))
            #css for the success ful login
            return """

<link rel="stylesheet" href="/static/style.css">
<div style="text-align:center; margin-top:60px;">
  <h2>Welcome to the patient portal</h2>
  <p>You are now logged in.</p>
</div>
"""

        #this is the VULNERABILITY- because this allows the raw username written to the log without sanitizing.
        
        #mitigation - sanitize before logging
        logging.warning("Failed login for user: %s",sanitize_for_log(username))
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







