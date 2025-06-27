# --- main.py ---
from algoritmos import *
from utils import *
from comunicacion_arduino import enviar_instrucciones
from visualizacion import visualizar_resultados

# Traducción final y verificada de image_ef9b64.png
laberinto_real_0 = [
    "#####################",
    "#S# # ### ### ###   #",
    "# # # # # # # # # # #",
    "# # ### # # ### # # #",
    "#   #   # #   #   # #",
    "### ####### ### ### #",
    "# # #     # #   #   #",
    "# # # ##### # ##### #",
    "#   # #   # #   #   #",
    "##### # ### ### # ###",
    "#####################"
]

laberinto_real_1 = [

    # A B C D E F G H I J
    "#####################", # 1 superior  - 1 absoluto
    "# # # $ $ # $ $ # # #", # 1 medio     - 2 absoluto
    "#$#$#$#####$#####$#$#", # 1 inferior  - 3 absoluto
    "# $ $ $ $ # $ $ $ $ #", # 2 medio     - 4 absoluto
    "#####$#$###$###$#####", # 2 inferior  - 5 absoluto
    "# # $ $ # # # # # $ #", # 3 medio     - 6 absoluto
    "#$###$###$#$#$#$#$#$#", # 3 inferior  - 7 absoluto
    "# $ $ $ $ $ $ $ # # #", # 4 medio     - 8 absoluto
    "#$###$###$#####$###$#", # 4 inferior  - 9 absoluto
    "# # $ # $ $ $ # $ $ #", # 5 medio    - 10 absoluto
    "#####################", # 5 inferior - 11 absoluto
]

laberinto_real_str = [

    # A B C D E F G H I J
    "#####################", # 1 superior  - 1 absoluto
    "#S# #     #     # # #", # 1 medio     - 2 absoluto
    "# # # ##### ##### # #", # 1 inferior  - 3 absoluto
    "#         #         #", # 2 medio     - 4 absoluto
    "#####   ### ### #####", # 2 inferior  - 5 absoluto
    "# #     # # # # #   #", # 3 medio     - 6 absoluto
    "# ### ### # # # # # #", # 3 inferior  - 7 absoluto
    "#               #E# #", # 4 medio     - 8 absoluto
    "# ### ### ##### ### #", # 4 inferior  - 9 absoluto
    "# #   #       #     #", # 5 medio    - 10 absoluto
    "#####################", # 5 inferior - 11 absoluto
]


def main():
    print("--- INICIANDO RESOLVEDOR DE LABERINTOS ---")

    inicio = encontrar_punto(laberinto_real_str, 'S')
    fin = encontrar_punto(laberinto_real_str, 'E')

    if inicio is None:
        print("ERROR: No se pudo encontrar el punto de inicio 'S' en la matriz del laberinto.")
        return
    if fin is None:
        print("ERROR: No se pudo encontrar el punto de fin 'E' en la matriz del laberinto.")
        return

    print(f"Laberinto cargado. Inicio: {inicio}, Fin: {fin}.")


    algoritmos = {
        "BFS": encontrar_camino_bfs, 
        "DFS": encontrar_camino_dfs,
        "Dijkstra": encontrar_camino_dijkstra, 
        "A*": encontrar_camino_a_star,
        "Flood Fill": encontrar_camino_flood_fill,
        "Wall Follower (Right)": encontrar_camino_wall_follower_right,
        "Wall Follower (Left)": encontrar_camino_wall_follower_left,
    }

    resultados = {}
    for nombre, func_algoritmo in algoritmos.items():
        print(f"\nEjecutando algoritmo: {nombre}...")
        camino, visitados = func_algoritmo(laberinto_real_str, inicio, fin)
        if camino:
            print(f"-> ¡ÉXITO! {nombre} encontró un camino de {len(camino)} pasos.")
            resultados[nombre] = {
                "camino": camino, 
                "visitados": visitados,
                "pasos": len(camino),
                "instrucciones": convertir_camino_a_instrucciones(camino)}
        else:
            print(f"-> {nombre} no encontró un camino, pero exploro {len(visitados)} nodos.")

    if resultados:
        # 1. Visualizar (Llamada a la nueva función)
        print("\n--- INICIANDO FASE DE VISUALIZACIÓN ---")
        visualizar_resultados(laberinto_real_str, resultados, inicio, fin)

        # La lógica de ranking y envío a Arduino puede ir después de visualizar
        mejor_opcion = resultados[min(resultados, key=lambda k: resultados[k]['pasos'])]
        print(f"\nMejor opción seleccionada: {min(resultados, key=lambda k: resultados[k]['pasos'])} con {mejor_opcion['pasos']} pasos.")
        
        # 2. Enviar a EEPROM
        instrucciones_finales = mejor_opcion['instrucciones']
        print(f"Instrucciones generadas: {instrucciones_finales}")
        print("Comunicando con Arduino para guardar en EEPROM (lógica pendiente)...")
        # enviar_instrucciones_a_arduino(instrucciones_finales)
    else:
        print("\nNo se encontró ninguna solución por ningún algoritmo.")

if __name__ == "__main__":
    main()