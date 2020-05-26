import argparse
import config
import os
import sys

from notion_to_blog import get_contents_from_notion

if __name__ == "__main__":
    description = "Export blog contents from Notion"
    parser = argparse.ArgumentParser(description=description)

    id = config.id
    token = os.environ.get("NOTION_TOKEN")

    get_contents_from_notion(token, id)
    