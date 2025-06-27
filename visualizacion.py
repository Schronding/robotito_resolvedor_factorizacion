# --- visualizacion.py ---
import matplotlib.pyplot as plt
import numpy as np

def visualizar_resultados(laberinto_str, resultados, inicio, fin):
    if not resultados:
        print("No hay resultados para visualizar.")
        return

    # ... (código para preparar grid_numerico se queda igual) ...
    alto = len(laberinto_str)
    ancho = len(laberinto_str[0])
    grid_numerico = np.zeros((alto, ancho))
    for r in range(alto):
        for c in range(ancho):
            if laberinto_str[r][c] == '#':
                grid_numerico[r, c] = 0
            else:
                grid_numerico[r, c] = 1

    # --- Generar gráficos individuales (Ahora con la exploración) ---
    print("Generando gráficos individuales con visualización de exploración...")
    for nombre, data in resultados.items():
        camino = data.get("camino")
        visitados = data.get("visitados", set())

        fig_ind, ax_ind = plt.subplots(figsize=(10, 5))
        ax_ind.imshow(grid_numerico, cmap='gray_r', origin='upper')

        # DIBUJAR NODOS VISITADOS (La clave)
        if visitados:
            y_visitados, x_visitados = zip(*visitados)
            ax_ind.scatter(x_visitados, y_visitados, s=15, color='gray', alpha=0.3, label='Nodos Explorados')

        # Dibujar el camino final si existe
        if camino:
            y_camino, x_camino = zip(*camino)
            ax_ind.plot(x_camino, y_camino, marker='o', markersize=3, linestyle='-', color='cyan', label='Camino Final')
        
        # Marcar inicio y fin
        ax_ind.plot(inicio[1], inicio[0], 'p', markersize=12, color='lime', label='Inicio')
        ax_ind.plot(fin[1], fin[0], '*', markersize=15, color='gold', label='Fin')

        pasos = data.get("pasos", 0)
        ax_ind.set_title(f'"{nombre}" | Pasos: {pasos} | Nodos Explorados: {len(visitados)}')
        ax_ind.set_xticks([])
        ax_ind.set_yticks([])
        ax_ind.legend()
        plt.tight_layout()

        nombre_archivo_ind = f'exploracion_{nombre.replace(" ", "_").lower()}.png'
        plt.savefig(nombre_archivo_ind)
        print(f"- Gráfico de {nombre} guardado en '{nombre_archivo_ind}'")
        plt.close(fig_ind)