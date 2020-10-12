# purpose: main program for shop functionalities 

#importing required items
import time
import sqlite3
import store_db

#build and conntect to the stores default database
store_db.deploy_db()
conn = sqlite3.connect('shop.db')
cur = conn.cursor()

#main page of the store
def mainPage(currUserID):

	while True:

		try:
			print("\n --------------- Store Home Page ---------------\n")
			print("\n What would you like to do?:\n 1. View Items to Purchase\n 2. Build Cart \n 3. View Your Previous Orders \n 4. Logout of the Store\n 5. Exit the Program")

			#selection variable for user to select what they want to do in the store
			selection = int(input("\n Please select an option (1, 2, 3, 4, or 5): "))

			#display inventory of store
			if (selection == 1):
				displayItems()

			#add items to cart
			elif (selection == 2):
				cartAdd(currUserID)

			#display previous orders 
			elif (selection == 3):
				previousOrders(currUserID)


			#logout of current account
			elif (selection == 4):
				print("\n --------------- Thanks you for shopping! ---------------\n")
				loginSetup()

			#exit the program
			elif (selection == 5):
				i = 1
				print("\n --------------- Thanks you for shopping! ---------------\n")

				#closing database connection and exiting program
				conn.close()
				exit()

			else:
				print("\n ***Please enter a valid option. (1, 2, 3, 4, or 5)***")

		except Exception as ex:
			print("\n ***Please enter a vaild option. (1, 2, 3, 4, or 5)***")


#login setup function
def loginSetup():

	#login and validate username and password
	currUserID = loginValidation()

	#send user to main store page 
	mainPage(currUserID)
	

#login function to check whether the user is in the db or not
def loginValidation():

	print("\n --------------- Please login to access the shop! ---------------\n")

	while True:
	
		try:
			#username input
			print("\n ----- Please input your username and password. Enter '0' to exit. -----\n")
			username = str(input(" Username: "))

			#exit the program is user does not want to login
			if (username == "0"):
				exit()

			password = str(input(" Password: "))

			#checking to see if username and password is in the database
			records1 = cur.execute("SELECT USERNAME, USERID FROM USERS WHERE USERNAME = ?", (username,))
			row1 = records1.fetchone()

			records2 = cur.execute("SELECT PASSWORD FROM USERS WHERE PASSWORD = ?", (password,))
			row2 = records2.fetchone()

			#finishing validation process if it is correct
			if (row1[0] == username and row2[0] == password):
				userID = row1[1]
				return userID
				break

		except Exception as ex:
			print("\n ***We do not have a record for the username/password given. Please try again.***")

		
#displays all the items the store has in stock
def displayItems():

	print("\n --------------- Current Store Inventory ---------------\n")
	print("{:<10s}{:<15s}{:<20s}{:<25s}{:<30s}{:<35s}".format("\nItem ID", "Name", "Description","Category","Price", "Quantity"))

	#getting all of the items from inventory
	records = cur.execute("SELECT * FROM ITEMS")

	#printing out all of the items
	for row in records:
		
		print(" {:<10d}{:<15s}{:<20s}{:<25s}{:<30.2f}{:<35d}".format(row[0], row[1], row[2],row[3],row[4], row[5]))

	return


#displays previous orders made by the user
def previousOrders(currUserID):

	print("\n --------------- Your Previous Orders ---------------\n")
	orders = True
	
	#getting past purchases
	records = cur.execute("SELECT * FROM PAST_PURCHASES WHERE USERID = ?", (currUserID, ))
	row = records.fetchone()

	#determining if there are past purchases
	if (row == None):
		print("\n ***You have no previous orders associated with this account.***")
		orders == False

	else:
		print("{:<10s}{:>15s}{:>20s}{:>25s}{:>30s}".format("\nPurchase ID", "User ID", "Order ID","Total", "Credit Card"))

	#printing out all of the past orders
	while (orders == True):
		print("{:<10d}{:>15d}{:>20d}{:>25.2f}{:>30d}".format(row[0], row[1], row[2], row[4], row[3]))
		row = records.fetchone()

		if (row == None):
			break

