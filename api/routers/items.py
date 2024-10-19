from typing import List

from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from routers import alumnes 

from internal import db_alumnes

from fastapi import FastAPI, File, UploadFile

router = APIRouter()

class tablaAlumne(BaseModel):
    nomAlumne: str
    cicle: str
    curs: int
    grup: str
    descAula: str
    
@router.post("/alumne/loadAlumnes")
async def loadAlumnes(file: UploadFile):
    contents = await file.read()
    inserts = contents.decode('utf-8').splitlines()#utilizamos decode para decodificar de byte a String y separamos por líneas el documento csv
    aulasInsertadas = []
    for insert in inserts:#recorremos los inserts
         alumno = insert.split(",") #cogemos los datos de los alumnos de cada insert
         descAula = alumno[0] 
         edifici = alumno[1]
         pis = int(alumno[2])
         nomAlumne = alumno[3] 
         cicle = alumno[4]
         curs = int(alumno[5])
         grup = alumno[6]
         db_alumnes.addAula(descAula, edifici,pis) #insert con comprobación dde aula
         db_alumnes.addAlumno(nomAlumne,cicle,curs,grup,descAula) #insert con comprobación de alumno
    return {"aula": aulasInsertadas}

@router.get("/alumne/list", response_model=List[tablaAlumne])
async def read_alumnes(orderby: str | None = None,  contain: str | None = None, skip: int = 0, limit: int | None = None):
    return alumnes.alumnes_schema(db_alumnes.read(orderby , contain, limit, skip))#read según que parámetros sean none o no none



         
    
