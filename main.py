import discord
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

## Import classes
from api import Api
from db import BettingRatDatabase

## Setup variables
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
poly_api = Api
rat_db = BettingRatDatabase()

# Setup logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
# Create discord bot object
bot = discord.Client(command_prefix='!', intents=intents)
tree= app_commands.CommandTree(bot)

## Events
@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=464877582807072788))
    print(f"Let's go gambling!")

## Commands
# Note that for events you need to copy the market name the link/chain icon abovce the polymarket logo
@tree.command(name="check_market_rates",
              guild=discord.Object(id=464877582807072788), 
              description="Returns the yes and no price of given market. ")
async def check_market_rate(interaction, market_name: str):
    # api get request to get token(needed for price request)
    market = poly_api.api_get_market(market_name)
    # if api was succesfull do
    if market!=None:
        # api get request  yes/no
        prices = poly_api.api_get_market_prices(poly_api, market)
        # if api was succesfull do
        if prices[0]!=None:
            await interaction.response.send_message(f"The buy price for {market_name} are buy: {prices[0]} and sell: {prices[1]}")
            return
    await interaction.response.send_message("Market request reached an unexpected result. Check the logs for more info")

@tree.command(name="add_tracking_market",
              guild=discord.Object(id=464877582807072788), 
              description="Add a market to the db for continues updates")
async def add_tracking_market(interaction, name: str, link: str, interval: str):
    new_record = rat_db.add_market(name, link.split("/")[-1], interval)
    # if db query was succesfull do
    if new_record!=None:
        await interaction.response.send_message(f'New row has been added: {new_record[0]}: link: {new_record[1]}, ineterval: {new_record[2]}')
    await interaction.response.send_message("Database query could not be completed. Check the logs for more info")

@tree.command(name="get_tracking_markets", 
              guild=discord.Object(id=464877582807072788), 
              description="Get the current list of markets added to the db")
async def get_tracking_markets(interaction):
    records = rat_db.get_markets()
    # if db query was succesfull do
    if records!=None:
        await interaction.response.send_message("In chronological order")
        for row in records:
            await interaction.channel.send(f'{row[0]}: link: {row[1]}, ineterval: {row[2]}, yes price: {row[3]}, no price: {row[4]}')
    await interaction.response.send_message("Database query could not be completed. Check the logs for more info")
    


bot.run(token, log_handler=handler, log_level=logging.DEBUG)