# ==========================================
# CONSTANTES CONFIGURABLES
# ==========================================
CAPACIDAD_MAXIMA = 10     # Límite fijo de cocheras en el predio
TARIFA_POR_HORA = 1200.0   # Costo por hora de permanencia

# ==========================================
# VARIABLES GLOBALES (CONTADORES Y ACUMULADORES)
# ==========================================
lugares_ocupados = 0          # Contador: Controla los autos adentro en tiempo real
total_vehiculos_atendidos = 0 # Contador: Cuántos autos ingresaron en todo el día
recaudacion_total = 0.0       # Acumulador: Suma de todo el dinero cobrado
total_horas_permanencia = 0   # Acumulador: Suma de todas las horas de los autos que salieron

# Estructura de almacenamiento dinámico (Diccionario activo)
# Guardará los datos con el formato: {"PATENTE": hora_entrada}
vehiculos_activos = {}


# ==========================================
# MÓDULOS / FUNCIONES (BOCETOS INICIALES)
# ==========================================

def mostrar_menu():
    """Muestra la interfaz visual del menú por consola."""
    print("\n" + "=" * 40)
    print("     SISTEMA DE GESTIÓN DE ESTACIONAMIENTO     ")
    print("=" * 40)
    # Mostramos los lugares libres dinámicamente en tiempo real
    lugares_libres = CAPACIDAD_MAXIMA - lugares_ocupados
    print(f" Cocheras Libres: {lugares_libres} / {CAPACIDAD_MAXIMA}")
    print("-" * 40)
    print("1. Registrar Ingreso de Vehículo")
    print("2. Registrar Egreso (Cobro y Salida)")
    print("3. Ver Vehículos Estacionados")
    print("4. Ver Estadísticas del Día")
    print("5. Salir del Sistema")
    print("=" * 40)


# ==========================================
# FUNCIONES DE VALIDACIÓN Y REGLAS DE NEGOCIO
# ==========================================

def validar_patente(patente_ingresada):
    """
    Limpia los espacios y pasa a mayúsculas la patente.
    Devuelve la patente si tiene entre 6 y 9 caracteres, o None si es inválida.
    """
    # .strip() saca espacios invisibles adelante y atrás; .upper() pasa a mayúsculas
    patente_limpia = patente_ingresada.strip().upper()
    
    # Validamos que el largo sea coherente (Patentes viejas, nuevas o del Mercosur)
    if len(patente_limpia) < 5 or len(patente_limpia) > 8:
        return None  # Significa que no es válida
        
    return patente_limpia


def registrar_ingreso():
    """Módulo para controlar y procesar el ingreso de un vehículo con su hora."""
    global lugares_ocupados, total_vehiculos_atendidos, vehiculos_activos

    print("\n--- REGISTRO DE INGRESO ---")
    
    # CONTROL 1: Espacio
    if lugares_ocupados >= CAPACIDAD_MAXIMA:
        print("[ERROR] Estacionamiento COMPLETAMENTE LLENO.")
        return

    # ENTRADA Y VALIDACIÓN DE PATENTE
    entrada_patente = input("Ingrese la patente del vehículo: ")
    patente = validar_patente(entrada_patente)

    if patente is None:
        print("[ERROR] Formato de patente inválido. Debe tener entre 6 y 9 caracteres.")
        return

    # CONTROL 2: Duplicados
    if patente in vehiculos_activos:
        print(f"[ERROR] El vehículo {patente} YA SE ENCUENTRA dentro.")
        return

    # ENTRADA Y VALIDACIÓN DE HORA (¡Lo nuevo!)
    entrada_hora = input("Ingrese la hora de ingreso (0-23): ")
    hora_ingreso = validar_hora(entrada_hora)

    if hora_ingreso is None:
        print("[ERROR] Hora inválida. Debe ser un número entero entre 0 y 23.")
        return

    # PROCESAMIENTO EXITOSO
    # Ahora guardamos la patente con su HORA REAL de entrada en el diccionario
    vehiculos_activos[patente] = hora_ingreso  
    
    lugares_ocupados += 1           
    total_vehiculos_atendidos += 1  
    
    print(f"[ÉXITO] Vehículo {patente} ingresado correctamente a las {hora_ingreso} hs.")

