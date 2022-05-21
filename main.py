#Python
from ast import For
from doctest import Example
from email import message
from tkinter.messagebox import NO
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, EmailStr
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import Cookie, FastAPI, Header, Query
from fastapi import status
from fastapi import Body, Query, Path, Form


app = FastAPI()

################ MODELS #################

class HairColor(Enum):
    white = "white"
    brow = "brown"
    black = "black"
    red = "red"

class Countries(Enum):
    argentina = "Argentina"
    chile = "Chile"
    uruguay = "Uruguay"
    paraguay = "Paraguay"
    colombia = "Colombia"
    venezuela = "Venezuela"
    peru = "Peru"
    bolivia = "Bolivia"
    brasil = "Brasil"
    ecuador = "Ecuador"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    country: Optional[Countries] = Field(default=None)

class PersonBase(BaseModel):
    firt_name : str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Miguel"
        )

    last_name : str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Torres"
        )
    age : int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color : Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married : Optional[bool] = Field(default=None, example=False)

class Person(PersonBase):
    password: str = Field(..., min_length=8, example='soyelpassdemiguel')

class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="Miguel2021")
    message: str = Field(default="Login Succesfuly..!")

###################### MODELS   ######################

@app.get(
    path="/", 
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello" : "World"}

##### Request and Response Body

@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED 
    )
def create_person(person : Person = Body(...)):
    return person

##### Validaciones: Query parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters"
        ),
    age: str = Query(
        ...,
        title = "Person Age",
        description="This is a age description"
        )
):
    return {name : age}


##### Validaciones: Path Parameters

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID.",
        gt=1)

):  
    return {person_id: "It Exists!"}


#### Validaciones: Request Body


@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK)
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    Location: Location = Body(...)
):
    results = person.dict()
    results.update(Location.dict())

    return results


### Forms

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...,), password: str = Form(...)):
    return LoginOut(username=username)


### Cookies and Headers Paraneters #### 

@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK
)
def contact(
    first_name:str = Form(
        ...,
        max_leght=20,
        min_length=1
    ),
    last_name:str = Form(
        ...,
        max_leght=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(..., 
    min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

