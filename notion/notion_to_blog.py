import os
import urllib.request
from datetime import datetime
from notion.client import NotionClient

def get_contents_from_notion(token_v2, collection_id):
    client = NotionClient(token_v2=token_v2)
    contents_collection = client.get_collection(collection_id)
    posts = contents_collection.get_rows()

    # Main Loop
    for post in posts:
        isFirst = True
        imageFormat = 'jpg'

        # Post Filter 
        # if(post.status != "🖨 Published"):
        #     continue
        # if(post.status != "✅ Completed"):
        #     continue
        # if(post.status != "🛠 In Progress"):
        #     continue
        # if(post.status != "📅 Planned"):
        #     continue
        # if(post.status != "🤔 Being Considered"):
        #     continue
        # if(post.status != "🧪 Test"):
        #     continue

        # Handle Frontmatter
        title = post.title.replace('[', '')
        title = title.replace(']', '')
        text = """---\ntitle: %s\nauthor: younho9\ndate: %s\nexcerpt: ""\n""" % (title, post.last_edited_time.strftime("%Y-%m-%d"))
        print("-------------------------------------------------------")
        print('📝 Title is "' + post.title + '"')
        slug = input("🔗 Add slug : ")
        text = text + "slug: " + slug + "\n"
        for block in post.children:
            # Handles Cover Image
            if (isFirst):
                if (block.type == "image"):
                    hero = block.source
                    if 'png' in block.source:
                        text = text + "hero: ./images/hero.png\n---\n\n"
                        imageFormat = 'png'
                    elif 'jpg' in block.source:
                        text = text + "hero: ./images/hero.jpg\n---\n\n"
                        imageFormat = 'jpg'
                else:
                    text = text + "---\n\n"
                isFirst = False
                continue
            # Handles Images
            if (block.type == "image"):
                text = text + "![" + block.id + "](" + block.source + ")\n\n"
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
                text = text + "```" + "\n" + block.title + "\n```\n\n"
            # Handles Bullets
            if (block.type == "bulleted_list"):
                text = text + "- " + block.title + "\n\n"
            # Handles Dividers
            # if (block.type == "divider"):
            #     text = text + "---" + "\n\n"
            # Handles Basic Text, Links, Single Line Code
            if (block.type == "text"):
                text = text + block.title + "\n\n"
            if (block.type == "bookmark"):
                text = text + "🔗 [" + block.title + "](" + block.link + ")\n\n"
            isFirst = False

        dir_name = "../content/posts/" + datetime.today().strftime("%Y-%m-%d") + "-" + slug
        try:
            os.mkdir(dir_name)
            os.mkdir(dir_name + "/images")
            if (imageFormat == 'png'):
                urllib.request.urlretrieve(hero, dir_name + "/images/hero.png")    
            elif (imageFormat == 'jpg'):
                urllib.request.urlretrieve(hero, dir_name + "/images/hero.jpg")    
        except:
            pass
        file = open(dir_name + "/index.md", "w")
        file.write(text)
        print("✅ Successfully exported blog content to" + dir_name + "/index.md")