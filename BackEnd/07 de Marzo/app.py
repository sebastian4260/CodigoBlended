# pip install flask mysqlclient flask_mysqldb
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
# ACA HAGO TODA LA CONFIGURACION DE MI BASE DE DATOS
app.config['MYSQL_HOST']='127.0.0.1' #localhost
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='veterinaria'

# CREO LA INSTANCIA CON MI CLASE MYSQL Y LE PASO TODA LA CONFIGURACION DE CONEXION
conexion = MySQL(app=app)

# DEFINO LA RUTA (ENDPOINT)
@app.route('/quien_eres')
def hola():
    return 'Hola yo soy el backend de veterinaria'

@app.route('/mascotas')
def mascotas():
    # CREO UNA CONEXION CON MI BD USANDO LA CADENA DE CONEXION
    conexionMYSQL = conexion.connection.cursor()
    # DEFINO MI CONSULTA SQL
    sentencia = "SELECT * FROM t_mascota"
    # EJECUTO MI CONSULTA SQL
    conexionMYSQL.execute(sentencia)
    #fetchall
    #fetchone
    # DEVUELVO LOS VALORES (YA SEA UNO (FETCHONE) O TODOS (FETCHALL))
    informacion = conexionMYSQL.fetchall()
    # CIERRO MI CONEXION
    conexionMYSQL.close()
    print(informacion)
    # VALIDO SI HAY INFORMACION O NO
    if informacion:
        return 'Si hay mascotas'
    else:
        return 'Todavia no hay mascotas registradas'

@app.route('/raza/agregar', methods=['POST'])
def agregar_raza():
    # GUARDO TODO LO ENVIADO POR EL USUARIO MEDIANTE EL BODY
    contenido = request.get_json()
    print(contenido['nombre'])
    # ABRO UNA CONEXION CON MI BD
    conexionMYSQL = conexion.connection.cursor()
    # EJECUTO LA SENTENCIA DE INSERCION
    conexionMYSQL.execute("INSERT INTO t_raza (raza_nom) VALUES ('"+contenido['nombre']+"')")
    # GUARDO LOS CAMBIOS EN MI BASE DE DATOS
    conexion.connection.commit()
    # CIERRO LA CONEXION
    conexionMYSQL.close()
    # LE RETORNO UN MENSAJE AL USUARIO
    return jsonify({
        'mensaje':'Exito',
        'contenido':'Se agrego exitosamente la raza'
    })

@app.route('/raza/traer_todos', methods=['GET'])
def traer_raza():
    # CREO LA CONEXION
    conexionMYSQL=conexion.connection.cursor()
    # EJECUTO LA SENTENCIA SQL
    conexionMYSQL.execute("SELECT * FROM T_RAZA")
    # DEVUELVO TODOS MIS RESULTADOS Y LO ALMACENO EN UNA VARIABLE
    informacion = conexionMYSQL.fetchall()
    resultado = []
    # ITERO ESA INFORMACION PARA GUARDARLA EN UNA LISTA
    for raza in informacion:
        print(raza)
        razadic={
            'id':raza[0],
            'nombre':raza[1]
        }
        resultado.append(razadic)
    # RETORNO UN MENSAJE AL USUARIO CON LA INFORMACION EXTRAIDA DE LA BD
    return jsonify({
        'message':'Exito',
        'contenido':resultado
    })

# ruta para agregar una especie
@app.route('/especie/agregar', methods=['POST'])
def agregar_especie():
    contenido = request.get_json()
    conexionMYSQL = conexion.connection.cursor()
    conexionMYSQL.execute("INSERT INTO t_especie(esp_nom) VALUES('",contenido['nombre'],"')")
    conexion.connection.commit()
    conexionMYSQL.close()
    return jsonify({
        'mensaje':'Exito',
        'contenido':'Se agrego exitosamente la especie'
    })
# ruta para agregar un tipo de usuario
@app.route('/tusu/agregar', methods=['POST'])
def agregar_tusu():
    contenido = request.get_json()
    conexionMYSQL = conexion.connection.cursor()
    conexionMYSQL.execute("INSERT INTO t_usu(tusu_desc) VALUES ('",contenido['nombre'],"')")
    conexion.connection.commit()
    conexionMYSQL.close()
    return jsonify({
        'mensaje':'Exito',
        'otra_llave':'otro_resultado'
    }), 201
    pass
# ruta para agregar un usuario
@app.route('/usuario/agregar', methods=['POST'])
def agregar_usuario():
    # antes de crear el usuario tengo que validar que el tipo de usuario ingresado sea un usuario que existe
    contenido = request.get_json()
    conexionMYSQL = conexion.connection.cursor()
    conexionMYSQL.execute("SELECT * FROM t_usu WHERE tusu_id="contenido['tipo_usuario'])
    tipos_usuario = conexionMYSQL.fetchone()
    if tipos_usuario:
        # valido que el tipo de usuario ingresado exista
        conexionMYSQL.execute("INSERT INTO t_persona (per_nom, per_ape, per_est, per_dir, per_fono, per_dni, tusu_id VALUES('",contenido['nombre'],"','",contenido['apellido'],"','",contenido['estado'],"','",contenido['direccion'],"','",contenido['telefono'],"','",contenido['dni'],"',",contenido['tipo_usuario'])
        conexion.connection.commit()
        conexionMYSQL.close()
        return jsonify({
            'mensaje':'Exito',
            'contenido':'Se agrego exitosamente el usuario'
        }), 201
    else:
        conexionMYSQL.close()
        return jsonify({
            'mensaje':'Error',
            'contenido':'El tipo de usuario no existe'
        }), 403
# ruta para agregar una mascota
@app.route('/mascota/agregar', methods=['POST'])
def agregar_mascota():
    # Antes de ingresar la mascota se deberia hacer una validacion sobre la especie, raza y la persona para ver si existen, y posterior a ello recien almacenar dicha mascota
    pass

# ESTO SIRVE PARA LEVANTAR EL SERVIDOR, SI ESTA CORRIENDO EL ARCHIVO PRINCIPAL SE VA A CUMPLIR LA CONDICION
if __name__=='__main__':
    # LEVANTO EL SERVIDOR Y LE ESTIPULO QUE EL PARAMETRO DEBUG TENDRA UN VALOR VERDADERO PARA QUE CUANDO HAGA ALGUN CAMBIO Y GUARDE, AUTOMATICAMENTE SE REINICE EL SERVIDOR
    app.run(debug=True)