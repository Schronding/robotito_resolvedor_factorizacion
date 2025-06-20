# algoritmos.py
import collections
import heapq
from utils import WALL, DIRECTIONS  # Importamos constantes y direcciones

# --- Algoritmos de Pathfinding --- 

# Cambiar el laberinto para aniadir dijsktra
def encontrar_camino_dijkstra():
    return 0

def reconstruir_camino(came_from, inicio, fin):
    """Reconstruye la lista de coordenadas del camino desde el final hasta el inicio."""
    actual = fin
    camino = []
    if fin not in came_from and fin != inicio: # Si el fin nunca fue alcanzado
        return []
    
    # Manejar el caso en que inicio y fin son el mismo
    if inicio == fin:
        return [inicio]

    while actual in came_from:
        camino.append(actual)
        if actual == inicio:
            break
        actual = came_from[actual]

    if not camino or camino[-1] != inicio:
        camino.append(inicio)

    return camino[::-1]

def encontrar_camino_seguidor_pared(laberinto_num, inicio, fin, height, width, tipo_seguidor):
    camino_actual = [inicio]
    r, c = inicio
    dir_mirada_idx = -1
    for dr_char_init in NEIGHBOR_ORDER_global: 
        dr_init, dc_init = DIRECTIONS_map[dr_char_init]
        nr_init, nc_init = r + dr_init, c + dc_init
        if 0 <= nr_init < height and 0 <= nc_init < width and laberinto_num[nr_init][nc_init] != WALL:
            dir_mirada_idx = DIR_TO_IDX[(dr_init, dc_init)]
            r, c = nr_init, nc_init
            camino_actual.append((r,c))
            break 
    if dir_mirada_idx == -1: return None
    max_pasos_simulacion = height * width * 2
    pasos_realizados = 0 
    while (r, c) != fin and pasos_realizados < max_pasos_simulacion:
        pasos_realizados += 1
        if tipo_seguidor == 'izquierda':
            idx_orden_prueba = [(dir_mirada_idx - 1 + 4) % 4, dir_mirada_idx, (dir_mirada_idx + 1) % 4, (dir_mirada_idx + 2) % 4]
        else: 
            idx_orden_prueba = [(dir_mirada_idx + 1) % 4, dir_mirada_idx, (dir_mirada_idx - 1 + 4) % 4, (dir_mirada_idx + 2) % 4]
        movimiento_efectuado_este_paso = False
        for idx_nueva_direccion_mirada in idx_orden_prueba:
            dr_new, dc_new = IDX_TO_DR_DC[idx_nueva_direccion_mirada]
            nr_new, nc_new = r + dr_new, c + dc_new
            if 0 <= nr_new < height and 0 <= nc_new < width and laberinto_num[nr_new][nc_new] != WALL:
                r, c = nr_new, nc_new
                camino_actual.append((r,c))
                dir_mirada_idx = idx_nueva_direccion_mirada
                movimiento_efectuado_este_paso = True
                break 
        if not movimiento_efectuado_este_paso: return None 
    if (r,c) == fin: return camino_actual
    else: return None

def encontrar_camino_bfs(laberinto_num, inicio, fin, height, width):
    """Encuentra el camino más corto usando Breadth-First Search."""
    queue = collections.deque([(inicio, [inicio])])
    visitado = {inicio}

    while queue:
        (r_curr, c_curr), camino_parcial = queue.popleft()

        if (r_curr, c_curr) == fin:
            return camino_parcial

        for dr, dc in DIRECTIONS:
            nr, nc = r_curr + dr, c_curr + dc
            pos_vecino = (nr, nc)

            if 0 <= nr < height and 0 <= nc < width and \
               laberinto_num[nr][nc] != WALL and pos_vecino not in visitado:
                visitado.add(pos_vecino)
                nuevo_camino = list(camino_parcial)
                nuevo_camino.append(pos_vecino)
                queue.append((pos_vecino, nuevo_camino))
    return None

