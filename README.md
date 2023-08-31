# Summarize webpages using OpenAI Completion APIs

This script is used to summarize the text content of a webpage by using the OpenAI Completion API. It uses the requests library to fetch the HTML content of a webpage, html2text to convert the HTML content to plain text and OpenAI completion API to generate a summary of the text content.

# Requirements
* Python 3
* openai API key and organization
* requests
* html2text
* tomli
* GPTCommons (as submodule)

# Usage
To use this script, you need to provide the `--lang` and the `--url` of the webpage as command line arguments.  
For example:  
`$ python Web_AI_Sum.py --lang French --url https://www.example.com`  
The script also requires an `openai.toml` file with the API key, organization details for the OpenAI API, model to be used and the maximum number of tokens per request.  
The config file should contain the following information:  
`[openai]`
- `apikey = "your_api_key"`
- `organization = "your_organization"`
- `model = "gtp-4"`
- `maxtokens = "1000"`

The script will then fetch the HTML content of the webpage, convert it to plain text, and generate a summary using the OpenAI API. The summary will be printed to the console.
