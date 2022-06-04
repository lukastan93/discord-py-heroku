import discord
import os
import requests
import json
import re
import random
from PIL import Image
from io import BytesIO
client = discord.Client()

def process_commands(message):
    response = requests.get("https://api.opensea.io/api/v1/collection/everyday-goddesses")
    dump = json.loads(response.text)

    content = message[1:]
    if content.split(" ")[0] in ["stats", "floor"]:
      embed=discord.Embed(title="Everyday Goddesses Stats", url="https://opensea.io/collection/everyday-goddesses/", description="Collection statistics for Everyday Goddesses.", color=discord.Color.blue())
      embed.set_author(name="MiniMort", url="https://twitter.com/nft_shiny", icon_url="https://i.imgur.com/7TkJmoi.png")
      embed.set_thumbnail(url="https://i.imgur.com/gPflHCF.png")
      embed.add_field(name="Floor Price", value="{}".format(str(dump["collection"]["stats"]["floor_price"]) + "Ξ"), inline=False)
      embed.add_field(name="1-Day Volume", value="{}".format(str(round(dump["collection"]["stats"]["one_day_volume"], 4)) + "Ξ"), inline=True)
      embed.add_field(name="1-Day Sales", value="{}".format(str(int(dump["collection"]["stats"]["one_day_sales"]))), inline=True)
      embed.add_field(name="Holder Count", value="{}".format(str(dump["collection"]["stats"]["num_owners"])), inline=True)
      return embed

    if content.split(" ")[0] == "rank":
      embed=discord.Embed(color=discord.Color.blue())
      embed.set_thumbnail(url="https://images.raritysniffer.com/500/500/ipfs/QmcKNVfrYpwYemYUFzBgbMwLaJEDj7MGaiU1BAoxDgESyx/{}.png".format(content.split(" ")[1]))
      embed.add_field(name="Token ID", value="{}".format(content.split(" ")[1]))

      response = requests.get("https://raritysniffer.dev/api/v1/collection?collection=0x9176e11a412b6ef5e8ddb045909a14112f7782b2&norm=true&traitCount=true&partial=false").json()

      for i in response["data"]:
        if i["id"] == int(content.split(" ")[1]):
          embed.add_field(name="Rank", value="{}".format(i["positionId"]))
      return embed

    if content.split(" ")[0] == "gas":
      embed=discord.Embed(title="Gas Tracker ⛽", url="https://etherscan.io/gastracker", description="Current gas prices on the ETH network.", color=0xffd500)
      page = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle").json()
      slow = page["result"]["SafeGasPrice"]
      medium = page["result"]["ProposeGasPrice"]
      fast = page["result"]["FastGasPrice"]
      embed.add_field(name="Slow", value="{}".format(slow), inline=True)
      embed.add_field(name="Medium", value="{}".format(medium), inline=True)
      embed.add_field(name="Fast", value="{}".format(fast), inline=True)
      return embed

    if content.split(" ")[0] == "img":
      embed=discord.Embed(color=discord.Color.blue())
      embed.set_image(url="https://everyday-goddesses.mypinata.cloud/ipfs/QmV9mucbh6G3NKgVnEWj9YPAeYK5c6YfyUx7XmKjPLWe1V/{}.png".format(content.split(" ")[1]))
      return embed

# def process_banner(message):
#         content = message[1:]
#         url = "https://everyday-goddesses.mypinata.cloud/ipfs/QmYozrpnGTCE9Qfs5PSzGcVYkDQXTFTgDo7pG5WJHrkGUK/{}.png".format(content.split(" ")[1])
#         background = Image.open("BG.png").convert("RGBA")
#         response = requests.get(url)
#         goddess = Image.open(BytesIO(response.content)).convert("RGBA")
#         def merge(im1, im2):
#             w = im1.size[0]
#             h = max(im1.size[1], im2.size[1])
#             im = Image.new("RGBA", (w, h))

#             im.paste(im1)
#             im.paste(im2, (int(w/3), int(h/2)), im2.convert("RGBA"))
#             return im

#         im1 = merge(background, goddess)
#         output = im1.save("output.png")
#         with open('output.png', 'rb') as f:
#           picture = discord.File(f)
#           return picture

def process_pride(message):
        content = message[1:]
        url = "https://everyday-goddesses.mypinata.cloud/ipfs/QmYozrpnGTCE9Qfs5PSzGcVYkDQXTFTgDo7pG5WJHrkGUK/{}.png".format(content.split(" ")[1])
        background = Image.open("pride.png").convert("RGBA")
        response = requests.get(url)
        goddess = Image.open(BytesIO(response.content)).convert("RGBA")
        def merge(im1, im2):
            w = im1.size[0]
            h = max(im1.size[1], im2.size[1])
            im = Image.new("RGBA", (w, h))

            im.paste(im1)
            im.paste(im2, im2.convert("RGBA"))
            return im

        im1 = merge(background, goddess)
        output = im1.save("output.png")
        with open('output.png', 'rb') as f:
          picture = discord.File(f)
          return picture



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$banner'):
        result = process_banner(message.content)
        await message.channel.send(file = result)

    elif message.content.startswith('$'):
        result = process_commands(message.content)
        await message.channel.send(embed = result)

    else:
      return "Invalid command."

client.run(os.getenv('TOKEN'))