document.addEventListener("DOMContentLoaded", function() {
    // Cridem a l'endpoint de l'API fent un fetch
        fetch("http://127.0.0.1:8000/alumne/list")
        .then(response => {
            if (!response.ok) {
                throw new Error("Error a la resposta del servidor");
            }
            return response.json();
        })
       .then(data => {
        console.log(data);
            const alumnesTableBody = document.querySelector("#tablaAlumne tbody");
            alumnesTableBody.innerHTML = ""; // Netejar la taula abans d'afegir res
            
            // Iterar sobre los alumnos y agregarlos al DOM
            data.forEach(alumne => {
                const row = document.createElement("tr");

                const nomCell = document.createElement("td");
                const cicleCell = document.createElement("td");
                const cursCell = document.createElement("td");
                const grupoCell = document.createElement("td");
                const aulaNomCell = document.createElement("td");
                nomCell.textContent = alumne.nomAlumne;
                cicleCell.textContent = alumne.cicle;
                cursCell.textContent = alumne.curs;
                grupoCell.textContent = alumne.grup;
                aulaNomCell.textContent = alumne.descAula;
                row.appendChild(nomCell);
                row.appendChild(cicleCell);
                row.appendChild(cursCell);
                row.appendChild(grupoCell);
                row.appendChild(aulaNomCell);
                alumnesTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error capturat:", error);
            alert("Error al carregar la llista d'alumnes");
        });
});