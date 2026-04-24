from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
# creando la aplicación Flask
app = Flask(__name__)
# configurando la conexión a la base de datos MySQL
mysql = MySQL(app)

# conexion a la BD tienda_db en MySQL
app.config['MYSQL_HOST'] = "localhost" # dirección del servidor MySQL
app.config['MYSQL_USER'] = "root" # nombre de usuario para la conexión a MySQL
app.config['MYSQL_PASSWORD'] = "" # contraseña para la conexión a MySQL
app.config['MYSQL_DB'] = "tienda_db" # nombre de la base de datos a la que se conectará la aplicación Flask
# ruta para probar la conexión a la base de datos
@app.route('/testdb') # definiendo la ruta para probar la conexión a la base de datos
def test(): # definiendo la función para probar la conexión a la base de datos
    cursor = mysql.connection.cursor() # obteniendo un cursor para ejecutar consultas SQL
    sql = "SELECT 1" # consulta SQL simple para probar la conexión a la base de datos
    cursor.execute(sql) # ejecutando la consulta SQL
    return "Conexión a la base de datos exitosa" # devolviendo un mensaje de éxito si la conexión a la base de datos es exitosa
    
#_____________________________________________________________________
# definiendo la ruta para la página de inicio
@app.route('/')
def inicio():
    return render_template('index.html') # renderizando la plantilla HTML 'index.html' como respuesta a la solicitud GET /

#_____________________________________________________________________
#ENDPOINT GET /categorias
@app.route('/categorias', methods=['GET']) # definiendo la ruta para obtener todas las categorías de la base de datos
def listar_categorias(): # obteniendo un cursor para ejecutar consultas SQL
    cursor = mysql.connection.cursor() # obteniendo un cursor para ejecutar consultas SQL
    sql = "SELECT id, nombre FROM categoria" # consulta SQL para obtener todas las categorías de la base de datos
    cursor.execute(sql) # ejecutando la consulta SQL para obtener todas las categorías de la base de datos
    datos = cursor.fetchall() # obteniendo todos los resultados de la consulta SQL y almacenándolos en la variable 'datos'

    if datos is None: # verificando si no se encontraron categorías en la base de datos
        msg = {
            "mensage": "No existe producto!!" # devolviendo un mensaje de error si no se encontraron categorías en la base de datos
        }
        return jsonify(msg) # devolviendo un mensaje de error si no se encontraron categorías en la base de datos
   
    categorias = [] # creando una lista vacía para almacenar las categorías obtenidas de la base de datos
    for fila in datos: # iterando sobre cada fila de resultados obtenidos de la consulta SQL para obtener todas las categorías de la base de datos
        categorias.append( # agregando cada categoría a la lista de categorías
            {
                "id": fila[0], # agregando el id de la categoría a la lista de categorías
                "nombre": fila[1] # agregando el nombre de la categoría a la lista de categorías
            }
        )
    cursor.close() # cerrando el cursor después de obtener todas las categorías de la base de datos
    return jsonify(categorias) # devolviendo la lista de categorías en formato JSON como respuesta a la solicitud GET /categorias

#_____________________________________________________________________
# endpoint GET /productos
@app.route('/productos', methods=['GET']) # definiendo la ruta para obtener todos los productos de la base de datos
def productos(): # obteniendo un cursor para ejecutar consultas SQL
    cursor = mysql.connection.cursor() # obteniendo un cursor para ejecutar consultas SQL
    sql = "SELECT id, nombre, precio, stock, categoria_id FROM producto" # consulta SQL para obtener todos los productos de la base de datos
    cursor.execute(sql) # ejecutando la consulta SQL para obtener todos los productos de la base de datos
    datos = cursor.fetchall() # obteniendo todos los resultados de la consulta SQL y almacenándolos en la variable 'datos'

    if datos is None: # verificando si no se encontraron productos en la base de datos
        msg = {
            "mensage": "No existe producto!!" # devolviendo un mensaje de error si no se encontraron productos en la base de datos
        }
        return jsonify(msg) # devolviendo un mensaje de error si no se encontraron productos en la base de datos
   
    productos = [] # creando una lista vacía para almacenar los productos obtenidos de la base de datos
    for fila in datos: # iterando sobre cada fila de resultados obtenidos de la consulta SQL para obtener todos los productos de la base de datos
        productos.append( # agregando cada producto a la lista de productos
            {
                "id": fila[0], # agregando el id del producto a la lista de productos
                "nombre": fila[1], # agregando el nombre del producto a la lista de productos
                "precio": float(fila[2]), # agregando el precio del producto a la lista de productos
                "stock": fila[3], # agregando el stock del producto a la lista de productos
                "categoria_id": fila[4] # agregando el id de la categoría del producto a la lista de productos
            }
        )
    cursor.close() # cerrando el cursor después de obtener todos los productos de la base de datos
    return jsonify(productos) # devolviendo la lista de productos en formato JSON como respuesta a la solicitud GET /productos






