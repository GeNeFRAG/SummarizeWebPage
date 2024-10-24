import sys
import requests
import html2text
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
    print("Fetching HTML content from the URL...")
    html = url.text

    # Create an instance of HTML2Text
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.bypass_tables = True
    text_maker.ignore_images = True

    print("Extracting text content from the HTML...")
    # Extract the text content from the HTML
    text = text_maker.handle(html)
    
    print("Text extraction complete.")
    return text

def show_text_summary(text, output_file=None, to_html=False, detail_level='analytical', max_words=200):
    """
    Generates a text summary of a given input text, removes duplicate or redundant information, and prints the result.
    If an output file is specified, writes the summary to the file instead of printing it.
    If to_html is True, converts the summary to HTML format before writing to the file.

    Args:
    text (str): The input text to be summarized and cleaned.
    output_file (str, optional): The path to the file where the summary should be written. Defaults to None.
    to_html (bool, optional): Whether to convert the summary to HTML format. Defaults to False.

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
        print("No text found to summarize.")
        return
    try:
        # Split the web content into chunks of 1000 characters
        print("Splitting the text into manageable chunks...")
        string_chunks = commons.split_into_chunks(text, commons.get_maxtokens(), 0.5)

        # Iterate through each chunk
        print(f"Summarizing website content using OpenAI completion API with model {commons.get_gptmodel()}. Detail level {detail_level}, max. words {max_words}...")
        
        responses = [
                    commons.get_chat_completion(
                            f"""Extract the key points and main ideas from the following text in an {detail_level} style. 
                            Focus on the most important information and key statements. Reply in {lang}. 
                            Text: ```{chunk}```"""
                         ) 
                        for chunk in string_chunks
                    ]
        complete_response_str = "\n".join(responses)
        complete_response_str = commons.clean_text(complete_response_str)

        # Reduce the text to the maximum number of tokens
        print("Reducing the text to the maximum number of tokens...")
        complete_response_str = commons.reduce_to_max_tokens(complete_response_str)

        print(f"Removing duplicate or redundant information using OpenAI completion API with model {commons.get_gptmodel()}...")
        prompt = f"""Remove duplicate or redundant information from the text below, keeping the tone consistent. Provide the answer in bullet points, and a maximum of {max_words} words.
                    Text: ```{complete_response_str}```"""
        response = commons.get_chat_completion(prompt)
        
        commons.write_summary_to_file(response, output_file, to_html)
    except Exception as e:
        print("Error: Unable to generate summary for the webpage.")
        print(e)
        return None

# Initialize Utility class
print("Initializing GPTCommons utility class...")
commons = GPTCommons.initialize_gpt_commons("openai.toml")

arg_descriptions = {
    "--help": "Help",
    "--lang": "Language (default: English)",
    "--url": "URL",
    "--output": "Output file name",
    "--html": "Convert output to HTML format (default: False)",
    "--detail_level": "Detail level (default: analytical)",
    "--max_words": "Maximum number of words of the summary (default: 200)"
}

# Getting language, url, output file, and html option from command line
print("Retrieving command-line arguments...")
lang = commons.get_arg('--lang', arg_descriptions, 'English')
url_str = commons.get_arg('--url', arg_descriptions, None)
output_file = commons.get_arg('--output', arg_descriptions, None)
to_html = commons.get_arg('--html', arg_descriptions, 'False').lower() == 'true'
detail_level = commons.get_arg('--detail_level', arg_descriptions, 'analytical')
# Parse max_length with error handling
try:
    max_words = int(commons.get_arg('--max_words', arg_descriptions, 200))
except ValueError:
    print("Error: Invalid value for --max_words. It must be an integer. Using default value of 200.")
    max_words = 200

if url_str is None:
    print("Error: URL not provided. Type '--help' for more information.")
    sys.exit(1)

# Check if the model exisits
print("Checking if the model exists...")
if not commons.is_valid_gpt_model(commons.get_gptmodel()):
    sys.exit(1)

# Execute
print(f"Fetching text from the website: {url_str}")
show_text_summary(get_text_from_html(requests.get(url_str)), output_file, to_html, detail_level, max_words)