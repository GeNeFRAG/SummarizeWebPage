import sys

import html2text
import openai
import requests
import tomli

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
        model_list = openai.Model.list() 
    
        #split the web content into chunks of 1000 characters
        string_chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]

        #iterate through each chunk
        for chunk in string_chunks:
            chunk = chunk + tldr_tag
            prompt = "Analyse and Summarize following text from a Webpage. Keep the answer short and concise. As Webpage text content is normally longer than the ChatGPT limits it's splittet in chunks of 1000 characters and the prompt is send for each iteration. Respond \"Unsure about answer\" if not sure about the answer. in short sentences and reply in " + lang + ": " + chunk
            
            # Call the OpenAI API to generate summary
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI research assistant. You use a tone that is technical and scientific and the respone grammatically correct in bulletpoint sentances"},
                    #{"role": "assistant", "content": "Sure! To summarize a Webpage, you can start by identifying the main topic or theme of the Page, and then highlighting the most important information or key points mentioned. You can also condense longer sentences and remove any unnecessary details. Would you like me to provide more details on this?"},
                    {"role": "user", "content": prompt}, 
                ]
            )

            # Print the summary
            #print(response["choices"][0]["text"])
            print(response['choices'][0]['message']['content'])
       
    except Exception as e:
        print("Error: Unable to generate summary for the paper.")
        print(e)
        return None

#Reading out OpenAI API keys and organization
try:
    with open("openai.toml","rb") as f:
        data = tomli.load(f)
        openai.api_key=data["openai"]["apikey"]
        openai.organization=data["openai"]["organization"]
except:
    print("Error: Unable to read openai.toml file.")
    sys.exit(1)

# Getting language, url from command line
lang=get_arg('--lang','English')
url_str=get_arg('--url', None)
if(url_str == None):
    print("Type “--help\" for more information.")
    sys.exit(1)
    
text = getTextFromHTML(requests.get(url_str))
showTextSummary(text)