#_____________________________________________________________________
# endpoint GET /productos/<id>
@app.route('/productos/<int:id>', methods=['GET']) # definiendo la ruta para obtener un producto específico de la base de datos utilizando su id
def producto_id(id): # obteniendo un cursor para ejecutar consultas SQL
    cursor = mysql.connection.cursor() # obteniendo un cursor para ejecutar consultas SQL
    # consulta SQL para obtener un producto específico de la base de datos utilizando su id
    sql = """SELECT id, nombre, precio, stock, categoria_id
             FROM producto
             WHERE id = %s""" # consulta SQL para obtener un producto específico de la base de datos utilizando su id
    cursor.execute(sql,(id,)) # ejecutando la consulta SQL para obtener un producto específico de la base de datos utilizando su id
    datos = cursor.fetchone() # obteniendo el resultado de la consulta SQL para obtener un producto específico de la base de datos utilizando su id y almacenándolo en la variable 'datos'

    if datos is None: # verificando si no se encontró el producto en la base de datos utilizando su id
        msg = {
            "mensage": "No existe producto!!"
        }
        return jsonify(msg)
   
    productos = []
    productos.append( # agregando el producto a la lista de productos
        {
            "id": datos[0],
            "nombre": datos[1],
            "precio": float(datos[2]),
            "stock": datos[3],
            "categoria_id": datos[4]
        }
    )
    cursor.close()
    return jsonify(productos) # devolviendo el producto en formato JSON como respuesta a la solicitud GET /productos/<id>

#_____________________________________________________________________
#endpoint GET /productos_categoria
@app.route('/productos_categoria', methods=['GET']) # definiendo la ruta para obtener todos los productos de la base de datos
def productos_con_categoria(): # obteniendo un cursor para ejecutar consultas SQL
    cursor = mysql.connection.cursor() # obteniendo un cursor para ejecutar consultas SQL       
    sql = """SELECT p.id,p.nombre,p.precio,p.stock,c.nombre
            FROM producto p
            JOIN categoria c ON c.id = p.categoria_id""" # consulta SQL para obtener todos los productos de la base de datos junto con el nombre de su categoría utilizando una unión entre las tablas 'producto' y 'categoria'
    cursor.execute(sql) # ejecutando la consulta SQL para obtener todos los productos de la base de datos
    datos = cursor.fetchall() # obteniendo todos los resultados de la consulta SQL y almacenándolos en la variable 'datos'

   
    productos = [] # creando una lista vacía para almacenar los productos obtenidos de la base de datos
    for fila in datos: # recorriendo cada fila de resultados obtenidos de la consulta SQL para obtener todos los productos de la base de datos junto con el nombre de su categoría utilizando una unión entre las tablas 'producto' y 'categoria'
        productos.append( # agregando cada producto a la lista de productos
            {
                "id": fila[0], # agregando el id del producto a la lista de productos
                "nombre": fila[1], # agregando el nombre del producto a la lista de productos
                "precio": fila[2], # agregando el precio del producto a la lista de productos
                "stock": fila[3], # agregando el stock del producto a la lista de productos
                "categoria": fila[4] # agregando el nombre de la categoría del producto a la lista de productos
            }
        )
    cursor.close() # cerrando el cursor después de obtener todos los productos de la base de datos
    return jsonify(productos) # devolviendo la lista de productos en formato JSON como respuesta a la solicitud GET /productos/<categoria_id>


