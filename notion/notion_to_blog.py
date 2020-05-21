import os
from datetime import datetime
from notion.client import NotionClient

def get_contents_from_notion(token_v2, notion_repo_url):
    client = NotionClient(token_v2=token_v2)
    notion_repo = client.get_block(notion_repo_url)
    
    # Main Loop
    for post in notion_repo.children:
        # Handle Frontmatter
        text = """---
title: %s
author: younho9
date: %s
hero: ./images/hero.jpg
excerpt: ""
""" % (post.title, datetime.today().strftime("%Y-%m-%d"))
        print("\n-------------------------------------------------------")
        print('Title is "' + post.title + '"')
        print("-------------------------------------------------------\n")
        slug = input("🔗 Add slug : ")
        text = text + "slug: " + slug + "\n---\n\n"
        for block in post.children:
            # Handles H1
            if (block.type == "header"):
                text = text + "## " + block.title + "\n\n"
            # Handles H2
            if (block.type == "sub_header"):
                text = text + "### " + block.title + "\n\n"
            # Handles H3
            if (block.type == "sub_sub_header"):
                text = text + "#### " + block.title + "\n\n"
            # Handles Code Blocks
            if (block.type == "code"):
                print("\n-------------------------------------------------------")
                print(block.title)
                print("-------------------------------------------------------\n")
                language = input("🗣  Input a language : ")
                text = text + "```" + language + "\n" + block.title + "\n```\n\n"
            # Handles Images
            if (block.type == "image"):
                text = text + "![" + block.id + "](" + block.source + ")\n\n"
            # Handles Bullets
            if (block.type == "bulleted_list"):
                text = text + "- " + block.title + "\n\n"
            # Handles Dividers
            if (block.type == "divider"):
                text = text + "---" + "\n\n"
            # Handles Basic Text, Links, Single Line Code
            if (block.type == "text"):
                text = text + block.title + "\n\n"
            if (block.type == "bookmark"):
                text = text + "🔗 [" + block.title + "](" + block.link + ")\n\n"
        print("\n-------------------------------------------------------")
        print("Title is " + post.title)
        print("-------------------------------------------------------\n")
        post_name = input("📝 Input name of post : ")
        post_name = post_name.replace(' ', '-')
        try:
            os.mkdir("../content/posts/" + datetime.today().strftime("%Y-%m-%d") + "-" + post_name)
        except:
            pass
        file = open("../content/posts/" + datetime.today().strftime("%Y-%m-%d") + "-" + post_name + "/index.md", "w")
        file.write(text)
        print("\n-------------------------------------------------------")
        print("✅Successfully exported blog content to content/posts/" + datetime.today().strftime("%Y-%m-%d") + "-"+ post_name + "/index.md")
        print("-------------------------------------------------------\n")