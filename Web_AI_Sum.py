import sys

import html2text
import openai
import requests
import tomli
import traceback

from GPTCommons import GPTCommons

def get_text_from_html(url):
    """
    Extracts text content from HTML retrieved from a URL.

    Args:
    url (requests.Response): A Response object containing the HTML content to extract text from.

    Returns:
    str: The extracted text content from the HTML.

    Example:
    >>> import requests
    >>> url_response = requests.get('https://www.example.com')
    >>> extracted_text = get_text_from_html(url_response)
    >>> print(extracted_text)
    'This is an example web page.\nIt contains some text content.'
    """
    html = url.text

    # Create an instance of HTML2Text
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.bypass_tables = True
    text_maker.ignore_images = True

    # Extract the text content from the html
    text = text_maker.handle(html)
    
    return text

def show_text_summary(text, maxtokens, gptmodel, lang, temperature=0):
    """
    Generates a text summary of a given input text, removes duplicate or redundant information, and prints the result.

    Args:
    text (str): The input text to be summarized and cleaned.
    maxtokens (int): The maximum number of tokens for each chunk.
    gptmodel (str): The model to use for generating the summary.
    lang (str): The language for the summary.
    temperature (float): The temperature to use for generating the summary.

    Returns:
    None

    Example:
    >>> web_content = "This is a long piece of text with multiple paragraphs. It contains information about various topics."
    >>> show_text_summary(web_content)
    [Summary of the text]
    [Cleaned text with duplicate/redundant information removed]

    Note:
    The function relies on the 'split_into_chunks' and 'get_completion' functions, and it uses a specific model ('gptmodel') and language ('lang') for text generation.
    """
    if text is None:
        return
    try:
        # Split the web content into chunks of 1000 characters
        string_chunks = commons.split_into_chunks(text, maxtokens, 0.5)

        # Iterate through each chunk
        print(f"Summarizing website content using OpenAI completion API with model {gptmodel}")
        responses = [commons.get_chat_completion(f"""You will be provided with text from any webpage delimited by triple backtips. Your task is to summarize the chunks in a distinguished analytical summary style. Reply in Language {lang}.```{chunk}```""", gptmodel, temperature) for chunk in string_chunks]
        complete_response_str = "\n".join(responses)
        complete_response_str = commons.clean_text(complete_response_str)

        # Reduce the text to the maximum number of tokens
        complete_response_str = commons.reduce_to_max_tokens(complete_response_str, maxtokens, gptmodel)

        print(f"Remove duplicate or redundant information using OpenAI completion API with model {gptmodel}")
        prompt = f"""Your task is to remove duplicate or redundant information in the provided text delimited by triple backtips. \
                Provide the answer in at most 5 bulletpoint sentences and keep the tone of the text and at most 500 words. \
                Your task is to create smooth transitions between each bulletpoint.
        ```{complete_response_str}```
                """
        response = commons.get_chat_completion(prompt, gptmodel, temperature)
        print(response)
    except Exception as e:
        print(f"Error: Unable to generate summary for the Webpage.")
        print(e)
        return None

# Reading out OpenAI API keys and organization
try:
    with open("openai.toml","rb") as f:
        data = tomli.load(f)
except Exception as e:
    print(f"Error: Unable to read openai.toml file.")
    print(e)
    traceback.print_exc()
    sys.exit(1)

try:
    api_key = data["openai"]["apikey"]
    if not api_key:
        raise ValueError("API key is missing or empty in the configuration.")
except KeyError:
    raise KeyError("API key is mandatory and missing in the configuration.")

try:
    gptmodel = data["openai"]["model"]
    if not gptmodel:
        raise ValueError("Model is missing or empty in the configuration.")
except KeyError:
    raise KeyError("Model is missing in the configuration.")

try:
    maxtokens = int(data["openai"]["maxtokens"])
except KeyError:
    raise KeyError("Max tokens is mandatory and missing in the configuration.")
except ValueError:
    raise ValueError("Max tokens must be an integer.")

try:
    temperature = float(data["openai"]["temperature"])
    if not (0 <= temperature <= 1):
        raise ValueError("Temperature must be between 0 and 1.")
except KeyError:
    raise KeyError("Temperature is mandatory and missing in the configuration.")
except ValueError:
    raise ValueError("Temperature must be a float between 0 and 1.")

# Initialize GPT utilities module
commons = GPTCommons(api_key=api_key)

# Getting language, url from command line
lang=commons.get_arg('--lang','English')
url_str=commons.get_arg('--url', None)
if(url_str == None):
    print("Type “--help\" for more information.")
    sys.exit(1)

# Execute
print(f"Fetching text from Website")
show_text_summary(get_text_from_html(requests.get(url_str)), maxtokens, gptmodel, lang, temperature)