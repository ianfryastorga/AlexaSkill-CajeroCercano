import logging
import os
import requests
import math
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_model.services import ServiceException

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

sb = CustomSkillBuilder(api_client=DefaultApiClient())

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371  
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R * c
    return distancia

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        speech_text = "Bienvenido a Cajero Cercano. Puedo ayudarte a encontrar los cajeros y cajas vecinas más cercanos. ¿Cómo puedo ayudarte?"
        return (
            handler_input.response_builder
            .speak(speech_text)
            .ask(speech_text)
            .response
        )

class BuscarCajeroIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BuscarCajeroIntent")(handler_input)
    
    def handle(self, handler_input):
        try:
            api_access_token = handler_input.request_envelope.context.system.api_access_token
            device_id = handler_input.request_envelope.context.system.device.device_id

            logger.info(f"api_access_token: {api_access_token}")
            logger.info(f"device_id: {device_id}")

            if not api_access_token:
                speech_text = "Necesito permisos para acceder a tu ubicación. Por favor, otorga los permisos necesarios en la aplicación Alexa."
                return handler_input.response_builder.speak(speech_text).set_should_end_session(True).response

            device_address_service_client = handler_input.service_client_factory.get_device_address_service()
            address = device_address_service_client.get_full_address(device_id)

            logger.info(f"Address response: {address}")

            if address is None:
                speech_text = "No he podido obtener tu dirección. Por favor, asegúrate de que tu dirección está configurada en la aplicación Alexa y que has otorgado los permisos necesarios."
                return handler_input.response_builder.speak(speech_text).set_should_end_session(True).response

            if (not address.address_line1) and (not address.city):
                speech_text = "No he podido obtener tu dirección completa. Por favor, verifica que tu dirección está configurada correctamente en la aplicación Alexa."
                return handler_input.response_builder.speak(speech_text).set_should_end_session(True).response

            full_address = f"{address.address_line1}, {address.city}, {address.state_or_region}, {address.postal_code}, {address.country_code}"
            logger.info(f"Dirección obtenida: {full_address}")

            geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
            geocode_params = {
                'address': full_address,
                'key': os.environ['GOOGLE_API_KEY']
            }
            geocode_response = requests.get(geocode_url, params=geocode_params)
            geocode_data = geocode_response.json()

            logger.info(f"Geocode response: {geocode_data}")

            if geocode_data['status'] == 'OK':
                user_location = geocode_data['results'][0]['geometry']['location']
                lat, lng = user_location['lat'], user_location['lng']

                logger.info(f"User coordinates: lat={lat}, lng={lng}")

                places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                places_params = {
                    'location': f"{lat},{lng}",
                    'radius': 2000, 
                    'keyword': 'cajero automático OR caja vecina',
                    'key': os.environ['GOOGLE_API_KEY'],
                    'language': 'es'
                }
                places_response = requests.get(places_url, params=places_params)
                places_data = places_response.json()

                logger.info(f"Places response: {places_data}")

                if places_data['status'] == 'OK' and places_data['results']:
                    lugares = places_data['results'][:3]
                    respuestas = []
                    for lugar in lugares:
                        nombre = lugar.get('name', 'un lugar')
                        direccion = lugar.get('vicinity', 'dirección desconocida')
                        lugar_location = lugar['geometry']['location']
                        lugar_lat = lugar_location['lat']
                        lugar_lng = lugar_location['lng']

                        distancia = calcular_distancia(lat, lng, lugar_lat, lugar_lng)
                        distancia = round(distancia, 2) 

                        respuesta = f"{nombre}, ubicado en {direccion}, a {distancia} kilómetros de distancia"
                        respuestas.append(respuesta)

                    speech_text = "Aquí están los cajeros y cajas vecinas más cercanos: " + "; ".join(respuestas) + "."
                else:
                    speech_text = "No pude encontrar cajeros o cajas vecinas cercanos a tu ubicación."
            else:
                speech_text = "No pude obtener las coordenadas de tu dirección."

        except ServiceException as e:
            if e.status_code == 401 or e.status_code == 403:
                logger.error("El token de autorización ha expirado o es inválido.")
                speech_text = "Tu sesión ha expirado o no has otorgado los permisos necesarios. Por favor, otorga los permisos en la aplicación Alexa."
            else:
                logger.error(f"ServiceException al obtener la dirección: {e}")
                speech_text = "No he podido obtener tu dirección. Por favor, inténtalo de nuevo más tarde."
        except Exception as e:
            logger.error(f"Excepción al procesar la solicitud: {e}", exc_info=True)
            speech_text = "Ocurrió un error al procesar tu solicitud. Por favor, inténtalo de nuevo más tarde."

        return handler_input.response_builder.speak(speech_text).set_should_end_session(True).response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        speech_text = "Puedes pedirme que busque los cajeros más cercanos diciendo: ¿Dónde están los cajeros más cercanos?"
        return (
            handler_input.response_builder
            .speak(speech_text)
            .ask(speech_text)
            .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (
            is_intent_name("AMAZON.CancelIntent")(handler_input) or
            is_intent_name("AMAZON.StopIntent")(handler_input)
        )
    
    def handle(self, handler_input):
        speech_text = "Hasta luego."
        return (
            handler_input.response_builder
            .speak(speech_text)
            .set_should_end_session(True)
            .response
        )

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        return handler_input.response_builder.response

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(BuscarCajeroIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Lambda Handler
lambda_handler = sb.lambda_handler()
