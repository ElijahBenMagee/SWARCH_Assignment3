#purpose: setup of the database for the shop

import sqlite3

def deploy_db():

	#creating the connection to the database
	conn = sqlite3.connect('shop.db')
	cur = conn.cursor()

	#reseeting the database each time the program is reopened
	dropUsers = '''DROP TABLE IF EXISTS USERS'''
	cur.execute(dropUsers)

	dropItems = '''DROP TABLE IF EXISTS ITEMS'''
	cur.execute(dropItems)

	dropOrderComp = '''DROP TABLE IF EXISTS ORDER_COMP'''
	cur.execute(dropOrderComp)

	#creating the users table
	usersTableSql = '''CREATE TABLE IF NOT EXISTS USERS 
		(USERID INTEGER PRIMARY KEY AUTOINCREMENT, 
		USERNAME CHAR(30) NOT NULL,
		PASSWORD CHAR(30) NOT NULL,
		ADDRESS CHAR(100));'''

	cur.execute(usersTableSql)

	#creating the items table
	itemsTableSql = '''CREATE TABLE IF NOT EXISTS ITEMS
		(ITEMID INTEGER PRIMARY KEY AUTOINCREMENT,
		NAME CHAR(100) NOT NULL UNIQUE,
		DESCRIPTION CHAR(300) NOT NULL,
		CATEGORY CHAR(100) NOT NULL,
		PRICE REAL NOT NULL,
		QUANTITY INTEGER NOT NULL);'''

	cur.execute(itemsTableSql)

	#creating the orders table
	ordersTableSql = '''CREATE TABLE IF NOT EXISTS ORDERS
		(ORDERID INTEGER PRIMARY KEY AUTOINCREMENT,
		USERID	INTEGER		NOT NULL,
		FOREIGN KEY (USERID) REFERENCES USERS(USERID));'''

	cur.execute(ordersTableSql)

	#creating the past purchases table
	pastTableSql = '''CREATE TABLE IF NOT EXISTS PAST_PURCHASES
		(PURCHASEID INTEGER PRIMARY KEY AUTOINCREMENT,
		USERID INTEGER NOT NULL,
		ORDERID INTEGER NOT NULL,
		CREDITCARD INTEGER NOT NULL,
		TOTAL REAL NOT NULL,
		FOREIGN KEY (USERID) REFERENCES USERS(USERID),
		FOREIGN KEY (ORDERID) REFERENCES ORDERS(ORDERID));'''

	cur.execute(pastTableSql)

	#creating the table that keeps track of what is in an order
	compTableSql = '''CREATE TABLE IF NOT EXISTS ORDER_COMP
	 	(ORDERID INTEGER NOT NULL,
	 	ITEMID INTEGER NOT NULL,
	 	QUANTITY INTEGER NOT NULL,
	 	PRIMARY KEY (ORDERID, ITEMID),
	 	FOREIGN KEY (ORDERID) REFERENCES ORDERS(ORDERID),
	 	FOREIGN KEY (ITEMID) REFERENCES ITEMS(ITEMID));'''

	cur.execute(compTableSql)

	#inserting three users into the users table
	user1 = "INSERT INTO USERS (USERNAME, PASSWORD, ADDRESS) \
	 	VALUES ('msstate', 'bulldogs', 'Mississippi State, MS 39762')"
	cur.execute(user1)

	user2 = "INSERT INTO USERS (USERNAME, PASSWORD, ADDRESS) \
	 	VALUES ('olemiss', 'landsharks', 'University, MS 38677')"
	cur.execute(user2)

	user3 = "INSERT INTO USERS (USERNAME, PASSWORD) \
	 	VALUES ('alabama', 'crimsontide')"
	cur.execute(user3)

	#inserting two household items into the items table 
	item1 = "INSERT INTO ITEMS (NAME, DESCRIPTION, CATEGORY, PRICE, QUANTITY) \
	 	VALUES ('Hefty Bags', 'Trash Bags', 'Household Items', 10.45, 28)"
	cur.execute(item1)

	item2 = "INSERT INTO ITEMS (NAME, DESCRIPTION, CATEGORY, PRICE, QUANTITY) \
	 	VALUES ('Bounty TP', 'Toilet Paper', 'Household Items', 13.99, 19)"
	cur.execute(item2)

	#inserting two books into the items table 
	item3 = "INSERT INTO ITEMS (NAME, DESCRIPTION, CATEGORY, PRICE, QUANTITY) \
	 	VALUES ('Catch-22', 'A Novel', 'Book', 12.24, 13 )"
	cur.execute(item3)

	item4 = "INSERT INTO ITEMS (NAME, DESCRIPTION, CATEGORY, PRICE, QUANTITY) \
	 	VALUES ('How to Code', 'A Textbook', 'Book', 36.99, 6)"
	cur.execute(item4)

	#inserting two toys into the items table
	item5 = "INSERT INTO ITEMS (NAME, DESCRIPTION, CATEGORY, PRICE, QUANTITY) \
	 	VALUES ('Crayons', 'Wax Crayons', 'Toy', 10.99, 11)"
	cur.execute(item5)

	item6 = "INSERT INTO ITEMS (NAME, DESCRIPTION, CATEGORY, PRICE, QUANTITY) \
	 	VALUES ('Action Figure', 'A Plastic Toy', 'Toy', 19.99, 9)"
	cur.execute(item6)

	#inserting two small electronics into the items table
	item7 = "INSERT INTO ITEMS (NAME, DESCRIPTION, CATEGORY, PRICE, QUANTITY) \
	 	VALUES ('Ipod Touch', 'MP3 Player', 'Small Electronics', 199.99, 17)"
	cur.execute(item7)

	item8 = "INSERT INTO ITEMS (NAME, DESCRIPTION, CATEGORY, PRICE, QUANTITY) \
	 	VALUES ('Rasberyy Pi', 'Small Computer', 'Small Electronics', 34.99, 4)"
	cur.execute(item8)

	#commiting the changes to the db and closing the connection
	conn.commit()
	conn.close()

	return