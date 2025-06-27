# --- algoritmos.py ---
from collections import deque
import heapq

# Las constantes y la función de obtener vecinos no cambian.
START, END, WALL, PATH = 'S', 'E', '#', ' '

def _obtener_vecinos_grilla(nodo, laberinto):
    vecinos, (r, c) = [], nodo
    alto, ancho = len(laberinto), len(laberinto[0])
    if r > 0 and laberinto[r - 1][c] != WALL: vecinos.append((r - 2, c))
    if r < alto - 1 and laberinto[r + 1][c] != WALL: vecinos.append((r + 2, c))
    if c > 0 and laberinto[r][c - 1] != WALL: vecinos.append((r, c - 2))
    if c < ancho - 1 and laberinto[r][c + 1] != WALL: vecinos.append((r, c + 2))
    return vecinos

# --- Algoritmos ADAPTADOS para devolver (camino, visitados) ---

def encontrar_camino_bfs(laberinto, inicio, fin):
    cola = deque([(inicio, [inicio])])
    visitados = {inicio}
    while cola:
        nodo, camino = cola.popleft()
        if nodo == fin: return camino, visitados
        for vecino in _obtener_vecinos_grilla(nodo, laberinto):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino + [vecino]))
    return None, visitados

def encontrar_camino_dfs(laberinto, inicio, fin):
    pila = [(inicio, [inicio])]
    visitados = {inicio}
    while pila:
        nodo, camino = pila.pop()
        if nodo == fin: return camino, visitados
        for vecino in _obtener_vecinos_grilla(nodo, laberinto):
            if vecino not in visitados:
                visitados.add(vecino)
                pila.append((vecino, camino + [vecino]))
    return None, visitados

def encontrar_camino_dijkstra(laberinto, inicio, fin):
    pq = [(0, inicio, [inicio])]
    visitados = set()
    while pq:
        costo, nodo, camino = heapq.heappop(pq)
        if nodo in visitados: continue
        visitados.add(nodo)
        if nodo == fin: return camino, visitados
        for vecino in _obtener_vecinos_grilla(nodo, laberinto):
            if vecino not in visitados:
                heapq.heappush(pq, (costo + 1, vecino, camino + [vecino]))
    return None, visitados

def _heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def encontrar_camino_a_star(laberinto, inicio, fin):
    pq = [(_heuristica_manhattan(inicio, fin), 0, inicio, [inicio])]
    visitados_con_costo = {inicio: 0}
    while pq:
        _, g_cost, nodo, camino = heapq.heappop(pq)
        if nodo == fin: return camino, set(visitados_con_costo.keys())
        for vecino in _obtener_vecinos_grilla(nodo, laberinto):
            nuevo_g_cost = g_cost + 1
            if vecino not in visitados_con_costo or nuevo_g_cost < visitados_con_costo[vecino]:
                visitados_con_costo[vecino] = nuevo_g_cost
                f_cost = nuevo_g_cost + _heuristica_manhattan(vecino, fin)
                heapq.heappush(pq, (f_cost, nuevo_g_cost, vecino, camino + [vecino]))
    return None, set(visitados_con_costo.keys())

def encontrar_camino_flood_fill(laberinto, inicio, fin):
    distancias = [[-1 for _ in row] for row in laberinto]
    cola = deque([(fin, 0)])
    if distancias[fin[0]][fin[1]] == -1:
        distancias[fin[0]][fin[1]] = 0
    visitados_ff = {fin}
    while cola:
        nodo, dist = cola.popleft()
        for vecino in _obtener_vecinos_grilla(nodo, laberinto):
            if distancias[vecino[0]][vecino[1]] == -1:
                visitados_ff.add(vecino)
                distancias[vecino[0]][vecino[1]] = dist + 1
                cola.append((vecino, dist + 1))
    if distancias[inicio[0]][inicio[1]] == -1: return None, visitados_ff
    camino = [inicio]
    nodo_actual = inicio
    while nodo_actual != fin:
        found_next = False
        for vecino in _obtener_vecinos_grilla(nodo_actual, laberinto):
            if distancias[vecino[0]][vecino[1]] == distancias[nodo_actual[0]][nodo_actual[1]] - 1:
                camino.append(vecino)
                nodo_actual = vecino
                found_next = True
                break
        if not found_next: return None, visitados_ff
    return camino, visitados_ff

def _wall_follower(laberinto, inicio, fin, direccion_mano):
    dirs = [(-2, 0), (0, 2), (2, 0), (0, -2)]
    pos, orientacion = inicio, 2 
    camino = [pos]
    giro_mano = 1 if direccion_mano == 'derecha' else -1
    max_pasos = len(laberinto) * len(laberinto[0]) * 4
    for _ in range(max_pasos):
        if pos == fin: return camino, set(camino)
        orientacion_palpar = (orientacion + giro_mano + 4) % 4
        r_muro, c_muro = pos[0] + dirs[orientacion_palpar][0]//2, pos[1] + dirs[orientacion_palpar][1]//2
        muro_al_lado = laberinto[r_muro][c_muro] == WALL
        if muro_al_lado:
            r_frente, c_frente = pos[0] + dirs[orientacion][0]//2, pos[1] + dirs[orientacion][1]//2
            if laberinto[r_frente][c_frente] != WALL:
                pos = (pos[0] + dirs[orientacion][0], pos[1] + dirs[orientacion][1])
                camino.append(pos)
            else:
                orientacion = (orientacion - giro_mano + 4) % 4
        else:
            orientacion = orientacion_palpar
            pos = (pos[0] + dirs[orientacion][0], pos[1] + dirs[orientacion][1])
            camino.append(pos)
    return None, set(camino)

def encontrar_camino_wall_follower_right(laberinto, inicio, fin):
    return _wall_follower(laberinto, inicio, fin, 'derecha')

def encontrar_camino_wall_follower_left(laberinto, inicio, fin):
    return _wall_follower(laberinto, inicio, fin, 'izquierda')