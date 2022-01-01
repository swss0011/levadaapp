from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from .db import Base
from sqlalchemy.orm import relationship
import datetime
#from sqlalchemy.sql import func
#https://stackoverflow.com/questions/4552380/how-to-get-current-date-and-time-from-db-using-sqlalchemy/4552838


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    familyname = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="profiles")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)

    profiles = relationship("Profile", back_populates="creator")


class VerifySingUp(Base):
    __tablename__ = "singup"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now) #(timezone=True), server_default=func.now())


class ChangePassword(Base):
    __tablename__ = "changepassword"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now)


class TreeDb(Base):
    __tablename__ = "treedb"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner = Column(Integer)
    readers = Column(String, default="")
    editors = Column(String, default="")
    search = Column(Boolean, default=False)
    view = Column(Boolean, default=False)
    notes = Column(String, default="")
    created_at = Column(DateTime, default=datetime.datetime.now)


class NodeNote(Base):
    __tablename__ = "nodenote"

    id = Column(Integer, primary_key=True, index=True)
    tree_id = Column(Integer)
    node_id = Column(Integer)
    owner = Column(Integer)
    text = Column(String, default="")
    readers = Column(String, default="")
    editors = Column(String, default="")
    search = Column(Boolean, default=False)
    view = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)


class Human(Base):
    __tablename__ = 'human'

    id = Column(Integer, primary_key=True)
    father_id = Column(Integer, ForeignKey('human.id'))
    mother_id = Column(Integer, ForeignKey('human.id'))
    children = relationship("Human")
    name: Column(String, default="")
    family_name: Column(String, default="")
    note = Column(String, default="")
    place = Column(String, default="")
    born_at = Column(DateTime)
    dead_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.now)