#displays items in the current cart
def cartDisplay(currUserID, shoppingCart):

	if (shoppingCart == []):
		cartAdd(currUserID)

	print("\n --------------- Your Current Cart ---------------\n")

	totalPrice = 0

	#print out current cart
	print("{:<10s}{:<15s}{:<20s}{:<25s}{:<30s}".format("\nItem ID", "Name", "Price", "Quantity", "Total Price"))

	for i in range(len(shoppingCart)):
		currIndex = shoppingCart[i][0]

		records = cur.execute("SELECT ITEMID, NAME, PRICE, QUANTITY FROM ITEMS WHERE ITEMID = ?", (currIndex,))
		row = records.fetchone()

		#find total price of the cart
		totalPrice = ((row[2] * shoppingCart[i][2]) + totalPrice)

		print("{:<10d}{:<15s}{:<20.2f}{:<25d}{:<30.2f}".format(row[0], row[1], row[2], shoppingCart[i][2], (row[2] * shoppingCart[i][2])))

	#print total of all items in the cart
	print("{:>75s}".format("------"))
	print("{:>75.2f}".format(totalPrice))

	#give the user options on what to do with their cart
	while True:
		try:
			cartStatus = int(input("\n What would you like to do?:\n\n 1. Proceed to checkout\n 2. Remove an item from your cart\n 3. Delete all items in your cart\n Select 1, 2, or 3: "))

			#checkout
			if (cartStatus == 1):
				checkout(currUserID, shoppingCart)
				break

			#remove an item
			elif (cartStatus == 2):
				cartRemove(currUserID, shoppingCart)
				break

			#deletion of cart
			elif (cartStatus == 3):
				mainPage(currUserID)
				break

			else:
				print("\n ***Please input a valid option. (1, 2, or 3)***")
		
		except Exception as ex:
			print("\n ***Please input a valid option. (1, 2, or 3)***")

	
#adds items to the cart
def cartAdd(currUserID):

	print("\n --------------- Add Items to your Cart ---------------\n")

	#list for shopping cart
	shoppingCart = []

	#status variavle for loop for adding items to cart
	shoppingStatus = True
	while (shoppingStatus == True):

		#getting the item ID and quantity of the desired item
		itemID = int(input("\n Enter the Item ID # that you would like to add to your cart: "))
		itemQuantity = int(input("\n Enter the quantity you would like to add to your cart: "))

		#sql to retrieve item info and check if theres that many in stock
		records = cur.execute("SELECT ITEMID, NAME, PRICE FROM ITEMS WHERE ITEMID = ? AND QUANTITY >= ?", (itemID, itemQuantity,))
		row = records.fetchone()

		#check if the item can be added to cart
		if (row == None):
			print ("\n ***The item number that you entered is either not in our system or we do not have enough stock.***")

		#add item to cart
		else:
			shoppingCart.append([row[0], row[1], itemQuantity])

			print("{:<10s}{:<15s}{:<25s}".format("\nItem ID", "Name", "Price"))
			print("{:<10d}{:<15s}{:<25.2f}".format(row[0], row[1], row[2]))
		
		#check if the customer wants to do more shopping
		while True:
			try:
				more = int(input("\n Would you like to continue shopping?\n Enter 0 for no\n Enter 1 for yes\n Choice: "))
				
				#wants to shop more
				if (more == 1):
					shoppingStatus = True
					break

				#does not want to shop more
				elif(more == 0):
					shoppingStatus = False
					break

				else:
					print("\n ***Please input a valid option. (0 or 1)***")

			except Exception as ex:
				print("\n ***Please input a valid option. (0 or 1)***")

	#display the current cart
	cartDisplay(currUserID, shoppingCart)


