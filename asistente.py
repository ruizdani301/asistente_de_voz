import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

"""
para ver todos los acentos
engine = pyttsx3.init()
for voz in engine.getProperty('voices'):
    print(voz)
"""
"""
    Pendiente instalar otro tipo de voz
"""

#EScuchar microfono y devolver el audio como texto

def trasformar_audio_a_texto():
    # almacenarrecognizer
    r = sr.Recognizer()
    # configuracion del microfono

    with sr.Microphone() as origen:
        #tiempo de espera
        r.pause_threshold = 0.8

        # informar q empezo la grabacion
        print("puedes hablar")
        #guardar lo escuchado
        audio = r.listen(origen)
        try:

            #buscar en google
            solicitud = r.recognize_google(audio, language = "es-CO")
            # Ver lo q se dijo
            print(solicitud)
            return solicitud

        except sr.UnknownValueError:
            print("desconocido")
            return "sigo esperando"
        except sr.RequestError:
            print("No se entendio lo q dijo")
        except sr.RequestError:
            print("algo salio mal")

#Funcion que devuelva la respuesta con voz
def hablar(mensaje):
    #encender el motor de pyttsx3
    engine = pyttsx3.init()
    # darle un acento a la voz, falta arreglar
    engine.setProperty('voice','spanish')

    #pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

#informar dia de la semana
def pedir_dia():
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miercoles',
                  3: 'Jueves',
                  4: 'viernes',
                  5: 'Sabado',
                  6: 'Domingo'}
    dia = datetime.date.today()
    print(dia)

    #dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)
    hablar(f"Hoy es, {calendario[dia_semana]}")

# informar hora
def pedir_hora():
    #Crear variable con horas
    hora = datetime.datetime.now()
    # decir la hora
    hora = f"Son las {hora.hour} horas con {hora.minute}"
    hablar(hora)

#Funcion saludo inicial
def saludo():
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        estado = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        estado = "Buenos dias"
    else:
        estado = "Buenas tardes"
    hablar(f"Hola daniel. {estado} soy sus asistente personal, dime como te ayudo")

def solicitar():
    #activar saludo inicial
    saludo()

    #variable de terminar
    iniciar = True

    while iniciar:
        #Activar el microfono
        solicitar = trasformar_audio_a_texto().lower()

        if 'abrir youtube' in solicitar:
            hablar("con gusto, Dani")
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir el navegador' in solicitar:
            hablar("con gusto")
            webbrowser.open("https://www.google.com/")
            continue
        elif 'hoy' in solicitar:
            pedir_dia()
            continue
        elif 'hora' in solicitar:
            pedir_hora()
            continue
        elif 'asistente' in solicitar:
            saludo()

        elif 'wikipedia' in solicitar:
            print("estoy en wiki")
            hablar("estoy buscando, en wikipedia")
            solicitar = solicitar.replace("busca en wikipedia", '')
            wikipedia.set_lang('es')
            #Hace q lea el primer parrafo
            resultado = wikipedia.summary(solicitar, sentences=1)
            hablar(resultado)
            continue

        elif 'busca en internet' in solicitar:
            print("estoy en wiki")
            hablar("estoy buscando, en internet")
            solicitar = solicitar.replace("busca en internet", '')
            pywhatkit.search(solicitar)
            hablar(resultado)
            continue
        elif 'reproducir' in solicitar:
            hablar("por su puesto")
            pywhatkit.playonyt(solicitar)
            continue
        elif 'broma' in solicitar:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de acciones' in solicitar:
            acciones = {'apple': 'APPL', 'amazon': 'AMZN'}
            accion = solicitar.split('de')[-1].strip()
            try:
                accion_buscada = acciones[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                hablar(f"encontre que {accion_buscada}")
                continue
            except:
                hablar("no encontre")
                continue

        elif 'gracias' in solicitar:
            hablar("de, nada")
        elif 'puedes irte' in solicitar:
            hablar("ok, si me necesitas, llamame")
solicitar()
