import openai
from bs4 import BeautifulSoup
import os
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def process_html(html_content, url):
    # Load configuration from YAML
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '..', 'config.yaml')

    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Extract the main content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    content_div = soup.find('div', class_='wiki-content')
    main_content = content_div.get_text() if content_div else None
    
    # Extract the title from the URL
    title = url.split("/")[-1]

    if main_content:
    
        # Construct the prompt for OpenAI
        system_prompt = """
    You are a html and markdown expert.
    The provided content is coming from a webcrawler used to read confluence content.
    It's html.
    If the html includes hmtl links, keep those and transform those as markdown links.
    If the html includes images, keep those and use the url to include those an markdown images.
    Reproduce the structure of the html document the best you can, using titles, subtitles, tables, etc.
    Answer directly without any kind of additional information.
    Your answer MUST only be a markdown formatted document.
    """
        user_prompt = f"Convert the following html content titled '{title}' into a Markdown document:\n\n{main_content}"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        # Estimate tokens in the message prompt and check against half of the token limit
        token_limit = config['parsing_model']['max_token'] // 2
        total_tokens = estimate_token_count(system_prompt) + estimate_token_count(user_prompt)

        if total_tokens > token_limit:
            # Truncate the main content
            excess_words = (total_tokens - token_limit) // 0.75
            main_content_words = main_content.split()[:-int(excess_words)]
            main_content = ' '.join(main_content_words)
            user_prompt = f"Convert the following html content titled '{title}' into a Markdown document:\n\n{main_content}"
            messages[-1]['content'] = user_prompt  # Update the message
            
            # Display a warning in red
            percentage_kept = (len(main_content_words) / len(main_content.split())) * 100
            warning_message = f"\033[91mWARNING: Truncating content due to token limit. Total tokens: {total_tokens}. Percentage of text kept: {percentage_kept:.2f}%. Source URL: {url}\033[0m"
            print(warning_message)

        # Send the prompt to the OpenAI API
        model = config['parsing_model']['model']
        print(f"Sending html page '{title}' to openai api, model '{model}', for processing")
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=config['parsing_model']['temperature']
        )

        markdown_content = response.choices[0]['message']['content'].strip()

        # Gather results and metadata
        result = {
            "content": markdown_content,
            "metadata": {
                "source": url,
                "title": title
            }
        }
        
        return result

def estimate_token_count(text):
    # A rough estimate based on the average tokens per word for English content
    word_count = len(text.split())
    estimated_tokens = int(word_count * 0.75)
    return estimated_tokens
