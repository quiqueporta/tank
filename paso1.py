# -*- encoding: utf-8 -*-
#
# Creamos la escena y ponemos el fondo

import random

import pilas
from pilas.escena import Normal


class Escena_Juego(Normal):
    """ Escena principal del juego. """

    def __init__(self):
        Normal.__init__(self)

    def iniciar(self):
        # Cargamos el fondo del juego.
        pilas.fondos.Pasto()

pilas.iniciar()

pilas.cambiar_escena(Escena_Juego())

pilas.ejecutar()
