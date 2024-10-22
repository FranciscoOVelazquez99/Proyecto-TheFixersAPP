import tkinter as tk
import ttkbootstrap as ttk

from datetime import date
from ttkbootstrap.constants import *
from ttkbootstrap import Style

from tkinter import messagebox

from conexion import conectar_db, crear_db, crear_admin

import mysql.connector
from mysql.connector import Error

crear_db()
crear_admin()


    # --- Función de Login ---
def verificar_login(username, password):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        query = "SELECT * FROM usuarios WHERE nombre = %s AND contraseña = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        conexion.close()
        if result:
            return True
        else:
            return False


class SistemaTecnico:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Servicio Técnico")
        self.root.geometry("400x500")
        
        self.style = Style(theme="flatly")
        
        self.crear_ventana_login()
    
    def crear_ventana_login(self):
        # Frame principal
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill="both")
        
        # Logo (asume que tienes un archivo logo.png en el mismo directorio)
        logo = tk.PhotoImage(file="logo.png")
        logo_label = ttk.Label(frame, image=logo)
        logo_label.image = logo
        logo_label.pack(pady=(0, 20))
        
        # Usuario
        ttk.Label(frame, text="Usuario:").pack(anchor="w")
        self.usuario_entry = ttk.Entry(frame, width=30)
        self.usuario_entry.pack(fill="x", pady=(0, 10))
        
        # Contraseña
        ttk.Label(frame, text="Contraseña:").pack(anchor="w")
        self.contrasena_entry = ttk.Entry(frame, show="*", width=30)
        self.contrasena_entry.pack(fill="x", pady=(0, 20))
        
        # Botón de acceso
        ttk.Button(frame, text="Acceder", command=self.login, style="primary.TButton").pack()
    

    def login(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()
        
        # Aquí deberías verificar las credenciales con la base de datos
        # Por ahora, usaremos un ejemplo simple
        if verificar_login(usuario, contrasena):
            self.mostrar_dashboard()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
    
    def mostrar_dashboard(self):
        # Limpiar la ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill="both")
        
        # Frame del menú (izquierda)
        menu_frame = ttk.Frame(main_frame, width=200, style="secondary.TFrame")
        menu_frame.pack(side="left", fill="y")
        
        # Botones del menú
        ttk.Button(menu_frame, text="Clientes", style="primary.TButton", command=self.mostrar_clientes).pack(pady=5, padx=10, fill="x")
        ttk.Button(menu_frame, text="Equipos", style="primary.TButton", command=self.mostrar_equipos).pack(pady=5, padx=10, fill="x")
        ttk.Button(menu_frame, text="Reparaciones", style="primary.TButton", command=self.mostrar_reparaciones).pack(pady=5, padx=10, fill="x")

        
        # Frame de contenido (derecha)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(side="right", expand=True, fill="both")
        
        # Ejemplo de métricas
        ttk.Label(content_frame, text="Métricas", font=("Helvetica", 16)).pack(pady=20)
        ttk.Label(content_frame, text="Reparaciones pendientes: 5").pack()
        ttk.Label(content_frame, text="Presupuestos por aprobar: 3").pack()
        ttk.Label(content_frame, text="Ingresos del mes: $150,000").pack()


    def mostrar_clientes(self):
        # Limpiar la ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill="both")
        
        # Frame superior para botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(action_frame, text="Agregar Cliente", style="success.TButton", command=self.agregar_cliente).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Editar Cliente", style="info.TButton", command=self.editar_cliente).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Eliminar Cliente", style="danger.TButton", command=self.eliminar_cliente).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Agregar Equipo al Cliente", style="info.TButton", command=self.agregar_equipo_a_cliente).pack(side="left", padx=5)

        ttk.Button(action_frame, text="Volver al Dashboard", style="secondary.TButton", command=self.mostrar_dashboard).pack(side="right", padx=5)
        
        # Frame para la lista de clientes
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Crear Treeview
        columns = ("ID", "Nombre", "Compañía","Contacto de la compañía", "Dirección", "Ciudad/Provincia/Código Postal", "Teléfono", "Correo", "CUIT/DNI")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Definir encabezados
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(expand=True, fill="both")
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Cargar datos de clientes
        self.cargar_clientes()

    def cargar_clientes(self):
        # Limpiar datos existentes
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Conectar a la base de datos y obtener clientes
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT id, nombre, compania, compania_contacto, direccion, ciudad_provincia_codigoPostal, telefono, correo, cuit_dni FROM cliente")
                for cliente in cursor.fetchall():
                    self.tree.insert("", "end", values=cliente)
            except Error as e:
                messagebox.showerror("Error", f"No se pudieron cargar los clientes: {e}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()

    def agregar_cliente(self):
        # Crear una nueva ventana para agregar cliente
        ventana_agregar = tk.Toplevel(self.root)
        ventana_agregar.title("Agregar Cliente")
        ventana_agregar.geometry("400x450")
        
        ttk.Label(ventana_agregar, text="Nombre:").pack()
        nombre_entry = ttk.Entry(ventana_agregar)
        nombre_entry.pack()
        
        ttk.Label(ventana_agregar, text="Compañía:").pack()
        compania_entry = ttk.Entry(ventana_agregar)
        compania_entry.pack()
        
        ttk.Label(ventana_agregar, text="Contacto de la compañía:").pack()
        compania_contacto_entry = ttk.Entry(ventana_agregar)
        compania_contacto_entry.pack()
        
        ttk.Label(ventana_agregar, text="Dirección:").pack()
        direccion_entry = ttk.Entry(ventana_agregar)
        direccion_entry.pack()
        
        ttk.Label(ventana_agregar, text="Ciudad/Provincia/Código Postal:").pack()
        ciudad_provincia_codigoPostal_entry = ttk.Entry(ventana_agregar)
        ciudad_provincia_codigoPostal_entry.pack()
        
        ttk.Label(ventana_agregar, text="Teléfono:").pack()
        telefono_entry = ttk.Entry(ventana_agregar)
        telefono_entry.pack()
        
        ttk.Label(ventana_agregar, text="Correo:").pack()
        correo_entry = ttk.Entry(ventana_agregar)
        correo_entry.pack()
        
        ttk.Label(ventana_agregar, text="CUIT/DNI:").pack()
        cuit_dni_entry = ttk.Entry(ventana_agregar)
        cuit_dni_entry.pack()
        
        def guardar_cliente():
            nombre = nombre_entry.get()
            compania = compania_entry.get()
            compania_contacto = compania_contacto_entry.get()
            direccion = direccion_entry.get()
            ciudad_provincia_codigoPostal = ciudad_provincia_codigoPostal_entry.get()
            telefono = telefono_entry.get()
            correo = correo_entry.get()
            cuit_dni = cuit_dni_entry.get()
            
            conexion = conectar_db()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    query = "INSERT INTO cliente (nombre, compania, compania_contacto, direccion, ciudad_provincia_codigoPostal, telefono, correo, cuit_dni) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(query, (nombre, compania, compania_contacto, direccion, ciudad_provincia_codigoPostal, telefono, correo, cuit_dni))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Cliente agregado correctamente")
                    ventana_agregar.destroy()
                    self.cargar_clientes()
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo agregar el cliente: {e}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()
        
        ttk.Button(ventana_agregar, text="Guardar", command=guardar_cliente).pack(pady=10)

    def editar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un cliente para editar")
            return
        
        cliente = self.tree.item(seleccion[0])['values']
        
        ventana_editar = tk.Toplevel(self.root)
        ventana_editar.title("Editar Cliente")
        ventana_editar.geometry("400x450")
        
        ttk.Label(ventana_editar, text="Nombre:").pack()
        nombre_entry = ttk.Entry(ventana_editar)
        nombre_entry.insert(0, cliente[1])
        nombre_entry.pack()
        
        ttk.Label(ventana_editar, text="Compañía:").pack()
        compania_entry = ttk.Entry(ventana_editar)
        compania_entry.insert(0, cliente[2])
        compania_entry.pack()

        ttk.Label(ventana_editar, text="Contacto de la compañía:").pack()
        compania_contacto_entry = ttk.Entry(ventana_editar)
        compania_contacto_entry.insert(0, cliente[3])
        compania_contacto_entry.pack()

        ttk.Label(ventana_editar, text="Dirección:").pack()
        direccion_entry = ttk.Entry(ventana_editar)
        direccion_entry.insert(0, cliente[4])
        direccion_entry.pack()

        ttk.Label(ventana_editar, text="Ciudad/Provincia/Código Postal:").pack()
        ciudad_provincia_codigoPostal_entry = ttk.Entry(ventana_editar)
        ciudad_provincia_codigoPostal_entry.insert(0, cliente[5])
        ciudad_provincia_codigoPostal_entry.pack()

        ttk.Label(ventana_editar, text="Teléfono:").pack()
        telefono_entry = ttk.Entry(ventana_editar)
        telefono_entry.insert(0, cliente[6])
        telefono_entry.pack()
        
        ttk.Label(ventana_editar, text="Correo:").pack()
        correo_entry = ttk.Entry(ventana_editar)
        correo_entry.insert(0, cliente[7])
        correo_entry.pack()
        
        ttk.Label(ventana_editar, text="CUIT/DNI:").pack()
        cuit_dni_entry = ttk.Entry(ventana_editar)
        cuit_dni_entry.insert(0, cliente[8])
        cuit_dni_entry.pack()
        
        def actualizar_cliente():
            nombre = nombre_entry.get()
            compania = compania_entry.get()
            compania_contacto = compania_contacto_entry.get()
            direccion = direccion_entry.get()
            ciudad_provincia_codigoPostal = ciudad_provincia_codigoPostal_entry.get()
            telefono = telefono_entry.get()
            correo = correo_entry.get()
            cuit_dni = cuit_dni_entry.get()
            
            conexion = conectar_db()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    query = "UPDATE cliente SET nombre=%s, compania=%s, compania_contacto=%s, direccion=%s, ciudad_provincia_codigoPostal=%s, telefono=%s, correo=%s, cuit_dni=%s WHERE id=%s"
                    cursor.execute(query, (nombre, compania, compania_contacto, direccion, ciudad_provincia_codigoPostal, telefono, correo, cuit_dni, cliente[0]))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
                    ventana_editar.destroy()
                    self.cargar_clientes()
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo actualizar el cliente: {e}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()
        
        ttk.Button(ventana_editar, text="Actualizar", command=actualizar_cliente).pack(pady=10)

    def eliminar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un cliente para eliminar")
            return
        
        cliente = self.tree.item(seleccion[0])['values']
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de que desea eliminar al cliente {cliente[1]}?"):
            conexion = conectar_db()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    query = "DELETE FROM cliente WHERE id=%s"
                    cursor.execute(query, (cliente[0],))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                    self.cargar_clientes()
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()
    def mostrar_equipos(self):
        # Limpiar la ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill="both")
        
        # Frame superior para botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(action_frame, text="Agregar Equipo", style="success.TButton", command=self.agregar_equipo).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Editar Equipo", style="info.TButton", command=self.editar_equipo).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Eliminar Equipo", style="danger.TButton", command=self.eliminar_equipo).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Volver al Dashboard", style="secondary.TButton", command=self.mostrar_dashboard).pack(side="right", padx=5)
        
        # Frame para la lista de equipos
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Crear Treeview
        columns = ("ID", "Marca PC", "Modelo PC", "Serial PC", "Procesador", "Memoria RAM", "Disco Duro", "Datos Falla")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Definir encabezados
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(expand=True, fill="both")
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Cargar datos de equipos
        self.cargar_equipos()

    def cargar_equipos(self):
        # Limpiar datos existentes
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Conectar a la base de datos y obtener equipos
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT id, marca_pc, modelo_pc, serial_pc, procesador, memoria_ram, disco_marca, datos_falla FROM equipo")
                for equipo in cursor.fetchall():
                    self.tree.insert("", "end", values=equipo)
            except Error as e:
                messagebox.showerror("Error", f"No se pudieron cargar los equipos: {e}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()
    def agregar_equipo_a_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un cliente para agregar un equipo")
            return

        cliente = self.tree.item(seleccion[0])['values']
        self.agregar_equipo(id_cliente=cliente[0], cliente_nombre=cliente[1])

    def agregar_equipo(self, id_cliente=None, cliente_nombre=None):
        ventana_agregar = tk.Toplevel(self.root)
        ventana_agregar.title("Agregar Equipo")
        ventana_agregar.geometry("1000x500")

        # Frame principal
        main_frame = ttk.Frame(ventana_agregar)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Frame superior para selección de cliente
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(top_frame, text="Cliente:").pack(side="left")
        cliente_var = tk.StringVar()
        cliente_combobox = ttk.Combobox(top_frame, textvariable=cliente_var, state="readonly")
        cliente_combobox.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # Cargar clientes en el combobox
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT id, nombre FROM cliente")
                clientes = cursor.fetchall()
                cliente_combobox['values'] = [f"{id} - {nombre}" for id, nombre in clientes]
                if id_cliente and cliente_nombre:
                    cliente_combobox.set(f"{id_cliente} - {cliente_nombre}")
            except Error as e:
                messagebox.showerror("Error", f"No se pudieron cargar los clientes: {e}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()

        # Frame izquierdo para marca y modelo
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=(0, 5))

        ttk.Label(left_frame, text="Marca PC:").pack(anchor="w")
        marca_pc_entry = ttk.Entry(left_frame, width=30)
        marca_pc_entry.pack(fill="x", pady=(0, 10))

        ttk.Label(left_frame, text="Modelo PC:").pack(anchor="w")
        modelo_pc_entry = ttk.Entry(left_frame, width=30)
        modelo_pc_entry.pack(fill="x", pady=(0, 10))

        # Frame central para otros campos
        center_frame = ttk.Frame(main_frame)
        center_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Canvas y scrollbar para el frame central
        canvas = tk.Canvas(center_frame)
        scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        campos = [
            "Serial PC", "Procesador", "Velocidad GHz", "Serial Procesador",
            "Memoria RAM", "RAM GB", "Serial RAM", "Disco Marca", "Disco GB",
            "Serial HD", "Tarjeta Video", "Tarjeta Tipo", "Serial Tarjeta",
            "Puertos DIM", "Puertos SODIMM"
        ]

        entries = {}
        for campo in campos:
            ttk.Label(scrollable_frame, text=campo + ":").pack(anchor="w")
            entry = ttk.Entry(scrollable_frame, width=30)
            entry.pack(fill="x", pady=(0, 5))
            entries[campo] = entry

        # Frame derecho para datos de falla
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        ttk.Label(right_frame, text="Datos Falla:").pack(anchor="w")
        datos_falla_text = tk.Text(right_frame, width=30, height=20)
        datos_falla_text.pack(fill="both", expand=True)

        def guardar_equipo():
            cliente_seleccionado = cliente_var.get().split(" - ")[0]
            datos = {
                "Marca PC": marca_pc_entry.get(),
                "Modelo PC": modelo_pc_entry.get(),
                **{campo: entry.get() for campo, entry in entries.items()},
                "Datos Falla": datos_falla_text.get("1.0", tk.END).strip()
            }
            
            conexion = conectar_db()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    
                    # Insertar el equipo
                    query_equipo = """
                    INSERT INTO equipo (id_cliente, marca_pc, modelo_pc, serial_pc, procesador, velocidad_ghz,
                    serial_procesador, memoria_ram, ram_gb, serial_ram, disco_marca, disco_gb,
                    serial_hd, tarjeta_video, tarjeta_tipo, serial_tarjeta, puertos_dim,
                    puertos_sodimm, datos_falla)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query_equipo, (cliente_seleccionado,) + tuple(datos.values()))
                    
                    # Obtener el ID del equipo recién insertado
                    equipo_id = cursor.lastrowid
                    
                    # Insertar la reparación
                    query_reparacion = """
                    INSERT INTO reparaciones (id_cliente, id_equipo, fecha_ingreso, estado)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query_reparacion, (cliente_seleccionado, equipo_id, date.today(), 'Pendiente'))
                    
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Equipo agregado y reparación iniciada correctamente")
                    ventana_agregar.destroy()
                    self.cargar_equipos()
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo agregar el equipo o iniciar la reparación: {e}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()

        ttk.Button(ventana_agregar, text="Guardar", command=guardar_equipo).pack(pady=10)


    def editar_equipo(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un equipo para editar")
            return
        
        equipo_id = self.tree.item(seleccion[0])['values'][0]  # Obtenemos solo el ID del equipo
        
        # Cargar los datos del equipo desde la base de datos
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)  # Usamos dictionary=True para obtener resultados como diccionarios
                query = """
                SELECT e.*, c.nombre as nombre_cliente
                FROM equipo e
                LEFT JOIN cliente c ON e.id_cliente = c.id
                WHERE e.id = %s
                """
                cursor.execute(query, (equipo_id,))
                equipo = cursor.fetchone()
                
                if not equipo:
                    messagebox.showerror("Error", "No se pudo encontrar el equipo en la base de datos")
                    return
                
            except Error as e:
                messagebox.showerror("Error", f"No se pudo cargar la información del equipo: {e}")
                return
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()
        
        ventana_editar = tk.Toplevel(self.root)
        ventana_editar.title("Editar Equipo")
        ventana_editar.geometry("800x600")

        # Frame principal
        main_frame = ttk.Frame(ventana_editar)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Frame superior para selección de cliente
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(top_frame, text="Cliente:").pack(side="left")
        cliente_var = tk.StringVar(value=f"{equipo['id_cliente']} - {equipo['nombre_cliente']}" if equipo['id_cliente'] else "")
        cliente_combobox = ttk.Combobox(top_frame, textvariable=cliente_var, state="readonly")
        cliente_combobox.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # Cargar clientes en el combobox
        self.cargar_clientes_combobox(cliente_combobox)

        # Frame izquierdo para marca y modelo
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=(0, 5))

        ttk.Label(left_frame, text="Marca PC:").pack(anchor="w")
        marca_pc_entry = ttk.Entry(left_frame, width=30)
        marca_pc_entry.insert(0, equipo['marca_pc'])
        marca_pc_entry.pack(fill="x", pady=(0, 10))

        ttk.Label(left_frame, text="Modelo PC:").pack(anchor="w")
        modelo_pc_entry = ttk.Entry(left_frame, width=30)
        modelo_pc_entry.insert(0, equipo['modelo_pc'])
        modelo_pc_entry.pack(fill="x", pady=(0, 10))

        # Frame central para otros campos
        center_frame = ttk.Frame(main_frame)
        center_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Canvas y scrollbar para el frame central
        canvas = tk.Canvas(center_frame)
        scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        campos = [
            "serial_pc", "procesador", "velocidad_ghz", "serial_procesador",
            "memoria_ram", "ram_gb", "serial_ram", "disco_marca", "disco_gb",
            "serial_hd", "tarjeta_video", "tarjeta_tipo", "serial_tarjeta",
            "puertos_dim", "puertos_sodimm"
        ]

        entries = {}
        for campo in campos:
            ttk.Label(scrollable_frame, text=campo.replace('_', ' ').title() + ":").pack(anchor="w")
            entry = ttk.Entry(scrollable_frame, width=30)
            entry.insert(0, equipo[campo] if equipo[campo] else "")
            entry.pack(fill="x", pady=(0, 5))
            entries[campo] = entry

        # Frame derecho para datos de falla
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        ttk.Label(right_frame, text="Datos Falla:").pack(anchor="w")
        datos_falla_text = tk.Text(right_frame, width=30, height=20)
        datos_falla_text.insert("1.0", equipo['datos_falla'] if equipo['datos_falla'] else "")
        datos_falla_text.pack(fill="both", expand=True)

        def actualizar_equipo():
            cliente_seleccionado = cliente_var.get().split(" - ")[0]
            datos = {
                "id_cliente": cliente_seleccionado,
                "marca_pc": marca_pc_entry.get(),
                "modelo_pc": modelo_pc_entry.get(),
                **{campo: entry.get() for campo, entry in entries.items()},
                "datos_falla": datos_falla_text.get("1.0", tk.END).strip()
            }
            
            conexion = conectar_db()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    query = """
                    UPDATE equipo SET
                    id_cliente=%s, marca_pc=%s, modelo_pc=%s, serial_pc=%s, procesador=%s, velocidad_ghz=%s,
                    serial_procesador=%s, memoria_ram=%s, ram_gb=%s, serial_ram=%s, disco_marca=%s,
                    disco_gb=%s, serial_hd=%s, tarjeta_video=%s, tarjeta_tipo=%s, serial_tarjeta=%s,
                    puertos_dim=%s, puertos_sodimm=%s, datos_falla=%s
                    WHERE id=%s
                    """
                    cursor.execute(query, tuple(datos.values()) + (equipo_id,))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Equipo actualizado correctamente")
                    ventana_editar.destroy()
                    self.cargar_equipos()
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo actualizar el equipo: {e}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()

        ttk.Button(ventana_editar, text="Actualizar", command=actualizar_equipo).pack(pady=10)

    def cargar_clientes_combobox(self, combobox):
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT id, nombre FROM cliente")
                clientes = cursor.fetchall()
                combobox['values'] = [f"{id} - {nombre}" for id, nombre in clientes]
            except Error as e:
                messagebox.showerror("Error", f"No se pudieron cargar los clientes: {e}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()
    def eliminar_equipo(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un equipo para eliminar")
            return
        
        equipo = self.tree.item(seleccion[0])['values']
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de que desea eliminar el equipo {equipo[1]} {equipo[2]}?"):
            conexion = conectar_db()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    query = "DELETE FROM equipo WHERE id=%s"
                    cursor.execute(query, (equipo[0],))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Equipo eliminado correctamente")
                    self.cargar_equipos()
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el equipo: {e}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()

    def mostrar_reparaciones(self):
        # Limpiar la ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("1000x600")
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill="both")
        
        # Frame superior para botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(action_frame, text="Agregar Reparación", style="success.TButton", command=self.agregar_reparacion).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Editar Reparación", style="info.TButton", command=self.editar_reparacion).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Actualizar Estado", style="warning.TButton", command=self.actualizar_estado_reparacion).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Presupuestos", style="info.TButton", command=self.mostrar_presupuestos).pack(side="left", padx=5)
        
        ttk.Button(action_frame, text="Volver al Dashboard", style="secondary.TButton", command=self.mostrar_dashboard).pack(side="right", padx=5)
        
        # Frame para la lista de reparaciones
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Crear Treeview
        columns = ("ID", "Cliente", "Equipo", "Fecha Ingreso", "Estado", "Fecha Salida")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Definir encabezados
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(expand=True, fill="both", side="left")
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Cargar datos de reparaciones
        self.cargar_reparaciones()

    def cargar_reparaciones(self):
        # Limpiar datos existentes
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Conectar a la base de datos y obtener reparaciones
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = """
                SELECT r.id, c.nombre, CONCAT(e.marca_pc, ' ', e.modelo_pc), 
                       r.fecha_ingreso, r.estado, r.fecha_salida
                FROM reparaciones r
                JOIN cliente c ON r.id_cliente = c.id
                JOIN equipo e ON r.id_equipo = e.id
                """
                cursor.execute(query)
                for reparacion in cursor.fetchall():
                    self.tree.insert("", "end", values=reparacion)
            except Error as e:
                messagebox.showerror("Error", f"No se pudieron cargar las reparaciones: {e}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()

    def agregar_reparacion(self):
        ventana_agregar = tk.Toplevel(self.root)
        ventana_agregar.title("Agregar Reparación")
        ventana_agregar.geometry("400x300")

        ttk.Label(ventana_agregar, text="Cliente:").pack()
        cliente_var = tk.StringVar()
        cliente_combobox = ttk.Combobox(ventana_agregar, textvariable=cliente_var, state="readonly")
        cliente_combobox.pack()
        self.cargar_clientes_combobox(cliente_combobox)

        ttk.Label(ventana_agregar, text="Equipo:").pack()
        equipo_var = tk.StringVar()
        equipo_combobox = ttk.Combobox(ventana_agregar, textvariable=equipo_var, state="readonly")
        equipo_combobox.pack()

        def actualizar_equipos(*args):
            id_cliente = cliente_var.get().split(" - ")[0]
            self.cargar_equipos_combobox(equipo_combobox, id_cliente)

        cliente_var.trace("w", actualizar_equipos)

        ttk.Label(ventana_agregar, text="Estado:").pack()
        estado_var = tk.StringVar(value="Pendiente")
        estado_combobox = ttk.Combobox(ventana_agregar, textvariable=estado_var, values=["Pendiente", "En progreso", "Completado"], state="readonly")
        estado_combobox.pack()

        def guardar_reparacion():
            id_cliente = cliente_var.get().split(" - ")[0]
            equipo_id = equipo_var.get().split(" - ")[0]
            estado = estado_var.get()
            
            conexion = conectar_db()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    query = """
                    INSERT INTO reparaciones (id_cliente, id_equipo, fecha_ingreso, estado)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query, (id_cliente, equipo_id, date.today(), estado))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Reparación agregada correctamente")
                    ventana_agregar.destroy()
                    self.cargar_reparaciones()
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo agregar la reparación: {e}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()

        ttk.Button(ventana_agregar, text="Guardar", command=guardar_reparacion).pack(pady=10)

    def editar_reparacion(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una reparación para editar")
            return
        
        reparacion_id = self.tree.item(seleccion[0])['values'][0]
        
        # Cargar los datos de la reparación desde la base de datos
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                query = """
                SELECT r.*, c.nombre as nombre_cliente, CONCAT(e.marca_pc, ' ', e.modelo_pc) as equipo
                FROM reparaciones r
                JOIN cliente c ON r.id_cliente = c.id
                JOIN equipo e ON r.id_equipo = e.id
                WHERE r.id = %s
                """
                cursor.execute(query, (reparacion_id,))
                reparacion = cursor.fetchone()
                
                if not reparacion:
                    messagebox.showerror("Error", "No se pudo encontrar la reparación en la base de datos")
                    return
                
            except Error as e:
                messagebox.showerror("Error", f"No se pudo cargar la información de la reparación: {e}")
                return
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()
        
        ventana_editar = tk.Toplevel(self.root)
        ventana_editar.title("Editar Reparación")
        ventana_editar.geometry("400x350")

        ttk.Label(ventana_editar, text="Cliente:").pack()
        cliente_var = tk.StringVar(value=f"{reparacion['id_cliente']} - {reparacion['nombre_cliente']}")
        cliente_combobox = ttk.Combobox(ventana_editar, textvariable=cliente_var, state="readonly")
        cliente_combobox.pack()
        self.cargar_clientes_combobox(cliente_combobox)

        ttk.Label(ventana_editar, text="Equipo:").pack()
        equipo_var = tk.StringVar(value=f"{reparacion['id_equipo']} - {reparacion['equipo']}")
        equipo_combobox = ttk.Combobox(ventana_editar, textvariable=equipo_var, state="readonly")
        equipo_combobox.pack()
        self.cargar_equipos_combobox(equipo_combobox, reparacion['id_cliente'])

        ttk.Label(ventana_editar, text="Estado:").pack()
        estado_var = tk.StringVar(value=reparacion['estado'])
        estado_combobox = ttk.Combobox(ventana_editar, textvariable=estado_var, values=["Pendiente", "En progreso", "Completado"], state="readonly")
        estado_combobox.pack()

        ttk.Label(ventana_editar, text="Fecha de salida:").pack()
        fecha_salida_entry = ttk.Entry(ventana_editar)
        fecha_salida_entry.insert(0, reparacion['fecha_salida'] if reparacion['fecha_salida'] else "")
        fecha_salida_entry.pack()


        def actualizar_reparacion():
            id_cliente = cliente_var.get().split(" - ")[0]
            equipo_id = equipo_var.get().split(" - ")[0]
            estado = estado_var.get()
            fecha_salida = fecha_salida_entry.get() or None

            
            conexion = conectar_db()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    query = """
                    UPDATE reparaciones
                    SET id_cliente=%s, id_equipo=%s, estado=%s, fecha_salida=%s
                    WHERE id=%s
                    """
                    cursor.execute(query, (id_cliente, equipo_id, estado, fecha_salida, reparacion_id))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Reparación actualizada correctamente")
                    ventana_editar.destroy()
                    self.cargar_reparaciones()
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo actualizar la reparación: {e}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()

        ttk.Button(ventana_editar, text="Actualizar", command=actualizar_reparacion).pack(pady=10)

    def actualizar_estado_reparacion(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una reparación para actualizar su estado")
            return
        
        reparacion_id = self.tree.item(seleccion[0])['values'][0]
        
        ventana_estado = tk.Toplevel(self.root)
        ventana_estado.title("Actualizar Estado de Reparación")
        ventana_estado.geometry("300x150")

        ttk.Label(ventana_estado, text="Nuevo Estado:").pack()
        estado_var = tk.StringVar()
        estado_combobox = ttk.Combobox(ventana_estado, textvariable=estado_var, values=["Pendiente", "En progreso", "Completado"], state="readonly")
        estado_combobox.pack()

        def guardar_estado():
            nuevo_estado = estado_var.get()
            
            conexion = conectar_db()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    query = "UPDATE reparaciones SET estado=%s WHERE id=%s"
                    cursor.execute(query, (nuevo_estado, reparacion_id))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Estado de reparación actualizado correctamente")
                    ventana_estado.destroy()
                    self.cargar_reparaciones()
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo actualizar el estado de la reparación: {e}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()

        ttk.Button(ventana_estado, text="Guardar", command=guardar_estado).pack(pady=10)

    def cargar_equipos_combobox(self, combobox, id_cliente):
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT id, marca_pc, modelo_pc FROM equipo WHERE id_cliente = %s", (id_cliente,))
                equipos = cursor.fetchall()
                combobox['values'] = [f"{id} - {marca} {modelo}" for id, marca, modelo in equipos]
            except Error as e:
                messagebox.showerror("Error", f"No se pudieron cargar los equipos: {e}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()



    def mostrar_presupuestos(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una reparación para ver sus presupuestos")
            return
        
        reparacion_id = self.tree.item(seleccion[0])['values'][0]
        
        ventana_presupuestos = tk.Toplevel(self.root)
        ventana_presupuestos.title(f"Presupuestos para Reparación #{reparacion_id}")
        ventana_presupuestos.geometry("800x500")

        # Frame para botones y combobox
        button_frame = ttk.Frame(ventana_presupuestos)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Nuevo Presupuesto", command=lambda: self.nuevo_presupuesto(reparacion_id)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Ver Detalles", command=self.ver_detalles_presupuesto).pack(side="left", padx=5)

        # Combobox para cambiar el estado del presupuesto
        ttk.Label(button_frame, text="Estado:").pack(side="left", padx=(20, 5))
        self.estado_var = tk.StringVar()
        estados = ["Pendiente", "Aprobado", "Rechazado"]
        estado_combobox = ttk.Combobox(button_frame, textvariable=self.estado_var, values=estados, state="readonly")
        estado_combobox.pack(side="left")
        estado_combobox.bind("<<ComboboxSelected>>", self.actualizar_estado_presupuesto)

        # Treeview para presupuestos
        columns = ("ID", "Fecha", "Validez", "Estado", "Total")
        self.tree_presupuestos = ttk.Treeview(ventana_presupuestos, columns=columns, show="headings")
        
        for col in columns:
            self.tree_presupuestos.heading(col, text=col)
            self.tree_presupuestos.column(col, width=100)
        
        self.tree_presupuestos.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Vincular la selección del Treeview con la actualización del combobox
        self.tree_presupuestos.bind("<<TreeviewSelect>>", self.actualizar_combobox_estado)
        
        # Cargar presupuestos
        self.cargar_presupuestos(reparacion_id)

    def actualizar_combobox_estado(self, event):
        seleccion = self.tree_presupuestos.selection()
        if seleccion:
            estado_actual = self.tree_presupuestos.item(seleccion[0])['values'][3]
            self.estado_var.set(estado_actual)

    def actualizar_estado_presupuesto(self, event):
        seleccion = self.tree_presupuestos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un presupuesto para cambiar su estado")
            return
        
        presupuesto_id = self.tree_presupuestos.item(seleccion[0])['values'][0]
        nuevo_estado = self.estado_var.get()
        
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = "UPDATE presupuesto SET estado = %s WHERE id = %s"
                cursor.execute(query, (nuevo_estado, presupuesto_id))
                conexion.commit()
                messagebox.showinfo("Éxito", f"Estado del presupuesto actualizado a: {nuevo_estado}")
                
                # Actualizar el estado en el Treeview
                for item in self.tree_presupuestos.get_children():
                    if self.tree_presupuestos.item(item)['values'][0] == presupuesto_id:
                        valores = list(self.tree_presupuestos.item(item)['values'])
                        valores[3] = nuevo_estado
                        self.tree_presupuestos.item(item, values=valores)
                        break
                
            except Error as e:
                messagebox.showerror("Error", f"No se pudo actualizar el estado del presupuesto: {e}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()

    def cargar_presupuestos(self, reparacion_id):
        for i in self.tree_presupuestos.get_children():
            self.tree_presupuestos.delete(i)
        
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = """
                SELECT p.id, p.fecha_presupuesto, p.validez, p.estado,
                       COALESCE(SUM(d.total), 0) as total
                FROM presupuesto p
                LEFT JOIN detalle d ON p.id = d.id_presupuesto
                WHERE p.id_reparaciones = %s
                GROUP BY p.id
                """
                cursor.execute(query, (reparacion_id,))
                for presupuesto in cursor.fetchall():
                    self.tree_presupuestos.insert("", "end", values=presupuesto)
            except Error as e:
                messagebox.showerror("Error", f"No se pudieron cargar los presupuestos: {e}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()

    def nuevo_presupuesto(self, reparacion_id):
        ventana_nuevo = tk.Toplevel(self.root)
        ventana_nuevo.title("Nuevo Presupuesto")
        ventana_nuevo.geometry("300x200")

        ttk.Label(ventana_nuevo, text="Fecha:").pack()
        fecha_entry = ttk.Entry(ventana_nuevo)
        fecha_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        fecha_entry.pack()

        ttk.Label(ventana_nuevo, text="Validez (días):").pack()
        validez_entry = ttk.Entry(ventana_nuevo)
        validez_entry.pack()

        def guardar_presupuesto():
            fecha = fecha_entry.get()
            validez = validez_entry.get()
            
            conexion = conectar_db()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    query = """
                    INSERT INTO presupuesto (id_reparaciones, fecha_presupuesto, validez, estado)
                    VALUES (%s, %s, %s, 'Pendiente')
                    """
                    cursor.execute(query, (reparacion_id, fecha, validez))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Presupuesto creado correctamente")
                    ventana_nuevo.destroy()
                    self.cargar_presupuestos(reparacion_id)
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo crear el presupuesto: {e}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()

        ttk.Button(ventana_nuevo, text="Guardar", command=guardar_presupuesto).pack(pady=10)

    def ver_detalles_presupuesto(self):
        seleccion = self.tree_presupuestos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un presupuesto para ver sus detalles")
            return
        
        presupuesto_id = self.tree_presupuestos.item(seleccion[0])['values'][0]
        
        ventana_detalles = tk.Toplevel(self.root)
        ventana_detalles.title(f"Detalles del Presupuesto #{presupuesto_id}")
        ventana_detalles.geometry("800x500")

        # Frame para botones
        button_frame = ttk.Frame(ventana_detalles)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Agregar Detalle", command=lambda: self.agregar_detalle(presupuesto_id)).pack(side="left", padx=5)

        # Treeview para detalles
        columns = ("ID", "Descripción", "Unidades", "Precio", "Total")
        self.tree_detalles = ttk.Treeview(ventana_detalles, columns=columns, show="headings")
        
        for col in columns:
            self.tree_detalles.heading(col, text=col)
            self.tree_detalles.column(col, width=100)
        
        self.tree_detalles.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Cargar detalles
        self.cargar_detalles(presupuesto_id)

    def cargar_detalles(self, presupuesto_id):
        for i in self.tree_detalles.get_children():
            self.tree_detalles.delete(i)
        
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = "SELECT id, descripcion, unidades, precio, total FROM detalle WHERE id_presupuesto = %s"
                cursor.execute(query, (presupuesto_id,))
                for detalle in cursor.fetchall():
                    self.tree_detalles.insert("", "end", values=detalle)
            except Error as e:
                messagebox.showerror("Error", f"No se pudieron cargar los detalles: {e}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()

    def agregar_detalle(self, presupuesto_id):
        ventana_detalle = tk.Toplevel(self.root)
        ventana_detalle.title("Agregar Detalle")
        ventana_detalle.geometry("300x250")

        ttk.Label(ventana_detalle, text="Descripción:").pack()
        descripcion_entry = ttk.Entry(ventana_detalle)
        descripcion_entry.pack()

        ttk.Label(ventana_detalle, text="Unidades:").pack()
        unidades_entry = ttk.Entry(ventana_detalle)
        unidades_entry.pack()

        ttk.Label(ventana_detalle, text="Precio:").pack()
        precio_entry = ttk.Entry(ventana_detalle)
        precio_entry.pack()

        def guardar_detalle():
            descripcion = descripcion_entry.get()
            unidades = int(unidades_entry.get())
            precio = float(precio_entry.get())
            total = unidades * precio
            
            conexion = conectar_db()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    query = """
                    INSERT INTO detalle (id_presupuesto, descripcion, unidades, precio, total)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (presupuesto_id, descripcion, unidades, precio, total))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Detalle agregado correctamente")
                    ventana_detalle.destroy()
                    self.cargar_detalles(presupuesto_id)
                    self.actualizar_total_presupuesto(presupuesto_id)
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo agregar el detalle: {e}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()

        ttk.Button(ventana_detalle, text="Guardar", command=guardar_detalle).pack(pady=10)

    def actualizar_total_presupuesto(self, presupuesto_id):
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = "SELECT SUM(total) FROM detalle WHERE id_presupuesto = %s"
                cursor.execute(query, (presupuesto_id,))
                total = cursor.fetchone()[0] or 0
                
                # Actualizar el total en el Treeview de presupuestos
                for item in self.tree_presupuestos.get_children():
                    if self.tree_presupuestos.item(item)['values'][0] == presupuesto_id:
                        valores = list(self.tree_presupuestos.item(item)['values'])
                        valores[-1] = total
                        self.tree_presupuestos.item(item, values=valores)
                        break
                
            except Error as e:
                messagebox.showerror("Error", f"No se pudo actualizar el total del presupuesto: {e}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()



if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaTecnico(root)
    root.mainloop()
