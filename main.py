# main.py
import time
import matplotlib.pyplot as plt

# Importar nuestras propias funciones modulares
from utils import parse_laberinto, convertir_camino_a_instrucciones
from algoritmos import encontrar_camino_bfs, encontrar_camino_a_estrella
from comunicacion_arduino import conectar_arduino, enviar_instrucciones, cerrar_conexion
from visualizacion import visualizar_todos_los_caminos

# Definición del laberinto a resolver
laberinto_real = [
    "###########",
    "S    #    #",
    "#### #   ##",
    "#         #",
    "#   ####  #",
    "#     #   #",
    "#     # ###",
    "#   #     #",
    "# ######  #",
    "#         #",
    "#########E#"
]

def main():
    """Función principal que orquesta todo el proceso."""
    print("--- INICIANDO RESOLVERDOR DE LABERINTOS ---")
    
    # 1. Parsear el laberinto
    lab_num, p_ini, p_fin, alto, ancho = parse_laberinto(laberinto_real)
    print(f"Laberinto parseado. Inicio: {p_ini}, Fin: {p_fin}.")

    # 2. Definir y ejecutar los algoritmos
    algoritmos_a_probar = {
        "BFS": encontrar_camino_bfs,
        "A-Star": encontrar_camino_a_estrella,
        # "DFS": encontrar_camino_dfs, # Puedes añadir más aquí
    }

    caminos_encontrados = []
    for nombre, func_algoritmo in algoritmos_a_probar.items():
        print(f"\nEjecutando algoritmo: {nombre}...")
        start_time = time.perf_counter()
        camino = func_algoritmo(lab_num, p_ini, p_fin, alto, ancho)
        end_time = time.perf_counter()
        
        if camino:
            print(f"-> {nombre} encontró un camino de {len(camino)} pasos en {end_time - start_time:.6f} segundos.")
            caminos_encontrados.append({
                "nombre": nombre,
                "longitud": len(camino),
                "coordenadas": camino,
                "instrucciones": convertir_camino_a_instrucciones(camino)
            })
        else:
            print(f"-> {nombre} no encontró un camino.")

    # 3. Analizar y ordenar los resultados
    if not caminos_encontrados:
        print("\nNingún algoritmo pudo encontrar un camino. Saliendo.")
        return

    # Ordenar por longitud (el más corto es el mejor)
    caminos_ordenados = sorted(caminos_encontrados, key=lambda x: x["longitud"])
    mejor_camino = caminos_ordenados[0]

    print("\n--- RANKING DE CAMINOS (del más corto al más largo) ---")
    for i, camino in enumerate(caminos_ordenados):
        print(f"{i}. {camino['nombre']}: {camino['longitud']} celdas, Instrucciones: {camino['instrucciones']}")

    # 4. Visualización
    print("\nGenerando visualización...")
    visualizar_todos_los_caminos(laberinto_real, caminos_ordenados, mejor_camino, alto, ancho)

    # 5. Interacción con Arduino
    puerto_serial = '/dev/ttyUSB0'  # CAMBIA ESTO a 'COM3', 'COM4', etc. en Windows
    arduino = conectar_arduino(puerto_serial)

    if arduino:
        try:
            while True:
                print("\n--- Menú de Arduino ---")
                print("Elige una opción:")
                for i, c in enumerate(caminos_ordenados):
                    print(f"  {i}: Enviar y GUARDAR ruta '{c['nombre']}'")
                print("  !E: EJECUTAR ruta guardada en Arduino")
                print("  !C: CALIBRAR robot")
                print("  s: Salir")

                opcion = input("Opción: ").lower()

                if opcion == 's':
                    break
                elif opcion in ['!e', '!c']:
                    enviar_instrucciones(arduino, opcion.upper())
                else:
                    try:
                        idx = int(opcion)
                        if 0 <= idx < len(caminos_ordenados):
                            instrucciones_a_enviar = "!S" + caminos_ordenados[idx]['instrucciones']
                            enviar_instrucciones(arduino, instrucciones_a_enviar)
                        else:
                            print("Índice fuera de rango.")
                    except ValueError:
                        print("Opción no válida.")
        finally:
            cerrar_conexion(arduino)
    
    # 6. Mostrar el gráfico al final de todo
    print("\nMostrando gráfico. Cierra la ventana para terminar el programa.")
    plt.show()


if __name__ == "__main__":
    main()