# utils.py
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

# ... otras funciones de utils ...

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