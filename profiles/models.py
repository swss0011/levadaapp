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
    reader = Column(String, default="")
    editor = Column(String, default="")
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


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer)
    tree_id = Column(Integer)
    created_by = Column(Integer)
    copy_from_person = Column(Integer, default=0)
    node_from_neo4j_id = Column(Integer)
    sex = Column(String)
    name = Column(String)
    second_name = Column(String, default="")
    father_name = Column(String, default="")
    date_of_birth_from = Column(String)
    date_of_birth_to = Column(String)
    date_of_death_from = Column(String, default="")
    date_of_death_to = Column(String, default="")
    is_active = Column(Boolean, default=True)
    location = Column(String, default="")
    note = Column(String, default="")
    note_markdown = Column(String, default="")
    mother_id = Column(Integer, default=0)
    father_id = Column(Integer, default=0)
    children_ids = Column(String, default="")
    image = Column(String, default="")



"""
class Human(Base):
    __tablename__ = 'human'

    id = Column(Integer, primary_key=True)
    father_id = Column(Integer, ForeignKey('human.id'), nullable=False)
    mother_id = Column(Integer, ForeignKey('human.id'), nullable=False)

    father = relationship("Human", foreign_keys=[father_id])
    mother = relationship("Human", foreign_keys=[mother_id])

    children = relationship("Human")
    name: Column(String, default="")
    family_name: Column(String, default="")
    note = Column(String, default="")
    place = Column(String, default="")
    born_at = Column(DateTime)
    dead_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.now)
"""