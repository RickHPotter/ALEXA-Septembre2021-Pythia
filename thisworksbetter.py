import logging

from ask_sdk_core.utils import is_intent_name, is_request_type, get_intent_name

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_core.dispatch_components import ( AbstractRequestHandler, AbstractExceptionHandler, 
                                               AbstractResponseInterceptor, AbstractRequestInterceptor )

from ask_sdk_model import (  Response, IntentRequest, DialogState, SlotConfirmationStatus, Slot )
from ask_sdk_model.dialog import ( ElicitSlotDirective, DelegateDirective )
from ask_sdk_model.slu.entityresolution import StatusCode

import json
import requests
from requests.auth import HTTPBasicAuth

##############################################################
#      **       **         ********   **     **       **     #
#     ****     /**        /**/////   //**   **       ****    #
#    **//**    /**        /**         //** **       **//**   #
#   **  //**   /**        /*******     //***       **  //**  #
#  **********  /**        /**////       **/**     ********** #
# /**//////**  /**        /**          ** //**   /**//////** #
# /**     /**  /********  /********   **   //**  /**     /** #
# //      //   ////////   ////////   //     //   //      //  #
##############################################################

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestIntentHandler")
        
        speak_output = "O que deseja, patrão?"
        ask_output = "Acelera, meu Consagrado."
        handler_input.response_builder.speak(speak_output).ask(ask_output)
        
        return handler_input.response_builder.response

class SeteIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):

        # type: (HandlerInput) -> bool
        return is_intent_name("SeteIntent")(handler_input)

    def handle(self, handler_input):

        slots = handler_input.request_envelope.request.intent.slots
        cod = slots['cod']
        
        # use speak without ask and Amazon will knock on your door with amazon guns and bezos cum to poison you
        speech = getRequest(cod.value, 'CODFIGURA')
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Capaz."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Adeus!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Você que lute."
        reprompt = "Por que choras?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = get_intent_name(handler_input)
        speak_output = "Motivo do meu colapso: " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Não sou eu. É você."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

#############################################################################################################
#  ********   **     **   ****     **     ******    **********   **     *******     ****     **    ******** #
# /**/////   /**    /**  /**/**   /**    **////**  /////**///   /**    **/////**   /**/**   /**   **//////  #
# /**        /**    /**  /**//**  /**   **    //       /**      /**   **     //**  /**//**  /**  /**        #
# /*******   /**    /**  /** //** /**  /**             /**      /**  /**      /**  /** //** /**  /********* #
# /**////    /**    /**  /**  //**/**  /**             /**      /**  /**      /**  /**  //**/**  ////////** #
# /**        /**    /**  /**   //****  //**    **      /**      /**  //**     **   /**   //****         /** #
# /**        //*******   /**    //***   //******       /**      /**   //*******    /**    //***   ********  #
# //          ///////    //      ///     //////        //       //     ///////     //      ///   ////////   #
#############################################################################################################

def getRequest(url_compound : str, data : str):

    url = 'http://177.72.161.199:7770/clientes?codcli=' + url_compound
    headers = { 'x-tipo-retorno': 'E' }

    response = requests.get(url, headers = headers, auth = HTTPBasicAuth('SUPERVISOR', 'SUPERV'))

    cambridge = response.json()
    #return str(response.text)
    return (data + ': ' + str(cambridge[0][data.upper()]))

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SeteIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()