import os
import yaml
import re
from bs4 import BeautifulSoup
from .fetch_html_selenium import fetch_html_selenium
from .process_html import process_html
from .md_splitter import split_markdown_document
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document

class ConfluenceCrawler:

    def __init__(self, base_url, verbosity=1):
        self.base_url = base_url
        self.verbosity = verbosity
        self.visited_urls = set(base_url)

        # Load configuration from YAML
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, '..', 'config.yaml')

        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        self.base_domain = config['base_url']

        # get the path of the faiss database and create it if it doesn't exist.
        self.faiss_path = config['faiss_data_dir']
        os.makedirs(self.faiss_path, exist_ok=True)

    def extract_links_from_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True) ]
        pattern = re.compile(r'.*/TPD/pages/\d+/')
        valid_links = [link if link.startswith('http') else self.base_domain + link for link in links if pattern.match(link) and 'login' not in link]
        return valid_links

    def explore_space(self, url, depth=3):
        if depth == 0 or url in self.visited_urls:
            return

        html_content = fetch_html_selenium(url)
        if not html_content:
            return  # Skip processing for invalid pages

        # add the url to the visited
        self.visited_urls.add(url)

        # process the content
        if self.verbosity > 2:
            # print(html_content)
            pass

        # if we aren't on the "pages" url
        if depth > 0:
            result = process_html(html_content, url)

            # display if needed
            if result and self.verbosity >= 1:
                print(result['content'])

            if result:
                # save into FAISS.
                chunks = split_markdown_document(result['content'], depth=3)
                documents = [Document(page_content=chunk, metadata=result['metadata']) for chunk in chunks]
                faiss_index = FAISS.from_documents(documents, embedding=OpenAIEmbeddings())
                faiss_db = os.path.join(self.faiss_path, result['metadata']['title'])
                faiss_index.save_local(faiss_db)


        # extract the links and explore
        links = self.extract_links_from_html(html_content)
        valid_links = [link for link in links if link not in self.visited_urls]
        if self.verbosity > 1:
            print(f"Collected URLs from {url}:")
            for link in valid_links:
                print(f" - {link}")
        # valid_links = [link for link in links if is_valid_link(link)]

        for link in valid_links:
            self.explore_space(link, depth-1)

        


