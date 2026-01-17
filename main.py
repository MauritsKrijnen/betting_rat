import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

## Import classes
import api

## Setup variables
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
new_api = api.Api

# Setup logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
# Create discord bot object
bot = commands.Bot(command_prefix='/', intents=intents)

## Events
@bot.event
async def on_ready():
    print(f"Let's go gambling!")

## Commands
@bot.command()
async def check_market_rate(ctx, market_name):
    market = new_api.api_get_market(market_name)
    if market!=None:
        prices = new_api.api_get_market_prices(new_api, market)
        if prices[0]!=None:
            await ctx.send(f"The buy price for {market_name} are buy: {prices[0]} and sell: {prices[1]}")
            return
    await ctx.send("Market get request denied")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)