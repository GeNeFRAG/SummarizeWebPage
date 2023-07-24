import re
import string
import sys

import html2text
import openai
import requests
import tomli


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
    # Remove line breaks and replace with spaces
    text = text.replace('\n', ' ')
    
    # Normalize whitespace (remove extra spaces, tabs, etc.)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Handle special characters (replace with spaces or remove them)
    special_characters = string.punctuation + "“”‘’"
    text = ''.join(char if char not in special_characters else ' ' for char in text)
    
    # Remove consecutive spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
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
        arg_value = sys.argv[sys.argv.index(arg_name) + 1]
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
        #model_list = openai.Model.list() 
    
        #split the web content into chunks of 1000 characters
        string_chunks = split_into_chunks(text, 9000, 0.5)

        #iterate through each chunk
        responses = ""
        for chunk in string_chunks:
            chunk = chunk + tldr_tag
            prompt = f"""You will be provided with text from any webpage delimited by triple backtips.\
                        Your task is to summarize the chunks in an executive summary style. \
                        Provide the answer in at most 5 bulletpoint sentences and at most 100 words. \
                        Respond \"Unsure about answer\" if not sure about the answer. \
                        Reply in Language {lang}.\
                        ```{chunk}```
                        """

             # Call the OpenAI API to generate summary
            response = get_completion(prompt, gptmodel)

            # Store the summary
            responses = responses + response

        responses = clean_text(responses)

        prompt = f"""Your task is to remove duplicate or similar information in provided text delimited by triple backtips. \
                Keep the bulletpoint sentance format. \
                Your task is to create smooth transitions between each bulletpoint.
        ```{responses}```
                """
        response = get_completion(prompt, gptmodel, 0.2)
        print(response)

    except Exception as e:
        print("Error: Unable to generate summary for the Webpage.")
        print(e)
        return None

# START OF SCRIPT
#Reading out OpenAI API keys and organization
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
text = get_text_from_html(requests.get(url_str))
show_text_summary(text)