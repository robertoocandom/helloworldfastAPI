#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Body, Header, Query, Path, Form, File, Cookie, UploadFile


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
    username: str = Field(..., max_length=20, example="Miguel.2022")
    message: str = Field(default="Login Succesfuly..!")

###################### MODELS   ######################

@app.get(
    path="/", 
    status_code=status.HTTP_200_OK,
    tags=['Home'],
    summary="Home of the aplication"

    )
def home():
    """
    Home of the application

    This end point will return a dictionary with the key "Hello" and the value "World"

    Parameters:
        - None     
    
    Returns Hello World as dictionary.
    """
    return {"Hello" : "World"}

##### Request and Response Body

@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=['Person'],
    summary="Create person in the app" 
    )
def create_person(person : Person = Body(...)):
    """
    Create Person

    This path operations creates a person in the app and save the information in the DB.
    
    Parameters:
    - Request body parameters:
        - **person: Person** -> A person model with first name, last name, age, hair color, marital status

    Returns a person model with first name, last name, age, hair color, marital status
    """
    return person

##### Validaciones: Query parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=['Person'],
    summary="Get person detail"
    )
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
    """
    Show Person Information

    This end point receives a person name and age returns a dictionary with th person information,
    
    Parameters:
    - Query parameters:
        - **name: str** (optional) -> Name of the person.
        - **age: str** (requiered) -> Age of the person. 

    Returns:
    - Dictionary with the person information (name : age).
    """
    return {name : age}


##### Validaciones: Path Parameters #####
persons = [1,2,3,4,5]

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=['Person'])
def show_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID.",
        gt=1)

):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="!This person doesn't exist!"
        )
    return {person_id: "It Exists!"}


#### Validaciones: Request Body


@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=['Person'])
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


############### Forms  ###########################

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=['Person'],
    summary=["Login"]
)
def login(username: str = Form(...), password: str = Form(...)):
    """
    Login
    
    Endpoint with the login of the app

    Parameters:
    - Form parameters:
        - **username: str** (requiered) -> User Name.
        - **password: str** (requiered) -> Password.

    Returns:
    - A dictionary with key "username" and value "Hola Mundo"
    - A dictionary with key "message" and value "Login Succesfuly" 

    """
    return LoginOut(username=username)



### Cookies and Headers Paraneters #### 

@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK,
    tags=['Contact'],
    summary="Contact"
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
    """
    Contact

    This end point receives a first name, email, message, ads and user agent and returns a dictionary with the first name, user_agent and ads.

    Parameters:
        
    - Form parameters:
        - **first_name:str** (required) -> First name of the person.
        - **last_name:str** (required) -> Last name of the person.
        - **email:EmailStr** (required) -> Email of the person.
        - **message:str** (required) -> Message of the person.

    - Header parameters:
        - **user_agent: str** (optional) -> User agent of the browser used by the person.

    - Cookie parameters:
        - **ads: str** (optional) -> Information of the cookies at browser.

    Returns:
        - Dictionary with the first name, user_agent and ads.
    """
    return user_agent


@app.post(
    path="/post-image",
    tags=['Image'],
    summary=["Upload Image"]
)
def post_image(
    image: UploadFile = File(...,)
):
    """
    Post Image

    This endpoint recieves an image and uploads it to the server.

    Parameters:

    - File parameters:
        - Image:UploadFile (required) -> Image to upload.
    
    Returns:
        - Dictionary with the image information (file name, type and size in KB.)
    """
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read()) / 1024, ndigits=2)
    }