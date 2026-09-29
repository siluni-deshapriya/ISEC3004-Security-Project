from flask import Flask, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "dev-key"

# fake database representing users in the banking app
accounts = {
"victim": {"password": "victim123", "balance": 1000}, # victim account
"attacker": {"password": "attacker123", "balance": 0}, # attacker account
"user": {"password": "user123", "balance": 500} # user acc for testing
}

@app.route("/") # home page
def home():
    return """
    <h2>Bank App</h2>
    <a href="/login"><button>Go to Login</button></a>""" # Go to /Login page - GET /login

@app.route("/login", methods=["GET", "POST"]) # login page
def login():
    if request.method == "POST": # if POSTed (submited)
        username = request.form["username"] # have the username
        password = request.form["password"] # have the password

        if username in accounts and accounts[username]["password"] == password: # if password maches
            session["user"] = username # create a cookie for the user
            return redirect(url_for("dashboard")) # direct to dashboard
        return "Invalid login. <a href='/login'>Try again</a>"
    return """
            <h2>Bank Login</h2>
            <form method="POST">
                Username: <input name="username"><br>
                <br>
                Password: <input name="password" type="password"><br>
                <br>
                <button type="submit">Login</button> 
            </form>
        """ # POST

@app.route("/dashboard") # dashboard
def dashboard():
    if "user" not in session: # if no user in session
        return redirect(url_for("login"))  # redirect to /login - GET
    
    user = session["user"] # Get the user name from session
    balance = accounts[user]["balance"] # Get the balance from user from fake db

    return f"""
        <h2>Welcome, {user}</h2>
        <p>Your balance: ${balance}</p>

        <h3>Transfer Funds</h3>
        <form method="POST" action="/transfer">
            To account: <input name="to"><br> 
            <br>
            Amount: <input name="amount"><br> 
            <br>
            <button type="submit">Transfer</button>
        </form> 

        <br>
        <a href="/logout">Logout</a>
    """ # Dashboard and transfer feature which POST form to /transfer and logout link /logout

# --- THE VULNERABILITY ---
# This transfer is done using only the session cookie.
# There is NO CSRF token check, so the server cannot tell whether
# this POST came from the real dashboard form or from an attacker.
# Any POST to /transfer with a valid session cookie is
# trusted and executed. this is the CSRF flaw.

@app.route("/transfer", methods=["POST"]) # Transfer code page - Transfer happens and display status
def transfer():
    if "user" not in session: # if no user in session
        return redirect(url_for("login")) # redirect to /login - GET
 
    sender = session["user"]  # Get the user name from session
    to = request.form["to"] # get the "to account" name from the form
    amount = int(request.form["amount"]) # get the "Ammount" from the form

    if accounts[sender]["balance"] >= amount and to in accounts: # check if user balance >= amount transfering AND the "to account" username is in fake db
        accounts[sender]["balance"] -= amount # decrease the amount from user
        accounts[to]["balance"] += amount # increase the amount from target
        return f"Transferred ${amount} to {to}. <a href='/dashboard'>Back</a>" #Confirmation and link to /dashboard

    return "Transfer failed. <a href='/dashboard'>Back</a>" # Transfer fail

@app.route("/logout") # logout
def logout():
    session.clear() # clear session/cookie
    return redirect(url_for("login")) # go to /login

if __name__ == "__main__":
    app.run(debug=True, port=5000)