import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import numpy as np

# ---------------- CONEXIÓN BASE DE DATOS ---------------- #
def conectar():
    conexion = sqlite3.connect("ventas.db")
    conexion.execute('''CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT NOT NULL,
        precio REAL NOT NULL,
        cantidad INTEGER NOT NULL
    )''')
    conexion.commit()
    return conexion

# ---------------- FUNCIONES ---------------- #
def mostrar_ventas():
    # Limpia la tabla antes de llenarla
    for fila in tabla.get_children():
        tabla.delete(fila)

    # Conecta a la base de datos
    conexion = sqlite3.connect("ventas.db")
    cursor = conexion.cursor()

    # Trae todas las ventas
    cursor.execute("SELECT * FROM ventas")
    ventas = cursor.fetchall()

    # Inserta cada venta en la tabla
    for v in ventas:
        tabla.insert("", "end", values=v)

    # Cierra la conexión
    conexion.close()

def registrar_venta():
    producto = entry_producto.get().strip()
    precio = entry_precio.get().strip()
    cantidad = entry_cantidad.get().strip()

    if not producto or not precio or not cantidad:
        messagebox.showwarning("Error", "Completa todos los campos.")
        return
    try:
        precio = float(precio)
        cantidad = int(cantidad)
    except ValueError:
        messagebox.showwarning("Error", "Precio y cantidad deben ser números.")
        return

    conexion = conectar()
    conexion.execute("INSERT INTO ventas (producto, precio, cantidad) VALUES (?, ?, ?)",
                     (producto, precio, cantidad))
    conexion.commit()
    conexion.close()

    entry_producto.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)
    mostrar_ventas()
    messagebox.showinfo("Éxito", "Venta registrada correctamente.")

def eliminar_venta():
    item = tabla.selection()
    if not item:
        messagebox.showwarning("Error", "Selecciona una venta para eliminar.")
        return
    id_venta = tabla.item(item)["values"][0]
    conexion = conectar()
    conexion.execute("DELETE FROM ventas WHERE id = ?", (id_venta,))
    conexion.commit()
    conexion.close()
    mostrar_ventas()
    messagebox.showinfo("Eliminado", "Venta eliminada correctamente.")

def mostrar_estadisticas():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT precio, cantidad, producto FROM ventas")
    datos = cursor.fetchall()
    conexion.close()

    if not datos:
        messagebox.showinfo("Estadísticas", "No hay ventas registradas.")
        return

    precios = np.array([fila[0] for fila in datos])
    cantidades = np.array([fila[1] for fila in datos])
    productos = [fila[2] for fila in datos]

    total_ventas = np.sum(precios * cantidades)
    producto_top = productos[np.argmax(cantidades)]
    promedio_precio = np.mean(precios)

    messagebox.showinfo("📊 Estadísticas", 
        f"💰 Total de ventas: ${total_ventas:.2f}\n"
        f"🏆 Producto más vendido: {producto_top}\n"
        f"📈 Promedio de precios: ${promedio_precio:.2f}"
    )

# ---------------- INTERFAZ GRÁFICA ---------------- #
ventana = tk.Tk()
ventana.title("✨ Dulce Hogar Tienda - Sistema de Ventas ✨")
ventana.geometry("700x500")
ventana.configure(bg="#800000")  # fondo rojo vino

# Título
titulo = tk.Label(ventana, text="Registro de Ventas", bg="#800000", font=("Arial", 18, "bold"), fg="white")
titulo.pack(pady=10)

# Formulario
frame_form = tk.Frame(ventana, bg="#800000")
frame_form.pack(pady=5)

tk.Label(frame_form, text="Producto:", bg="#800000", fg="white").grid(row=0, column=0, padx=5, pady=5)
entry_producto = tk.Entry(frame_form)
entry_producto.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Precio:", bg="#800000", fg="white").grid(row=1, column=0, padx=5, pady=5)
entry_precio = tk.Entry(frame_form)
entry_precio.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Cantidad:", bg="#800000", fg="white").grid(row=2, column=0, padx=5, pady=5)
entry_cantidad = tk.Entry(frame_form)
entry_cantidad.grid(row=2, column=1, padx=5, pady=5)

btn_agregar = tk.Button(frame_form, text="Registrar venta", bg="#5cb85c", fg="white", command=registrar_venta)
btn_agregar.grid(row=3, column=0, columnspan=2, pady=10)

# Tabla de ventas
tabla = ttk.Treeview(ventana, columns=("id", "producto", "precio", "cantidad"), show="headings", height=10)
tabla.heading("id", text="ID")
tabla.heading("producto", text="Producto")
tabla.heading("precio", text="Precio")
tabla.heading("cantidad", text="Cantidad")
tabla.pack(pady=10)

# Botones inferiores
frame_botones = tk.Frame(ventana, bg="#800000")
frame_botones.pack(pady=10)

btn_eliminar = tk.Button(frame_botones, text="🗑️ Eliminar venta", bg="#d9534f", fg="white", command=eliminar_venta)
btn_eliminar.grid(row=0, column=0, padx=10)

btn_estadisticas = tk.Button(frame_botones, text="📊 Ver estadísticas", bg="#0275d8", fg="white", command=mostrar_estadisticas)
btn_estadisticas.grid(row=0, column=1, padx=10)

btn_refrescar = tk.Button(frame_botones, text="🔄 Refrescar lista", bg="#f0ad4e", fg="white", command=mostrar_ventas)
btn_refrescar.grid(row=0, column=2, padx=10)

mostrar_ventas()
ventana.mainloop()











