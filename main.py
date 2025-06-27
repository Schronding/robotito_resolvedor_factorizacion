# Hola profe :D
from algoritmos import *
from utils import *
from comunicacion_arduino import *
from visualizacion import *

laberinto_real_str = [

    # A B C D E F G H I J
    "#####################", # 1 superior  - 1 absoluto
    "# # #     #     # # #", # 1 medio     - 2 absoluto
    "# # # ##### ##### # #", # 1 inferior  - 3 absoluto
    "#    S    #      E  #", # 2 medio     - 4 absoluto
    "#####   ### ### #####", # 2 inferior  - 5 absoluto
    "# #     # # # # #   #", # 3 medio     - 6 absoluto
    "# ### ### # # # # # #", # 3 inferior  - 7 absoluto
    "#               # # #", # 4 medio     - 8 absoluto
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
        "BFS": lambda lab, ini, fin: encontrar_camino_bfs(lab, ini, fin),
        "DFS": lambda lab, ini, fin: encontrar_camino_dfs(lab, ini, fin),
        "Dijkstra (Simple)": lambda lab, ini, fin: encontrar_camino_dijkstra(lab, ini, fin, costo_giro=0),
        "A* (Simple)": lambda lab, ini, fin: encontrar_camino_a_star(lab, ini, fin, costo_giro=0),
        "Dijkstra (Penaliza Giros)": lambda lab, ini, fin: encontrar_camino_dijkstra(lab, ini, fin, costo_giro=1.5),
        "A* (Penaliza Giros)": lambda lab, ini, fin: encontrar_camino_a_star(lab, ini, fin, costo_giro=1.5),
        "Flood Fill": lambda lab, ini, fin: encontrar_camino_flood_fill(lab, ini, fin),
        "Wall Follower (Right)": lambda lab, ini, fin: encontrar_camino_wall_follower_right(lab, ini, fin),
        "Wall Follower (Left)": lambda lab, ini, fin: encontrar_camino_wall_follower_left(lab, ini, fin),
    }

    resultados = {}
    for nombre, func_algoritmo in algoritmos.items():
        print(f"\nEjecutando algoritmo: {nombre}...")
        camino, visitados, costo = func_algoritmo(laberinto_real_str, inicio, fin)
        
        if camino:
            print(f"-> ¡ÉXITO! {nombre} encontró un camino de {len(camino) - 1} movimientos.")
            resultados[nombre] = {
                "camino": camino,
                "visitados": visitados,
                "pasos": len(camino),
                "costo": costo,  
                "instrucciones": convertir_camino_a_instrucciones(camino)
            }
        else:
            print(f"-> {nombre} no encontró un camino, pero exploró {len(visitados)} nodos.")

    if resultados:
        # 1. Visualizar (Llamada a la nueva función)
        print("\n--- INICIANDO FASE DE VISUALIZACIÓN ---")
        visualizar_resultados(laberinto_real_str, resultados, inicio, fin)

    # --- FASE INTERACTIVA: RANKING Y ENVÍO A ARDUINO ---
    print("\n--- RANKING DE RESULTADOS (mejor a peor según COSTO) ---")
    
    # Ordenar los resultados por el COSTO total
    ranking = sorted(resultados.items(), key=lambda item: item[1]['costo'])
    
    for i, (nombre, data) in enumerate(ranking):
        rank_num = i
        pasos = data['pasos']
        costo_total = data['costo']
        instrucciones = data['instrucciones']
        # Mostramos el costo en el ranking
        print(f" {rank_num}. Algoritmo: {nombre}")
        print(f"    Pasos: {pasos-1} | Costo Total: {costo_total:.2f} | Instrucciones: {len(instrucciones)}")
        print(f"    Instrucciones: {instrucciones}")

    # Llamada única a la función de comunicación
    manejar_comunicacion_con_arduino(ranking)
    
    print("\n--- PROYECTO FINALIZADO ---")

if __name__ == "__main__":
    main()