import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

## Import classes
import api
import db

## Setup variables
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
poly_api = api.Api
rat_db = db.BettingRatDatabase

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
# Get market + its prices
@bot.command()
async def check_market_rate(ctx, market_name):
    market = poly_api.api_get_market(market_name)
    if market!=None:
        prices = poly_api.api_get_market_prices(poly_api, market)
        if prices[0]!=None:
            await ctx.send(f"The buy price for {market_name} are buy: {prices[0]} and sell: {prices[1]}")
            return
    await ctx.send("Market request reached an unexpected result. Check the logs for more info")

@bot.command()
async def get_tracking_markets(ctx):
    records = rat_db.get_markets()
    if records!=None:
        await ctx.send("In chronological order")
        for row in records:
            await ctx.send(f'{row[0]}: link: {row[1]}, ineterval: {row[2]}, yes price: {row[3]}, no price: {row[4]}')
    await ctx.send("Database query could not be completed. Check the logs for more info")

@bot.command()
async def add_tracking_market(ctx, name, link, interval):
    new_record = rat_db.add_market(name, link, interval)
    if new_record!=None:
        await ctx.send(f'New row has been added: {new_record[0]}: link: {new_record[1]}, ineterval: {new_record[2]}, yes price: {new_record[3]}, no price: {new_record[4]}')
    await ctx.send("Database query could not be completed. Check the logs for more info")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)