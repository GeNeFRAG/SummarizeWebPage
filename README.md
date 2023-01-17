<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
    <h1>README</h1>
    <p>This script is used to summarize the text content of a webpage by using the OpenAI API. It uses the <code>requests</code> library to fetch the HTML content of a webpage, <code>html2text</code> to convert the HTML content to plain text, <code>openai</code> to generate a summary of the text content, <code>sys</code> to handle command line arguments, and <code>tomli</code> to read the OpenAI API key and organization from a configuration file.</p>
    <h2>How to use</h2>
    <p>To use this script, you need to provide the <code>maxtokens</code> and the <code>URL</code> of the webpage as command line arguments. For example:</p>
    <pre>python summarizeWebPage.py 100 https://www.example.com</pre>
    <p>The script also requires an <code>openai.toml</code> file with the API key and organization details for the OpenAI API. The file should contain the following information:</p>
    <pre>
[openai]
apikey = "your_api_key"
organization = "your_organization"</pre>
    <p>The script will then fetch the HTML content of the webpage, convert it to plain text, and generate a summary using the OpenAI API. The summary will be printed to the console.</p>
    <h2>Functionality</h2>
    <p>The script has two main functions: <code>getTextFromHTML</code> and <code>showTextSummary</code>. The <code>getTextFromHTML</code> function takes a url as input and returns the text content of the webpage, while the <code>showTextSummary</code> function takes in the text content of the webpage and generates a summary using OpenAI API. The script also reads the OpenAI API key and organization from the openai.toml file.</p>
</body>
</html>