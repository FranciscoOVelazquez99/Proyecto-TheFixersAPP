import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
import hashlib

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

# --- Función de Login ---
def verificar_login(username, password):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        conexion.close()
        if result:
            return True
        else:
            return False
    return False

# --- Ventana de Login ---
class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Login - Servicio Técnico")
        self.master.geometry("300x200")
        self.master.resizable(False, False)

        # Usuario
        self.label_username = tk.Label(master, text="Usuario:")
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(master)
        self.entry_username.pack()

        # Contraseña
        self.label_password = tk.Label(master, text="Contraseña:")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.pack()

        # Botón de Login
        self.button_login = tk.Button(master, text="Ingresar", command=self.login)
        self.button_login.pack(pady=20)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if verificar_login(username, password):
            messagebox.showinfo("Éxito", "Login exitoso.")
            self.master.destroy()
            root = tk.Tk()
            app = MainWindow(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrecta.")

# --- Ventana Principal ---
class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestión de Inventarios - Servicio Técnico")
        self.master.geometry("600x400")
        self.master.resizable(False, False)

        # Pestañas
        self.tab_control = ttk.Notebook(master)

        # Pestaña Registrar Reparación
        self.tab_registrar = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_registrar, text='Registrar Reparación')

        # Pestaña Actualizar Estado
        self.tab_actualizar = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_actualizar, text='Actualizar Estado')

        # Pestaña Ver Reparaciones
        self.tab_ver = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_ver, text='Ver Reparaciones')

        self.tab_control.pack(expand=1, fill='both')

        self.crear_tab_registrar()
        self.crear_tab_actualizar()
        self.crear_tab_ver()

    # --- Pestaña Registrar Reparación ---
    def crear_tab_registrar(self):
        frame = self.tab_registrar

        # Cliente
        tk.Label(frame, text="Cliente:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_cliente = tk.Entry(frame, width=40)
        self.entry_cliente.grid(row=0, column=1, padx=10, pady=10)

        # Dispositivo
        tk.Label(frame, text="Dispositivo:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_dispositivo = tk.Entry(frame, width=40)
        self.entry_dispositivo.grid(row=1, column=1, padx=10, pady=10)

        # Problema
        tk.Label(frame, text="Problema:").grid(row=2, column=0, padx=10, pady=10, sticky='ne')
        self.text_problema = tk.Text(frame, width=30, height=5)
        self.text_problema.grid(row=2, column=1, padx=10, pady=10)

        # Costo
        tk.Label(frame, text="Costo (USD):").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.entry_costo = tk.Entry(frame, width=40)
        self.entry_costo.grid(row=3, column=1, padx=10, pady=10)

        # Botón Registrar
        self.button_registrar = tk.Button(frame, text="Registrar Reparación", command=self.registrar_reparacion)
        self.button_registrar.grid(row=4, column=1, pady=20)

    def registrar_reparacion(self):
        cliente = self.entry_cliente.get()
        dispositivo = self.entry_dispositivo.get()
        problema = self.text_problema.get("1.0", tk.END).strip()
        costo = self.entry_costo.get()

        if not cliente or not dispositivo or not problema:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return

        try:
            costo = float(costo)
        except ValueError:
            messagebox.showerror("Error", "El costo debe ser un número.")
            return

        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            query = """INSERT INTO reparaciones (cliente, dispositivo, problema, fecha_ingreso, costo)
                       VALUES (%s, %s, %s, CURDATE(), %s)"""
            try:
                cursor.execute(query, (cliente, dispositivo, problema, costo))
                conexion.commit()
                messagebox.showinfo("Éxito", "Reparación registrada correctamente.")
                # Limpiar campos
                self.entry_cliente.delete(0, tk.END)
                self.entry_dispositivo.delete(0, tk.END)
                self.text_problema.delete("1.0", tk.END)
                self.entry_costo.delete(0, tk.END)
            except Error as e:
                messagebox.showerror("Error", f"Error al registrar la reparación:\n{e}")
            finally:
                cursor.close()
                conexion.close()

    # --- Pestaña Actualizar Estado ---
    def crear_tab_actualizar(self):
        frame = self.tab_actualizar

        # ID de Reparación
        tk.Label(frame, text="ID de Reparación:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_id_reparacion = tk.Entry(frame, width=40)
        self.entry_id_reparacion.grid(row=0, column=1, padx=10, pady=10)

        # Nuevo Estado
        tk.Label(frame, text="Nuevo Estado:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.combo_estado = ttk.Combobox(frame, values=["Pendiente", "En Proceso", "Completada", "Entregada"])
        self.combo_estado.grid(row=1, column=1, padx=10, pady=10)
        self.combo_estado.current(0)

        # Botón Actualizar
        self.button_actualizar = tk.Button(frame, text="Actualizar Estado", command=self.actualizar_estado)
        self.button_actualizar.grid(row=2, column=1, pady=20)

    def actualizar_estado(self):
        reparacion_id = self.entry_id_reparacion.get()
        nuevo_estado = self.combo_estado.get()

        if not reparacion_id:
            messagebox.showerror("Error", "Por favor, ingresa el ID de la reparación.")
            return

        try:
            reparacion_id = int(reparacion_id)
        except ValueError:
            messagebox.showerror("Error", "El ID de reparación debe ser un número.")
            return

        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            query = "UPDATE reparaciones SET estado = %s WHERE id = %s"
            try:
                cursor.execute(query, (nuevo_estado, reparacion_id))
                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "No se encontró una reparación con ese ID.")
                else:
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Estado actualizado correctamente.")
                    # Limpiar campos
                    self.entry_id_reparacion.delete(0, tk.END)
            except Error as e:
                messagebox.showerror("Error", f"Error al actualizar el estado:\n{e}")
            finally:
                cursor.close()
                conexion.close()

    # --- Pestaña Ver Reparaciones ---
    def crear_tab_ver(self):
        frame = self.tab_ver

        # Tabla de Reparaciones
        columns = ("ID", "Cliente", "Dispositivo", "Problema", "Fecha Ingreso", "Estado", "Costo")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botón para Cargar Datos
        self.button_cargar = tk.Button(frame, text="Cargar Reparaciones", command=self.cargar_reparaciones)
        self.button_cargar.pack(pady=10)

    def cargar_reparaciones(self):
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            query = "SELECT * FROM reparaciones"
            try:
                cursor.execute(query)
                reparaciones = cursor.fetchall()
                # Limpiar la tabla
                for row in self.tree.get_children():
                    self.tree.delete(row)
                # Insertar nuevas filas
                for reparacion in reparaciones:
                    self.tree.insert("", tk.END, values=reparacion)
            except Error as e:
                messagebox.showerror("Error", f"Error al cargar las reparaciones:\n{e}")
            finally:
                cursor.close()
                conexion.close()

# --- Ejecutar la Aplicación ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
