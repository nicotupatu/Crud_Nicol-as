// definir una constante global para la url base
const BASE_URL = "http://127.0.0.1:5000";

// Funcion para visalizar los datos en la pantalla

function visualizar(data) {
    let tabla = ""; // Se debi inicializar una variable que permita almacenar el HTML de la tabla
    
    // Se recorren todos los elementos del array baul y crea una fila en la tabla

    data.baul.forEach(item => {
        tabla += `
            <tr data-id="${item.id_baul}">
                <td>${item.id_baul}</td>
                <td>${item.Plataforma}</td>
                <td>${item.usuario}</td>
                <td>${item.clave}</td>
                <td>
                    <!-- boton para editar -->
                    <button type='button' class='btn btn-info' onclick="location.href = 'edit.html?variable1=${item.id_baul}'"> <img src='imagenes/edit.png' height='30' width='30'/></button>
                </td>
                <td>
                    <!-- buton para eliminar -->
                    <button type='button' class='btn btn-warning' onclick='eliminar(${item.id_baul})'> <img src='imagenes/delete.png' height='30' width='30'/> </button>
                </td>
            </tr>`;
    });
    
    // Insertar la filas generadas en el cuerpo de la tabla
    document.getElementById('data').innerHTML = tabla ;
}

// Funcion para realizar una consulta general (GET)
function consulta_general() {
    fetch(`${BASE_URL}/`)
        .then(response => {
            if (!response.ok) throw new Error(`Error: ${response.status}`); // Manejo de errores HTTP
            return response.json();
        })
        .then( data => visualizar(data)) // Muestra los datos en la tabla
        .catch(error => console.error('Error:', error)); // Captura y muestra los errores en la pantalla
        
}

// Funcion para eliminar un registro por ID (Delete)

function eliminar(id) {
    fetch(`${BASE_URL}/eliminar/${id}`, { method: 'DELETE'}) //Solicitud delete
    .then(response => {
        if (!response.ok) throw new Error(`Error: ${response.status}`); // Manejo de errores HTTP
        return response.json();
    })
    .then(res => {
        actualizarDOM(id); // Elimina el elemento directamente del DOM
        Swal.fire({
            title: "Mensaje",
            text: `${res.mensaje} exitosamente`,
            icon: "success"
          }); // muestra notificacion de exito
    })
    .catch(error => console.error('Error:', error)); // Muestra errores en la consola
}

// Funcion para actualizar el DOM depsues de eliminar un elemento
function actualizarDOM(id) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (row){
        row.romove;
        consulta_general();  // REFRESCA LA PAGINA SIN ACTUALIZAR MANUALMENTE
    }
}

// Funcion para registrar un nuevo registro (POST)
function registrar(){
    // obtiene los valors de los campos de entrada
    const plat = document.getElementById("plataforma").value;
    const usua = document.getElementById("usuario").value;
    const clav = document.getElementById("clave").value;

    // Crea el objeto de datos
    const data = {
        plataforma: plat,
        usuario: usua,
        clave: clav
    };

    console.log(data); // para mostrar datos para depuracion

    fetch(`${BASE_URL}/registro/`,{
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) throw new Error(`Error: ${response.status}`); // Manejo de errores HTTP
        return response.json();
    })
    .then(response => {
        if (response.mensaje === "Error") {
            Swal.fire({
                title: "Mensaje",
                text: `${response.mensaje}`,
                icon: "error"
            });
            swal('Mensaje', "Error en el registro", "error"); // Alerta de error
        } else {
            consulta_general(); // refresca la tabla de datos sin recargar la pagina
            Swal.fire({
                title: "Mensaje",
                text: `${response.mensaje} exitosamente`,
                icon: "success"
            });
        }
    })
    .catch(error => console.error('Error:', error));
}

// funcion para consultar un registro individual (GET)

function consulta_individual(id) {
    fetch(`${BASE_URL}/consulta_individual/${id}`) // solicitud get al endpoint
    .then(response => {
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        return response.json();
    })
    .then(data => {
        console.log(data)
        document.getElementById("plataforma").value = data.baul.Plataforma;
        document.getElementById("usuario").value = data.baul.usuario;
        document.getElementById("clave").value = data.baul.clave;
    })
    .catch(error => console.error('Error:', error));
}

// Funcion para modificar un registo existente put

function modificar(id) {
    const plat = document.getElementById("plataforma").value;
    const usua = document.getElementById("usuario").value;
    const clav = document.getElementById("clave").value;

    // CREA UN OBJETO DE DATOS

    const data={
        plataforma : plat,
        usuario: usua,
        clave: clav,
    };

    fetch(`${BASE_URL}/actualizar/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
        headers:{
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        return response.json();
    })
    .then(response => {
        if (response.mensaje === "Error"){
            Swal.fire({
                title: "Mensaje",
                text: `${response.mensaje}`,
                icon: "error"
            });
        } else{
            consulta_general();
            Swal.fire({
                title: "Mensaje",
                text: `${response.mensaje} exitosamente`,
                icon: "success"
            });
        }
    })
    .catch(error => console.error('Error:', error));
}