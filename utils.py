import time

# --- Definiciones del Laberinto ---
WALL_CHAR = '#'
PATH_CHAR = ' '
START_CHAR = 'S'
END_CHAR = 'E'

# --- Para la conversión a números ---
WALL = 1
PATH = 0
START = 2
END = 3

# Mapeos para algoritmos basados en dirección indexada
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)] # N, S, W, E
DIR_TO_IDX = {(-1,0):0, (0,1):1, (1,0):2, (0,-1):3} # N, E, S, W

def parse_laberinto(laberinto_str_list):
    """Convierte el laberinto de strings a una representación numérica y encuentra S y E."""
    mapa_numerico = []
    pos_inicio = None
    pos_fin = None
    height = len(laberinto_str_list)
    width = len(laberinto_str_list[0]) if height > 0 else 0

    for r_idx, fila_str in enumerate(laberinto_str_list):
        if len(fila_str) != width:
            raise ValueError(f"Las filas deben tener la misma longitud.")
        fila_num = []
        for c_idx, char in enumerate(fila_str):
            if char == WALL_CHAR:
                fila_num.append(WALL)
            elif char == PATH_CHAR:
                fila_num.append(PATH)
            elif char == START_CHAR:
                fila_num.append(START)
                pos_inicio = (r_idx, c_idx)
            elif char == END_CHAR:
                fila_num.append(END)
                pos_fin = (r_idx, c_idx)
            else:
                fila_num.append(WALL)
        mapa_numerico.append(fila_num)

    if not pos_inicio or not pos_fin:
        raise ValueError("El laberinto debe tener un punto de inicio 'S' y fin 'E'.")
        
    return mapa_numerico, pos_inicio, pos_fin, height, width

def crear_grafo_desde_laberinto(laberinto_str_list):
    """
    Toma una lista de strings representando el laberinto en rejilla duplicada
    y la convierte en un grafo (representado como una lista de adyacencia).
    Esta es la función central que traduce el mapa en una estructura navegable.
    """
    grafo = {}
    alto = len(laberinto_str_list)
    ancho = len(laberinto_str_list[0])
    
    # Recorremos solo las posiciones de las celdas (coordenadas impares)
    for r in range(1, alto, 2):
        for c in range(1, ancho, 2):
            # La celda es un nodo válido en el grafo.
            nodo_actual = (r, c)
            grafo[nodo_actual] = []
            
            # Checar vecinos usando la lógica correcta de la rejilla duplicada
            # Arriba
            if r > 0 and laberinto_str_list[r - 1][c] != '#':
                grafo[nodo_actual].append((r - 2, c))
            # Abajo
            if r < alto - 1 and laberinto_str_list[r + 1][c] != '#':
                grafo[nodo_actual].append((r + 2, c))
            # Izquierda
            if c > 0 and laberinto_str_list[r][c - 1] != '#':
                grafo[nodo_actual].append((r, c - 2))
            # Derecha
            if c < ancho - 1 and laberinto_str_list[r][c + 1] != '#':
                grafo[nodo_actual].append((r, c + 2))
    return grafo
    
def encontrar_punto(laberinto, caracter):
    """
    Recorre la matriz del laberinto y devuelve las coordenadas (fila, col)
    del primer carácter que coincida.
    """
    for r, fila in enumerate(laberinto):
        for c, celda in enumerate(fila):
            if celda == caracter:
                return (r, c)
    return None # Devuelve None si no encuentra el carácter

def convertir_camino_a_instrucciones(camino):
    if not camino or len(camino) < 2:
        return []

    instrucciones = []
    # Orientación: 0:Arriba, 1:Derecha, 2:Abajo, 3:Izquierda
    # Asumimos que el robot empieza mirando hacia abajo (Sur)
    orientacion_actual = 2  

    for i in range(len(camino) - 1):
        actual = camino[i]
        siguiente = camino[i+1]

        dr, dc = siguiente[0] - actual[0], siguiente[1] - actual[1]

        if dr == 2: orientacion_objetivo = 2  # Abajo
        elif dr == -2: orientacion_objetivo = 0 # Arriba
        elif dc == 2: orientacion_objetivo = 1  # Derecha
        elif dc == -2: orientacion_objetivo = 3  # Izquierda
        else: continue

        diff = (orientacion_objetivo - orientacion_actual + 4) % 4
        
        if diff == 1: # 90 grados a la derecha
            instrucciones.append('R')
        elif diff == 3: # 90 grados a la izquierda
            instrucciones.append('L')
        elif diff == 2: # 180 grados
            instrucciones.append('R')
            instrucciones.append('R')
        
        instrucciones.append('F')
        orientacion_actual = orientacion_objetivo
        
    return "".join(instrucciones) # Unimos todo en un solo string

def medir_tiempo(func):
    """Decorador para medir el tiempo de ejecución de una función."""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"La función '{func.__name__}' tardó {end_time - start_time:.6f} segundos.")
        return result
    return wrapper