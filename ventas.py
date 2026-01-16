import sqlite3
import numpy as np

# Conexión a la base de datos (se crea automáticamente si no existe)
conexion = sqlite3.connect("ventas.db")

# Crear la tabla si no existe
conexion.execute('''
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto TEXT NOT NULL,
    precio REAL NOT NULL,
    cantidad INTEGER NOT NULL
)
''')
conexion.commit()

# ---------------- FUNCIONES ---------------- #

def registrar_venta():
    nombre = input("Ingrese el nombre del producto: ").strip()
    while nombre == "":
        print("El nombre no puede estar vacío.")
        nombre = input("Ingrese el nombre del producto: ").strip()

    precio = input("Ingrese el precio del producto: ").strip()
    while not precio.replace(".", "").isnumeric():
        print("El precio debe ser un número.")
        precio = input("Ingrese el precio del producto: ").strip()
    precio = float(precio)

    cantidad = input("Ingrese la cantidad vendida: ").strip()
    while not cantidad.isnumeric():
        print("La cantidad debe ser un número entero.")
        cantidad = input("Ingrese la cantidad vendida: ").strip()
    cantidad = int(cantidad)

    conexion.execute("INSERT INTO ventas (producto, precio, cantidad) VALUES (?, ?, ?)",
                     (nombre, precio, cantidad))
    conexion.commit()
    print(" Venta registrada con éxito.")


def mostrar_ventas():
    cursor = conexion.execute("SELECT * FROM ventas")
    ventas = cursor.fetchall()

    if not ventas:
        print("No hay ventas registradas.")
    else:
        print("\n--- LISTA DE VENTAS ---")
        for v in ventas:
            print(f"ID {v[0]} | Producto: {v[1]}, Precio: {v[2]}, Cantidad: {v[3]}")


def estadisticas():
    cursor = conexion.execute("SELECT precio, cantidad, producto FROM ventas")
    datos = cursor.fetchall()

    if not datos:
        print("No hay ventas registradas.")
        return

    precios = np.array([fila[0] for fila in datos])
    cantidades = np.array([fila[1] for fila in datos])
    productos = [fila[2] for fila in datos]

    total_ventas = np.sum(precios * cantidades)
    idx_max = np.argmax(cantidades)
    producto_top = productos[idx_max]

    print("\n--- ESTADÍSTICAS ---")
    print(f"Total de ventas: {total_ventas:.2f}")
    print(f"Producto más vendido: {producto_top}")
    print(f"Promedio de precios: {np.mean(precios):.2f}")


def buscar_producto():
    nombre = input("Ingrese el nombre del producto a buscar: ").strip().lower()
    cursor = conexion.execute("SELECT * FROM ventas WHERE LOWER(producto) = ?", (nombre,))
    resultados = cursor.fetchall()

    if resultados:
        print("\n--- RESULTADOS ---")
        for v in resultados:
            print(f"ID {v[0]} | Producto: {v[1]}, Precio: {v[2]}, Cantidad: {v[3]}")
    else:
        print("No se encontró el producto.")


def borrar_venta():
    mostrar_ventas()
    try:
        id_venta = int(input("Ingrese el ID de la venta a borrar: "))
        conexion.execute("DELETE FROM ventas WHERE id = ?", (id_venta,))
        conexion.commit()
        print(" Venta eliminada con éxito.")
    except ValueError:
        print("Entrada inválida.")


def borrar_todas_las_ventas():
    confirmacion = input("¿Estás seguro de que quieres borrar TODAS las ventas? (s/n): ").strip().lower()
    if confirmacion == "s":
        conexion.execute("DELETE FROM ventas")
        conexion.commit()
        print("Todas las ventas han sido eliminadas.")
    else:
        print("Operación cancelada.")


# ---------------- PROGRAMA PRINCIPAL ---------------- #
def menu():
    while True:
        print("\n✨ Dulce Hogar Tienda ✨")
        print("\n - REGISTRO DE VENTAS -")
        print("1. Registrar venta")
        print("2. Mostrar ventas")
        print("3. Estadísticas")
        print("4. Buscar producto")
        print("5. Borrar venta")
        print("6. Borrar TODAS las ventas")
        print("7. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_venta()
        elif opcion == "2":
            mostrar_ventas()
        elif opcion == "3":
            estadisticas()
        elif opcion == "4":
            buscar_producto()
        elif opcion == "5":
            borrar_venta()
        elif opcion == "6":
            borrar_todas_las_ventas()
        elif opcion == "7":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("Opción inválida, intente de nuevo.")

    conexion.close()

# Ejecutar programa
menu()









#nada que ver 
# controllers.py
class VentasController:
    def __init__(self, ventas_repo):
        self.repo = ventas_repo

    def registrar_venta(self, producto, precio, cantidad):
        # validaciones
        self.repo.insertar(producto, precio, cantidad)

    def obtener_estadisticas(self):
        datos = self.repo.obtener_todas()
        # calcular totales con numpy o manualmente
        return datos




