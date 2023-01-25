# finance

A web app via which you can manage portfolios of stocks. Not only will this tool allow you to check real stocks’ actual prices and portfolios’ values, it will also let you simulate buying and selling stocks by querying IEX for stocks’ prices.

### register
Via register, you are able to register for an account and log in! And you see your rows via phpLiteAdmin or sqlite3.

1. Requires that a user input is a username, implemented as a text field whose name is username. Renders an apology if the user’s input is blank or the username already exists.
2. Requires that a user input is a password, implemented as a text field whose name is password, and then that same password again, implemented as a text field whose name is confirmation. Renders an apology if either input is blank or the passwords do not match.
3. Submit the user’s input via POST to /register.
4. Inserts the new user into a database, storing a hash of the user’s password, not the password itself. 

![Screenshot_20230125_112558](https://user-images.githubusercontent.com/106766191/214589322-5eaf402f-a0f1-49cf-9b3e-6177bf5aa9ae.png)
## index
Index displays an HTML table summarizing, for the user currently logged in, which stocks the user owns, the numbers of shares owned, the current price of each stock, and the total value of each holding (i.e., shares times price). Also display the user’s current cash balance along with a grand total (i.e., stocks’ total value plus cash).

![Screenshot_20230123_062234](https://user-images.githubusercontent.com/106766191/214593293-08cb3147-a370-41be-a5c2-8f004b3d2ba2.png)
## quote
Quote allows a user to look up a stock’s current price.
1. Requires that a user inputs a stock’s symbol, implemented as a text field whose name is symbol.
2. Submits the user’s input via POST to /quote.
3. In response to a POST, quote can render that second template, embedding within it one or more values from lookup.
![Screenshot_20230123_062350](https://user-images.githubusercontent.com/106766191/214590287-e3326279-443e-480f-bd56-6d4c7e314773.png)

## buy
Buy enables a user to simulate buying stocks.
1. Requires that a user inputs a stock’s symbol, implemented as a text field whose name is symbol. Renders an apology if the input is blank or the symbol does not exist.
2. Requires that a user inputs a number of shares, implemented as a field whose name is shares. Renders an apology if the input is not a positive integer.
3. Requires that the users cash is positive, the stock price is up to date and stores the inforamtion about a purchase in a database.

![Screenshot_20230123_062121](https://user-images.githubusercontent.com/106766191/214592477-f48180ad-dc8e-4c77-a422-87ab9c5e84d3.png)
## sell
Sell enables a user to sell shares of a stock (that he or she owns).
1. Requires that a user inputs a stock’s symbol, implemented as a select menu whose name is symbol. Renders an apology if the user fails to select a stock or if (somehow, once submitted) the user does not own any shares of that stock.
2. Requires that a user inputs a number of shares, implemented as a field whose name is shares. Renders an apology if the input is not a positive integer or if the user does not own that many shares of the stock.

![Screenshot_20230123_062155](https://user-images.githubusercontent.com/106766191/214592978-11ceebba-955d-4440-aefa-2e4c2821d590.png)

### history
History displays an HTML table summarizing all of a user’s transactions ever, listing row by row each and every buy and every sell.
![Screenshot_20230123_062217](https://user-images.githubusercontent.com/106766191/214597407-8fe676fa-ec78-4b17-bf79-bbfc4159b3c6.png)
