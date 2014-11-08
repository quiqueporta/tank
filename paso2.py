# -*- encoding: utf-8 -*-
#
# Creamos los tanques con sus controles asociados.

import random

import pilas
from pilas.escena import Normal
from pilas.actores import Actor


class Tanque(Actor):

    def __init__(self, control, imagen):

        # Obtenemos la imagen del tanque.
        imagen_tanque = pilas.imagenes.cargar_imagen(imagen)

        x = random.randrange(-320, 320)
        y = random.randrange(-240, 240)

        # Iniciamos el actor con la imagen del tanque.
        super(Tanque, self).__init__(imagen_tanque, x=x, y=y)

        # Establecemos la habilidad de disparar al tanque.
        self.aprender(pilas.habilidades.Disparar,
                      control=control,
                      frecuencia_de_disparo=2)

        # Establecemos la habilidad de moverse.
        self.aprender(pilas.habilidades.MoverseComoCoche,
                      control=control,
                      velocidad_maxima=2,
                      deceleracion=0.05,
                      velocidad_rotacion=0.5)

        # Habilidad para que nunca desaparezca de la pantalla.
        self.aprender(pilas.habilidades.SeMantieneEnPantalla)

        self.aprender(pilas.habilidades.PuedeExplotar)


class Escena_Juego(Normal):
    """ Escena principal del juego. """

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

    def crear_tanque(self, arriba, abajo, izquierda, derecha, disparo, imagen):

        teclas = {izquierda: 'izquierda',
                  derecha: 'derecha',
                  arriba: 'arriba',
                  abajo: 'abajo',
                  disparo: 'boton'}
        control = pilas.control.Control(pilas.escena_actual(), teclas)
        tanque = Tanque(control, imagen)
        return tanque


class Escena_Menu(Normal):
    """ Escena del menú del juego. """

    def iniciar_juego(self):
        pilas.cambiar_escena(Escena_Juego())

    def salir_del_juego(self):
        pilas.terminar()

    def iniciar(self):
        # Cargamos el fondo del juego.
        pilas.fondos.Tarde()

        opciones = [
            ('Iniciar Juego', self.iniciar_juego),
            ('Salir', self.salir_del_juego),
        ]

        pilas.actores.Menu(opciones)

pilas.iniciar()

pilas.cambiar_escena(Escena_Menu())

pilas.ejecutar()
