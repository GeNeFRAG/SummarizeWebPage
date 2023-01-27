import requests
import html2text
import openai
import sys
import tomli

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
            chunk = "Analyse and Summarize following text in short sentences: " + chunk
            
            # Call the OpenAI API to generate summary
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=chunk,
                temperature=1,
                max_tokens=maxtoken,
                frequency_penalty=0.2,
                presence_penalty=0.2,
                echo=False,
                stop=["\n"]
            )
            # Print the summary
            print(response["choices"][0]["text"])
       
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

# Getting max_tokens, url from command line
if len(sys.argv) == 1:
    print("Usage: SummarizeWebPage <maxtokens> <URL to Website>")
    sys.exit(1)
try:
    maxtoken=int(sys.argv[1])
    url=requests.get(sys.argv[2])
except Exception as e:
    print("Error retrieving commandline arguments")
    print(e)
    sys.exit(1)
    
text = getTextFromHTML(url)
showTextSummary(text)