import argparse
import os
import sys

from notion_to_blog import get_contents_from_notion

if __name__ == "__main__":
    description = "Export blog contents from Notion"
    parser = argparse.ArgumentParser(description=description)

    url = "https://www.notion.so/younho9/Blog-post-younho9-dev-f48c98cb9344475f9b720956b2b72f99"
    token = os.environ.get("NOTION_TOKEN")

    get_contents_from_notion(token, url)
    