import logging
from flask import Flask, request, render_template

#setting up the application name
app = Flask(__name__)

logging.basicConfig(filename="app.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


logging.getLogger("werkzeug").setLevel(logging.ERROR)


USERS = {"admin":"admin"}


@app.route("/")#homepage

def home():
        
        return render_template("login.html")



@app.route("/login", methods=["POST"])
def login():
        username = request.form.get("username","")
        password = request.form.get("password","")

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

        
        logging.warning("Failed login for user: %s",username)
        return """

<link rel="stylesheet" href="/static/style.css">
<div style="text-align:center; margin-top:60px;">
  <h2>Invalid credentials</h2>
  <p>Please try again.</p>
</div>
"""


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)







