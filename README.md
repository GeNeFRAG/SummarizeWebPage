# Summarize Webpages Using OpenAI Completion APIs

This script summarizes the text content of a webpage using the OpenAI Completion API.

## Requirements
* Python 3
* openai
* requests
* html2text
* tomli
* tiktoken
* GPTCommons (as submodule)

## Usage

To use this script, provide the following command-line arguments:

### Arguments

- `--url`: URL of the webpage.
- `--lang`: (Optional) Language of the summary (default: English).
- `--output`: (Optional) Output file name (default: STDOUT).
- `--html`: (Optional) Convert output to HTML (default: False).
- `--detail_level`: (Optional) Detail level of the summary (default: analytical).
- `--max_words`: (Optional) Maximum number of words for the summary (default: 200).

### OpenAI Configuration

The script requires an `openai.toml` file with API key, organization details, model, and maximum tokens per request. The config file should have the following format:

`[openai]`
- `apikey = "your_api_key"`
- `organization = "your_organization"`
- `model = "gpt-4"`
- `maxtokens = "1000"`

### Example

`$ python Web_AI_Sum.py --lang English --url https://yoururl.com --output yourfile.html --html True --detail_level high --max_words 500`

## Installation

To install the dependencies listed in the requirements.txt file, you can use the following command:

`pip install -r requirements.txt`

## Including GPTCommons.py

Ensure that the GPTCommons.py file is in your Python path

`git clone https://github.com/GeNeFRAG/GPT_commons.git`