import random # Para poder elegir movimientos al azar
import copy 


#Varibles constantes
GATO = 'G'
RATON = 'R'
VACIO = ' '

#--------------------------------------------------------

def crear_tablero(ancho, alto):
    tablero = []

    for _ in range(alto):
        fila_actual = []

        for _ in range(ancho):
            fila_actual.append(VACIO)
        
        tablero.append(fila_actual)

    return tablero

def colocar_personajes(tablero, pos_gato, pos_raton):
    fila_gato, col_gato = pos_gato
    fila_raton, col_raton = pos_raton

    tablero[fila_gato][col_gato] = GATO
    tablero[fila_raton][col_raton] = RATON

def imprimir_tablero(tablero):
    for fila in tablero:
        print(' | '.join(fila))
        print('---' * len(fila))

def obtener_movimientos_posibles(tablero, posicion):
    # No salir de los limites del tablero

    fila, col = posicion
    alto = len(tablero)
    ancho = len(tablero[0])
    movimientos_validos = []

    # (-1, 0) -> Arriba
    # ( 1, 0) -> Abajo
    # ( 0,-1) -> Izquierda
    # ( 0, 1) -> Derecha

    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for df, dc in direcciones:
        nueva_fila, nueva_col = fila + df, col + dc

        if 0 <= nueva_fila < alto and 0 <= nueva_col < ancho:
            movimientos_validos.append((nueva_fila, nueva_col))

    return movimientos_validos


def evaluar_estado(pos_gato, pos_raton):
    fila_gato, col_gato = pos_gato
    fila_raton, col_raton = pos_raton

    distancia = abs(fila_gato - fila_raton) + abs(col_gato - col_raton)

    return distancia 

def minimax(tablero, pos_gato, pos_raton, profundidad, es_turno_maximizador):
    #tablero: El estado actual del juego.
    #- pos_gato, pos_raton: Coordenadas actuales.
    #- profundidad: ¿Cuántos turnos hacia el futuro miramos?
    #- es_turno_maximizador: Booleano. True si es el turno del Ratón (MAX), False si es del Gato (MIN).

    if profundidad == 0 or pos_gato == pos_raton:
        return evaluar_estado(pos_gato, pos_raton)
    
    # Caso recursivo
    if es_turno_maximizador: #Turno del raton MAX
        mejor_valor = -float('inf') #Peor valor posible

        movimientos_posibles = obtener_movimientos_posibles(tablero, pos_raton)

        for nueva_pos_raton in movimientos_posibles:
            valor = minimax(tablero, pos_gato, nueva_pos_raton, profundidad - 1, False)
            mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:#Turno del gato
        peor_valor = float('inf') #Mejor valor posible

        movimientos_posibles = obtener_movimientos_posibles(tablero, pos_gato)

        for nueva_pos_gato in movimientos_posibles:
            valor = minimax(tablero, nueva_pos_gato, pos_raton, profundidad - 1, True)
            peor_valor = min(peor_valor, valor)
        return peor_valor
    
def encontrar_mejor_movimiento_raton(tablero, pos_gato, pos_raton, profundidad):
    #Esta funcion utiliza minimac para analizar cada movimiento posible

    mejor_valor = -float('inf')
    mejor_movimiento = pos_raton #Se queda quieto si es que no hay donde moverse

    movimientos_posibles = obtener_movimientos_posibles(tablero, pos_raton)

    for movimiento in movimientos_posibles:
        valor = minimax(tablero, pos_gato, movimiento, profundidad - 1, False)

        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = movimiento

    return mejor_movimiento

def encontrar_mejor_movimiento_gato(tablero, pos_gato, pos_raton, profundidad):
    #En este caso es minimizar la puntuacion

    peor_valor = float('inf') #Empezar con el valor mas alto posible
    mejor_movimiento = pos_gato

    #Movimientos que el gato puede hacer
    movimientos_posibles = obtener_movimientos_posibles(tablero, pos_gato)

    for movimiento in movimientos_posibles:
        valor = minimax(tablero, movimiento, pos_raton, profundidad - 1, True)

        if valor < peor_valor:
            peor_valor = valor
            mejor_movimiento = movimiento
    return mejor_movimiento
# -------------------------------------------------------------------------------
# COMO SE EJECUTA EL JUEGO

#Configuracion del juego
ANCHO_TABLERO = 5
ALTO_TABLERO = 5

#El gato empieza en la esquina superior izquierda 
posicion_inicial_gato = (0, 0)

#El raton empieza en la esquina inferior derecha
posicion_inicial_raton = (1, 1)

NUMERO_DE_TURNOS = 15 #Duracion de la simulacion por turnos

PROFUNDIDAD_IA = 3 #Profundidad de busqueda de Minimax

#---------------------------------------------------------------------------------

#EJECUCION DE LOGICA
print("¡Bienvenido al laberinto del Gato y el Raton!")

mi_tablero = crear_tablero(ANCHO_TABLERO, ALTO_TABLERO)

posicion_actual_gato = posicion_inicial_gato
posicion_actual_raton = posicion_inicial_raton

colocar_personajes(mi_tablero, posicion_inicial_gato, posicion_inicial_raton)

print("--- Turno 0: Estado Inicial ---")
imprimir_tablero(mi_tablero)

#----------------------------------------------------------------------------------
#BUCLE PRINCIPAL DEL JUEGO

for turno in range(1, NUMERO_DE_TURNOS + 1):
    print(f"\n--- Turno {turno} ---")

    #TURNO DEL RATON
    nueva_posicion_raton = encontrar_mejor_movimiento_raton(
        mi_tablero,
        posicion_actual_gato,
        posicion_actual_raton,
        PROFUNDIDAD_IA
    )

    if nueva_posicion_raton != posicion_actual_raton:
        mi_tablero[posicion_actual_raton[0]][posicion_actual_raton[1]] = VACIO
        mi_tablero[nueva_posicion_raton[0]][nueva_posicion_raton[1]] = RATON
        posicion_actual_raton = nueva_posicion_raton
        print(f"El Ratón huye a {posicion_actual_raton}")
    else:
        print("El Ratón decide no moverse o está atrapado.")

    if posicion_actual_gato == posicion_actual_raton:
        imprimir_tablero(mi_tablero)
        print("\n¡El Ratón cometió un error y fue atrapado!")
        break
    imprimir_tablero(mi_tablero)

    #TURNO DEL GATO

    print("El Gato esta pensando...")
    nueva_posicion_gato = encontrar_mejor_movimiento_gato(
        mi_tablero,
        posicion_actual_gato,
        posicion_actual_raton,
        PROFUNDIDAD_IA
    )

    if nueva_posicion_gato != posicion_actual_gato:
        mi_tablero[posicion_actual_gato[0]][posicion_actual_gato[1]] = VACIO
        mi_tablero[nueva_posicion_gato[0]][nueva_posicion_gato[1]] = GATO
        posicion_actual_gato = nueva_posicion_gato
        print(f'El Gato persigue a {posicion_actual_gato}')
    else:
        print("El Gato decide no moverse.")

    #Si el gato gana dp de su movimiento
    if posicion_actual_gato == posicion_actual_raton:
        imprimir_tablero(mi_tablero)
        print("\n¡El Gato ha atrapado al Ratón!")
        break

    imprimir_tablero(mi_tablero)

else:
    print(f"\n¡El tiempo se acabó! El Ratón ha escapado después de {NUMERO_DE_TURNOS} turnos.") 

