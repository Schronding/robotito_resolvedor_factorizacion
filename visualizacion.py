import matplotlib.pyplot as plt
import numpy as np

def visualizar_resultados(laberinto_str, resultados, inicio, fin):
    """
    Genera y guarda visualizaciones de los caminos encontrados.
    """
    if not resultados:
        print("No hay resultados para visualizar.")
        return

    # --- 1. Preparar la base del laberinto ---
    alto = len(laberinto_str)
    ancho = len(laberinto_str[0])
    grid_numerico = np.zeros((alto, ancho))
    for r in range(alto):
        for c in range(ancho):
            if laberinto_str[r][c] == '#':
                grid_numerico[r, c] = 0
            else:
                grid_numerico[r, c] = 1

    # --- 2. Identificar el camino óptimo (por costo) ---
    caminos_validos = {nombre: data for nombre, data in resultados.items() if data.get("camino")}
    if not caminos_validos:
        print("No se encontraron caminos válidos para visualizar.")
        return
    
    mejor_nombre_por_costo = min(caminos_validos, key=lambda k: caminos_validos[k]['costo'])
    camino_optimo = caminos_validos[mejor_nombre_por_costo]['camino']
    print(f"\nVisualización: El camino de menor costo es el de '{mejor_nombre_por_costo}'.")

    # --- 3. GENERAR GRÁFICO COMBINADO (CON LEYENDA SIMPLE) ---
    print("Generando gráfico combinado de caminos...")
    fig_comb, ax_comb = plt.subplots(figsize=(12, 6))
    fig_comb.subplots_adjust(right=0.75)
    
    ax_comb.imshow(grid_numerico, cmap='gray_r', origin='upper')

    colores = ['green', 'purple', 'blue', 'orange', 'cyan', 'magenta']
    color_idx = 0
    
    for nombre, data in caminos_validos.items():
        camino = data['camino']
        y_coords, x_coords = zip(*camino)
        
        if nombre == mejor_nombre_por_costo:
            continue
        else:
            ax_comb.plot(x_coords, y_coords, linestyle='-', color=colores[color_idx % len(colores)], label=nombre)
            color_idx += 1

    y_opt, x_opt = zip(*camino_optimo)
    label_optimo = f"{mejor_nombre_por_costo} (Óptimo)"
    ax_comb.plot(x_opt, y_opt, linestyle='-', color='red', linewidth=3, label=label_optimo, zorder=10)

    ax_comb.plot(inicio[1], inicio[0], 'p', markersize=12, color='lime', label='Inicio', zorder=11)
    ax_comb.plot(fin[1], fin[0], '*', markersize=15, color='gold', label='Fin', zorder=11)

    ax_comb.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    ax_comb.set_title('Comparación de Caminos Finales')
    ax_comb.set_xticks([])
    ax_comb.set_yticks([])
    
    nombre_archivo_combinado = 'comparacion_caminos.png'
    plt.savefig(nombre_archivo_combinado)
    print(f"- Gráfico combinado guardado en '{nombre_archivo_combinado}'")
    plt.close(fig_comb)

    # --- 4. GENERAR GRÁFICOS INDIVIDUALES  ---
    print("\nGenerando gráficos individuales...")
    for nombre, data in resultados.items():
        camino = data.get("camino")
        visitados = data.get("visitados", set())

        fig_ind, ax_ind = plt.subplots(figsize=(10, 5))
        ax_ind.imshow(grid_numerico, cmap='gray_r', origin='upper')

        if visitados:
            try:
                y_visitados, x_visitados = zip(*visitados)
                ax_ind.scatter(x_visitados, y_visitados, s=15, color='gray', alpha=0.3, label='Nodos Explorados')
            except ValueError:
                pass

        if camino:
            y_camino, x_camino = zip(*camino)
            ax_ind.plot(x_camino, y_camino, marker='o', markersize=3, linestyle='-', color='cyan', label='Camino Final')
        
        ax_ind.plot(inicio[1], inicio[0], 'p', markersize=12, color='lime', label='Inicio')
        ax_ind.plot(fin[1], fin[0], '*', markersize=15, color='gold', label='Fin')

        pasos = data.get("pasos", 0)
        costo = data.get("costo", float('inf'))
        
        titulo = f'"{nombre}" | Pasos: {pasos - 1 if pasos > 0 else 0} | Costo: {costo:.2f} | Nodos Explorados: {len(visitados)}'
        if not camino:
            titulo = f'"{nombre}" | No encontró camino | Nodos Explorados: {len(visitados)}'

        ax_ind.set_title(titulo)
        ax_ind.set_xticks([])
        ax_ind.set_yticks([])
        ax_ind.legend(loc='upper right')
        plt.tight_layout()

        nombre_archivo_ind = f'exploracion_{nombre.replace(" ", "_").replace("(", "").replace(")", "").lower()}.png'
        plt.savefig(nombre_archivo_ind)
        print(f"- Gráfico de {nombre} guardado en '{nombre_archivo_ind}'")
        plt.close(fig_ind)