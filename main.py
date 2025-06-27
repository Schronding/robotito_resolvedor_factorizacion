# --- main.py ---
from algoritmos import *
from utils import convertir_camino_a_instrucciones
from comunicacion_arduino import enviar_instrucciones

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

comprobacion_laberinto = [

    # A B C D E F G H I J
    "#####################", # 1 superior  - 1 absoluto
    "#S# #     #     # # #", # 1 medio     - 2 absoluto
    "# # # ##### ##### # #", # 1 inferior  - 3 absoluto
    "#         #         #", # 2 medio     - 4 absoluto
    "##### # ### ### #####", # 2 inferior  - 5 absoluto
    "# #     # # # # #   #", # 3 medio     - 6 absoluto
    "# ### ### # # # # # #", # 3 inferior  - 7 absoluto
    "#               #E# #", # 4 medio     - 8 absoluto
    "# ### ### ##### ### #", # 4 inferior  - 9 absoluto
    "# #   #       #     #", # 5 medio    - 10 absoluto
    "#####################", # 5 inferior - 11 absoluto
]


def main():
    print(comprobacion_laberinto == laberinto_real_0)
    print("--- INICIANDO RESOLVEDOR DE LABERINTOS ---")
    laberinto = [list(fila) for fila in comprobacion_laberinto]
    
    # Coordenadas para el laberinto de la imagen
    inicio = (1, 1) # Celda A1
    fin = (7, 13)   # Celda G4 (un final alcanzable)

    # Marcamos el final en la matriz para visualización
    laberinto[fin[0]][fin[1]] = 'E'
    laberinto_str = ["".join(fila) for fila in laberinto]

    print(f"Laberinto cargado. Inicio: {inicio}, Fin: {fin}.")

    algoritmos = {
        "BFS": encontrar_camino_bfs, "DFS": encontrar_camino_dfs,
        "Dijkstra": encontrar_camino_dijkstra, "A*": encontrar_camino_a_star,
        "Flood Fill": encontrar_camino_flood_fill,
        "Wall Follower (Right)": encontrar_camino_wall_follower_right,
        "Wall Follower (Left)": encontrar_camino_wall_follower_left,
    }

    resultados = {}
    for nombre, func_algoritmo in algoritmos.items():
        print(f"\nEjecutando algoritmo: {nombre}...")
        camino = func_algoritmo(laberinto_str, inicio, fin)
        if camino:
            print(f"-> ¡ÉXITO! {nombre} encontró un camino de {len(camino)} pasos.")
            resultados[nombre] = {"camino": camino, "pasos": len(camino),
                                  "instrucciones": convertir_camino_a_instrucciones(camino)}
        else:
            print(f"-> {nombre} no encontró un camino.")

    if resultados:
        # ... (lógica de ranking y envío a Arduino) ...
        pass

if __name__ == "__main__":
    main()