import openai
import os
from pdfminer.high_level import extract_text
import json

# Load the configuration from the JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Initialize GPT-4 API using the API key from the config file
client = openai.OpenAI(
    api_key=config['OPENAI_API_KEY']
)

# Function to clean and format text using GPT-4
def clean_and_format_text_with_gpt(text):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": f"Clean and format the following text for readability and ensure section headers are H2 (##):\n\n{text}",
            }
        ],
    )
    formatted_text = response.choices[0].message.content.strip()
    # Extracting token usage information
    total_tokens = response.usage.total_tokens
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    return formatted_text, total_tokens, input_tokens, output_tokens

# Function to calculate cost based on token usage
def calculate_cost(input_tokens, output_tokens):
    # GPT-4o pricing
    price_per_1k_input_tokens = 0.0025
    price_per_1k_output_tokens = 0.01

    input_cost = (input_tokens / 1000) * price_per_1k_input_tokens
    output_cost = (output_tokens / 1000) * price_per_1k_output_tokens
    total_cost = input_cost + output_cost
    return total_cost

# Function to convert PDF to Markdown with AI
def pdf_to_markdown_with_ai(pdf_path, md_output_path):
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    # Extract text from PDF
    text = extract_text(pdf_path)
    # Clean and format text using GPT-4
    cleaned_text, total_tokens, input_tokens, output_tokens = clean_and_format_text_with_gpt(text)

    # Calculate cost
    cost = calculate_cost(input_tokens, output_tokens)

    with open(md_output_path, 'w') as md_file:
        md_file.write(cleaned_text)
    
    print(f'Markdown file created at {md_output_path}')
    print(f'Total tokens used: {total_tokens}')
    print(f'Input tokens: {input_tokens}')
    print(f'Output tokens: {output_tokens}')
    print(f'Estimated cost: ${cost:.4f}')

# Usage example
pdf_path = r"C:\your\dir\path\file.pdf"
md_output_path = r"C:\your\dir\path\file.md"

pdf_to_markdown_with_ai(pdf_path, md_output_path)
