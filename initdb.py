# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from setupdb import User, Category, Item

engine = create_engine('sqlite:///catalog.db')

DBSession = sessionmaker(bind=engine)
session = DBSession()

print("Creating data...")

# Create user
user1 = User(username="Samuel Cardoso", email="scksamuel.sc@gmail.com",
             picture='''https://lh4.googleusercontent.com/-R_xSTT7918M/AAAAAAAAAAI/AAAAAAAADmE/SHzJSMfwnpI/photo.jpg''')
session.add(user1)
session.commit()

# Create category
category1 = Category(name="Hardware")
session.add(category1)
session.commit()

# Create items
item1 = Item(name="Videogame",
             description='''A new device that will provide lots of fun for you and your friends.''',
             category=category1,
             user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Mobile Phone",
             description='''A calling device that will allow you to spend hours talking to friends.''',
             category=category1,
             user=user1)
session.add(item2)
session.commit()


# Create category
category2 = Category(name="Vehicles")
session.add(category2)
session.commit()

# Create items
item1 = Item(name="Tour Bus",
             description='''It fits the whole family and there's still plenty of space for your friends.''',
             category=category2,
             user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Bycicle",
             description='''A two-wheeled vehicle for those who do not like engines''',
             category=category2,
             user=user1)
session.add(item2)
session.commit()

# Create category
category3 = Category(name="Clothes")
session.add(category3)
session.commit()

# Create items
item1 = Item(name="Pants",
             description='''It covers private places of your body. Essential for anyone planning to going out.''',
             category=category3,
             user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Scarf",
             description='''It protects your neck from the cold. For those planning to go out during a blizzard.''',
             category=category3,
             user=user1)
session.add(item2)
session.commit()

item3 = Item(name="Leather Jacket",
             description="To wear if you're on a motorcycle.",
             category=category3,
             user=user1)
session.add(item3)
session.commit()

# Create category
category4 = Category(name="Furniture")
session.add(category4)
session.commit()

# Create items
item1 = Item(name="Couch",
             description="Softer than a chair.",
             category=category4,
             user=user1)
session.add(item1)
session.commit()

# Create items
item2 = Item(name="Chair",
             description="Harder than a couch.",
             category=category4,
             user=user1)
session.add(item2)
session.commit()

# Create items
item3 = Item(name="Bedside table",
             description='''A great deal if you're lazy or want to keep something close to you.''',
             category=category4,
             user=user1)
session.add(item3)
session.commit()

# End init
session.close()

print("Successfully added categories and items!")
