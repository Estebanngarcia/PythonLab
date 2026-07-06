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
    """Módulo para controlar y procesar el ingreso de un vehículo."""
    # Usamos 'global' para poder modificar las variables que creamos arriba del todo
    global lugares_ocupados, total_vehiculos_atendidos, vehiculos_activos

    print("\n--- REGISTRO DE INGRESO ---")
    
    # CONTROL 1: ¿Hay espacio disponible?
    if lugares_ocupados >= CAPACIDAD_MAXIMA:
        print("[ERROR] Estacionamiento COMPLETAMENTE LLENO. No se permiten más ingresos.")
        return  # Corta la función acá mismo y vuelve al menú

    # ENTRADA DE DATOS
    entrada = input("Ingrese la patente del vehículo: ")
    patente = validar_patente(entrada)

    # CONTROL 2: ¿La patente es válida?
    if patente is None:
        print("[ERROR] Formato de patente inválido. Debe tener entre 6 y 9 caracteres.")
        return

    # CONTROL 3: ¿El auto ya está adentro?
    if patente in vehiculos_activos:
        print(f"[ERROR] El vehículo {patente} YA SE ENCUENTRA dentro del estacionamiento.")
        return

    # PROCESAMIENTO EXITOSO
    # Guardamos la patente en el diccionario. Ponemos "8" simulando que entró a las 8 hs.
    vehiculos_activos[patente] = 8  
    
    # Actualizamos los contadores
    lugares_ocupados += 1           # Suma 1 a los que están adentro ahora
    total_vehiculos_atendidos += 1  # Suma 1 al historial del día
    
    print(f"[ÉXITO] Vehículo {patente} ingresado correctamente.")

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
            print("\n Egreso y cálculo de importe.")
        elif opcion == "3":
            print("\n Listar las patentes que están adentro.")
        elif opcion == "4":
            print("\n Calcular el tiempo promedio y estadísticas.")
        elif opcion == "5":
            print("\nGracias por utilizar el sistema. Cerrando gestión...")
            sistema_activo = False
        else:
            # Manejo básico de error si el usuario ingresa una opción inexistente
            print("\n[ERROR] Opción inválida. Por favor, ingrese un número del 1 al 5.")


# Punto de entrada seguro en Python
if __name__ == "__main__":
    main()