from dotenv import find_dotenv, load_dotenv
from transformers import pipeline
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from openai import OpenAI
import os
import re

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def img2text(url):
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    text = image_to_text(url)[0]["generated_text"]
    return text

def is_url(text: str) -> bool:
    url_regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    return re.match(url_regex, text) is not None

def generate_story(scenario):
    template = """
    You are a story teller;
    You can generate a short story based on a simple narrative, the story should be no more than 20 words;

    CONTEXT: {}
    STORY:
    """.format(scenario)

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # Use GPT-3.5 Turbo model
        prompt=template,  # Input prompt for text generation
        max_tokens=100,  # Maximum number of tokens to generate
        n=1,  # Number of completions to generate
        temperature=0.8,  # Controls the randomness of the generated text
        frequency_penalty=0.5,
        stop=None  # Reduce repetition
    )

    generated_text = response.choices[0].text.strip()
    return generated_text

def get_response(user_input: str) -> str:

    lowered: str = user_input.lower()

    if lowered == '':
        return 'You\'re quiet'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif is_url(user_input):
        processed_text = img2text(user_input)
        story = generate_story(processed_text) 
        processed_and_printed = True # Generate story based on image text
        return f"Image Text: {processed_text}\n\nStory: {story}"
    else:
        return 'I\'m not sure how to respond to that.'
    
    