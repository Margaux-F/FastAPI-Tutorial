from fastapi import FastAPI, Form
import uvicorn
from typing import Optional #Rendre les paramètres optionels
from pydantic import BaseModel

app = FastAPI()

# Modèle de coordonnées en entrée
class CoordIn(BaseModel):
    password : str
    lat : float 
    lon : float
    zoom : Optional[int] = None
    description : Optional[str] = None

# Modèle de coordonnées en sortie
class CoordOut(BaseModel):   
    lat : float 
    lon : float
    zoom : Optional[int] = None
    description : Optional[str] = None


# get, put, delete

# Méthode get
@app.get("/")
async def hello_world():
    return {"hello" : "world"}


# Exemple de post avec paramètres ajoutés
# @app.post("/position/{priority}") # Pour écrire dans notre base de données par exemple
# async def make_position(priority: int, coord: Coord, value: bool):
#     # db write completed
#     return {"priority" : priority, "new_coordinate" : coord.dict(), "value" : value}

@app.post("/position/", response_model = CoordOut, response_model_exclude={"description"})
#response_model_include={"description"} Mets uniquement la description en sortie
#response_model_exclude={"description"} Enlève uniquement la description en sortie

async def make_position( coord: CoordIn):
    # db write completed
    # Sans modèle de retour, return un dictionnaire
    # return {"new_coordinate" : coord.dict()}
    # Avec un modèle re return, le retourner directement
    return coord


@app.get("/component/{component_id}") # path parameter 
async def get_component(component_id : int):
    # operations 
    return {"component_id" : component_id}

@app.post("/login/")
async def login(username: str = Form(...), password : str = Form(...)):
    return {username: username}




@app.get("/component/")
async def read_component(number: int, text: Optional[str]):
    return {"number" : number, "text": text}

# #http://127.0.0.1:8000/component/?number=12&text=component%20name
# # Rendre text optionel : Optional[str] et lien : http://127.0.0.1:8000/component/?number=12&text=



if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port = 8000)