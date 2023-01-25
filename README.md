# finance
A website to simulate buying and selling of stock.


A web app via which you can manage portfolios of stocks. Not only will this tool allow you to check real stocks’ actual prices and portfolios’ values, it will also let you simulate buying and selling stocks by querying IEX for stocks’ prices.

Via register, you are able to register for an account and log in! And you see your rows via phpLiteAdmin or sqlite3.
*Requires that a user input is a username, implemented as a text field whose name is username. Renders an apology if the user’s input is blank or the username already exists.
*Requires that a user input is a password, implemented as a text field whose name is password, and then that same password again, implemented as a text field whose name is confirmation. Renders an apology if either input is blank or the passwords do not match.
*Submit the user’s input via POST to /register.
*Inserts the new user into a database, storing a hash of the user’s password, not the password itself. 
