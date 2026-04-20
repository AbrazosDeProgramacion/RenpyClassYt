## IF, ELIF, ELSE.
---
La sintaxis básica de los condicionales en Ren'Py sigue la estructura lógica de Python, utilizando if, elif y else. Es fundamental recordar que cada instrucción termina con dos puntos (:) y que el código que depende de la condición debe estar indentado (con sangría).

## Estructura Básica
---

- if: Evalúa una condición inicial.
- elif (opcional): Significa "si no, si..."; evalúa una nueva condición solo si la anterior fue falsa.
- else (opcional): Ejecuta un bloque de código si ninguna de las condiciones anteriores se cumplió.

'''renpy

if puntos >= 10:
    e "¡Felicidades! Conseguiste el mejor final."
elif puntos >= 5:
    e "Es un final decente."
else:
    e "Lo siento, este es el final malo."
'''



## Reglas Clave de Sintaxis
---

- Dos puntos (:): Obligatorios al final de cada línea de condición.
- Indentación: El contenido dentro de cada bloque debe estar alineado a la derecha (usualmente 4 espacios).
- Operadores de comparación:
    == (igual a)
    != (distinto de)
    > o < (mayor o menor que).

Variables: Puedes verificar variables booleanas directamente como if tiene_llave: (si es True) o if not tiene_llave: (si es False).

---

## Uso en Menús
---

También puedes usar condiciones para ocultar o mostrar opciones en un menú de decisiones según el estado de una variable:

'''renpy

menu:
    "Ir al parque":
        jump parque
    "Entrar a la casa" if tiene_llave:
        jump casa
'''


Para asegurar que tus variables funcionen correctamente, recuerda definirlas siempre **antes** de la etiqueta label start: usando la palabra clave default.



En Ren'Py, el uso de condicionales (if / else) va mucho más allá de simplemente cambiar un diálogo; se integran en casi todas las capas del motor para controlar la lógica del juego, la interfaz y hasta el texto individual.

Aquí tienes un desglose de todos sus usos, ubicaciones y modos de redacción:

1. En el Guion Principal (Control de Flujo)

Es el uso más común para ramificar la historia basado en variables.

**Sintaxis Estándar:** Se escribe la palabra clave, la condición y dos puntos (:).

Modo de redactar:

'''renpy

if puntos_amor >= 10:
    "Ella te sonríe cálidamente."
elif puntos_amor > 5:
    "Ella te saluda con la mano."
else:
    "Ella te ignora por completo."

'''

2. En Menús de Elección (Condiciones de Opción)

Puedes ocultar o mostrar opciones específicas dentro de un menu basándote en si se cumple una condición.

- Sintaxis: La condición if se coloca al final de la frase de la opción, justo antes de los dos puntos.

Modo de redactar:

'''renpy

menu:
    "Hablar con ella":
        jump charla
    "Usar la llave mágica" if tiene_llave: # Solo aparece si 'tiene_llave' es True
        jump secreto
'''


3. En Pantallas e Interfaz (Screen Language)

Se usa dentro de screens.rpy para mostrar u ocultar elementos de la GUI (botones, imágenes, barras).

Ubicación: Dentro de bloques screen, vbox, hbox o frame.

Modo de redactar:

'''renpy

screen info_personaje():
    vbox:
        text "Nombre: [nombre_jugador]"
        if nivel_veneno > 0:
            text "¡ESTÁS ENVENENADO!" color "#f00"
'''


4. Condicionales de una sola línea (Python Inline)

Útil para asignar valores a variables de forma rápida sin ocupar varias líneas de código.

Sintaxis: $ variable = valor_si_cierto if condicion else valor_si_falso.

Modo de redactar:

'''renpy

$ estado_animo = "Feliz" if puntos > 5 else "Triste"

'''

5. Dentro de Diálogos (Interpolación y Etiquetas de Texto)

Ren'Py permite variar palabras específicas dentro de una misma frase sin duplicar el bloque de código.

Modo nativo (Interpolación):

'''renpy

$ genero = "o" if es_hombre else "a"
"Bienvenid[genero] al club de literatura."
'''


Uso de etiquetas {if}: (Requiere versiones modernas de Ren'Py o addons específicos).

renpy
'''
"Te ves {if salud < 20}muy mal{else}bastante bien{/if} hoy."
'''


6. En Definiciones de Personajes e Imágenes

Puedes usar condicionales para determinar qué nombre o imagen mostrar dinámicamente.

Nombres dinámicos:

'''renpy

define p = Character("[nombre_personaje]") # Cambia si la variable cambia
'''



7. Imágenes condicionales (ConditionSwitch): Permite que una imagen cambie automáticamente según variables.

'''renpy

image protagonista = ConditionSwitch(
    "puntos > 10", "prota_feliz.png",
    "True", "prota_serio.png" # El 'True' final actúa como un 'else'
)

'''

Para dominar los condicionales en Ren'Py, existen tres conceptos "avanzados" que separan a un principiante de un programador eficiente:

1. Los Operadores Lógicos (and, or, not)

No estás limitado a una sola condición. Puedes combinar varias en una misma línea:

- and: Deben cumplirse todas.
- if tiene_llave and tiene_mapa:
- or: Debe cumplirse al menos una.
- if dia == "Sábado" or dia == "Domingo":
- not: Invierte el valor (si algo es falso).
- if not tiene_dinero:

2. El "Else" implícito en imágenes: ConditionSwitch

Cuando defines imágenes que cambian según variables, Ren'Py usa una sintaxis de lista. El último elemento siempre debe ser "True" para actuar como un else (el caso por defecto), de lo contrario, el juego podría dar error si ninguna condición se cumple.

'''renpy

image fondo_dinamico = ConditionSwitch(
    "tiempo == 'noche'", "fondo_oscuro.jpg",
    "True", "fondo_dia.jpg"
)

'''

3. Persistencia (persistent)

Puedes usar if/else con variables que "recuerdan" lo que pasó en otras partidas (finales desbloqueados, haber visto una escena secreta).

Sintaxis: Se usa el prefijo persistent.

'''renpy

if persistent.final_visto:
    "Ya conoces este destino, pero algo se siente diferente..."

'''

4. Verificación de "Pertenencia" (in)

Muy útil para inventarios o listas de nombres. En lugar de comparar uno por uno, preguntas si un elemento está dentro de una lista.

'''renpy

if "poción" in inventario:
    "Bebes la poción y recuperas vida."
'''


5. El peligro de la Indentación

Ren'Py es extremadamente estricto:

Un solo espacio de diferencia en la sangría (el hueco a la izquierda) hará que el código falle o que el else se asocie al if equivocado.
Regla de oro: Si abres un bloque con :, todo lo que esté "dentro" debe tener exactamente el mismo nivel de sangría.

