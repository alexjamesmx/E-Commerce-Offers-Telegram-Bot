from pymongo import MongoClient
import logging
from datetime import datetime
from consts import DB_CONFIG_MONGO

def establish_connection():
    try:
        client = MongoClient(DB_CONFIG_MONGO['uri'])
        db = client[DB_CONFIG_MONGO['database']]
        return db
    except Exception as e:
        logging.error(f"Error al conectar a MongoDB: {e}")
    return None


def save_product(product_id, date_sent=datetime.now()) :
    try:
        collection = db.productos_enviados
        collection.insert_one({'id': product_id, 'fecha_envio': date_sent})
    except Exception as e:
        logging.error(f"Error saving product {e}")

def already_published(product_id):
    try:
        collection = db.productos_enviados
        return collection.find_one({'id': product_id}) is not None
    except Exception as e:
        logging.error(f"Error verifying product: {e}")
    return False



#function for importing data from a SQL file and saving it to MongoDB 

# def importar_datos_desde_sql(file_path):
#     print(file_path)
#     with open(file_path, 'r') as file:
#         sql_content = file.read()

#     # Extract values from the SQL file
#     pattern = re.compile(r"\(\s*'([^']*)'\s*,\s*'([^']*)'\s*\)")
#     # print(sql_content) 
#     matches = pattern.findall(sql_content)
#     print(matches)

#     for match in matches:
#         producto_id = match[0]
#         fecha_envio = datetime.strptime(match[1], '%Y-%m-%d %H:%M:%S')
#         guardar_producto(producto_id, fecha_envio)



db = establish_connection() 