"""
 This code sample demonstrates an implementation of the Lex Code Hook Interface
 in order to serve a bot which manages Insurance account services. Bot, Intent,
 and Slot models which are compatible with this sample can be found in the 
 Lex Console as part of the 'TelecomMobileServices' template.
"""

import time
import os
import logging

from dialogstate_utils import (get_slot)
from pedidos import (estado_pedido)

messages = { 
    'ayuda': "Te puedo ayudar a:\n - Saber donde está tu pedido \n * Recordar tu numero de pedido \
            \n\n Qué quieres hacer?",
    'saludo': "Hola, esta es una demostración de lo que se puede lograr con un Bot de Autoservicio. Prueba diciendo: ayuda.",
    'fallback': "Disculpa, eso no lo entendí. Te puedo ayudar a:\n - Saber donde está tu pedido \n - Recordar tu numero de pedido \
            \n\n Qué quieres hacer? ",
    'PEDIDO_DEMO': '111999',
    'hora_despacho': '11:35',
    'estado_pedido': "El pedido {pedido_id} se encuentra en despacho programado para el día {dia_despacho}, \
        llegando entre 9:00 y 12:00. \nAlgo más en lo que te pueda ayudar?",
    'pedido_incorrecto': "Estás seguro del número de pedido? El {pedido_id} No existe. Revisa y vuelvea intentarlo.",
    'pedido_entregado': "El {pedido_id} ya fue entregado el día {dia_despacho} a las {hora_despacho}.",
    'pedido_no_numer': "Revisa bien. El número de pedido debería ser de 6 o más dígitos. Intenta nuevamente."

}
logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)

# --- Main handler & Dispatch ---

def get_intent(intent_request):
    interpretations = intent_request['interpretations']
    if len(interpretations) > 0:
        return interpretations[0]['intent']
    else:
        return None

def dispatch(intent_request):
    """
    Route to the respective intent module code
    """
    #print(intent_request)
    intent = get_intent(intent_request)
    intent_name = intent['name']
    session_attributes = intent_request['sessionState']['sessionAttributes']
    if intent_name == 'FallbackIntent':
        return {
            'sessionState': {
                'sessionAttributes': session_attributes,
                'activeContexts': [],
                'dialogAction': {
                    'type': 'ElicitIntent'
                },
                "state": "Fulfilled"
            },
            'requestAttributes': {},
        'messages':[{'contentType': 'PlainText', 'content': messages['fallback']}]
        }

    
   
    if intent_name == 'Ayuda':
        return {
            'sessionState': {
                'sessionAttributes': session_attributes,
                'activeContexts': [],
                'dialogAction': {
                    'type': 'ElicitIntent'
                },
                "state": "Fulfilled"
            },
            'requestAttributes': {},
        'messages': [{'contentType': 'PlainText', 'content': messages['ayuda']}]
        }
    
    if intent_name == 'Saludo':
        return {
            'sessionState': {
                'sessionAttributes': session_attributes,
                'activeContexts': [],
                'dialogAction': {
                    'type': 'ElicitIntent'
                },
                "state": "Fulfilled"
            },
            'requestAttributes': {},
        'messages': [{'contentType': 'PlainText', 'content': messages['saludo']}]
            
        }
    

    
    if intent_name == 'EstadoPedido':
        return estado_pedido(intent_request, messages)




def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/Santiago'
    time.tzset()
    print('event: ', event)

    return dispatch(event)
