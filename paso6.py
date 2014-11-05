# -*- encoding: utf-8 -*-
#
# Añadimos nuevos items para recoger.

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
        super(Tanque, self).__init__(imagen_tanque, x=x, y=y)

        # Establecemos la habilidad de disparar al tanque.
        self.aprender(pilas.habilidades.Disparar,
                      control=control,
                      frecuencia_de_disparo=2,
                      cuando_dispara=self.plantar_bomba)

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

        self.tiene_bomba = False

    def definir_enemigo(self, enemigo):
        self.habilidades.Disparar.definir_colision(enemigo, self.impacto)
        self.enemigo = enemigo

    def impacto(self, proyectil, enemigo):
        proyectil.eliminar()
        pilas.actores.Humo(proyectil.x, proyectil.y)
        enemigo.quitar_vida()

    def quitar_vida(self, cantidad=1):
        self.vidas.reducir(cantidad)
        if self.vidas.obtener() <= 0:
            self.eliminar()

    def plantar_bomba(self):
        if self.tiene_bomba:
            bomba = pilas.actores.Bomba(x=self.x, y=self.y)
            bomba.escala = 0.5

            self.tiene_bomba = False

            pilas.escena_actual().colisiones.agregar(self.enemigo,
                                                     bomba,
                                                     self.impacto_bomba)

    def impacto_bomba(self, tanque, bomba):
        bomba.eliminar()
        tanque.quitar_vida(2)


class Escena_Juego(Normal):
    """ Escena principal del juego. """

    def iniciar(self):
        # Cargamos el fondo del juego.
        pilas.fondos.Pasto()

        VIDAS_INICIALES = 3

        self.vidas_J1 = pilas.actores.Puntaje(VIDAS_INICIALES, x=250, y=200,
                                              color=pilas.colores.blanco)
        texto_J1 = pilas.actores.Texto("Verde:", x=200, y=200)
        texto_J1.definir_color(pilas.colores.blanco)

        self.tanque_J1 = self.crear_tanque(pilas.simbolos.ARRIBA,
                                           pilas.simbolos.ABAJO,
                                           pilas.simbolos.IZQUIERDA,
                                           pilas.simbolos.DERECHA,
                                           pilas.simbolos.ALTGR,
                                           "images/tanque.png",
                                           self.vidas_J1)

        texto_J2 = pilas.actores.Texto("Rojo:", x=-250, y=200)
        texto_J2.definir_color(pilas.colores.blanco)

        self.vidas_J2 = pilas.actores.Puntaje(VIDAS_INICIALES, x=-200, y=200,
                                              color=pilas.colores.blanco)
        self.tanque_J2 = self.crear_tanque(pilas.simbolos.w,
                                           pilas.simbolos.s,
                                           pilas.simbolos.a,
                                           pilas.simbolos.d,
                                           pilas.simbolos.SHIFT,
                                           "images/tanque2.png",
                                           self.vidas_J2)

        self.tanque_J1.definir_enemigo(self.tanque_J2)
        self.tanque_J2.definir_enemigo(self.tanque_J1)

        self.tareas.siempre(15, self.crear_bomba)

        self.tareas.siempre(15, self.crear_estrella)

        pilas.eventos.actualizar.conectar(self.comprobar_ganador)

    def comprobar_ganador(self, evento):

        if self.tanque_J1.vidas.obtener() == 0:
            self.efecto_ganador(self.tanque_J2)

        if self.tanque_J2.vidas.obtener() == 0:
            self.efecto_ganador(self.tanque_J1)

    def efecto_ganador(self, ganador):
        ganador.x = 0
        ganador.y = 0
        ganador.escala = [3]
        ganador.rotacion = [360]

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

    def crear_bomba(self):
        x = random.randrange(-320, 320)
        y = random.randrange(-240, 240)
        bomba = pilas.actores.Bomba(x, y)
        bomba.escala = 0.5
        self.colisiones.agregar(
            [self.tanque_J1, self.tanque_J2],
            bomba,
            self.obtener_bomba)

    def obtener_bomba(self, tanque, bomba):
        tanque.tiene_bomba = True
        bomba.destruir()

    def crear_estrella(self):
        x = random.randrange(-320, 320)
        y = random.randrange(-240, 240)
        estrella = pilas.actores.Estrella(x, y)
        estrella.escala = 0.4
        self.colisiones.agregar(
            [self.tanque_J1, self.tanque_J2],
            estrella,
            self.aumentar_velocidad)

    def aumentar_velocidad(self, tanque, estrella):
        estrella.eliminar()
        tanque.habilidades.MoverseComoCoche.set_velocidad_maxima(4)
        self.tareas.una_vez(5, self.reducir_velocidad, [tanque])

    def reducir_velocidad(self, tanque):
        tanque.habilidades.MoverseComoCoche.set_velocidad_maxima(2)


class Escena_Menu(Normal):
    """ Escena del menú del juego. """

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
