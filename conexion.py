
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

script_sql= """
CREATE SCHEMA IF NOT EXISTS servicio_tecnico;

USE servicio_tecnico;

-- Tabla de usuarios para el ingreso
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    rol VARCHAR(255) NOT NULL,
    contraseña VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    compania VARCHAR(50) DEFAULT null,
    compania_contacto VARCHAR(255) DEFAULT null,
    direccion VARCHAR(255),
    ciudad_provincia_codigoPostal VARCHAR(255),
    telefono VARCHAR(255),
    correo VARCHAR(255),
    cuit_dni VARCHAR(255) UNIQUE
);

CREATE TABLE equipo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente int NOT NULL,
    marca_pc VARCHAR(100) NOT NULL,
    modelo_pc VARCHAR(100) NOT NULL,
    serial_pc VARCHAR(100),
    procesador VARCHAR(100),
    velocidad_ghz VARCHAR(100),
    serial_procesador VARCHAR(100),
    memoria_ram VARCHAR(100),
    ram_gb VARCHAR(100),
    serial_ram VARCHAR(100),
    disco_marca VARCHAR(100),
    disco_gb VARCHAR(100),
    serial_hd VARCHAR(100),
    tarjeta_video VARCHAR(100),
    tarjeta_tipo VARCHAR(100),
    serial_tarjeta VARCHAR(100),
    puertos_dim VARCHAR(100),
    puertos_sodimm VARCHAR(100),
    datos_falla TEXT NOT NULL,

    CONSTRAINT cliente_id_equipo
    FOREIGN KEY (id_cliente)
    REFERENCES cliente (id)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS reparaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente int NOT NULL,
    id_equipo int NOT NULL,
    fecha_ingreso DATE NOT NULL,
    estado VARCHAR(50) DEFAULT 'Pendiente',
    fecha_salida DATE,


    CONSTRAINT cliente_id_reparaciones
    FOREIGN KEY (id_cliente)
    REFERENCES cliente (id)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
   

    CONSTRAINT equipo_id_reparaciones
    FOREIGN KEY (id_equipo)
    REFERENCES equipo (id)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS presupuesto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_reparaciones int NOT NULL,
    fecha_presupuesto DATE,
    validez VARCHAR(10),
    estado VARCHAR(50) DEFAULT 'Pendiente', # Pendiente, Aceptado, Rechazado


    CONSTRAINT reparaciones_id_presupuesto
    FOREIGN KEY (id_reparaciones)
    REFERENCES reparaciones (id)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS detalle (
    id INT AUTO_INCREMENT PRIMARY KEY,
   
    id_presupuesto int NOT NULL,
    descripcion TEXT NOT NULL,
    unidades int NOT NULL,
    precio int NOT NULL,
    total int NOT NULL,

    CONSTRAINT presupuesto_id_detalle
    FOREIGN KEY (id_presupuesto)
    REFERENCES presupuesto (id)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
);

"""


# --- Configuración de la Base de Datos ---
def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",        # Reemplaza con tu usuario de MySQL
            password="",# Reemplaza con tu contraseña de MySQL
            database="servicio_tecnico"
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        messagebox.showerror("Error de Conexión", f"Error al conectar a la base de datos:\n{e}")
        return None
        
def crear_db():
    try:
        conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""
        )
        if conexion.is_connected():
            consulta_db = "select schema_name from information_schema.schemata where schema_name = 'servicio_tecnico'"
            cursor = conexion.cursor()
            cursor.execute(consulta_db)
            result = cursor.fetchone()
            if not result:
                cursor.execute(script_sql)
                conexion.commit()
            cursor.close()
            conexion.close()
    except Error as e:
        messagebox.showerror("Error de Conexión", f"Error al crear la base de datos:\n{e}")

def crear_admin():
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="servicio_tecnico"
            )
            if conexion.is_connected():
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM usuarios WHERE nombre = 'admin'")
                result = cursor.fetchone()
                if not result:
                    cursor.execute("INSERT INTO usuarios (nombre, rol, contraseña) VALUES ('admin', 'admin', 'admin')")
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Usuario administrador creado correctamente.")
                cursor.close()
            conexion.close()
        except Error as e:
            messagebox.showerror("Error de Conexión", f"Error al crear el usuario administrador:\n{e}")