import random # Para poder elegir movimientos al azar
import copy 


#Varibles constantes 
GATO = 'G'
RATON = 'R'
VACIO = ''

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
# -------------------------------------------------------------------------------
# COMO SE EJECUTA EL JUEGO

ANCHO_TABLERO = 8
ALTO_TABLERO = 8

#El gato empieza en la esquina superior izquierda 
posicion_inicial_gato = (0, 0)

#El raton empieza en la esquina inferior derecha
posicion_inicial_raton = (7, 7)

NUMERO_DE_TURNOS = 5 #Duracion de la simulacion por turnos

#EJECUCION DE LOGICA
print("¡Bienvenido al laberinto del Gato y el Raton!")

mi_tablero = crear_tablero(ANCHO_TABLERO, ALTO_TABLERO)

posicion_actual_gato = posicion_inicial_gato
posicion_actual_raton = posicion_inicial_raton

colocar_personajes(mi_tablero, posicion_inicial_gato, posicion_inicial_raton)

print("--- Turno 0: Estado Inicial ---")
imprimir_tablero(mi_tablero)

#Bucle principal del juego

for turno in range(1, NUMERO_DE_TURNOS + 1):
    print(f"\n--- Turno {turno} ---")

    #MUEVE EL RATON
    movimientos_raton = obtener_movimientos_posibles(mi_tablero, posicion_actual_raton)

    if movimientos_raton: #SI la lista de movimientos esta vacia
        #Se elige movimiento valido al azar 
        nueva_posicion_raton = random.choice(movimientos_raton)

        #Se actualiza el tablero y se borra la vieja ubicacion del raton
        fila_vieja, col_vieja = posicion_actual_raton
        mi_tablero[fila_vieja][col_vieja] = VACIO

        #Se le coloca a su nueva ubicacion
        fila_nueva, col_nueva = nueva_posicion_raton
        mi_tablero[fila_nueva][col_nueva] = RATON

        posicion_actual_raton = nueva_posicion_raton
        print(f"El ratón se mueve a {posicion_actual_raton}")
    else: 
        print("El ratón no tiene dónde moverse. ¡Está atrapado!")
    
    imprimir_tablero(mi_tablero)

