from typing import List, Optional
from pydantic import BaseModel


class Profile(BaseModel):
    name: str
    familyname: str


class ProfileFromBase(Profile):
    class Config():
        orm_mode = True


class User(BaseModel):
    username: str
    email: str
    password: str


class UserPass(BaseModel):
    password: str


class ShowUser(BaseModel):
    username: str
    email: str
    profiles: List[ProfileFromBase] = []

    class Config():
        orm_mode = True


class ShowProfile(BaseModel):
    name: str
    familyname: str
    creator: ShowUser

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class Node(BaseModel):
    node_id: str
    gender: str
    name: str
    familyname: str
    address: str
    born: str
    dead: str
    treeid: str
    copyid: str


class Edge(BaseModel):
    parent_gender: str
    child_gender: str
    parent_name: str
    parent_familyname: str
    child_name: str
    child_familyname: str


class Tree(BaseModel):
    name: str
    search: Optional[bool] = False
    notes: Optional[str] = ""
    view: Optional[bool] = False

class TreePut(BaseModel):
    name: Optional[str] = ""
    search: Optional[bool] = False
    notes: Optional[str] = ""
    view: Optional[bool] = False

class TreeFindSearch(BaseModel):
    text: str
    search: Optional[bool] = True
    view: Optional[bool] = False


class NodeNote(BaseModel):
    text: Optional[str] = ""
    node_id: Optional[int] = 0
    tree_id: Optional[int] = 0
    search: Optional[bool] = False
    view: Optional[bool] = False

class Human(BaseModel):
    name: str
    family_name: str
    father_id: Optional[int] = 0
    mother_id: Optional[int] = 0
    note: Optional[str] = ""
    place: Optional[str] = ""
    born_at: str
    dead_at: Optional[str] = ""
