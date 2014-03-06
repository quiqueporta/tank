# -*- encoding: utf-8 -*-
#
# Creamos los marcadores de vidas y restamos vida con impacto.

import random

import pilas
from pilas.escena import Normal
from pilas.actores import Actor


class Tanque(Actor):

    def __init__(self, control, imagen, vidas):

        # Obtenemos la imagen del tanque.
        imagen_tanque = pilas.imagenes.cargar_imagen(imagen)

        x = random.randrange(-320, 320)
        y = random.randrange(-240, 240)

        # Iniciamos el actor con la imagen del tanque.
        Actor.__init__(self, imagen_tanque, x=x, y=y)

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

        self.vidas = vidas

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


class Escena_Juego(Normal):
    """ Escena principal del juego. """

    def __init__(self):
        Normal.__init__(self)

    def iniciar(self):
        # Cargamos el fondo del juego.
        pilas.fondos.Pasto()

        self.vidas_J1 = pilas.actores.Puntaje(3, x=200)
        self.tanque_J1 = self.crear_tanque(pilas.simbolos.ARRIBA,
                                           pilas.simbolos.ABAJO,
                                           pilas.simbolos.IZQUIERDA,
                                           pilas.simbolos.DERECHA,
                                           pilas.simbolos.ALTGR,
                                           "images/tanque.png",
                                           self.vidas_J1)

        self.vidas_J2 = pilas.actores.Puntaje(3, x=-200)
        self.tanque_J2 = self.crear_tanque(pilas.simbolos.w,
                                           pilas.simbolos.s,
                                           pilas.simbolos.a,
                                           pilas.simbolos.d,
                                           pilas.simbolos.SHIFT,
                                           "images/tanque2.png",
                                           self.vidas_J2)

        self.tanque_J1.definir_enemigo(self.tanque_J2)
        self.tanque_J2.definir_enemigo(self.tanque_J1)

    def crear_tanque(self, arriba, abajo, izquierda, derecha, disparo, imagen,
                     vidas):

        teclas = {izquierda: 'izquierda',
                  derecha: 'derecha',
                  arriba: 'arriba',
                  abajo: 'abajo',
                  disparo: 'boton'}
        control = pilas.control.Control(pilas.escena_actual(), teclas)
        tanque = Tanque(control, imagen, vidas)
        return tanque

pilas.iniciar()

pilas.cambiar_escena(Escena_Juego())

pilas.ejecutar()
