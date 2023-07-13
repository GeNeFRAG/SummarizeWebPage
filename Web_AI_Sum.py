import sys

import html2text
import openai
import requests
import tomli

def get_completion(prompt, model):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def optimize_text_for_api(text, max_tokens):
    tokenized_text = text.split()  # Tokenize the text by splitting on spaces
    if len(tokenized_text) > max_tokens:
        tokenized_text = tokenized_text[:max_tokens]  # Truncate the text to fit within the token limit
        optimized_text = ' '.join(tokenized_text)  # Join the tokens back into a string
        print("Text has been optimized to fit within the token limit.")
        return optimized_text
    else:
        return text

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
def getTextFromHTML(url):
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
def showTextSummary(text):
    if text is None:
        return
    try:
        # tldr tag to be added at the end of each summary
        tldr_tag = "\n tl;dr:"
        #model_list = openai.Model.list() 
    
        #split the web content into chunks of 1000 characters
        string_chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]

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

        responses = optimize_text_for_api(responses, maxtokens)

        prompt = f"""Your task is to remove duplicate or similar information in provided text delimited by triple backtips. \
                Your task is to create smooth transitions between each bulletpoint.
        ```{responses}```
                """
        response = get_completion(prompt, gptmodel)
        print(response)

    except Exception as e:
        print("Error: Unable to generate summary for the Webpage.")
        print(e)
        return None

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
text = getTextFromHTML(requests.get(url_str))
showTextSummary(text)