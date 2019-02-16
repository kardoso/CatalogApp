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
pic = "https://lh4.googleusercontent.com/"
pic += "-R_xSTT7918M/AAAAAAAAAAI/AAAAAAAADmE/"
pic += "SHzJSMfwnpI/photo.jpg"
user1 = User(username="Samuel Cardoso", email="scksamuel.sc@gmail.com",
             picture=pic)
session.add(user1)
session.commit()

# Create category
print("Adding fun...")
category1 = Category(name="Hardware")
session.add(category1)
session.commit()

# Create items
desc = "A new device that will provide lots "
desc += "of fun for you and your friends."
img = "https://www.bhphotovideo.com/images/"
img += "images2500x2500/sega_00378_3_atari_flashback_8_game_1361837.jpg"
item1 = Item(name="Videogame",
             description=desc,
             image=img,
             category=category1,
             user=user1)
session.add(item1)
session.commit()

desc = "A calling device that will allow you "
desc += "to spend hours talking to your friends."
img = "https://2.bp.blogspot.com/-A9zA8gZSgVk/W6jWwt87tQI/"
img += "AAAAAAAAHDw/mdGEDqu-9MQ1nlB494DG844tgPZyBKxmACLcBGAs/"
img += "s1600/Phones-History-and-Old-Mobile-Phone-Images-photo-picture-1.jpg"
item2 = Item(name="Mobile Phone",
             description=desc,
             image=img,
             category=category1,
             user=user1)
session.add(item2)
session.commit()

print("Making the world more accessible...")
# Create category
category2 = Category(name="Vehicles")
session.add(category2)
session.commit()

# Create items
desc = "It fits the whole family and there's "
desc += "still plenty of space for your friends."
img = "http://www.busforsale.com/buses/photos/"
img += "marlin/thumb/thumb_marlinext4.jpg"
item1 = Item(name="Tour Bus",
             description=desc,
             image=img,
             category=category2,
             user=user1)
session.add(item1)
session.commit()

desc = "A two-wheeled vehicle for those who do not like engines"
img = "https://rukminim1.flixcart.com/image/832/832/jasj6a80/"
img += "cycle/a/4/r/trium-27-5-inch-mtb-bicycle-21-speed-black-"
img += "premium-edition-original-imafyahcbahnbrj2.jpeg"

item2 = Item(name="Bycicle",
             description=desc,
             image=img,
             category=category2,
             user=user1)
session.add(item2)
session.commit()

print("Warming up cold hearts...")
# Create category
category3 = Category(name="Clothes")
session.add(category3)
session.commit()

# Create items
desc = "It covers private places of your body. "
desc += "Essential for anyone planning to going out."
img = "https://http2.mlstatic.com/"
img += "calca-jeans-vintage-cintura-alta-mom-jeans-"
img += "unisex-seminova-D_NQ_NP_"
img += "661014-MLB27940910161_082018-F.jpg"
item1 = Item(name="Pants",
             description=desc,
             image=img,
             category=category3,
             user=user1)
session.add(item1)
session.commit()

desc = "It protects your neck from the cold."
desc += "For those planning to go out during a blizzard."
img = "https://www.hogarth-design.com/media/"
img += "catalog/product/cache/5/image/1200x1200/"
img += "9df78eab33525d08d6e5fb8d27136e95/t/e/"
img += "terracotta-rt007-fm27-pic_1.jpg"
item2 = Item(name="Scarf",
             description=desc,
             image=img,
             category=category3,
             user=user1)
session.add(item2)
session.commit()

desc = "To wear if you're on a motorcycle."
img = "https://images-na.ssl-images-amazon.com/"
img += "images/I/91d71CCngaL._SY550_.jpg"
item3 = Item(name="Leather Jacket",
             description=desc,
             image=img,
             category=category3,
             user=user1)
session.add(item3)
session.commit()

print("Cleaning up the house...")
# Create category
category4 = Category(name="Furniture")
session.add(category4)
session.commit()

# Create items
img = "https://www.decofurnsa.co.za/wp-content/"
img += "uploads/2017/07/Max-Sleeper-Couch-"
img += "BLACK-up-side-view-WEB.jpg"
item1 = Item(name="Couch",
             description="Softer than a chair.",
             image=img,
             category=category4,
             user=user1)
session.add(item1)
session.commit()

img = "https://ii.worldmarket.com/fcgi-bin/"
img += "iipsrv.fcgi?FIF=/images/worldmarket/"
img += "source/48251_XXX_v1.tif&wid=2000&cvt=jpeg"
item2 = Item(name="Chair",
             description="Harder than a couch.",
             image=img,
             category=category4,
             user=user1)
session.add(item2)
session.commit()

desc = "A great deal if you're lazy "
desc += "or want to keep something close to you."
img = "https://hniesfp.imgix.net/8/"
img = "images/detailed/63/thaisBS_main.jpg"
item3 = Item(name="Bedside table",
             description=desc,
             image=img,
             category=category4,
             user=user1)
session.add(item3)
session.commit()

img = "https://secure.img2-fg.wfcdn.com/im/"
img += "57938101/resize-h310-w310%5Ecompr-r85/"
img += "4416/44162100/zainab-195-table-lamp.jpg"
item4 = Item(name="Bedside lamp",
             description="Very useful to read before sleep.",
             image=img,
             category=category4,
             user=user1)
session.add(item4)
session.commit()

# End init
session.close()

print("Everything is where it should be.")
print("Successfully added categories and items!")
