import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user = session["user_id"]
    # collecting the necesary base data and store it together for display
    indexs = db.execute(
        "SELECT symbol, quote, SUM(shares) AS shares FROM purchase WHERE buyer = (SELECT username FROM users WHERE id = ?) GROUP BY symbol", user)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user)

    # storage for the total amount of ownd money (cash + stock)
    total = 0.0

    # add the dictionary with current price and price * shares // add shares to total
    for i in range(len(indexs)):
        index = lookup(indexs[i]["symbol"])
        indexs[i]["quote"] = index["name"]
        indexs[i]["price"] = "%.2f" % (index["price"])
        indexs[i]["total"] = float(indexs[i]["price"]) * float(indexs[i]["shares"])
        total += indexs[i]["total"]
        indexs[i]["total"] = "%.2f" % (indexs[i]["total"])

    total += cash[0]["cash"]
    total = "%.2f" % (total)
    cash = "%.2f" % (cash[0]["cash"])
    return render_template("index.html", cash=cash, indexs=indexs, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # gernal checks that user provides input and correct input (Cybersecurity)
        if not request.form.get("symbol"):
            return apology("You have to provide a symbol")
        elif not request.form.get("shares"):
            return apology("You have to provide amount of shares to buy")
        txt = request.form.get("shares")
        numeric = txt.isnumeric()
        if numeric == False:
            return apology("Has to be a whole number")
        if int(request.form.get("shares")) < 1:
            return apology("You have to provide a positiv amount of shares")

        # lookup the stocks current price
        elif lookup(request.form.get("symbol")) == None:
            return apology("Symbol does not exist")

        stringcheck = request.form.get("symbol")
        not_usable = ",;"
        if any(c in not_usable for c in stringcheck):
            return apology("Do not use , or ;")

        else:
            results = lookup(request.form.get("symbol"))
            user = session["user_id"]
            cash = db.execute("Select cash FROM users WHERE id = ?", user)
            # check if buying is possible
            total = float(request.form.get("shares")) * results["price"]
            if total > cash[0]["cash"]:
                return apology("Not enough money to buy this amount of stock")
            else:
                symbol = request.form.get("symbol")
                buyer = db.execute("SELECT username FROM users WHERE id = ?", user)
                shares = request.form.get("shares")
                price = results["price"]
                quote = results["name"]
                date = datetime.datetime.now()

                db.execute("INSERT INTO purchase(symbol, quote, buyer, shares, price, total, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           symbol, quote, buyer[0]["username"], shares, price, total, date)
                # track the amount of money spent also in your users database
                db.execute("UPDATE users SET cash = ? WHERE id = ?", ((cash[0]["cash"]) - total), user)

        flash("Bought!")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    user = session["user_id"]
    """Show history of transactions"""
    # collecting the necesary base data and store it together for display
    indexs = db.execute(
        "SELECT symbol, quote, shares, price, date FROM purchase WHERE buyer = (SELECT username FROM users WHERE id = ?)", user)

    # add the dictionary with current price and priceh * shares // add shares to total
    for i in range(len(indexs)):
        index = lookup(indexs[i]["symbol"])
        indexs[i]["quote"] = index["name"]
        indexs[i]["total"] = float(index["price"]) * float(indexs[i]["shares"])
        indexs[i]["total"] = "%.2f" % (indexs[i]["total"])

        if indexs[i]["shares"] > 0:
            indexs[i]["exchange"] = "Bought"
        if indexs[i]["shares"] < 0:
            indexs[i]["exchange"] = "Sold"

    return render_template("history.html", indexs=indexs)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # Look for the search inout
        search = request.form.get("symbol")

        not_usable = ",;"
        if any(c in not_usable for c in search):
            return apology("Do not use , or ;", 400)

        if not search:
            return apology("Must give a Quote", 400)

        results = lookup(search)

        if results == None:
            return apology("Quote does not exist", 400)

        results["price"] = usd(results["price"])
        # make use of the lookup function
        return render_template("quoted.html", name=results["name"], price=results["price"], symbol=results["symbol"])

    elif request.method == "GET":
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide Confirmation password", 400)

        # Personal touch check ensure numbers is involved in PW
        check = request.form.get("password")
        contains_digit = any(map(str.isdigit, check))
        if contains_digit == False:
            return apology("must provide password with number")

        # check for special characters
        stringcheck = request.form.get("username")
        special_characters = "!@#$%^&*()-+?_=<>/"
        if not any(c in special_characters for c in check):
            return apology("Has to contain a special character")
        not_usable = ",;"
        if any(c in not_usable for c in check):
            return apology("Do not use , or ;")
        if any(c in not_usable for c in stringcheck):
            return apology("Do not use , or ;")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username doesnt exists
        if len(rows) != 0:
            return apology("username already exists", 400)

        # Ensure password is the same
        elif request.form.get("password1") != request.form.get("password2"):
            return apology("password is not the same", 400)

        # Storing the User input in the Database
        db.execute("INSERT INTO users(username, hash) VALUES ( ?, ?)", request.form.get("username"),
                   generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))

        session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        txt = request.form.get("shares")
        numeric = txt.isnumeric()
        if numeric == False:
            return apology("Has to be a whole number")
        stringcheck = request.form.get("symbol")
        not_usable = ",;"
        if any(c in not_usable for c in stringcheck):
            return apology("Do not use , or ;")
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        # Ensure amount was submitted
        if not request.form.get("shares"):
            return apology("must provide amount")
        if 1 > float(request.form.get("shares")):
            return apology("must provide positiv amount")
        # to query through the database

        user = session["user_id"]
        # make checks
        # name
        resymbol = request.form.get("symbol")
        checksymbol = db.execute(
            "SELECT symbol FROM purchase WHERE buyer = (SELECT username FROM users WHERE id = ?) AND symbol = ?", user, resymbol)
        if checksymbol == None:
            return apology("Did not buy this stock")
        # amount
        amount = int(request.form.get("shares"))
        shares = db.execute(
            "SELECT symbol, SUM(shares) AS shares FROM purchase WHERE buyer = (SELECT username FROM users WHERE id = ?) AND symbol = ? GROUP BY symbol", user, resymbol)
        if len(shares) == 0:
            return apology("Quote not found")

        if amount > shares[0]["shares"]:
            return apology("Not enough stock")

        # convert amount into negativ
        amount = amount * (-1)
        # lookup current stock price
        stock = lookup(resymbol)
        buyer = db.execute("Select username FROM users WHERE id = ?", user)
        total = amount * stock["price"]
        date = datetime.datetime.now()

        cash = db.execute("Select cash FROM users WHERE id = ?", user)
        # store the sold in purchase symbol, quote, buyer, date, shares, price, total
        db.execute("INSERT INTO purchase(symbol, quote, buyer, shares, price, total, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   stock["symbol"], stock["name"], buyer[0]["username"], amount, stock["price"], total, date)
        # add the amount of money to the cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", ((cash[0]["cash"]) - total), user)

        flash("Successfully sold")
        return redirect("/")
    else:
        user = session.get("user_id")
        quote = db.execute("SELECT symbol FROM purchase WHERE buyer = (SELECT username FROM users WHERE id = ?) GROUP BY symbol", user)
        return render_template("sell.html", quotes=quote)
