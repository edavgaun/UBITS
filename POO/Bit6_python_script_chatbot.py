import json
from termcolor import colored
import random
import requests

class Chatbot:
  def __init__(self, name="UBITS-Bot", claves_url=""):
    self.name=name
    self.conversacion="Registro de la conversación\n\n"
    self._claves=self.Get_Diccionario_Claves(claves_url)
    self.__repetir=0

    self.Presentacion()
    self.Bienvenida()
    self.Inicio()

  ##############################################################################
  def Inicio(self):
    # Ciclo infinito que revisará si el usuario proporciona una respuesta
    # Positiva, Negativa, o Vaga. En caso de suministrar una respuesta  
    # negativa 3 respuestas o vagas, el programa terminará.
    while True:
      respuesta=self.mensaje_usuario()
      if respuesta.title() in self._claves["Afirmacion"]:
        break
      elif respuesta.title() in self._claves["Negacion"]:
        self.Despedida()
        break
      else:
        self.__repetir+=1
        if self.__repetir>2:
          self.No_avanza()
          break
        else:
          self.Respuesta_default()
    self.repetir=0
    self.Opciones()

  ##############################################################################
  def Mensaje_Bot(self, bot=True,*mensaje):
    # Creando un indicador al inicio del mensaje para que se vea que se vea que
    # es un mensaje del ChatBot
    if bot==True:
      respuesta=self.name,":", *mensaje
    # En caso de que el mensaje sea muy largo, se divide en 2 líneas
    else:
      respuesta="\t", *mensaje
    # Todos los textos serán concatenados para presentarse al usuario
    respuesta=" ".join(respuesta)
    # Se registra la conversación en memoria
    self.conversacion+=respuesta
    self.conversacion+="\n"
    # Se muestra el mensaje del bot al usuario
    print(colored(respuesta, "red", attrs=["bold"]))

  ##############################################################################
  def Get_Diccionario_Claves(self, ruta=""):
    # Se busca el diccionario de palabras del ChatBot en un sitio del internet
    resp = requests.get(ruta)
    # Se convierte la información en un diccionario de Python
    dictionary = json.loads(resp.text)
    return dictionary

  ##############################################################################
  def respuesta(self, tema):
    # Función para obtener una respuesta aleatoria desde el diccionario de claves
    # que obtuvo el ChatBot
    return random.choice(self._claves[tema])

  ##############################################################################
  def mensaje_usuario(self):
    # Se mostrará una línea en pantalla para que el usuario agregue información
    print(colored("Usuario : ", "blue", attrs=["bold"]), end="")
    mensaje=input("\t")
    # Se almacena la respuesta del usuario en memoria
    self.conversacion+="Usuario : "
    self.conversacion+=mensaje
    self.conversacion+="\n"
    print()
    return mensaje

  ##############################################################################
  def Presentacion(self):
    self.Mensaje_Bot(True,"Bienvenido, mi nombre es", self.name)
    self.Mensaje_Bot(False, self.respuesta("Nombre"), ":")
    self.usuario=self.mensaje_usuario().title()
    self.Mensaje_Bot(True, self.respuesta("Apellido"), ":")
    self.usuario_apellido=self.mensaje_usuario().title()
  
  ##############################################################################
  def Bienvenida(self):
    self.Mensaje_Bot(True, self.respuesta("Agradecimiento"),self.usuario)
    self.Mensaje_Bot(False, "Te comento, soy un Chatbot diseñado para poder ayudarte.")
    self.Mensaje_Bot(False, "¿Te parece si comenzamos?")

  ##############################################################################
  def Respuesta_default(self):
      self.Mensaje_Bot(True, self.respuesta("Default"))

  ##############################################################################
  def Opciones(self):
      self.Mensaje_Bot(True, "En esta sección podrás colocar las opciones que quieras mostrar al usuario")
      self.Mensaje_Bot(False, "Por ejemplo un listado de preguntas frecuentes (FAQ's).\n")
      self.Mensaje_Bot(False, "Dependiendo la respuesta que de, lo vas dirigiendo utilizando métodos.\n")
      self.Mensaje_Bot(False, "Eso es algo que ya podrás desarrollar por tu cuenta.\n")
      self.Despedida()

  ##############################################################################
  def Despedida(self, corta=False):
    print("\n")
    # Respuesta corta en caso de que el usuario haya incurriedo en varias interacciones erroneas
    if corta:
      self.Mensaje_Bot(False, "Por mi parte es todo,", self.respuesta("Despedida"), self.usuario)
    # Respuesta larga en caso de que el usuario haya concluido con el chat
    else:
      self.Mensaje_Bot(True, self.respuesta("Agradecimiento"), self.usuario, ", espero que la sesión")
      self.Mensaje_Bot(False, "te haya sido de utilidad. Por mi parte es todo")
      self.Mensaje_Bot(False, self.respuesta("Despedida"))
  
  ##############################################################################
  def No_avanza(self):
    self.Mensaje_Bot(True, "Disculpa, esta conversación no avanza, será mejor que intentemos en otra ocasión")
    self.Despedida(True)


