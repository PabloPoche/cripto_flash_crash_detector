'''
send_sms.py
Contiene la funcion encargada de enviar al usuario un SMS en caso de producirse un flash crash.

- send:     Envia SMS a un usuario registrado en twilio, trial account(*).

Luego de registrado el usuario en www.twilio.com se le asigna un:
Account SID, Auth Token y un numero en twilio desde donde enviar SMS.
(*)Para la version gratuita, se dispone de un saldo de 20usd y solo puede enviarse SMS 
a usuarios registrados y con numeros verificados(ej: +5493364672xxx) en la plataforma.

'''

from twilio.rest import Client


def send(cripto):
    account = "ACabb87b4b3c2342f759fd26a9a07389ca"          # Account SID
    token = "5c2ec355afe15b9f07def11da2d740ad"              # Auth Token
    client = Client(account, token)
    message = client.messages.create(to="+5493364672xxx",   # My verified phone numbers(trial account).
                                    from_="+17246233124",   # My Twilio phone number
                                    body= cripto + " Flash Crash Detected!")
    return