def calcular_importe(hora_entrada, hora_salida):
    """
    Función pura que calcula las horas de permanencia y el importe a pagar.
    Soporta el cambio de día (si sale al día siguiente).
    Devuelve una tupla: (horas_totales, importe_final)
    """
    if hora_salida >= hora_entrada:
        # Caso normal dentro del mismo día
        horas = hora_salida - hora_entrada
    else:
        # Caso donde cruzó la medianoche (ej: entra a las 23 y sale a las 2)
        horas = (24 - hora_entrada) + hora_salida
        
    # Regra de negocio: Si sale en la misma hora, se le cobra al menos 1 hora
    if horas == 0:
        horas = 1
        
    importe = horas * TARIFA_POR_HORA
    return horas, importe


def registrar_egreso():
    """Módulo encargado de gestionar la salida del vehículo, el cobro y las estadísticas."""
    global lugares_ocupados, recaudacion_total, total_horas_permanencia, vehiculos_activos

    print("\n--- REGISTRO DE EGRESO (COBRO Y SALIDA) ---")
    
    # CONTROL 1: ¿Hay autos en el estacionamiento?
    if lugares_ocupados == 0:
        print("[ERROR] No hay ningún vehículo registrado en el sistema.")
        return

    # Entrada y validación de la patente a egresar
    entrada_patente = input("Ingrese la patente del vehículo a egresar: ")
    patente = validar_patente(entrada_patente)

    if patente is None:
        print("[ERROR] Formato de patente inválido.")
        return

    # CONTROL 2: ¿El vehículo realmente está adentro?
    if patente not in vehiculos_activos:
        print(f"[ERROR] El vehículo {patente} no está registrado en este estacionamiento.")
        return

    # Entrada y validación de la hora de salida
    entrada_hora_salida = input("Ingrese la hora de salida (0-23): ")
    hora_salida = validar_hora(entrada_hora_salida)

    if hora_salida is None:
        print("[ERROR] Hora inválida. Debe ser un número entero entre 0 y 23.")
        return

    # PROCESAMIENTO MATEMÁTICO (Llamada a la función pura)
    # Recuperamos la hora de entrada que estaba guardada en el diccionario
    hora_entrada = vehiculos_activos[patente]
    
    horas_estacionado, importe_a_pagar = calcular_importe(hora_entrada, hora_salida)

    # ACTUALIZACIÓN DE VARIABLES GLOBALES (Acumuladores y Contadores)
    del vehiculos_activos[patente]       # Borramos el auto del diccionario
    lugares_ocupados -= 1                # Restamos 1 a los activos
    recaudacion_total += importe_a_pagar # Acumulador de dinero
    total_horas_permanencia += horas_estacionado # Acumulador de horas para el promedio posterior

    # SALIDA DE DATOS: Ticket de cobro para el usuario
    print("\n" + "-" * 35)
    print(f"       TICKET DE SALIDA - {patente}       ")
    print("-" * 35)
    print(f"Hora de Entrada       : {hora_entrada} hs.")
    print(f"Hora de Salida        : {hora_salida} hs.")
    print(f"Tiempo de permanencia : {horas_estacionado} hs.")
    print(f"Tarifa por hora       : ${TARIFA_POR_HORA}")
    print(f"TOTAL A PAGAR         : ${importe_a_pagar:.2f}")
    print("-" * 35)
    print("[ÉXITO] Pago registrado y coche liberado.")
    
    
