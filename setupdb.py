# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import hashlib
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
secret_key = hashlib.sha256(os.urandom(1024)).hexdigest()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    picture = Column(String)
    email = Column(String, index=True)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    # picture = Column(LargeBinary)
    image = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'creation_date': self.creation_date,
            'image': self.image,
            'category': self.category.name,
            'category_id': self.category_id,
            'creator': self.user.username
        }


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
