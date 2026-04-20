
default pos_x = 500
default pos_y = 500

default objeto_x = 800
default objeto_y = 500
default tiene_llave = False 
default modo_debug = True 




default dir_x = 0
default dir_y = 0
default velocidad = 5 # Píxeles que se mueve por cada "frame"


default esta_transicionando = False #<------- boolean


default nivel_actual = 1 #<-----------

define l = Character("Lolo", color="#f0f",)
define m = Character("Marcus", color="#fff",)

image fondo_laberinto ="images/fondo_laberinto.png"
# image personaje1:
#     Solid("#00FF00")
#     xsize 50 
#     ysize 50 

image personaje1 = "images/lolo.png"
image marco = "images/marcus.png"
image marco2 = "images/marcus2.png"

# Sonidos
define audio.recoger = "audio/edr-recoger.ogg"
define audio.error = "audio/u_8iuwl7zrk0-error.ogg"
define audio.victoria = "audio/u_o8xh7gwsrj-victoria.wav"

screen controles_movimiento():
    # --- CAPA DE DEBUG ---
    if modo_debug:
        frame:
            align (0.05, 0.05)
            background Solid("#00000077") 
            padding (10, 10)
            vbox:
                text "DEBUG MODE" color "#0f0" size 18
                text "X: [pos_x] | Y: [pos_y]" color "#0f0" size 20
                text "Llave: [tiene_llave]" color "#0f0" size 20

    # Personaje y elementos
    add "personaje1" xpos pos_x ypos pos_y

    # Lógica de la META (Visual)
    if not tiene_llave:
        add "marco" xpos 1200 ypos 450 
    else:
        add "marco2" xpos 1200 ypos 450 

    # --- LÓGICA DE DETECCIÓN (TIMERS) ---

    # --- DETECTORES DE META Y LLAVE (LIMPIOS) ---
    
    # 1. Detectar Llave (Solo si no está transicionando)
    if not tiene_llave and not esta_transicionando:
        add "llave.png" xpos objeto_x ypos objeto_y

        # distancia entre Lolo y la llave
        if abs(pos_x - objeto_x) < 40 and abs(pos_y - objeto_y) < 40:
            timer 0.01 action [SetVariable("tiene_llave", True), Play("sound", audio.recoger)]

    # # 2. Detectar Meta (Usando la bandera para evitar repeticiones)
    # if pos_x >= 1130 and not esta_transicionando:
    #     if tiene_llave:
    #         # Activamos la bandera para bloquear otros disparos
    #         timer 0.01 action [Call("hablar_con_guardia_verdad")]
    #     else:
    #         # Si no tiene la llave, llamamos a la puerta (no requiere bandera porque es un call)
    #         timer 0.01 action Call("hablar_con_guardia_falso")

    # 2. Detectar Meta (Usando la bandera para evitar repeticiones)
    if pos_x >= 1200 and not esta_transicionando:
        if tiene_llave:
            # Activamos la bandera para bloquear otros disparos
            timer 0.01 action [SetVariable("esta_transicionando", True), Jump("gestor_niveles")]
        else:
            # Si no tiene la llave, llamamos a la puerta (no requiere bandera porque es un call)
            timer 0.01 action Call("puerta_bloqueada")

    # Botones de dirección
    vbox:
        align (0.9, 0.9)
        spacing 10
        textbutton "↑" action SetVariable("pos_y", pos_y - 50)
        hbox:
            spacing 10
            textbutton "←" action If(pos_x > 100, SetVariable("pos_x", pos_x - 50), None)
            textbutton "→" action SetVariable("pos_x", pos_x + 50)
        textbutton "↓" action SetVariable("pos_y", pos_y + 50)

    # --- Detectores de Teclado ---
    # "K_UP" es la flecha arriba, "w" es la tecla W, etc.
    
    # key "K_UP" action SetVariable("pos_y", pos_y - 50)
    # key "K_DOWN" action SetVariable("pos_y", pos_y + 50)
    # key "K_LEFT" action If(pos_x > 100, SetVariable("pos_x", pos_x - 50), None)
    # key "K_RIGHT" action SetVariable("pos_x", pos_x + 50)

    # # También puedes añadir las teclas WASD para los que prefieren ese estilo:
    # key "w" action SetVariable("pos_y", pos_y - 50)
    # key "s" action SetVariable("pos_y", pos_y + 50)
    # key "a" action If(pos_x > 100, SetVariable("pos_x", pos_x - 50), None)
    # key "d" action SetVariable("pos_x", pos_x + 50)


    # --- DETECTORES DE TECLADO ---
    # Al presionar (keyDown), cambiamos la dirección
    key "K_UP" action SetVariable("dir_y", -1)
    key "K_DOWN" action SetVariable("dir_y", 1)
    key "K_LEFT" action SetVariable("dir_x", -1)
    key "K_RIGHT" action SetVariable("dir_x", 1)

    # Al soltar (keyUp), detenemos el movimiento
    key "keyup_K_UP" action SetVariable("dir_y", 0)
    key "keyup_K_DOWN" action SetVariable("dir_y", 0)
    key "keyup_K_LEFT" action SetVariable("dir_x", 0)
    key "keyup_K_RIGHT" action SetVariable("dir_x", 0)

    # --- EL MOTOR DE MOVIMIENTO (TIMER) ---
    # Este timer se ejecuta 60 veces por segundo (0.016 segundos aprox)
    timer 0.02 repeat True action [
        If(dir_x != 0 or dir_y != 0, [
            SetVariable("pos_x", pos_x + (dir_x * velocidad)),
            SetVariable("pos_y", pos_y + (dir_y * velocidad))
        ])
    ]

    # --- DETECTORES DE META Y LLAVE ---
    # Para movimiento fluido, es mejor usar distancias (abs)
    if not tiene_llave:
        add "llave.png" xpos objeto_x ypos objeto_y
        if abs(pos_x - objeto_x) < 40 and abs(pos_y - objeto_y) < 40:
            timer 0.01 action [SetVariable("tiene_llave", True), Play("sound", audio.recoger)]

    if pos_x >= 1200:
        if tiene_llave:
            timer 0.01 action Jump("gestor_niveles")
        else:
            timer 0.01 action Call("puerta_bloqueada")

    # Dibujamos a Lolo
    add "personaje1" xpos pos_x ypos pos_y



