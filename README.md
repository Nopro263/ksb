# What is the ksb (KinderSachenBörse)?
The Kindersachenbörse is a bi-annually second hand shop in Austria, where people bring used stuff and we sell it for them.

# Why this software?
Due to logistical requirements, the people that bring items (the sellers) must tell us beforehand what these items will be.
The currently used software is a bunch of old php scripts that lack some important features (e.g. multiple languages), so I've rewritten the complete software in python.

# What does this software do?
This software is split into two parts: the seller part and the employee part.\
The seller part offers the creation of accounts an so called "lists" where each list can contain up to 60 articles and (in production) has a fee of 10€.\
The employe part is a small pos system where we have an overview of all articles, lists and users. Every transaction happens in this system.

# More info

The demo is available at https://ksb.unser.dns64.de

The demo employee has the following credentials\
Username: `employee1` \
Passwort: `password!`

Feel free to create an account, but **do not use your real data**, as it will be visible from the employee account

# The process
#### The seller
1. A potential seller creates an account.
2. They create a new list.
3. This seller enters all items they whish to sell.
4. If they are done, they press print and print the document.
5. They cut the paper at the dashed lines and put these tags on the items the are selling.
6. On the day of the event, the bring the first page and all items for sale and pay the fees of their lists.
#### We (the organisators)
7. We scan the tag of every item to import it. (to verify that we have received it)
8. We put the items up for sale
9. People go through the items and buy a selection.
10. We ring them up and scan every tag of their purchase.
### The aftermath
11. We sort every item back to its seller.
12. The sellers get their money and the remaining items.