from collections import deque
import heapq

START, END, WALL, PATH = 'S', 'E', '#', ' '

def _obtener_vecinos_grilla(nodo, laberinto):
    vecinos, (r, c) = [], nodo
    alto, ancho = len(laberinto), len(laberinto[0])
    if r > 0 and laberinto[r - 1][c] != WALL: vecinos.append((r - 2, c))
    if r < alto - 1 and laberinto[r + 1][c] != WALL: vecinos.append((r + 2, c))
    if c > 0 and laberinto[r][c - 1] != WALL: vecinos.append((r, c - 2))
    if c < ancho - 1 and laberinto[r][c + 1] != WALL: vecinos.append((r, c + 2))
    return vecinos

def encontrar_camino_bfs(laberinto, inicio, fin):
    cola = deque([(inicio, [inicio])])
    visitados = {inicio}
    while cola:
        nodo, camino = cola.popleft()
        if nodo == fin: 
            return camino, visitados, len(camino) # Devuelve el número de pasos como costo
        for vecino in _obtener_vecinos_grilla(nodo, laberinto):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino + [vecino]))
    return None, visitados, float('inf')

def encontrar_camino_dfs(laberinto, inicio, fin):
    pila = [(inicio, [inicio])]
    visitados = {inicio}
    while pila:
        nodo, camino = pila.pop()
        if nodo == fin: 
            return camino, visitados, len(camino) # Devuelve el número de pasos como costo
        for vecino in _obtener_vecinos_grilla(nodo, laberinto):
            if vecino not in visitados:
                visitados.add(vecino)
                pila.append((vecino, camino + [vecino]))
    return None, visitados, float('inf')

def encontrar_camino_dijkstra(laberinto, inicio, fin, costo_giro=0):
    pq = [(0, inicio, [inicio], None)]
    costos_visitados = {}
    while pq:
        costo, nodo, camino, dir_previa = heapq.heappop(pq)
        if (nodo, dir_previa) in costos_visitados and costos_visitados[(nodo, dir_previa)] <= costo: continue
        costos_visitados[(nodo, dir_previa)] = costo
        if nodo == fin:
            return camino, set(n[0] for n in costos_visitados), costo # Devuelve el costo final
        for vecino in _obtener_vecinos_grilla(nodo, laberinto):
            dr, dc = vecino[0] - nodo[0], vecino[1] - nodo[1]
            if dr == 2: dir_actual = 2
            elif dr == -2: dir_actual = 0
            elif dc == 2: dir_actual = 1
            else: dir_actual = 3
            costo_movimiento = 1
            penalizacion = costo_giro if dir_previa is not None and dir_actual != dir_previa else 0
            nuevo_costo = costo + costo_movimiento + penalizacion
            heapq.heappush(pq, (nuevo_costo, vecino, camino + [vecino], dir_actual))
    return None, set(n[0] for n in costos_visitados), float('inf')

def _heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def encontrar_camino_a_star(laberinto, inicio, fin, costo_giro=0):
    pq = [(_heuristica_manhattan(inicio, fin), 0, inicio, [inicio], None)]
    costos_visitados = {}
    while pq:
        _, g_cost, nodo, camino, dir_previa = heapq.heappop(pq)
        if (nodo, dir_previa) in costos_visitados and costos_visitados[(nodo, dir_previa)] <= g_cost: continue
        costos_visitados[(nodo, dir_previa)] = g_cost
        if nodo == fin:
            return camino, set(n[0] for n in costos_visitados), g_cost # Devuelve el costo final (g_cost)
        for vecino in _obtener_vecinos_grilla(nodo, laberinto):
            dr, dc = vecino[0] - nodo[0], vecino[1] - nodo[1]
            if dr == 2: dir_actual = 2
            elif dr == -2: dir_actual = 0
            elif dc == 2: dir_actual = 1
            else: dir_actual = 3
            costo_movimiento = 1
            penalizacion = costo_giro if dir_previa is not None and dir_actual != dir_previa else 0
            nuevo_g_cost = g_cost + costo_movimiento + penalizacion
            if (vecino, dir_actual) not in costos_visitados or nuevo_g_cost < costos_visitados[(vecino, dir_actual)]:
                f_cost = nuevo_g_cost + _heuristica_manhattan(vecino, fin)
                heapq.heappush(pq, (f_cost, nuevo_g_cost, vecino, camino + [vecino], dir_actual))
    return None, set(n[0] for n in costos_visitados), float('inf')

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
        if not found_next: return None, visitados_ff, float('inf')
    return camino, visitados_ff, len(camino)

def _wall_follower(laberinto, inicio, fin, direccion_mano):
    # Direcciones: 0:Arriba(-y), 1:Derecha(+x), 2:Abajo(+y), 3:Izquierda(-x)
    dirs = [(-2, 0), (0, 2), (2, 0), (0, -2)]
    pos, orientacion = inicio, 2 
    camino = [pos]
    
    giro_mano = 1 if direccion_mano == 'derecha' else -1

    # Límite de pasos para evitar bucles infinitos en laberintos con islas
    max_pasos = len(laberinto) * len(laberinto[0]) * 2 

    for _ in range(max_pasos):
        if pos == fin:
            return camino, set(camino), len(camino)

        orientacion_palpar = (orientacion + giro_mano + 4) % 4
        
        # Chequeo de Muro adyacente
        r_muro, c_muro = pos[0] + dirs[orientacion_palpar][0]//2, pos[1] + dirs[orientacion_palpar][1]//2
        if not (0 <= r_muro < len(laberinto) and 0 <= c_muro < len(laberinto[0])):
             # Si intenta "palpar" fuera del laberinto, es un error, salimos.
             return None, set(camino), float('inf')
        
        muro_al_lado = laberinto[r_muro][c_muro] == WALL
        
        if muro_al_lado:
            # Chequeo de Muro de frente
            r_frente, c_frente = pos[0] + dirs[orientacion][0]//2, pos[1] + dirs[orientacion][1]//2
            if not (0 <= r_frente < len(laberinto) and 0 <= c_frente < len(laberinto[0])):
                return None, set(camino), float('inf') # Intenta avanzar fuera del laberinto

            if laberinto[r_frente][c_frente] != WALL:
                # Avanza
                pos = (pos[0] + dirs[orientacion][0], pos[1] + dirs[orientacion][1])
                camino.append(pos)
            else:
                # Gira sobre su eje
                orientacion = (orientacion - giro_mano + 4) % 4
        else:
            # Gira hacia el lado abierto y avanza
            orientacion = orientacion_palpar
            pos = (pos[0] + dirs[orientacion][0], pos[1] + dirs[orientacion][1])
            camino.append(pos)
            
    return None, set(camino), float('inf')

def encontrar_camino_wall_follower_right(laberinto, inicio, fin):
    return _wall_follower(laberinto, inicio, fin, 'derecha')

def encontrar_camino_wall_follower_left(laberinto, inicio, fin):
    return _wall_follower(laberinto, inicio, fin, 'izquierda')