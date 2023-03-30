import sys

import html2text
import openai
import requests
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
            prompt = "Analyse and Summarize following text in short sentences and reply in " + lang + ": " + chunk
            
            # Call the OpenAI API to generate summary
            """
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=1,
                max_tokens=maxtoken,
                frequency_penalty=0.2,
                presence_penalty=0.2,
                echo=False,
                stop=["\n"]
            )
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a super smart academic researcher looking for truth"},
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
if len(sys.argv) < 3:
    print("Usage: Web_AI_Sum.py <Reply language> <URL to Website>")
    sys.exit(1)
try:
    lang=sys.argv[1]
    url=requests.get(sys.argv[2])
except Exception as e:
    print("Error retrieving commandline arguments")
    print(e)
    sys.exit(1)
    
text = getTextFromHTML(url)
showTextSummary(text)