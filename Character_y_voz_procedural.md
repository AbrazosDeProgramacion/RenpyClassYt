**Código completo:** Copia y pega en un nuevo proyecto.

```python
init python:
    import random

    def lolo_voz_procedural(event, interact=True, **kwargs):
        if event == "begin" and interact:
            volumen = random.uniform(0.7, 1.0)
            renpy.sound.set_volume(volumen, delay=0, channel="sound")
            
            # Crea una lista con 4 tonos aleatorios
            beeps = ["audio/lolo_{}.ogg".format(random.choice(["bajo", "medio", "agudo", "muy agudo"])) for _ in range(3)]
            
            # Los reproduce todos a la vez (como un acorde rápido)
            renpy.play(beeps, channel="sound")

# Lo aplicamos a Lolo
define l = Character("Lolo", color="#ff9900", callback=lolo_voz_procedural)

# Definimos una variable de estado que afectará al nombre
default nombre_revelado = False

init python:
    # Función que devuelve el nombre basándose en el estado del juego
    def get_npc_name():
        if nombre_revelado:
            return "Marcus, El Sabio"  
        return "Desconocido"   

# Así queda más limpio y moderno
define m = Character(name=get_npc_name, dynamic=True, color="#10C802")

image lolo_img = "lolo.png"
image marcus_img = "marcus.png"
image bosque_img = "bosque.jpeg"

# Escenario de prueba
label start:
    scene bosque_img 
    show lolo_img at left
    show marcus_img at right
    with dissolve
    
    l "Estoy explorando el bosque y veo a alguien."
    
    # Aquí, el nombre será "Desconocido"
    m "Hola, viajero. No tengo mucho que decirte."
    
    "Decido entablar una conversación y ganarme su confianza."
    
    # Cambiamos el estado
    $ nombre_revelado = True
    
    l "¡Ya confío en ti! ¿Cómo te llamas?"
    
    # Aquí, mágicamente, el nombre será "Marcus, El Sabio"
    m "Ahora que me conoces, puedes llamarme 'Marcus, El Sabio'."
    
    return
```