def encontrar_camino_dfs(laberinto_num, inicio, fin, height, width, N_caminos_max, caminos_existentes_coords_set):
    caminos_encontrados_dfs = []
    laberinto_transitable = [list(fila) for fila in laberinto_num]
    if laberinto_transitable[inicio[0]][inicio[1]] == START: laberinto_transitable[inicio[0]][inicio[1]] = PATH
    if laberinto_transitable[fin[0]][fin[1]] == END: laberinto_transitable[fin[0]][fin[1]] = PATH
    pila = collections.deque([(inicio, [inicio])]) 
    while pila:
        (r_curr, c_curr), camino_parcial = pila.pop()
        if (r_curr, c_curr) == fin:
            camino_tuple = tuple(camino_parcial)
            if camino_tuple not in caminos_existentes_coords_set:
                caminos_encontrados_dfs.append(list(camino_parcial))
                if len(caminos_encontrados_dfs) >= N_caminos_max: return caminos_encontrados_dfs
            continue 
        for dr_char in NEIGHBOR_ORDER_global:
            dr, dc = DIRECTIONS_map[dr_char]
            nr_next, nc_next = r_curr + dr, c_curr + dc
            if 0 <= nr_next < height and 0 <= nc_next < width and \
               laberinto_transitable[nr_next][nc_next] != WALL and \
               (nr_next, nc_next) not in camino_parcial: 
                nuevo_camino_parcial = list(camino_parcial); nuevo_camino_parcial.append((nr_next, nc_next))
                pila.append(((nr_next, nc_next), nuevo_camino_parcial))
    return caminos_encontrados_dfs

def heuristica_manhattan(a, b):
    """Calcula la distancia de Manhattan."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def encontrar_camino_a_estrella(laberinto_num, inicio, fin, height, width):
    """Encuentra el camino más corto usando el algoritmo A* (A-Star)."""
    pq = [(heuristica_manhattan(inicio, fin), inicio)]
    g_score = {inicio: 0}
    came_from = {}

    while pq:
        _, pos_actual = heapq.heappop(pq)

        if pos_actual == fin:
            return reconstruir_camino(came_from, inicio, fin)

        r_curr, c_curr = pos_actual
        for dr, dc in DIRECTIONS:
            nr, nc = r_curr + dr, c_curr + dc
            pos_vecino = (nr, nc)

            if 0 <= nr < height and 0 <= nc < width and laberinto_num[nr][nc] != WALL:
                g_score_tentativo = g_score.get(pos_actual, float('inf')) + 1
                if g_score_tentativo < g_score.get(pos_vecino, float('inf')):
                    came_from[pos_vecino] = pos_actual
                    g_score[pos_vecino] = g_score_tentativo
                    f_score = g_score_tentativo + heuristica_manhattan(pos_vecino, fin)
                    heapq.heappush(pq, (f_score, pos_vecino))
    return None

def encontrar_camino_flood_fill(laberinto_num, inicio, fin, height, width):
    """
    Encuentra un camino usando una variación del algoritmo Flood Fill.
    1. Calcula la distancia desde el final hacia todas las celdas alcanzables.
    2. Traza el camino desde el inicio, siempre moviéndose a la celda con menor distancia.
    """
    # Paso 1: "Inundar" el laberinto con distancias desde el punto final.
    distancias = [[-1 for _ in range(width)] for _ in range(height)]
    queue = collections.deque([(fin, 0)])
    distancias[fin[0]][fin[1]] = 0

    while queue:
        (r_curr, c_curr), dist = queue.popleft()
        for dr, dc in DIRECTIONS:
            nr, nc = r_curr + dr, c_curr + dc
            if 0 <= nr < height and 0 <= nc < width and \
               laberinto_num[nr][nc] != WALL and distancias[nr][nc] == -1:
                distancias[nr][nc] = dist + 1
                queue.append(((nr, nc), dist + 1))
    
    # Si la celda de inicio no fue alcanzada, no hay camino.
    if distancias[inicio[0]][inicio[1]] == -1:
        return None

    # Paso 2: Trazar el camino desde el inicio hacia el final.
    camino = [inicio]
    r_actual, c_actual = inicio
    while (r_actual, c_actual) != fin:
        dist_actual = distancias[r_actual][c_actual]
        movimiento_realizado = False
        for dr, dc in DIRECTIONS:
            nr, nc = r_actual + dr, c_actual + dc
            if 0 <= nr < height and 0 <= nc < width and \
               distancias[nr][nc] == dist_actual - 1:
                r_actual, c_actual = nr, nc
                camino.append((r_actual, c_actual))
                movimiento_realizado = True
                break
        if not movimiento_realizado:
            # No debería ocurrir si el inicio fue alcanzado en el paso 1.
            return None 
            
    return camino