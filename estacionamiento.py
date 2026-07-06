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
    print(" Cocheras Libres: {lugares_libres} / {CAPACIDAD_MAXIMA}")
    print("-" * 40)
    print("1. Registrar Ingreso de Vehículo")
    print("2. Registrar Egreso (Cobro y Salida)")
    print("3. Ver Vehículos Estacionados")
    print("4. Ver Estadísticas del Día")
    print("5. Salir del Sistema")
    print("=" * 40)


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
            print("\n Ingreso del vehículo.")
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