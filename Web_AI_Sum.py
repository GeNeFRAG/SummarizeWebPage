import re
import string
import sys

import html2text
import openai
import requests
import tomli

SPECIAL_CHARACTERS = string.punctuation + "“”‘’"
PATTERN = re.compile(r'[\n\s]+')

def split_into_chunks(text, chunk_size=1000, overlap_percentage=1):
    #split the web content into chunks of 1000 characters
    text = clean_text(text)

    # Calculate the number of overlapping characters
    overlap_chars = int(chunk_size * overlap_percentage)

    # Initialize a list to store the chunks
    chunks = []

    # Loop through the text with the overlap
    for i in range(0, len(text), chunk_size - overlap_chars):
        # Determine the end index of the current chunk
        end_idx = i + chunk_size

        # Slice the text to form a chunk
        chunk = text[i:end_idx]

        # Append the chunk to the list
        chunks.append(chunk)

    return chunks

def clean_text(text):
    # Replace line breaks and consecutive whitespace with a single space
    text = re.sub(PATTERN, ' ', text).strip()
    
    # Handle special characters (replace with spaces or remove them)
    text = ''.join(char if char not in SPECIAL_CHARACTERS else ' ' for char in text)
    
    return text

def get_completion(prompt, model, temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_arg(arg_name, default=None):
    """
    Safely reads a command line argument by name.
    :param arg_name: the name of the argument to read.
    :param default: the default value to return if the argument is not found.
    :return: the value of the argument if found, or the default value.
    """
    if "--help" in sys.argv:
        print("Usage: python Web_AI_Sum.py [--help] [--lang] [--url]")
        print("Arguments:")
        print("\t--help\t\tHelp\t\tNone")
        print("\t--lang\t\tLanguage\tEnglish")
        print("\t--url\t\tURL\t\tNone")
        # Add more argument descriptions here as needed
        sys.exit(0)
    try:
        arg_index = sys.argv.index(arg_name)
        arg_value = sys.argv[arg_index + 1]
        return arg_value
    except (IndexError, ValueError):
        return default

# This function takes a url as input and returns the text content of the webpage
def get_text_from_html(url):
    html = url.text

    # Create an instance of HTML2Text
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.bypass_tables = True
    text_maker.ignore_images = True

    # Extract the text content from the html
    text = text_maker.handle(html)
    
    return text

# This function takes in the text content of the webpage and generates a summary using OpenAI API
def show_text_summary(text):
    if text is None:
        return
    try:
        # tldr tag to be added at the end of each summary
        tldr_tag = "\n tl;dr:"
    
        #split the web content into chunks of 1000 characters
        string_chunks = split_into_chunks(text, 9000, 0.5)

        # Iterate through each chunkprint(f"Summarizing transcript using OpenAI completion API with model {gptmodel}")
        print(f"Summarizing website content using OpenAI completion API with model {gptmodel}")
        responses = [get_completion(f"""You will be provided with text from any webpage delimited by triple backtips. Your task is to summarize the chunks in a distinguished analytical executive summary style. Reply in Language {lang}.```{chunk}```""", gptmodel) for chunk in string_chunks]
        complete_response_str = "\n".join(responses)
        complete_response_str = clean_text(complete_response_str)

        print(f"Remove duplicate or redundant information using OpenAI completion API with model {gptmodel}")
        prompt = f"""Your task is to remove duplicate or redundant information in the provided text delimited by triple backtips. \
                Provide the answer in at most 5 bulletpoint sentences and keep the tone of the text and at most 100 words. \
                Your task is to create smooth transitions between each bulletpoint.
        ```{complete_response_str}```
                """
        response = get_completion(prompt, gptmodel, 0.2)
        print(response)
    except Exception as e:
        print("Error: Unable to generate summary for the Webpage.")
        print(e)
        return None

# Reading out OpenAI API keys and organization
try:
    with open("openai.toml","rb") as f:
        data = tomli.load(f)
        openai.api_key=data["openai"]["apikey"]
        openai.organization=data["openai"]["organization"]
        gptmodel=data["openai"]["model"]
        maxtokens = int(data["openai"]["maxtokens"])
except:
    print("Error: Unable to read openai.toml file.")
    sys.exit(1)

# Getting language, url from command line
lang=get_arg('--lang','English')
url_str=get_arg('--url', None)
if(url_str == None):
    print("Type “--help\" for more information.")
    sys.exit(1)

# Execute
print(f"Fetching text from Website")
show_text_summary(get_text_from_html(requests.get(url_str)))