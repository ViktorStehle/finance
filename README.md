# finance
A website to simulate buying and selling of stock.


A web app via which you can manage portfolios of stocks. Not only will this tool allow you to check real stocks’ actual prices and portfolios’ values, it will also let you simulate buying and selling stocks by querying IEX for stocks’ prices.

### register
Via register, you are able to register for an account and log in! And you see your rows via phpLiteAdmin or sqlite3.
*Requires that a user input is a username, implemented as a text field whose name is username. Renders an apology if the user’s input is blank or the username already exists.
*Requires that a user input is a password, implemented as a text field whose name is password, and then that same password again, implemented as a text field whose name is confirmation. Renders an apology if either input is blank or the passwords do not match.
*Submit the user’s input via POST to /register.
*Inserts the new user into a database, storing a hash of the user’s password, not the password itself. 
![Screenshot_20230125_112558](https://user-images.githubusercontent.com/106766191/214589322-5eaf402f-a0f1-49cf-9b3e-6177bf5aa9ae.png)

### quote
Quote allows a user to look up a stock’s current price.
*Requires that a user inputs a stock’s symbol, implemented as a text field whose name is symbol.
*Submits the user’s input via POST to /quote.
*In response to a POST, quote can render that second template, embedding within it one or more values from lookup.
![Screenshot_20230123_062350](https://user-images.githubusercontent.com/106766191/214590287-e3326279-443e-480f-bd56-6d4c7e314773.png)

###buy
Buy enables a user to simulate buying stocks.
