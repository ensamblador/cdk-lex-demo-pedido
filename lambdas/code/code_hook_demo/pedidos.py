import dialogstate_utils as dialog
from datetime import datetime, timedelta
import locale


def get_localized_date(date):

    # Set locale to Spanish
    locale.setlocale(locale.LC_TIME, 'es_ES')
    # Set UTC offset for Santiago, Chile
    utc_offset = -4
    santiago_offset = timedelta(hours=utc_offset)  # Create a timedelta with the UTC offset for Santiago
    localized_date = date + santiago_offset      # Add the UTC offset to the provided date and time
    formatted_date = localized_date.strftime('%A %d de %B de %Y') # Format date with weekday, day, month, and year
    return formatted_date

def get_today_minus_x_days(x):
    today = datetime.now().date()  # Get today's date without the time
    delta = timedelta(days=x)     # Create a timedelta with x days
    result = today - delta        # Subtract the timedelta from today's date
    return result

def is_number(value):
    try:
        int(value)  # Try converting the value to float
        return True   # If successful, value is a number
    except ValueError:
        return False  # If conversion fails, value is not a number


def get_tomorrow_date():
    today = datetime.now() # Get current date and time
    tomorrow = today + timedelta(days=1) # Add 1 day to get tomorrow's date
    return tomorrow.date() # Return only the date part, not the time



def estado_pedido(intent_request, messages):
    content_type =  'PlainText'

    intent = dialog.get_intent(intent_request)
    active_contexts = dialog.get_active_contexts(intent_request)
    session_attributes = dialog.get_session_attributes(intent_request)
    


    if intent['state'] == 'ReadyForFulfillment':
        
        pedido_id = dialog.get_slot('PedidoId', intent)
        print ('pedido:', pedido_id)
        PEDIDO_DEMO = messages['PEDIDO_DEMO']
        pedido_incorrecto = messages['pedido_incorrecto'].format(pedido_id=pedido_id)

        if not is_number(pedido_id): 

            return dialog.elicit_slot('PedidoId', active_contexts,session_attributes, intent,[{'contentType': 'PlainText', 'content': pedido_incorrecto}])    
        
        if int(pedido_id) > int(PEDIDO_DEMO):

            return dialog.elicit_intent( active_contexts, session_attributes, intent, [{'contentType': 'PlainText', 'content': pedido_incorrecto}])

        if int(pedido_id) < int(PEDIDO_DEMO):
            delta = (int(PEDIDO_DEMO) -int(pedido_id) ) // 500
            print('delta days:', delta)
            dia_despacho = get_localized_date(get_today_minus_x_days(delta))
            
            pedido_entregado = messages['pedido_entregado'].format(pedido_id=pedido_id, dia_despacho= dia_despacho, hora_despacho=messages['hora_despacho'])

            return dialog.elicit_intent( active_contexts, session_attributes, intent, [{'contentType': 'PlainText', 'content': pedido_entregado}])


        if pedido_id == messages['PEDIDO_DEMO']:
                
                dia_despacho =get_localized_date(get_tomorrow_date())
                pedido_entregado = messages['estado_pedido'].format(pedido_id=pedido_id, dia_despacho= dia_despacho)

                return dialog.elicit_intent(
                active_contexts, session_attributes, intent, 
                [{'contentType': 'PlainText', 'content': pedido_entregado}])
    

    elif intent['state'] == 'InProgress':
        pedido_id = dialog.get_slot('PedidoId', intent)
        pedido_no_numer = messages['pedido_no_numer']
    
        print ('pedido:', pedido_id)
        if  pedido_id:        
            if not is_number(pedido_id): 

                return dialog.elicit_slot('PedidoId', active_contexts,session_attributes, intent,[{'contentType': 'PlainText', 'content': pedido_no_numer}])    
        
        
        return dialog.delegate(active_contexts, session_attributes, intent)


    else:
        return dialog.delegate(active_contexts, session_attributes, intent)

