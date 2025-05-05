from flask import Flask, jsonify, request
from flask_cors import CORS

# PYMYSQL permite la que halla una conexion entre en el archivo de python y la base de datos

import pymysql 

# BCRYPT permite encriptar las contraseñas para mayor seguridad

import bcrypt

# FLASGGER esta extension de flask facilita la cracion de APId de flask

from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

# con el siguiente codigo se hace posible la conexion a la base de datos
def conectar(vhost,vuser,vpass,vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn

#Ruta para consulta general
@app.route("/", methods=['GET'])
def consulta_general():
    """
    Consulta general del baul de contraseñas
    ---
    responses:
    200:
      descripcion: Lista de registros
    """
    try:
        conn = conectar('localhost', 'root', '290307', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("SELECT * FROM baul")
        datos = cur.fetchall()
        data = []
        
        for row in datos:
            dato = {
                'id_baul': row[0],
                'Plataforma': row[1],
                'usuario': row[2],
                'clave': row[3]
            }
            data.append(dato)
        cur.close()
        conn.close()
        return jsonify({'baul': data, 'mensaje': 'Baul de constraseñas'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})


#Ruta para consulta individual
@app.route('/consulta_individual/<codigo>', methods=['GET'])
def consulta_individual(codigo):
    """
    Consulta individual por ID
    ----
    parameters:
      - name: codigo
        in: path
        requried: true
        type: integer
    responses:
      200:
        description: Registro encontrado
    """
    try:
        conn = conectar('localhost', 'root', '290307', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM baul WHERE id_baul = '{codigo}'")
        datos = cur.fetchone()
        cur.close()
        conn.close()
        if datos:
            dato = {'id_baul': datos[0], 'Plataforma': datos[1], 'usuario': datos[2], 'clave':datos[3]}
            return jsonify({'baul': dato, 'mensaje': 'Resgistro encontado'})
        else:
            return jsonify({'mensaje': 'Registro no encontrado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

# si el codigo no funciona colocar / al final

@app.route('/registro/', methods=['POST'])
def registro():
    """
    Registrar nueva contraseña
    -----
    parameters: 
      - name: body
        in: body
        requeried: True
        schema:
          type: object
          propierties:
            plataforma:
              type: string
            usuario:
              type: string
            clave:
              type: string
    responses:
        200:
          description: Registro agregado
    """
    
    try:
        data = request.get_json()
        plataforma = data['plataforma']
        usuario = data['usuario']
        clave = bcrypt.hashpw(data['clave'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        conn = conectar('localhost', 'root', '290307', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("INSERT INTO baul (plataforma, usuario, clave) VALUES (%s, %s, %s)",
                    (plataforma,usuario,clave))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro agregado'})
        
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'error'})

#Ruta para eliminar registro
@app.route('/eliminar/<codigo>', methods=['DELETE'])
def eliminar(codigo):

    """
    Eliminar registro por su ID
    ---
    parameters:
      - name: codigo
        in: path
        requeried: True
        type: integer
    responses:
      200:
        description: Resgistro eliminado
    """

# Si el codigo no funciona colocar depues de codigo una , linea 159

    try:
        conn = conectar('localhost', 'root', '290307', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("DELETE FROM baul WHERE id_baul = %s", (codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Regristro Eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})



# Ruta para actualizar un registro
@app.route('/actualizar/<codigo>', methods=['PUT'])
def actualizar(codigo):
    """
    Actualizar registro por ID
    ----          
    parameters:
      - name: codigo
        in: path
        requeried: true
        type: integer
      - name: body
        in: body
        requeried: true
        sschema:
          type: object
          propierties:
            plataforma:
                type: string
            usuario:
                type: string
            clave:
                type: string
    responses:
      200:
        description: Registro Actualizado
    """
    try:
        data = request.get_json()
        plataforma = data['plataforma']
        usuario = data['usuario']
        clave = bcrypt.hashpw(data['clave'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = conectar('localhost', 'root', '290307', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("UPDATE baul SET plataforma = %s, usuario = %s, clave = %s WHERE id_baul = %s",
                    (plataforma, usuario, clave, codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro actualizado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})
        
if __name__=='__main__':
    app.run(debug=True)