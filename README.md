# What is the ksb (KinderSachenBörse)?
The Kindersachenbörse is a bi-annually second hand shop in Austria, where people bring used stuff and we sell it for them.

# Why this software?
Due to logistical requirements, the people that bring items (the sellers) must tell us beforehand what these items will be.
The currently used software is a bunch of old php scripts that lack some important features, so I've rewritten the complete software in python.

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