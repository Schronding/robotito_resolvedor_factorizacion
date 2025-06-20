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

def convertir_camino_a_instrucciones(camino_coordenadas):
    """Convierte una lista de coordenadas (r, c) a una cadena de instrucciones F, L, R."""
    if not camino_coordenadas or len(camino_coordenadas) < 2:
        return ""
        
    instrucciones = []
    # Determinar la dirección inicial
    dr_actual, dc_actual = (camino_coordenadas[1][0] - camino_coordenadas[0][0], camino_coordenadas[1][1] - camino_coordenadas[0][1])
    dir_idx_actual = DIR_TO_IDX.get((dr_actual, dc_actual))
    
    if dir_idx_actual is None:
        # Esto puede pasar si el primer movimiento no es cardinal, lo que es un error en la generación del camino.
        # Por simplicidad, asumimos una dirección inicial (ej. Este) si el robot está en 'S' y se mueve.
        # Una mejor solución es asegurar que el camino siempre sea válido.
        # Aquí, para el primer paso, asumimos que siempre es 'F'.
        # La lógica original tenía una suposición similar.
        print("Advertencia: Movimiento inicial no cardinal. La primera instrucción puede ser incorrecta.")
        dir_idx_actual = 1 # Asumir Este por defecto
    
    instrucciones.append('F') # El primer movimiento siempre es avanzar.

    for i in range(1, len(camino_coordenadas) - 1):
        dr_nuevo, dc_nuevo = (camino_coordenadas[i+1][0] - camino_coordenadas[i][0], camino_coordenadas[i+1][1] - camino_coordenadas[i][1])
        dir_idx_nuevo = DIR_TO_IDX.get((dr_nuevo, dc_nuevo))

        if dir_idx_nuevo is None:
            continue # Ignorar movimientos no válidos

        if dir_idx_nuevo == dir_idx_actual:
            instrucciones.append('F')
        elif dir_idx_nuevo == (dir_idx_actual + 1) % 4: # Giro a la derecha
            instrucciones.extend(['R', 'F'])
        elif dir_idx_nuevo == (dir_idx_actual - 1 + 4) % 4: # Giro a la izquierda
            instrucciones.extend(['L', 'F'])
        else: # Giro de 180 grados
            instrucciones.extend(['R', 'R', 'F'])
        
        dir_idx_actual = dir_idx_nuevo
        
    return "".join(instrucciones)

def medir_tiempo(func):
    """Decorador para medir el tiempo de ejecución de una función."""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"La función '{func.__name__}' tardó {end_time - start_time:.6f} segundos.")
        return result
    return wrapper