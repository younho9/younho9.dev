import os
import config
import urllib.request

from datetime import datetime
from notion.client import NotionClient

collection_id = config.id
token = os.environ.get("NOTION_TOKEN")

client = NotionClient(token_v2=token)
contents_collection = client.get_collection(collection_id)
posts = contents_collection.get_rows()

# Main Loop
for post in posts:
    # Post Filter 
    if(post.status == "🖨 Published"):
        continue
    # if(post.status == "✅ Completed"):
    #     continue
    if(post.status == "🛠 In Progress"):
        continue
    if(post.status == "📅 Planned"):
        continue
    if(post.status == "🤔 Being Considered"):
        continue
    if(post.status == "🧪 Test"):
        continue

    # Handle Frontmatter
    title = post.title.replace("[", "")
    title = title.replace("]", "")
    text = """---
title: %s
author: younho9
date: %s
excerpt: %s
""" % (title, post.created_time.strftime("%Y-%m-%d"), post.excerpt)
    
    # Handles slug url
    print("-------------------------------------------------------")
    print('📝 Title is "' + post.title + '"')
    slug = input("🔗 Add slug : ")
    text = text + "slug: " + slug + "\n"
    
    # Handles hero Image
    if not post.hero:
        text = text + "---\n\n"
    elif "png" in post.hero[0]:
        text = text + "hero: " + "./images/hero.png\n---\n\n"
        image_format = "png"
    elif "jpg" in post.hero[0]:
        text = text + "hero: " + "./images/hero.jpg\n---\n\n"
        image_format = "jpg"

    # Get blog post
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
            text = text + "```" + block.language.lower() + "\n" + block.title + "\n```\n\n"
        # Handles Callout Blocks
        if (block.type == "callout"):
            text = text + "> " + block.icon + " " + block.title + "\n\n"
        # Handles Quote Blocks
        if (block.type == "quote"):
            text = text + "> " + block.title + "\n\n"
        # Handles Bookmark Blocks
        if (block.type == "bookmark"):
            text = text + "🔗 [" + block.title + "](" + block.link + ")\n\n"
        # Handles Images
        if (block.type == "image"):
            text = text + "![" + block.id + "](" + block.source + ")\n\n"
        # Handles Bullets
        if (block.type == "bulleted_list"):
            text = text + "- " + block.title + "\n\n"
        # Handles Dividers
        # if (block.type == "divider"):
        #     text = text + "---" + "\n\n"
        # Handles Basic Text, Links, Single Line Code
        if (block.type == "text"):
            text = text + block.title + "\n\n"

    # Make blog post directory
    dir_name = "../content/posts/" + post.created_time.strftime("%Y-%m-%d") + "-" + slug
    try:
        os.mkdir(dir_name)
    except:
        pass

    # Handles post cover Image
    if post.hero:
        try:
            os.mkdir(dir_name + "/images")
        except:
            pass
        if "png" in post.hero[0]:
            urllib.request.urlretrieve(post.hero[0], dir_name + "/images/hero.png")
        elif "jpg" in post.hero[0]:
            urllib.request.urlretrieve(post.hero[0], dir_name + "/images/hero.jpg")
    
    file = open(dir_name + "/index.md", "w")
    print(text)
    print("✅ Successfully exported blog content to" + dir_name + "/index.md")
    file.write(text)