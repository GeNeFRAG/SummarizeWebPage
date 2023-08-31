import sys

import html2text
import openai
import requests
import tomli

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

def show_text_summary(text):
    """
    Generates a text summary of a given input text, removes duplicate or redundant information, and prints the result.

    Args:
    text (str): The input text to be summarized and cleaned.

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
        # tldr tag to be added at the end of each summary
        tldr_tag = "\n tl;dr:"
    
        #split the web content into chunks of 1000 characters
        string_chunks = commons.split_into_chunks(text, maxtokens, 0.5)

        # Iterate through each chunkprint(f"Summarizing transcript using OpenAI completion API with model {gptmodel}")
        print(f"Summarizing website content using OpenAI completion API with model {gptmodel}")
        responses = [commons.get_completion(f"""You will be provided with text from any webpage delimited by triple backtips. Your task is to summarize the chunks in a distinguished analytical summary style. Reply in Language {lang}.```{chunk}```""", gptmodel, temperature) for chunk in string_chunks]
        complete_response_str = "\n".join(responses)
        complete_response_str = commons.clean_text(complete_response_str)

        print(f"Remove duplicate or redundant information using OpenAI completion API with model {gptmodel}")
        prompt = f"""Your task is to remove duplicate or redundant information in the provided text delimited by triple backtips. \
                Provide the answer in at most 5 bulletpoint sentences and keep the tone of the text and at most 500 words. \
                Your task is to create smooth transitions between each bulletpoint.
        ```{complete_response_str}```
                """
        response = commons.get_completion(prompt, gptmodel, temperature)
        print(response)
    except Exception as e:
        print(f"Error: Unable to generate summary for the Webpage.")
        print(e)
        return None

# Initialize GPT utilities module
commons = GPTCommons()

# Reading out OpenAI API keys and organization
try:
    with open("openai.toml","rb") as f:
        data = tomli.load(f)
except Exception as e:
    print(f"Error: Unable to read openai.toml file.")
    print(e)
    sys.exit(1)
openai.api_key=data["openai"]["apikey"]
openai.organization=data["openai"]["organization"]
gptmodel=data["openai"]["model"]
maxtokens = int(data["openai"]["maxtokens"])
temperature = float(data["openai"]["temperature"])
print(f"gptmodel={gptmodel}")
print(f"maxtokens={maxtokens}")
print(f"temperature={temperature}")

# Getting language, url from command line
lang=commons.get_arg('--lang','English')
url_str=commons.get_arg('--url', None)
if(url_str == None):
    print("Type “--help\" for more information.")
    sys.exit(1)

# Execute
print(f"Fetching text from Website")
show_text_summary(get_text_from_html(requests.get(url_str)))