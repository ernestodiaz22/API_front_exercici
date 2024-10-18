from internal.client import db_client
from routers import alumnes
import mysql.connector

def read():
    try:
        conn = db_client()  
        cur = conn.cursor()  
        cur.execute("SELECT alumne.nomAlumne, alumne.cicle,alumne.curs, alumne.grup,aula.descAula FROM alumne INNER JOIN aula ON alumne.idAula = aula.idAula")  
        alumnes = cur.fetchall()  
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        if conn and hasattr(conn, "close"):  
            conn.close()  
    
    return alumnes 

def read_all():
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT alumne.idAlumne,alumne.nomAlumne, alumne.cicle, alumne.curs, alumne.grup, aula.idAula, aula.descAula, aula.edifici, aula.pis FROM alumne INNER JOIN aula ON alumne.idAula = aula.idAula")
        alumnes = cur.fetchall()
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        if conn and hasattr(conn, "close"):  
            conn.close()  
    return alumnes 

def read_id(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT * FROM alumne WHERE idAlumne = %s"
        value = (id,)
        cur.execute(query,value) 
        alumne = cur.fetchone()
    except Exception as e:
         return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        if conn and hasattr(conn, "close"): 
            conn.close() 
    
    return alumne

def create(idAula,nomAlumne,cicle,curs,grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "INSERT INTO alumne (idAula,nomAlumne,cicle,curs,grup) VALUES (%s,%s,%s,%s,%s);"
        values=(idAula,nomAlumne,cicle,curs,grup)
        cur.execute(query,values)

        conn.commit()
        alumne_id = cur.lastrowid
    except mysql.connector.Error as e: #capturar errores mysql
        if e.errno == 1452: #código de error que corresponde a las claves foráneas
            return {"status": -1, "message": "El id del aula no coincide con ninguna aula existente."} 
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally:
        conn.close()
    return {"status": 1, "alumne_id": alumne_id}

def delete_alumne(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "DELETE FROM alumne WHERE idAlumne =  %s;"
        cur.execute(query,(id,))
        deleted_recs = cur.rowcount
        conn.commit()
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
        
    return deleted_recs

def update_alumne(idAula, id, nomAlumne, cicle, curs, grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        
        # comprobar si al id existe
        cur.execute("SELECT COUNT(*) FROM aula WHERE idAula = %s", (idAula,))
        if cur.fetchone()[0] == 0:
            return {"status": -1, "message": "El id del aula no coincide con ninguna aula existente."}

        # Realizar la actualización
        query = "UPDATE alumne SET idAula = %s, nomAlumne = %s, cicle = %s, curs = %s, grup = %s WHERE idAlumne = %s;"
        values = (idAula, nomAlumne, cicle, curs, grup, id)
        cur.execute(query, values)
        
        # Comprobar si existe alguna fila
        if cur.rowcount == 0:
            return {"status": -1, "message": "No se encontró el alumno para actualizar."}

        conn.commit()
        return {"status": 1, "message": "El alumno ha sido actualizado correctamente."}

    except mysql.connector.Error as e:  # Capturar errores de MySQL
        if e.errno == 1452:  # Código de error que corresponde a las claves foráneas
            return {"status": -1, "message": "El id del aula no coincide con ninguna aula existente."}
        else:
            return {"status": -1, "message": f"Error de conexión: {e}"}
    except Exception as e:
        return {"status": -1, "message": f"Error de conexión: {e}"}
    finally:
        conn.close()



           