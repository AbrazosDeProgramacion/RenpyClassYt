## spline editor
## originally written by renpytom or Aenakume -
## http://lemmasoft.renai.us/forums/viewtopic.php?p=55676
## updated by John Hoffman
#-------------------------------------------------------------------------
## Actualizado y traducido por el canal "Abrazos de Programación por Lily"
##https://www.youtube.com/@Bonnie-s2w


init python:

    theme.roundrect()

    style.window.background = None
    
    _game_menu_screen = None

    class Point(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

    import pygame
    import os
    
    HANDLE_SIZE = 9
    DOT_SIZE = 3

    # The size of the viewable area of the screen.
    X = int(config.screen_width*0.1875)
    Y = int(config.screen_height*0.1875)
    W = int(config.screen_width*0.625)
    H = int(config.screen_height*0.625)
    
    class SplineEditor(renpy.Displayable):

        def __init__(self):
            super(SplineEditor, self).__init__()

            self.mode = "addmove"
            
            self.lead_handle = [ ]
            self.points = [ ]
            self.trail_handle = [ ]

            self.handle = Image("images/handle.png")
            self.point = Image("images/bullet.png")
            self.dot = Image("images/dot.png")
            
            self.dragging = None
            self.reflect = None
            self.reflected = None
            self.relative_drag = [ ]

            self.spline_dots = [ ]
            self.spline_points = [ ]

            self.delay = 3.0
            self.closed = False

            self.show_preview = False
            
        


        def render(self, width, height, st, at):

            rv = renpy.Render(width, height)
            # Forzamos que el displayable ocupe toda la pantalla
            rv.fill((0, 0, 0, 0)) 
            
            # 1. Dibujamos la línea continua (spline_dots) como puntos azules pequeños
            for i in self.spline_dots:
                dot = renpy.Render(DOT_SIZE*2, DOT_SIZE*2)
                dot.fill((0, 0, 255, 255))
                rv.blit(dot, (int(i[0]) - DOT_SIZE, int(i[1]) - DOT_SIZE))

            # 2. Dibujamos las líneas de los handles usando el Canvas (solo líneas, sin texto)
            canv = rv.canvas()
            for (a, p, b) in zip(self.lead_handle, self.points, self.trail_handle):
                canv.line((192, 192, 255, 255), (int(a.x), int(a.y)), (int(p.x), int(p.y)))
                canv.line((192, 192, 255, 255), (int(b.x), int(b.y)), (int(p.x), int(p.y)))

            # 3. Dibujamos los handles de control como cuadrados rojos
            for i in self.lead_handle + self.trail_handle:
                handle = renpy.Render(8, 8)
                handle.fill((255, 100, 100, 255))
                rv.blit(handle, (int(i.x) - 4, int(i.y) - 4))

            # 4. Dibujamos los nodos principales (puntos negros) + SUS COORDENADAS
            for p in self.points:
                # Creamos el punto principal negro
                point = renpy.Render(HANDLE_SIZE, HANDLE_SIZE)
                point.fill((0, 0, 0, 255))
                rv.blit(point, (int(p.x) - HANDLE_SIZE//2, int(p.y) - HANDLE_SIZE//2))
                
                # Creamos y dibujamos el texto de la coordenada
                coord_str = "(%.0f, %.0f)" % (p.x, p.y)
                coord_text = Text(coord_str, color="#333333", size=14)
                coord_render = renpy.render(coord_text, width, height, st, at)
                rv.blit(coord_render, (int(p.x) + 12, int(p.y) + 12))

            # 5. Texto del Delay en la esquina
            delay_text = Text("Delay: %.1f" % self.delay, color="#000000", size=20)
            delay_render = renpy.render(delay_text, width, height, st, at)
            rv.blit(delay_render, (config.screen_width - 150, config.screen_height - 50))
            
            return rv
                

        def event(self, ev, x, y, st):

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.mouse1down(x, y)

            if ev.type == pygame.MOUSEMOTION or (ev.type == pygame.MOUSEBUTTONUP and ev.button == 1):
                self.mousemotion(x, y)
                
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.mouse1up(x, y)

            if ev.type == pygame.KEYDOWN:
                self.keydown(ev.key, ev.unicode)


                
        def mouse1down(self, x, y):

            if self.mode == "addmove":

                # True if we're close enough to the handle to drag it.
                def near(p):
                    if abs(p.x - x) <= HANDLE_SIZE / 2 and abs(p.y - y) <= HANDLE_SIZE / 2:
                        return True
                    else:
                        return False

                point = None
                relative = [ ]
                
                for p, p1, p2 in zip(self.points, self.lead_handle, self.trail_handle):
                    if near(p):
                        point = p
                        relative = [
                            (p1.x - p.x, p1.y - p.y, p1),
                            (p2.x - p.x, p2.y - p.y, p2),
                            ]
                        
                for p in self.lead_handle:
                    if near(p):
                        point = p
                        relative = [ ]
                        
                for p in self.trail_handle:
                    if near(p):
                        point = p
                        relative = [ ]
                        
                if point:
                    self.mode = "drag"
                    self.dragging = point
                    self.relative_drag = relative
                    return 
                
                self.dragging = Point(x, y)
                self.reflect = Point(x, y)
                self.reflected = Point(x, y)

                self.points.append(self.reflect)
                self.lead_handle.append(self.reflected)
                self.trail_handle.append(self.dragging)

                self.mode = "mirrordrag"
                self.recompute_spline()
                renpy.redraw(self, 0)

        def mousemotion(self, x, y):

            if self.mode == "mirrordrag":

                self.dragging.x = x
                self.dragging.y = y

                self.reflected.x = 2 * self.reflect.x - x
                self.reflected.y = 2 * self.reflect.y - y

                self.recompute_spline()                
                renpy.redraw(self, 0)

            if self.mode == "drag":
                self.dragging.x = x
                self.dragging.y = y

                for (xo, yo, p) in self.relative_drag:
                    p.x = xo + x
                    p.y = yo + y
                
                self.recompute_spline()                
                renpy.redraw(self, 0)
                

        def mouse1up(self, x, y):
            # Guardamos la posición para dibujar el punto verde de feedback
            self.click_feedback = (x, y)
            
            if self.mode == "mirrordrag":
                self.mode = "addmove"
                
            if self.mode == "drag":
                self.mode = "addmove"

            self.recompute_spline()                
            renpy.redraw(self, 0)

        def keydown(self, key, unicode):
            if key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
                if self.points:
                    self.points.pop()
                    self.lead_handle.pop()
                    self.trail_handle.pop()

            # elif unicode == "p":
            #     # En lugar de saltar, simplemente marcamos que queremos ver la vista previa
            #     self.show_preview = True
            #     renpy.redraw(self, 0)

            elif unicode == "+":
                self.delay += .1

            elif unicode == "-":
                self.delay -= .1
                if self.delay < .1:
                    self.delay = .1

            elif unicode == "c":
                self.closed = not self.closed

            elif unicode == "n":
                renpy.jump("start")

            elif unicode == "w":
                renpy.jump("write")
                
            self.recompute_spline()
            renpy.redraw(self, 0)
            
                
                
        def recompute_spline(self):
            self.spline_dots = [ ]

            spline_points = [ ]
            self.spline_points = spline_points

            if len(self.points) < 2:
                return

            spline_points.append(((self.points[0].x, self.points[0].y),))

            for i in range(0, len(self.points) - 1):
                spline_points.append((
                        (self.points[i+1].x,
                         self.points[i+1].y),
                        (self.trail_handle[i].x,
                         self.trail_handle[i].y),
                        (self.lead_handle[i+1].x,
                         self.lead_handle[i+1].y),
                        ))

            if self.closed:
                spline_points.append((
                        (self.points[0].x,
                         self.points[0].y),
                        (self.trail_handle[-1].x,
                         self.trail_handle[-1].y),
                        (self.lead_handle[0].x,
                         self.lead_handle[0].y),
                        ))
                
            pi = _SplineInterpolator(spline_points)

            if self.closed:
                numdots = len(self.points) * 15
            else:
                numdots = (len(self.points) - 1) * 15
                
            for j in range(0, numdots + 1):
                t = 1.0 * j / numdots

                x, y, xo, yo = pi(t, (800, 600, DOT_SIZE, DOT_SIZE))
                self.spline_dots.append((x, y))


        def relative_spline(self):
            def make_relative(t):
                x, y = t
                return (1.0 * (x - X) / W, 1.0 * (y - Y) / H)
            
            return list(tuple(make_relative(i) for i in j) for j in self.spline_points)

    # Nicely formats nested tuples and floats.
    def format(v):
        if isinstance(v, tuple):
            return "(" + ", ".join(format(i) for i in v) + ",)"
        else:
            return "%.3f" % v
            



screen background:
    add "#FFF"

    text "Editor de movimiento Ren'Py":
        align (0.01,0.01)
        size 28
        color "#BBB"

    add Frame("images/frame.png",3,3):
        size (W,H)
        anchor (0,0)
        pos (X,Y)

    text "bordes de la pantalla":
        anchor (0.0,1.0)
        pos (X+20,Y-5)
        size 12
        color "#BBB"

    vbox:
        align (0.01,0.99)
        text "Clic para añadir o editar puntos":
            size 16
            color "#BBB"
        text "Retroceso - quita los últimos puntos":
            size 16
            color "#BBB"
        text "w - escribe código y muestra animación, n - nueva trayectoria, c - cerrar trayectoria":
            size 16
            color "#BBB"

    vbox:
        align (0.99,0.99)
        text "velocidad:":
            size 16
            color "#BBB"
        text "+/- aumentar/disminuir":
            size 16
            color "#BBB"

    # ---> NUEVO: Añadimos el editor directamente en la pantalla
    add se


screen preview_screen(motion):
    add "#000"
    add "images/smile.png" at motion
    text "Animación generada. Click para volver al editor.":
        align (0.5, 0.95)
        color "#FFF"          
    
label confirm_quit:
    $ renpy.quit()
    
label main_menu:
    return

label start:

    python:
        se = SplineEditor()

label edit:
    scene None
    show screen background(_layer="master")

    # Este bucle mantiene el editor vivo y funcionando
    while True:
        $ result = ui.interact()
        
        # Si presionamos "p" y hay suficientes puntos, lanzamos la vista previa
        if se.show_preview:
            $ se.show_preview = False # Reseteamos la bandera
            
            if len(se.points) >= 2:
                # Calculamos el movimiento
                $ motion = SplineMotion(se.relative_spline(), se.delay, repeat=True)
                
                # Escondemos el editor y mostramos la animación limpia
                hide screen background
                show screen preview_screen(motion)
                
                # Esperamos a que el usuario haga clic
                pause
                
                # Ocultamos la vista previa y volvemos al editor
                hide screen preview_screen
                show screen background(_layer="master")


    
label write:

    # Si no hay puntos suficientes, no hacemos nada y volvemos a editar
    if len(se.points) < 2:
        jump edit

    python:
        # 1. Guardamos el archivo como siempre
        path = os.path.join(config.gamedir, "splinedata.rpy")
        with open(path, 'w', encoding='utf-8') as f:
            f.write("init python:\n")
            f.write("    spline = SplineMotion([\n")
            for t in se.relative_spline():
                f.write("        %s,\n" % format(t))
            f.write("        ], %.1f, anchors=(0.5, 0.5), repeat=False)\n" % se.delay)
            f.close()

    # 2. Preparamos la animación
    $ motion = SplineMotion(se.relative_spline(), se.delay, repeat=True)

    # 3. Escondemos el editor y mostramos la pantalla de animación
    hide screen background
    show screen preview_screen(motion)

    # Mensaje de confirmación
    "Archivo splinedata.rpy guardado. Revisando movimiento..."

    # 4. Al hacer clic, volvemos al editor
    hide screen preview_screen
    jump edit

        
        
    
    

    
