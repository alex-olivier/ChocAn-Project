import re

# Validate user input with retry on failure
def prompt_until_valid(regex, prompt_message, error_message) -> str:
    while True:
        value = input(prompt_message)
        if re.match(regex, value):
            return value
        print(error_message)
