def alumne_schema(alumne) -> dict:
    return {
        "nomAlumne": alumne[0],
        "cicle": alumne[1],
        "curs": alumne[2],
        "grup": alumne[3],
        "descAula": alumne[4]
    }

def alumnes_schema(alumnes)-> dict:
    return [alumne_schema(alumne) for alumne in alumnes]


