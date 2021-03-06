from typing import List, Optional, Literal
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


class UserSingUp(BaseModel):
    username: str
    email: str
    password: str
    second_password: str


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

class TreeForEditor(BaseModel):
    tree_id: str
    name: str
    search: Optional[bool] = False
    notes: Optional[str] = ""
    view: Optional[bool] = False

class ShowTreeForRW(BaseModel):
    tree_ids: str
    status: Literal['reader', 'editor']

class TreeEditorsReaders(BaseModel):
    status: Literal['reader', 'editor']
    tree_id: str
    id: str

class TreeEditorsReadersView(BaseModel):
    status: Literal['reader', 'editor']
    tree_id: str

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

class PersonEdge(BaseModel):
    from_id: int
    to_id: int

class PersonUpdate(BaseModel):
    name: Optional[str] = ""
    second_name: Optional[str] = ""
    father_name: Optional[str] = ""
    date_of_birth_from: Optional[str] = ""
    date_of_birth_to: Optional[str] = ""
    date_of_death_from: Optional[str] = ""
    date_of_death_to: Optional[str] = ""
    is_active: Optional[bool] = True
    note: Optional[str] = ""
    location: Optional[str] = ""
    note_markdown: Optional[str] = ""
    image: Optional[str] = ""

class Person(BaseModel):
    owner_id: str
    tree_id: str
    created_by: str
    copy_from_person: Optional[str] = ""
    node_from_neo4j_id: str
    sex: Literal['male', 'female']
    name: str
    second_name: Optional[str] = ""
    father_name: Optional[str] = ""
    date_of_birth_from: str
    date_of_birth_to: str
    date_of_death_from: Optional[str] = ""
    date_of_death_to: Optional[str] = ""
    is_active: Optional[bool] = True
    note: Optional[str] = ""
    location: str
    note_markdown: Optional[str] = ""
    mother_id: Optional[str] = ""
    father_id: Optional[str] = ""
    children_ids: Optional[str] = ""
    image: Optional[str] = ""

class PersonCreate(BaseModel):
    tree_id: int
    sex: Literal['male', 'female']
    name: str
    second_name: Optional[str] = ""
    father_name: Optional[str] = ""
    date_of_birth_from: str
    date_of_birth_to: Optional[str] = ""
    date_of_death_from: Optional[str] = ""
    date_of_death_to: Optional[str] = ""
    is_active: Optional[bool] = True
    note: Optional[str] = ""
    location: str
    note_markdown: Optional[str] = ""
    image: Optional[str] = ""
