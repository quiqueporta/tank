# -*- encoding: utf-8 -*-
import random

import pilas
from pilas.escena import Normal
from pilas.actores import Actor


class Tanque(Actor):

    def __init__(self, control, imagen="images/tanque.png"):

        # Obtenemos la imagen del tanque.
        imagen_tanque = pilas.imagenes.cargar_imagen(imagen)

        x = random.randrange(-320, 320)
        y = random.randrange(-240, 240)

        # Iniciamos el actor con la imagen del tanque.
        Actor.__init__(self, imagen_tanque, x=x, y=y)

        # Establecemos la habilidad de disparar al tanque.
        self.aprender(pilas.habilidades.Disparar,
                      control=control,
                      frecuencia_de_disparo=2,
                      cuando_dispara=self.plantar_bomba)

        # Establecemos la habilidad de moverse.
        self.aprender(pilas.habilidades.MoverseComoCoche, control=control,
                      velocidad_maxima=2,
                      deceleracion=0.05,
                      velocidad_rotacion=0.5)

        # Habilidad para que nunca desaparezca de la pantalla.
        self.aprender(pilas.habilidades.SeMantieneEnPantalla)

        self.aprender(pilas.habilidades.PuedeExplotar)

        self.tiene_bomba = False

        self.vidas = pilas.actores.Puntaje(3, x=-200)

    def definir_enemigo(self, enemigo):
        self.habilidades.Disparar.definir_colision(enemigo, self.impacto)
        self.enemigo = enemigo

    def impacto(self, proyectil, enemigo):
        proyectil.eliminar()
        pilas.actores.Humo(proyectil.x, proyectil.y)
        enemigo.quitar_vida()

    def quitar_vida(self):
        self.vidas.reducir(1)
        if self.vidas.obtener() <= 0:
            self.eliminar()

    def plantar_bomba(self):
        if self.tiene_bomba:
            bomba = pilas.actores.Bomba(x=self.x, y=self.y)
            bomba.escala = 0.5

            self.tiene_bomba = False

            pilas.escena_actual().colisiones.agregar(self.enemigo,
                                                     bomba,
                                                     self.destruir_enemigo)

    def destruir_enemigo(self, tanque, bomba):
        bomba.eliminar()
        tanque.eliminar()

class Escena_Juego(Normal):
    """ Escena principal del juego. """

    def __init__(self):
        Normal.__init__(self)

    def iniciar(self):
        # Cargamos el fondo del juego.
        pilas.fondos.Pasto()

        self.tanque_J1 = self.crear_tanque(pilas.simbolos.ARRIBA,
                                 pilas.simbolos.ABAJO,
                                 pilas.simbolos.IZQUIERDA,
                                 pilas.simbolos.DERECHA,
                                 pilas.simbolos.ALTGR,
                                 "images/tanque.png")

        self.tanque_J2 = self.crear_tanque(pilas.simbolos.w,
                                 pilas.simbolos.s,
                                 pilas.simbolos.a,
                                 pilas.simbolos.d,
                                 pilas.simbolos.SHIFT,
                                 "images/tanque2.png")

        self.tanque_J1.definir_enemigo(self.tanque_J2)
        self.tanque_J2.definir_enemigo(self.tanque_J1)


        pilas.escena_actual().tareas.siempre(20, self.crear_bomba)

        self.hay_bomba_en_juego = False

    def crear_tanque(self, arriba, abajo, izquierda, derecha, disparo, imagen):
        teclas = {izquierda: 'izquierda',
                  derecha: 'derecha',
                  arriba: 'arriba',
                  abajo: 'abajo',
                  disparo: 'boton'}
        control = pilas.control.Control(pilas.escena_actual(), teclas)
        tanque = Tanque(control, imagen)
        return tanque

    def crear_bomba(self):
        if not self.hay_bomba_en_juego:
            x = random.randrange(-320, 320)
            y = random.randrange(-240, 240)
            bomba = pilas.actores.Bomba(x,y)
            bomba.escala = 0.5
            pilas.escena_actual().colisiones.agregar(
                [self.tanque_J1, self.tanque_J2],
                bomba,
                self.obtener_bomba)
            self.hay_bomba_en_juego = True

    def obtener_bomba(self, tanque, bomba):
        tanque.tiene_bomba = True
        bomba.destruir()
        self.hay_bomba_en_juego = False



pilas.iniciar()

pilas.cambiar_escena(Escena_Juego())

pilas.ejecutar()
