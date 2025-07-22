import os
import sys
from datetime import datetime, timedelta

def validate_date_mapping():
    # Configuración de fechas de ejemplo (ajusta según sea necesario)
    start_date = datetime(2025, 7, 14)  # Lunes
    date_range = [start_date + timedelta(days=i) for i in range(7)]
    
    # Mapeo actual de columnas a días
    dia_a_indice = {
    0: 0,  # L -> Lunes (Monday)
    1: 1,  # M -> Martes (Tuesday)
    2: 2,  # M -> Miércoles (Wednesday) - tercera columna
    3: 3,  # J -> Jueves (Thursday)
    4: 4,  # V -> Viernes (Friday)
    5: 5,  # S -> Sábado (Saturday)
    6: 6   # D -> Domingo (Sunday)
}
    
    # Días de la semana en español
    dias_semana = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    print("="*50)
    print("VALIDACIÓN DE MAPEO DE FECHAS")
    print("="*50)
    print(f"\nFecha de inicio: {start_date.strftime('%Y-%m-%d')} ({dias_semana[start_date.weekday()]})")
    
    # Mostrar mapeo de columnas
    print("\n" + "="*50)
    print("MAPEO DE COLUMNAS A DÍAS")
    print("="*50)
    print("Columna\tDía\t\tFecha")
    print("-"*50)
    for col in sorted(dia_a_indice.keys()):
        dia_idx = dia_a_indice[col]
        if 0 <= dia_idx < len(dias_semana):
            dia_nombre = dias_semana[dia_idx]
            fecha = (start_date + timedelta(days=dia_idx)).strftime('%Y-%m-%d')
            print(f"{col}\t{dia_nombre}\t\t{fecha}")
    
    # Validar las primeras 15 filas
    print("\n" + "="*50)
    print("VALIDACIÓN DE PRIMERAS 15 FILAS")
    print("="*50)
    print("Fila\tColumna\tDía\t\tFecha\t\tEstado")
    print("-"*70)
    
    # Simulamos 15 filas del PDF (cada una con una columna diferente, repitiendo después de 7)
    for fila in range(15):
        col = fila % 7  # Ciclar a través de las 7 columnas
        dia_idx = dia_a_indice.get(col, -1)
        
        if 0 <= dia_idx < len(date_range):
            fecha = date_range[dia_idx]
            dia_nombre = dias_semana[dia_idx]
            fecha_str = fecha.strftime('%Y-%m-%d')
            
            # Verificar si el día es correcto para esta posición
            dia_esperado = dias_semana[dia_idx]
            estado = "CORRECTO" if dias_semana[fecha.weekday()] == dia_esperado else "ERROR"
            
            print(f"{fila+1:02d}\t{col}\t{dia_nombre}\t{fecha_str}\t{estado}")
        else:
            print(f"{fila+1:02d}\t{col}\t-\t-\t\tError: Índice de día inválido")
    
    # Verificación del orden de días
    print("\n" + "="*50)
    print("VERIFICACIÓN DE ORDEN DE DÍAS")
    print("="*50)
    print("Columna\tDía\t\tFecha\t\tEstado")
    print("-"*70)
    
    dias_esperados = ['Lun', 'Mar', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']
    orden_correcto = True
    
    for col in range(7):
        dia_idx = dia_a_indice.get(col, -1)
        if 0 <= dia_idx < len(date_range):
            fecha = date_range[dia_idx]
            dia_actual = dias_semana[fecha.weekday()]
            dia_esperado = dias_esperados[col] if col < len(dias_esperados) else '?'
            
            if dia_actual != dia_esperado:
                orden_correcto = False
                estado = f"ERROR: Esperado {dia_esperado}"
            else:
                estado = "CORRECTO"
                
            print(f"{col}\t{dia_actual}\t\t{fecha.strftime('%Y-%m-%d')}\t{estado}")
    
    print("\n" + "="*50)
    if orden_correcto:
        print("✓ El orden de los días es correcto")
    else:
        print("✗ Hay un problema con el orden de los días")
    print("="*50 + "\n")

if __name__ == "__main__":
    validate_date_mapping()