def validar_hora(hora_texto):
    """Valida que la hora ingresada sea un número entero entre 0 y 23.
    Devuelve el número entero si es válido, o None si hay error."""
    
    # Manejo básico de errores por si ingresan letras en vez de números
    if not hora_texto.isdigit():
        return None
        
    hora_entera = int(hora_texto)
    
    # Estructura condicional de rango (0 a 23 horas)
    if hora_entera < 0 or hora_entera > 23:
        return None
        
    return hora_entera

def mostrar_vehiculos_estacionados():
    """Módulo que recorre el diccionario para listar los autos que están adentro."""
    print("\n--- VEHÍCULOS DENTRO DEL PREDIO ---")
    
    # CONTROL: Si el diccionario está vacío, avisamos al usuario en vez de dejar la pantalla en blanco
    if len(vehiculos_activos) == 0:
        print("No hay vehículos estacionados en este momento.")
        return

    print(f"Total de autos estacionados: {lugares_ocupados}")
    print("-" * 35)
    
    # ESTRUCTURA REPETITIVA: Recorremos las claves (patentes) y valores (horas) del diccionario
    for patente, hora in vehiculos_activos.items():
        print(f"• Patente: {patente}  |  Ingresó a las: {hora} hs.")
        
    print("-" * 35)

def calcular_tiempo_promedio():
    """
    Función pura que calcula el tiempo promedio de permanencia.
    Retorna el promedio, o 0 si todavía no salieron vehículos.
    """
    # Calculamos cuántos vehículos ya egresaron (atendidos totales menos los que siguen adentro)
    vehiculos_egresados = total_vehiculos_atendidos - lugares_ocupados
    
    # VALIDACIÓN CRÍTICA: Controlamos que ya haya salido al menos un auto para evitar división por cero
    if vehiculos_egresados == 0:
        return 0.0
        
    # Aplicamos la fórmula del promedio
    promedio = total_horas_permanencia / vehiculos_egresados
    return promedio


def mostrar_estadisticas():
    """Módulo encargado de calcular y presentar el reporte analítico en pantalla."""
    print("\n" + "*" * 40)
    print("        ESTADÍSTICAS OPERATIVAS DEL DÍA        ")
    print("*" * 40)
    
    # Cálculo del porcentaje de ocupación actual en tiempo real
    porcentaje_ocupacion = (lugares_ocupados / CAPACIDAD_MAXIMA) * 100
    
    # Llamamos a nuestra función pura para obtener el promedio de tiempo
    tiempo_promedio = calcular_tiempo_promedio()
    
    # Muestra de resultados utilizando acumuladores y contadores globales
    print(f"-> Vehículos que ingresaron hoy : {total_vehiculos_atendidos}")
    print(f"-> Ocupación actual de cocheras : {porcentaje_ocupacion:.1f}%")
    print(f"-> Tiempo promedio de estadía   : {tiempo_promedio:.1f} hs.")
    print("-" * 40)
    print(f"-> RECAUDACIÓN TOTAL ACUMULADA  : ${recaudacion_total:.2f}")
    print("*" * 40)
# ==========================================
# PROGRAMA PRINCIPAL (CONTROL DE FLUJO)
# ==========================================
def main():
    sistema_activo = True
    
    # Ciclo repetitivo controlado por bandera para mantener la consola viva
    while sistema_activo:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        # Estructura condicional para evaluar la opción elegida
        if opcion == "1":
            registrar_ingreso()
        elif opcion == "2":
            registrar_egreso()
        elif opcion == "3":
            mostrar_vehiculos_estacionados()
        elif opcion == "4":
           mostrar_estadisticas()
        elif opcion == "5":
            print("\nGracias por utilizar el sistema. Cerrando gestión...")
            sistema_activo = False
        else:
            # Manejo básico de error si el usuario ingresa una opción inexistente
            print("\n[ERROR] Opción inválida. Por favor, ingrese un número del 1 al 5.")


# Punto de entrada seguro en Python
if __name__ == "__main__":
    main()