label start:

    # Asegurarnos de que empezamos en el nivel 1 #<-------------------------------------
    $ nivel_actual = 1 
    jump cargar_nivel


label hablar_con_guardia_falso:
    show lolo_sp at left
    show marcus_sp at right
    with dissolve

    l "Disculpe Sr. Guardia. Necesito entrar a la academia, por favor"
    m "¿Quién eres? Su llave, por favor."
    l "¿Llave?"
    m "..."
    m "Es: [tiene_llave]" #[tiene_llave] ¿False o True? (interpolación)
    m "¡Vete de aquí!" 
    hide lolo_sp
    hide marcus_sp
    with dissolve
    return

label hablar_con_guardia_verdad:
    m "Su llave, por favor."
    l "Aquí está."
    m "Puede pasar."
    return

# --- EL CEREBRO DE LOS NIVELES ---# <---------------------------------------------------
label cargar_nivel:
    # IMPORTANTE: Reiniciamos las variables de control aquí
    $ tiene_llave = False
    $ esta_transicionando = False # <--- AÑADE ESTO
    
    # Configuramos las posiciones según el nivel. if-if-if-else: gana Lolo sin jugar XD
    if nivel_actual == 1:
        scene fondo_laberinto
        $ pos_x = 500
        $ pos_y = 500
        $ objeto_x = 800
        $ objeto_y = 500
        "Nivel 1: Usa los botones para moverte. ¡Busca la llave para salir!"

    elif nivel_actual == 2:
        scene fondo_nivel_2 # Asumiendo que tienes otro fondo
        $ pos_x = 100
        $ pos_y = 300
        $ objeto_x = 900
        $ objeto_y = 100
        "Nivel 2: Las cosas se complican..."

    elif nivel_actual == 3:
        scene fondo_nivel_3 
        $ pos_x = 200
        $ pos_y = 200
        $ objeto_x = 700
        $ objeto_y = 400
        "Nivel 3: ¡El último desafío!"

    else:
        # EL SEGURO: Si el nivel es 4, 5, o cualquier otro número que no exista arriba...
        jump victoria_final

    # IMPORTANTE: Reiniciamos la llave SIEMPRE al empezar un nivel
    $ tiene_llave = False

    # Mostramos la pantalla y esperamos que el jugador interactúe
    show screen controles_movimiento
    $ ui.interact()


# --- LA TRANSICIÓN ENTRE NIVELES ---
label gestor_niveles:
    # 1. Escondemos la interfaz
    hide screen controles_movimiento
    $ dir_x = 0
    $ dir_y = 0
    play sound audio.victoria

    # Verificamos si estamos en el nivel 3 ANTES de sumar nada.
    if nivel_actual >= 3:
        jump victoria_final
    else:
        # Si no es el último, avisamos y pasamos al siguiente
        "¡Bien hecho! Nivel [nivel_actual] completado."
        $ nivel_actual += 1
        jump cargar_nivel

label victoria_final: # <--------------------------------------------------------
    "¡Felicidades! Lolo ha logrado escapar del laberinto por completo."
    return


label puerta_bloqueada:
    play sound audio.error
    "La puerta está cerrada. ¡Busca la llave primero!"
    $ pos_x -= 60  # Empujón hacia la izquierda
    $ dir_x = 0    # Detener el movimiento automático
    return   
 
 
 