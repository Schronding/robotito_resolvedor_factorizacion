# comunicacion_arduino.py
import serial
import time

def conectar_arduino(puerto, baudrate=9600):
    """Intenta conectar con el Arduino en un puerto específico."""
    try:
        arduino_conn = serial.Serial(port=puerto, baudrate=baudrate, timeout=1)
        print(f"Conectado a Arduino en {arduino_conn.name}.")
        print("Esperando 2 segundos para que Arduino se inicialice...")
        time.sleep(2)
        # Limpiar buffer de entrada
        while arduino_conn.in_waiting > 0:
            init_msg = arduino_conn.readline().decode('utf-8', errors='ignore').rstrip()
            if init_msg:
                print(f"Arduino (inicio): {init_msg}")
        return arduino_conn
    except serial.SerialException as e:
        print(f"Error al conectar con Arduino en {puerto}: {e}")
        return None

def enviar_instrucciones(arduino_serial, instrucciones_str):
    """Envía una cadena de instrucciones al Arduino y espera feedback."""
    if not arduino_serial or not arduino_serial.isOpen():
        print("La conexión serial no está abierta.")
        return

    print(f"Enviando al Arduino: {instrucciones_str}")
    arduino_serial.write((instrucciones_str + '\n').encode('utf-8'))
    
    # Tiempo de espera dinámico basado en el comando
    tiempo_de_espera_total = 5.0 # Por defecto
    if instrucciones_str.upper() == "!E":
        tiempo_de_espera_total = 20.0
    elif instrucciones_str.upper() == "!C":
        tiempo_de_espera_total = 3.0
    elif instrucciones_str.upper().startswith("!S"):
        # Un cálculo simple basado en la longitud de la instrucción
        tiempo_de_espera_total = len(instrucciones_str) * 0.5 + 4.0 # 0.5s por comando + 4s buffer

    print(f"Esperando feedback ({tiempo_de_espera_total:.1f}s)...")
    start_time = time.time()
    while time.time() - start_time < tiempo_de_espera_total:
        if arduino_serial.in_waiting > 0:
            try:
                respuesta = arduino_serial.readline().decode('utf-8', errors='ignore').rstrip()
                if respuesta:
                    print(f"Arduino: {respuesta}")
            except Exception as e:
                print(f"Error leyendo de Arduino: {e}")
        time.sleep(0.05)
    print("Lectura de feedback finalizada.")

def cerrar_conexion(arduino_serial):
    """Cierra la conexión serial si está abierta."""
    if arduino_serial and arduino_serial.isOpen():
        arduino_serial.close()
        print("Conexión serial cerrada.")