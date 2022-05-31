'''Importamos las librerías -sys-, para poder invocar la salida de la interfaz y -pygame-.'''
'''Importamos la librería de variables locales de PYGAME, para poder invocar sus códigos de identificación para las teclas, el ratón, etc...'''

'''Esta clase será el objeto termómetro.'''




from pygame.locals import *
import sys
import pygame
class Termometro():
    '''Los atributos de nuestro termómetro será una tupla (privada) para contener las posibles unidades.'''
    __unidades = ("C", "F")

    '''El método constructor no recibirá valores. Unicamente asignará su disfraz al objeto.'''

    def __init__(self):
        self.disfraz = pygame.image.load("images/termo1.png")

    '''Este método contendrá la codificación para hacer que el termometro convierta la cantidad a la nueva unidad.'''

    def convertir(self, cantidad, nuevaUnidad):
        resultado = 0
        if nuevaUnidad == self.__unidades[0]:
            resultado = (cantidad - 32) * 5 / 9
        else:
            resultado = 32 + (cantidad * 9 / 5)

        return resultado


'''Esta clase será el objeto caja para introducir cantidades.'''


class BoxDatos():
    '''Los atributos de nuestra caja serán la cantidad, una cadena que casteará la cantidad, su posición, su tamaño y un contador para saber cuantos puntos decimales contiene la caja.'''
    __valor = None
    __strValor = None
    __posicion = []
    __tama = []
    __cuentaPuntos = 0

    '''El método constructor podrá recibir opcionalmente una cantidad con la que inicializará (seteará) la caja de entrada.'''

    def __init__(self, valor=0):
        self.valor(valor)

        '''Nuestra caja será un rectángulo en el que podremos escribir, por tanto le asignamos una fuente y un tamaño.'''
        self.__fuente = pygame.font.SysFont("Verdana", 21)

    '''Este método nos permitirá renderizar la caja de entrada. Devolverá la caja y una foto de su texto.'''

    def render(self):
        '''Para poder renderizar nuestra caja, asignamos una renderización de texto. Una foto de una cadena de texto, de un color RGB.'''
        fotoTexto = self.__fuente.render(self.__strValor, True, (133, 27, 99))

        '''Y también una renderización de la caja propiamente dicha. Obtenemos su rectángulo, lo posicionamos en nuestro Frame y lo dimensionamos.'''
        rectangulo = fotoTexto.get_rect()
        rectangulo.left = self.__posicion[0]
        rectangulo.top = self.__posicion[1]
        rectangulo.size = self.__tama

        return [rectangulo, fotoTexto]

    '''Este método nos permitirá evaluar los eventos de la caja de entrada.
       Dentro del método KEYDOWN de PYGAME existe un elemento -unicode- que nos devuelve el caracter de la tecla que pulsemos.
       Cuando tecleemos una cantidad, habrá que irla añadiendo dígito a dígito a la cadena que se representa (como una foto) en la caja de entrada (y fijamos un máximo de diez dígitos).
       También debemos permitir la correción, atendiendo a la tecla de borrado, y eliminando el ultimo carácter de la cadena representada.
       Al tiempo que modificamos la cadena representada tenemos que modificar también el valor numérico y para ello usamos el método -valor-'''

    def unEventoTecla(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.unicode in '-.0123456789' and len(self.__strValor) < 10:
                if evento.unicode == '-' and len(self.__strValor) == 0:
                    self.__strValor += evento.unicode
                if evento.unicode == '.' and self.__cuentaPuntos == 0:
                    if len(self.__strValor) == 0:
                        self.__strValor += "0"
                    self.__cuentaPuntos += 1
                    self.__strValor += evento.unicode
                elif evento.unicode not in '-.':
                    self.__strValor += evento.unicode
            elif evento.key == K_BACKSPACE:
                if len(self.__strValor) != 0:
                    if self.__strValor[-1] == '.':
                        self.__cuentaPuntos -= 1
                    self.__strValor = self.__strValor[:-1]

    '''Este método setter/getter permitirá cambiar el valor de la caja de entrada.
       Si no se informa un valor en la invocación, el método devolverá el valor que la caja de entrada tenga en ese momento.
       Si se informa, validará que sea un valor numérico entero, para ello lo convertirá en una cadena (para poderla escribir en la caja) y después intentará castearla a entero.
       Si el valor informado no es válido el setter no hará nada y por ende el valor de la caja de entrada no se cambiará.'''

    def valor(self, val=None):
        if val == None:
            if len(self.__strValor) == 0:
                self.valor(0)
            else:
                self.__valor = float(self.__strValor)

            return self.__valor
        else:
            val = str(val)
            try:
                self.__valor = round(float(val), 2)
                self.__strValor = "{}".format(str(self.__valor))

                if '.' in self.__strValor:
                    self.__cuentaPuntos = 1
                else:
                    self.__cuentaPuntos = 0
            except:
                pass

    '''Este método setter/getter permitirá cambiar el tamaño de la caja de entrada.
       Si no se informa una lista con dos valores en la invocación, el método devolverá el tamaño que la caja de entrada tenga en ese momento.
       Si se informa, validará que la lista tenga dos valores numéricos enteros, intentando castearlos a enteros.
       Si la lista informada no es válida el setter no hará nada y por ende el tamaño de la caja de entrada no se cambiará.'''

    def tama(self, val=None):
        if val == None:
            return self.__tama
        else:
            try:
                self.__tama = [int(val[0]), int(val[1])]
            except:
                pass

    '''Este método setter/getter permitirá cambiar las coordenadas posicionales de la caja de entrada.
       Si no se informa una lista con dos valores en la invocación, el método devolverá las coordenadas posicionales que la caja de entrada tenga en ese momento.
       Si se informa, validará que la lista tenga dos valores numéricos enteros, intentando castearlos a enteros.
       Si la lista informada no es válida el setter no hará nada y por ende las coordenadas posicionales de la caja de entrada no se cambiarán.'''

    def posicion(self, val=None):
        if val == None:
            return self.__posicion
        else:
            try:
                self.__posicion = [int(val[0]), int(val[1])]
            except:
                pass


'''Esta clase será el objeto selector.'''


class Selector():
    '''Los atributos de nuestro selector serán dos tuplas (privadas) para contener las posibles unidades y sus disfraces y la unidad y el disfraz del selector (privados).'''
    __unidades = ("C", "F")
    __disfraces = (pygame.image.load("images/posiC.png"),
                   pygame.image.load("images/posiF.png"))
    __unidad = None

    '''El método constructor inicializará el selector en ºC.'''

    def __init__(self, unidad="C"):
        self.__unidad = unidad

    '''Este método getter devolverá la unidad del selector.'''

    def unidad(self):
        return self.__unidad

    '''Este método getter devolverá el disfraz adecuado a la unidad del selector.'''

    def disfraz(self):
        return self.__disfraces[int(self.__unidades.index(self.__unidad))]

    '''Este método nos permitirá cambiar la unidad del selector.'''

    def cambiar(self):
        if self.__unidad == self.__unidades[0]:
            self.__unidad = self.__unidades[1]
        else:
            self.__unidad = self.__unidades[0]


'''Nuestra clase principal (objeto) será un Frame en el que habrá un termómetro, un campo de entrada en el que pondremos una cantidad y un selector para poder convertir la cantidad en dos unidades diferentes.'''


class ConversordeTemperatura():
    '''Los atributos serán los elementos del Frame (inicializados).'''
    termometro = None
    boxEntrada = None
    selectorUnidad = None

    '''El método constructor no recibirá valores. Se encargará de definir la base de la ventana de ejecución (el Frame) y su título.'''

    def __init__(self):
        '''Lo primero es definir la pantalla fijando su tamaño y su título.'''
        self.__frame = pygame.display.set_mode((290, 415))
        pygame.display.set_caption("Conversor [ ºC / ºF ]")

        '''Ahora creamos un termómetro, un selector y una caja de entrada para incluirlos en nuestro Frame.'''
        self.termometro = Termometro()
        self.selectorUnidad = Selector()
        self.boxEntrada = BoxDatos()
        self.boxEntrada.posicion((106, 58))
        self.boxEntrada.tama((133, 28))

    '''Definimos un método para cerrar la aplicación de forma más elegante.'''

    def __close(self):
        pygame.quit()
        sys.exit()

    '''Este método será el que inicie nuestra aplicación.'''

    def iniciar(self):
        '''Lanzamos un bucle infinito, ya que nuestra aplicación solo acabará si decidimos finalizarla con el botón que cierra la ventana terminando la ejecución.'''
        while True:
            '''Comprobamos los eventos. En nuestro caso, este paso es también la ejecución del código de la aplicación.
               El primero, el cierre de ventana.
               Lo siguiente es detectar si pulsamos teclas para escribir en la caja de entrada, para ello enviamos el evento al método -unEventoTecla- del objeto BoxDatos y que lo analice.
               Por último, estaremos atentos a los clicks del ratón que harán que el selector cambie. El método MOUSEBUTTONDOWN de PYGAME detecta los clicks del ratón.
               Cuando hagamos un click, pediremos al selector que cambie de unidad y al termómetro que convierta la cantidad de la caja de entrada.'''
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.__close()
                elif evento.type == MOUSEBUTTONDOWN:
                    self.selectorUnidad.cambiar()
                    self.boxEntrada.valor(self.termometro.convertir(
                        self.boxEntrada.valor(), self.selectorUnidad.unidad()))

                self.boxEntrada.unEventoTecla(evento)

            '''Redibujamos todos los objetos.
               Pintamos el frame (nuestra ventana o pantalla) rellenándolo con un color RBG y el termómetro, que fijamos en sus coordenadas.
               A continuación redibujamos el selector (que podría cambiar) fijándolo en sus coordenadas.'''
            self.__frame.fill((255, 170, 85))
            self.__frame.blit(self.termometro.disfraz, (50, 34))
            self.__frame.blit(self.selectorUnidad.disfraz(), (108, 153))

            '''Para poder redibujar la caja de entrada y su valor, ejecutamos el método -render- del objeto BoxDatos.
               Pintamos el rectángulo que devuelve en la primera posición de la lista con su color RGB.
               Y dibujamos la foto del texto que devuelve en la segunda posición de la lista, como si fuera un disfraz.'''
            renderCaja = self.boxEntrada.render()
            pygame.draw.rect(self.__frame, (255, 255, 200), renderCaja[0])
            self.__frame.blit(renderCaja[1], self.boxEntrada.posicion())

            '''Renderizamos la pantalla'''
            pygame.display.flip()


'''Nuestra ejecución como programa principal iniciará el framework de PYGAME, instanciará un objeto termometro-conversor e invocará su metodo empezar para que se inicie la ejecución.'''
if __name__ == "__main__":
    pygame.init()
    TermoConver = ConversordeTemperatura()
    TermoConver.iniciar()
