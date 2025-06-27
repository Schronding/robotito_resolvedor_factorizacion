import serial
import time
import sys

PUERTO_ARDUINO = '/dev/ttyUSB0'  # Puerto fijo
BAUD_RATE = 9600

def manejar_comunicacion_con_arduino(ranking_resultados):
    """
    Inicia el menú interactivo para enviar comandos al Arduino.
    """
    if not ranking_resultados:
        print("No se encontraron caminos para enviar al Arduino.")
        return

    print("\n--- MODO DE COMUNICACIÓN CON ARDUINO ---")
    print(f"Intentando conectar a Arduino en el puerto: {PUERTO_ARDUINO}")

    try:
        # Usamos 'with' para asegurar que la conexión se cierre automáticamente
        with serial.Serial(port=PUERTO_ARDUINO, baudrate=BAUD_RATE, timeout=2) as arduino:
            print(f"¡Conexión exitosa con {arduino.name}!")
            print("Esperando 2 segundos para que el Arduino se inicialice...")
            time.sleep(2)  # Pausa crítica 

            # Limpiar cualquier dato inicial en el buffer de entrada del Arduino
            while arduino.in_waiting > 0:
                linea = arduino.readline().decode('utf-8', errors='ignore').strip()
                if linea:
                    print(f"Arduino (mensaje de inicio): {linea}")

            # Bucle de menú interactivo
            while True:
                print("\n--- MENÚ DE COMANDOS DE ARDUINO ---")
                prompt_message = (
                    f"  - Ranking (0 a {len(ranking_resultados)-1}) o '!S<ranking>' (ej: !S0) -> GUARDAR y Ejecutar\n"
                    f"  - '!E' -> EJECUTAR desde EEPROM\n"
                    f"  - '!C' -> BORRAR EEPROM\n"
                    f"  - 's' -> SALIR del modo de envío\n"
                    "Ingresa tu comando: "
                )
                comando_usuario = input(prompt_message).strip()
                
                if comando_usuario.lower() == 's':
                    print("Saliendo del modo de comunicación.")
                    break

                instrucciones_a_enviar = ""

                if comando_usuario.upper() in ['!E', '!C']:
                    instrucciones_a_enviar = comando_usuario.upper()
                
                elif comando_usuario.upper().startswith("!S"):
                    try:
                        rank_str = comando_usuario[2:]
                        rank_idx = int(rank_str)
                        if 0 <= rank_idx < len(ranking_resultados):
                            nombre_algo, data = ranking_resultados[rank_idx]
                            instrucciones_a_enviar = "!S" + data['instrucciones']
                        else:
                            print(f"Error: Ranking '{rank_idx}' fuera de rango.")
                            continue
                    except (ValueError, IndexError):
                        print(f"Error: Comando '{comando_usuario}' no válido. Use formato como '!S0'.")
                        continue
                else:
                    try:
                        rank_idx = int(comando_usuario)
                        if 0 <= rank_idx < len(ranking_resultados):
                            # Por defecto, si se ingresa solo un número, se asume que se quiere guardar y ejecutar.
                            nombre_algo, data = ranking_resultados[rank_idx]
                            instrucciones_a_enviar = "!S" + data['instrucciones']
                        else:
                            print(f"Error: Ranking '{rank_idx}' fuera de rango.")
                            continue
                    except ValueError:
                        print(f"Error: Comando '{comando_usuario}' no reconocido.")
                        continue
                
                # --- Envío de la instrucción al Arduino ---
                if instrucciones_a_enviar:
                    print(f"Enviando al Arduino: \"{instrucciones_a_enviar}\"")
                    # El .ino espera un newline para terminar de leer con readStringUntil('\n')
                    arduino.write((instrucciones_a_enviar + '\n').encode('utf-8'))
                    
                    # Esperar y leer la respuesta del Arduino para confirmación
                    time.sleep(0.5) # Dar tiempo al Arduino para procesar y responder
                    while arduino.in_waiting > 0:
                        respuesta = arduino.readline().decode('utf-8', errors='ignore').strip()
                        if respuesta:
                            print(f"Arduino dice: {respuesta}")

    except serial.SerialException as e:
        print(f"*** ERROR DE CONEXIÓN ***")
        print(f"No se pudo conectar al puerto '{PUERTO_ARDUINO}'.")
        print(f"Detalle: {e}")
        print("Por favor, verifica que el Arduino esté conectado y que ningún otro programa esté usando el puerto.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")