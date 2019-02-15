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
             image="https://www.bhphotovideo.com/images/images2500x2500/sega_00378_3_atari_flashback_8_game_1361837.jpg",
             category=category1,
             user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Mobile Phone",
             description='''A calling device that will allow you to spend hours talking to your friends.''',
             image="https://2.bp.blogspot.com/-A9zA8gZSgVk/W6jWwt87tQI/AAAAAAAAHDw/mdGEDqu-9MQ1nlB494DG844tgPZyBKxmACLcBGAs/s1600/Phones-History-and-Old-Mobile-Phone-Images-photo-picture-1.jpg",
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
             image="http://www.busforsale.com/buses/photos/marlin/thumb/thumb_marlinext4.jpg",
             category=category2,
             user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Bycicle",
             description='''A two-wheeled vehicle for those who do not like engines''',
             image="https://rukminim1.flixcart.com/image/832/832/jasj6a80/cycle/a/4/r/trium-27-5-inch-mtb-bicycle-21-speed-black-premium-edition-original-imafyahcbahnbrj2.jpeg",
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
             image="https://http2.mlstatic.com/calca-jeans-vintage-cintura-alta-mom-jeans-unisex-seminova-D_NQ_NP_661014-MLB27940910161_082018-F.jpg",
             category=category3,
             user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Scarf",
             description='''It protects your neck from the cold. For those planning to go out during a blizzard.''',
             image="https://www.hogarth-design.com/media/catalog/product/cache/5/image/1200x1200/9df78eab33525d08d6e5fb8d27136e95/t/e/terracotta-rt007-fm27-pic_1.jpg",
             category=category3,
             user=user1)
session.add(item2)
session.commit()

item3 = Item(name="Leather Jacket",
             description="To wear if you're on a motorcycle.",
             image="https://images-na.ssl-images-amazon.com/images/I/91d71CCngaL._SY550_.jpg",
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
             image="https://www.decofurnsa.co.za/wp-content/uploads/2017/07/Max-Sleeper-Couch-BLACK-up-side-view-WEB.jpg",
             category=category4,
             user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Chair",
             description="Harder than a couch.",
             image="https://ii.worldmarket.com/fcgi-bin/iipsrv.fcgi?FIF=/images/worldmarket/source/48251_XXX_v1.tif&wid=2000&cvt=jpeg",
             category=category4,
             user=user1)
session.add(item2)
session.commit()

item3 = Item(name="Bedside table",
             description='''A great deal if you're lazy or want to keep something close to you.''',
             image="https://hniesfp.imgix.net/8/images/detailed/63/thaisBS_main.jpg",
             category=category4,
             user=user1)
session.add(item3)
session.commit()

item4 = Item(name="Bedside lamp",
             description='''Very useful to read before sleep.''',
             image="https://secure.img2-fg.wfcdn.com/im/57938101/resize-h310-w310%5Ecompr-r85/4416/44162100/zainab-195-table-lamp.jpg",
             category=category4,
             user=user1)
session.add(item4)
session.commit()

# End init
session.close()

print("Successfully added categories and items!")
