from typing import List

from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from routers import alumnes 

from internal import db_alumnes

from datetime import datetime

router = APIRouter()

class alumne(BaseModel):
    idAlumne: int
    idAula: int
    nomAlumne: str
    cicle: str
    curs: int
    grup: str
    createdAt:datetime
    updatedAt:datetime

class tablaAlumne(BaseModel):
    nomAlumne: str
    cicle: str
    curs: int
    grup: str
    descAula: str

@router.get("/alumne/list", response_model=List[tablaAlumne])
def read_alumnes():
    return alumnes.alumnes_schema(db_alumnes.read())

@router.get("/alumne/listAll")
def read_alumnesAula():
    return alumnes.alumnesAulas_schema(db_alumnes.read_all())

@router.get("/alumne/show/{id}", response_model=alumne)
def read_alumne_id(id:int):
    if db_alumnes.read_id(id) is not None:
        alumne = alumnes.alumne_schema(db_alumnes.read_id(id))
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    return alumne

@router.post("/alumne/add")
async def create_alumne(data:alumne):
        idAula = data.idAula
        nomAlumne = data.nomAlumne
        cicle = data.cicle
        curs = data.curs
        grup = data.grup
        query = db_alumnes.create(idAula,nomAlumne, cicle,curs,grup)
        if query["status"] == -1:
             return{"message": query["message"]}
        return {
            "msg": "S’ha afegit correctement"
        }
@router.put("/alumne/update/{id}")
async def update_alumne(data:alumne, id:int):
        idAula = data.idAula
        nomAlumne = data.nomAlumne
        cicle = data.cicle
        curs = int(data.curs)
        grup = data.grup
        query = db_alumnes.update_alumne(idAula,id,nomAlumne,cicle,curs,grup)
        if query["status"] == -1:
             return{"message": query["message"]}
        return {
            "msg": "S’ha modificat correctement",
        }

@router.post("/alumne/delete/{id}")
def delete_alumne(id:int):
    deleted_records = db_alumnes.delete_alumne(id)
    if deleted_records == 0:
       raise HTTPException(status_code=404, detail="Items to delete not found") 
    return {
        "msg": "S’ha modificat correctement",
    }

         
    