#_____________________________________________________________________
#endpoint GET /producto/categoria/<id_categoria>
@app.route('/productos/categoria/<int:id>', methods=['GET']) # definiendo la ruta para obtener todos los productos de una categoría específica de la base de datos utilizando el id de la categoría
def productos_por_categoria(id): # obteniendo un cursor para ejecutar consultas SQL
    cursor = mysql.connection.cursor() # obteniendo un cursor para ejecutar consultas SQL
    sql = """SELECT p.id,p.nombre,p.precio,p.stock,c.nombre
            FROM producto p
            JOIN categoria c ON c.id = p.categoria_id
            WHERE c.id = %s""" # consulta SQL para obtener todos los productos de una categoría específica de la base de datos utilizando el id de la categoría
    cursor.execute(sql,(id,)) # ejecutando la consulta SQL para obtener todos los productos de una categoría específica de la base de datos utilizando el id de la categoría
    datos = cursor.fetchall() # obteniendo todos los resultados de la consulta SQL y almacenándolos en la variable 'datos'

   
    productos = [] # creando una lista vacía para almacenar los productos obtenidos de la base de datos
    for fila in datos: # recorriendo cada fila de resultados obtenidos de la consulta SQL para obtener todos los productos de una categoría específica de la base de datos utilizando el id de la categoría
        productos.append( # agregando cada producto a la lista de productos
            {
                "id": fila[0], # agregando el id del producto a la lista de productos
                "nombre": fila[1], # agregando el nombre del producto a la lista de productos
                "precio": float(fila[2]), # agregando el precio del producto a la lista de productos
                "stock": fila[3], # agregando el stock del producto a la lista de productos
                "categoria": fila[4] # agregando el nombre de la categoría del producto a la lista de productos
            }
        )
    cursor.close() # cerrando el cursor después de obtener todos los productos de una categoría específica de la base de datos utilizando el id de la categoría
    return jsonify(productos) # devolviendo la lista de productos en formato JSON como respuesta a la solicitud GET /producto/categoría/<id_categoria>

# @app.route('/')
# def inicio():
#     return render_template('index.html')


#_____________________________________________________________________
# # Tarea: implementación de endpoints

# Implementar endpoints para: producto mas caro, producto con poco stock, cantidad de productos por categoría


# En un PDF con caratula capturas de pantalla del código de cada endpoint y el resultado en el navegador o en postman

# Crear un repositorio para el proyecto en su github, subir el proyecto, luego en la caratula debajo del titulo colocar el enlace del repositorio
#_____________________________________________________________________
# 1. Endpoint: Producto más caro
@app.route('/productos/mas-caro', methods=['GET'])
def producto_mas_caro():
    cursor = mysql.connection.cursor()
    # Aplicando ORDER BY y LIMIT 1 para obtener el de mayor precio
    sql = "SELECT id, nombre, precio FROM producto ORDER BY precio DESC LIMIT 1"
    cursor.execute(sql)
    datos = cursor.fetchone()
    cursor.close()

    if datos:
        return jsonify({
            "id": datos[0],
            "nombre": datos[1],
            "precio": float(datos[2])
        })
    return jsonify({"mensaje": "No hay productos"}), 404

# 2. Endpoint: Productos con poco stock (menor a 5 unidades)
@app.route('/productos/poco-stock', methods=['GET'])
def poco_stock():
    cursor = mysql.connection.cursor()
    sql = "SELECT id, nombre, stock FROM producto WHERE stock < 5"
    cursor.execute(sql)
    datos = cursor.fetchall()
    cursor.close()

    resultado = []
    for fila in datos:
        resultado.append({
            "id": fila[0],
            "nombre": fila[1],
            "stock": fila[2]
        })
    
    return jsonify(resultado)

# 3. Endpoint: Cantidad de productos por categoría
@app.route('/categorias/cantidad-productos', methods=['GET'])
def cantidad_por_categoria():
    cursor = mysql.connection.cursor()
    # Realizamos un JOIN para traer el nombre de la categoría y contamos
    sql = """
        SELECT c.nombre, COUNT(p.id) as total 
        FROM categoria c 
        LEFT JOIN producto p ON c.id = p.categoria_id 
        GROUP BY c.nombre
    """
    cursor.execute(sql)
    datos = cursor.fetchall()
    cursor.close()

    resultado = []
    for fila in datos:
        resultado.append({
            "categoria": fila[0],
            "cantidad": fila[1]
        })
    
    return jsonify(resultado)









#_____________________________________________________________________












#_____________________________________________________________________
# ejecutando la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)