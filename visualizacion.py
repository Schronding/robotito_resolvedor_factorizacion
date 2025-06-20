# visualizacion.py
import matplotlib.pyplot as plt

def visualizar_todos_los_caminos(laberinto_str, todos_los_caminos, mejor_camino, height, width):
    """
    Visualiza todos los caminos encontrados en un solo gráfico.
    Esta versión es más robusta y está diseñada para funcionar.
    """
    if not todos_los_caminos:
        print("No hay caminos para visualizar.")
        return

    fig, ax = plt.subplots(figsize=(width/1.5, height/1.5))
    ax.set_facecolor('black') # Fondo negro
    
    # Dibujar caminos y celdas transitables
    for r in range(height):
        for c in range(width):
            if laberinto_str[r][c] != '#':
                ax.add_patch(plt.Rectangle((c, r), 1, 1, color='white', fill=True))

    # Marcar inicio y fin
    if todos_los_caminos:
        start_node = todos_los_caminos[0]["coordenadas"][0]
        end_node = todos_los_caminos[0]["coordenadas"][-1]
        ax.add_patch(plt.Rectangle((start_node[1], start_node[0]), 1, 1, color='cyan', fill=True))
        ax.add_patch(plt.Rectangle((end_node[1], end_node[0]), 1, 1, color='red', fill=True))

    # Colores para los caminos (que no son el mejor)
    colores = ['blue', 'orange', 'purple', 'yellow', 'magenta']
    
    # Dibujar todos los caminos secundarios
    for i, data_camino in enumerate(todos_los_caminos):
        camino_coords = data_camino["coordenadas"]
        if tuple(camino_coords) == tuple(mejor_camino["coordenadas"]):
            continue
        
        camino_x, camino_y = zip(*[(c + 0.5, r + 0.5) for r, c in camino_coords])
        ax.plot(camino_x, camino_y, color=colores[i % len(colores)], linewidth=2, alpha=0.7, label=data_camino["nombre"])

    # Dibujar el MEJOR camino al final, más grueso y en verde brillante
    if mejor_camino:
        mejor_camino_coords = mejor_camino["coordenadas"]
        mejor_x, mejor_y = zip(*[(c + 0.5, r + 0.5) for r, c in mejor_camino_coords])
        ax.plot(mejor_x, mejor_y, color='lime', linewidth=4.5, alpha=1.0, zorder=10, label=f"★ MEJOR: {mejor_camino['nombre']}")

    ax.invert_yaxis()
    ax.set_aspect('equal', adjustable='box')
    plt.title("Análisis Comparativo de Rutas", color='white')
    plt.legend()
    plt.xticks([])
    plt.yticks([])