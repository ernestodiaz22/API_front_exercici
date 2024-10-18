def alumne_schema(alumne) -> dict:
    return {
        "nomAlumne": alumne[0],
        "cicle": alumne[1],
        "curs": alumne[2],
        "grup": alumne[3],
        "descAula": alumne[4]
    }
def alumneAula_schema(alumne) -> dict:
    return {
        "idAlumne": alumne[0],
        "nomAlumne": alumne[1],
        "cicle": alumne[2],
        "curs": alumne[3],
        "grup": alumne[4],
        "idAula": alumne[5],
        "descAula": alumne[6],
        "edifici": alumne[7],
        "pis": alumne[8]
    }

def alumnes_schema(alumnes)-> dict:
    return [alumne_schema(alumne) for alumne in alumnes]

def alumnesAulas_schema(alumnes)-> dict:
    return [alumneAula_schema(alumne) for alumne in alumnes]

