#Python
from doctest import Example
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI, Query
from fastapi import Body, Query, Path


app = FastAPI()

###### MODELS #################

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
        example="MIguel"
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
    password: str = Field(..., min_length=8)

class PersonOut(PersonBase):
    pass
    
###################### MODELS   ######################

@app.get("/")
def home():
    return {"Hello" : "World"}

##### Request and Response Body

@app.post("/person/new", response_model=Person, response_model_exclude={'password'})
def create_person(person : Person = Body(...)):
    return person

##### Validaciones: Query parameters

@app.get("/person/detail")
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

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID.",
        gt=1)

):  
    return {person_id: "It Exists!"}



#### Validaciones: Request Body


@app.put("/person/{person_id}")
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
