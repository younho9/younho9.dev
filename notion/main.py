import config
import argparse
import sys

from notion_to_blog import get_contents_from_notion

if __name__ == "__main__":
    description = "Export blog contents from Notion"
    parser = argparse.ArgumentParser(description=description)

    url = config.url
    token = config.token_v2

    get_contents_from_notion(token, url)
    