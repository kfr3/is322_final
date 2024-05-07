from transformers import pipeline
import re

def img2text(url):
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    text = image_to_text(url)[0]["generated_text"]
    return text

def is_url(text: str) -> bool:
    url_regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    return re.match(url_regex, text) is not None
    
def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'You\'re quiet'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif is_url(user_input):
        processed_text = img2text(user_input)
        return processed_text
    else:
        return 'I\'m not sure how to respond to that.'
    
    