
def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'You\'re quiet'
    elif 'hello' in lowered:
        return 'Hello there!'
    
    