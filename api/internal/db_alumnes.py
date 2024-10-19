from internal.client import db_client
from routers import alumnes
import mysql.connector
    
def read(orderby = None, contain = None, limit = None, skip = None):
    try:
        conn = db_client()  
        cur = conn.cursor()
        query = "SELECT alumne.nomAlumne, alumne.cicle,alumne.curs, alumne.grup,aula.descAula FROM alumne INNER JOIN aula ON alumne.idAula = aula.idAula" #query por defecto los alumnos sin parámetros
        if orderby is not None:#query orderby
            query = f"SELECT alumne.nomAlumne, alumne.cicle, alumne.curs, alumne.grup, aula.descAula FROM alumne INNER JOIN aula ON alumne.idAula = aula.idAula ORDER BY nomAlumne  {orderby}"
        elif contain is not None:#query contain
           query = f"SELECT alumne.nomAlumne, alumne.cicle, alumne.curs, alumne.grup, aula.descAula FROM alumne INNER JOIN aula ON alumne.idAula = aula.idAula WHERE alumne.nomAlumne LIKE '%{contain}%'"
        elif limit is not None and skip is not None:#query limit
           query = f"SELECT alumne.nomAlumne, alumne.cicle, alumne.curs, alumne.grup, aula.descAula FROM alumne INNER JOIN aula ON alumne.idAula = aula.idAula LIMIT {limit} OFFSET {skip}"
        cur.execute(query)  
        alumnes = cur.fetchall()  
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        if conn and hasattr(conn, "close"):  
            conn.close()  
    
    return alumnes 

#AÑADIR AULA
def addAula(descAula, edifici, pis):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT * FROM aula WHERE descAula LIKE %s"#busco si existe otro aula con el mismo nombre
        values = (descAula,)
        cur.execute(query, values)
        aula = cur.fetchone()
        if aula is None:#si no existe
            aula = cur.fetchone()
            query = "INSERT INTO aula (descAula, edifici, pis) VALUES (%s,%s,%s)"#inserto aula
            values=(descAula, edifici, pis)
            cur.execute(query,values)
            conn.commit()
            
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        conn.close()
    return {"status": 1}

#AÑADIR ALUMNOS
def addAlumno(nomAlumne,cicle,curs,grup,descAula):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT * FROM alumne WHERE nomAlumne LIKE %s AND cicle LIKE %s AND curs = %s AND grup LIKE %s"#busco que no exista un alumno matriculado en el mismo curso, grupo o ciclo
        values = (nomAlumne, cicle, curs, grup)
        cur.execute(query,values)
        alumno = cur.fetchone()
        if alumno is None:#si no existe
            query = "SELECT aula.idAula FROM aula WHERE descAula = %s"#busco el id del alumno para hacer el insert
            values = (descAula,)
            cur.execute(query, values)
            aula = cur.fetchone()
            idAula = aula[0]#id del aula
            query = "INSERT INTO alumne (idAula,nomAlumne,cicle,curs,grup) VALUES (%s,%s,%s,%s,%s);"#inserte de alumno
            values = (idAula,nomAlumne,cicle,curs,grup)
            cur.execute(query, values)
            conn.commit()
            idAlumno = cur.lastrowid#id del aula
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        conn.close()
    return {"status": 1}




           