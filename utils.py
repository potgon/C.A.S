from datetime import datetime
import openai
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def greetResponse():
    current_time = datetime.datetime.now().time().hour
    if current_time >= 6 or current_time <= 12: 
        return "Good morning! How may I assist you?"
    elif current_time > 12 or current_time <= 19:
        return "Good afternoon! How may I assist you?"
    elif current_time > 19 or current_time < 6:
        return "Good evening! How may I assist you?"
    
    
def get_secret():
    """Extracts the OpenAI API key from the AWS' Secrets Manager tool

    Raises:
        e: Secret extraction generic error

    Returns:
        str: OpenAI API key
    """

    secret_name = "openai_api_key"
    region_name = "eu-west-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        logging.error("Exception extracting secret: %s", str(e))
        
    return get_secret_value_response['SecretString']

def make_prompt(prompt, model = "gpt-3.5-turbo", temperature = 0.7):
    """Sends the prompt to GPT using gpt-3.5-turbo as the default model with a default temperature of 0.7

    Args:
        prompt (str): Prompt that will be sent to OpenAI
        model (str, optional): OpenAI language model. Defaults to "gpt-3.5-turbo".
        temperature (int, optional): Prompt temperature. Determines the randomness of the response. Defaults to 0.7

    Returns:
        str: OpenAI's response
    """
    
    openai.api_key = get_secret()
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature
    )
    return response['choices'][0]['message']['content']

def is_affirmative_response(answer):
    yes_responses = ["yes", "sure", "yup", "of course", "yeah"]
    return answer in yes_responses

def is_negative_response(answer):
    no_responses = ["no", "nope", "don't", "do not", "not really", "nop"]
    return answer in no_responses