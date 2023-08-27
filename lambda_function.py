import json
import logging
import utils
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)   
    
def build_response(output):
    return {
        'statusCode': 200,
        'body': json.dumps({
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': output
                },
                'shouldEndSession': True
            }
        })
    }
    
    
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input) -> Response:
        # type: (HandlerInput) -> Response
        greet_text = utils.greetResponse()
        reprompt_text = "How can I help you?"
        return handler_input.response_builder.speak(greet_text).reprompt(reprompt_text).response
    
class GPTIntentHandler(AbstractRequestHandler):
    """Handler for GPT intent."""
    def can_handler(self, handler_input):
        return ask_utils.is_intent_name("GPTIntent")(handler_input) or ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)
    
    def handler(self, handler_input):
        if ask_utils.is_intent_name("GPTIntent")(handler_input):
            query = handler_input.request_envelope.request.intent.slots["Query"].value
        else:
            query = handler_input.request_envelope.request.intent.query
        
        speech_text = utils.make_prompt(query)
        return handler_input.response_builder.speak(speech_text).response
    
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        pass
        
class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        
class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response
    
class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return (
            handler_input.request_envelope.request.intent.name == "AMAZON.FallbackIntent"
        )

    def handle(self, handler_input: HandlerInput) -> Response:
        speech_text = "I'm sorry, I didn't understand that. Please try again."

        return (
            handler_input.response_builder
                .speak(speech_text)
                .ask(speech_text)
                .response
        )

class IntentReflectorHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        response_text = f"You just triggered {intent_name}."
        return build_response(response_text)


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()