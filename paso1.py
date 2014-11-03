# -*- encoding: utf-8 -*-
#
# Creamos las escenas y el menú del juego

import pilas
from pilas.escena import Normal


class Escena_Juego(Normal):
    """ Escena principal del juego. """

    def __init__(self):
        super(Escena_Juego, self).__init__()

    def iniciar(self):
        # Cargamos el fondo del juego.
        pilas.fondos.Pasto()


class Escena_Menu(Normal):
    """ Escena del menú del juego. """

    def __init__(self):
        super(Escena_Menu, self).__init__()

    def iniciar_juego(self):
        pilas.cambiar_escena(Escena_Juego())

    def salir_del_juego(self):
        import sys
        sys.exit(0)

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
