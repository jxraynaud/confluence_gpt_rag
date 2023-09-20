import argparse
import os
import sys
import asyncio
import yaml
from confluence_rag_builder.confluence_crawler import ConfluenceCrawler

def setup_arg_parser():
    parser = argparse.ArgumentParser(description="Confluence Data Parser Script")

    # Add verbosity argument
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help="Increase verbosity level. Can be specified multiple times, e.g., -vvv for highest verbosity.")

    return parser

def main():
    args = setup_arg_parser().parse_args()

    # Load configuration from YAML
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '..', 'config.yaml')

    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    BASE_URL = config['base_url'] + '/wiki/spaces/TPD/pages'

    # Initialize the crawler
    crawler = ConfluenceCrawler(BASE_URL, verbosity=args.verbose)

    # Depending on the verbosity level, you can adjust logging or print statements.
    if args.verbose == 1:
        # Level -v: Add some basic logging here, for instance:
        print("Starting the data parser with basic verbosity...")
    elif args.verbose == 2:
        # Level -vv: Add more detailed logging here
        print("Starting the data parser with detailed verbosity...")
    elif args.verbose >= 3:
        # Level -vvv: Add the most detailed logging here
        print("Starting the data parser with maximum verbosity...")


    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    crawler.explore_space(BASE_URL)


if __name__ == "__main__":
    main()