#removes items from the cart
def cartRemove(currUserID, shoppingCart):

	#input to detmine what item and how many should be removed
	removeId = int(input("\n Please enter the Item ID number that you wish to remove: "))
	removeQuantity = int(input("\n Please enter the number of this item you want to remove: "))

	#iterating through cart to find item
	for i in range(len(shoppingCart)):
		
		#totally removal of item
		if ((shoppingCart[i][0] == removeId) and (shoppingCart[i][2] <= removeQuantity)):
			shoppingCart.pop(i)
			print("\n This item has been removed from your cart.")
			break

		#reduction in quantity
		if ((shoppingCart[i][0] == removeId) and (shoppingCart[i][2] > removeQuantity)):
			shoppingCart[i][2] = (shoppingCart[i][2] - removeQuantity)
			print("\n", removeQuantity, "item(s) removed from your cart.")
			break

	#displaying cart after changes are made
	cartDisplay(currUserID, shoppingCart)


#checkout when the user is satisfied with their cart
def checkout(currUserID, shoppingCart):

	#getting address associated with address
	records = cur.execute("SELECT ADDRESS FROM USERS WHERE USERID = ?", (currUserID, ))
	row = records.fetchone()

	#determining if the account has an address associated with it
	if (row[0] != None):
		print("\n Address infromation is already established.")
		address = row[0]

	#inputing address if there is none and updating db
	else:
		address = input(" Please provide your shipping address: ")
		cur.execute("UPDATE USERS SET ADDRESS = ? WHERE USERID = ?", (address, currUserID, ))
		print("\n Thank you. Your information has been stored for future use. ")
		
	#getting the credit card number of the user
	while True:
		creditCard = input(" Please input your 10 digit credit card number: ")

		if ((creditCard.isdigit()) and (len(str(creditCard)) == 10)):
			creditCard = int(creditCard)
			break

		else:
			print("\n ***Please enter a valid 10 digit credit card number (1234567890).***")

	#creating an order entry in db
	cur.execute("INSERT INTO ORDERS (USERID)\
		VALUES(?)", (currUserID, ))

	#getting orderid of the newley created order instance
	records = cur.execute("SELECT MAX(ORDERID) FROM ORDERS WHERE USERID = ?", (currUserID, ))
	row = records.fetchone()
	orderId = row[0]
	
	total = 0

	#iterating through shopping cart
	for item in shoppingCart:
		price = 0
		itemId = item[0]
		itemQuantity = item[2]

		#getting price of the current item in the cart
		records = cur.execute("SELECT PRICE FROM ITEMS WHERE ITEMID = ?", (itemId, ))
		row = records.fetchone()
		price = row[0]

		#updating order total based on price and quantity
		total += price * itemQuantity

		#inserting info into order composition table
		cur.execute("INSERT INTO ORDER_COMP (ORDERID, ITEMID, QUANTITY)\
			VALUES (?, ?, ?)", (orderId, itemId, itemQuantity, ))

		#getting current stock quantity of the item
		records = cur.execute("SELECT QUANTITY FROM ITEMS WHERE ITEMID = ?", (itemId, ))
		row = records.fetchone()
		currQuantity = row[0]

		#updating stock number and updating db
		updatedQuantity = currQuantity - itemQuantity
		cur.execute("UPDATE ITEMS SET QUANTITY = ? WHERE ITEMID = ?", (updatedQuantity, itemId))

	#inserting purchase into the past purchase table
	cur.execute("INSERT INTO PAST_PURCHASES (USERID, ORDERID, CREDITCARD, TOTAL)\
		VALUES (?, ?, ?, ?)", (currUserID, orderId, creditCard, total))

	conn.commit()

	#printing out order confirmation
	print("\n ----- Order Confirmed. -----")
	print("{:<10s}{:<15s}{:<25s}{:<45s}".format("\nOrderID", "Total", "Credit Card #", "Shipping Address"))
	print("{:<10d}{:<15.2f}{:<25d}{:<45s}".format(orderId, total, creditCard, address))

	#returning to main page after purchase is done
	mainPage(currUserID)


#main function of the program
def main():

	print("\n --------------- Welcome to our wonderful store! ---------------\n")

	#function to setup login process
	loginSetup()

#calling main
if __name__ == "__main__":
	main()