import discord
from discord import app_commands
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import datetime

## Import classes
from api import Api
from db import BettingRatDatabase

## Setup variables
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
poly_api = Api
rat_db = BettingRatDatabase()
# ratnest id copy
discord_server_id = int(os.getenv('DISCORD_SERVER_ID'))
discord_channel_id = int(os.getenv('DISCORD_CHANNEL_ID'))
minimum_price_difference = 0.02

# non discord functions
def get_api_data(market_link):
    # api get request to get token(needed for price request)
    market = poly_api.api_get_market(market_link.split("/")[-1])
    # if api was succesfull do
    if market!=None:
        # api get request  yes/no
        prices = poly_api.api_get_market_prices(poly_api, market)
        # if api was succesfull do
        if prices[0]!=None:
            return prices
    return None

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
    await tree.sync(guild=discord.Object(id=discord_server_id))  
    loop_price_checker.start()
    print(f"Let's go gambling!")

## Commands
# Note that for events you need to copy the market name the link/chain icon abovce the polymarket logo
@tree.command(name="check_market_rates",
              guild=discord.Object(id=discord_server_id), 
              description="Returns the yes and no price of given market. ",
              )
async def check_market_rate(interaction, market_link: str):
    result = get_api_data(market_link)
    if result!=None:
        await interaction.response.send_message(f"The price for {market_link} are yes: {result[0]} and no: {result[1]}")
        return
    await interaction.channel.send("Market request reached an unexpected result. Check the logs for more info")

@tree.command(name="add_tracking_market",
              guild=discord.Object(id=discord_server_id), 
              description="Add a market to the db for continues updates")
async def add_tracking_market(interaction, name: str, link: str, interval: str):
    prices = get_api_data(link)
    new_record = rat_db.add_market(name, link.split("/")[-1], interval, prices[0], prices[1])
    # if db query was succesfull do
    if new_record!=None:
        await interaction.response.send_message(f'New row has been added: {new_record[0]}: link: {new_record[1]}, ineterval: {new_record[2]}')
        return
    await interaction.channel.send("Database query could not be completed. Check the logs for more info")

@tree.command(name="get_tracking_markets", 
              guild=discord.Object(id=discord_server_id), 
              description="Get the current list of markets added to the db")
async def get_tracking_markets(interaction):
    records = rat_db.get_markets()
    # if db query was succesfull do
    if records!=None:
        await interaction.response.send_message("In chronological order")
        for row in records:
            await interaction.channel.send(f'{row[0]}: link: {row[1]}, ineterval: {row[2]}, yes price: {row[4]}, no price: {row[5]}')
    await interaction.channel.send("Database query could not be completed. Check the logs for more info")

##Tasks
# loop price checker
@tasks.loop(seconds=31)
async def loop_price_checker():
    await bot.wait_until_ready() 
    channel = bot.get_channel(discord_channel_id)
    # Get discord channel to send messages to
    db_markets = rat_db.get_markets()
    if db_markets!=None:
        # For every channel check if the interval has passed since the last time the price was updated
        # record[2]=interval record[3]=last datetime updated
        for record in db_markets:
            if datetime.datetime.strptime(record[3], '%Y-%m-%d %H:%M:%S')<datetime.datetime.now()-datetime.timedelta(minutes=int(record[2])):
                result = get_api_data(record[1])
                result = (float(result[0]), float(result[1]))
                # check if prices differ by more then intended%
                if result!=None:
                    if abs(record[4]-result[0])>0.02 or abs(record[5]-result[1])>minimum_price_difference: 
                        # update db with new prices
                        rat_db.update_market_price(link=record[1],new_price=result)
                        await channel.send(f"**Price check Update!**\nThe buy price for **{record[0]}** has shifted by {round(abs(record[4]-result[0])*100, 2)}%")
                        ## if the old price is higher then the new price give a sad message for yes
                        if record[4]-result[0]>0:
                            await channel.send(f"<:tdogSad:577149476880252967> The yes price has dropped from {record[4]} to {result[0]} <:tdogSad:577149476880252967>")
                            await channel.send(f":chart_with_upwards_trend: The no price has gone up from {record[5]} to {result[1]} :chart_with_upwards_trend:")
                        else:
                            await channel.send(f":chart_with_upwards_trend: The yes price has gone up from {record[4]} to {result[0]} :chart_with_upwards_trend:")
                            await channel.send(f"<:tdogSad:577149476880252967> The no price has dropped from {record[5]} to {result[1]} <:tdogSad:577149476880252967>")
                    else:
                        # if price did not increase update datetime for next check interval
                        rat_db.update_market_price(link=record[1],new_price=[record[4],record[5]])
                else:
                    await channel.send("Market request reached an unexpected result. Check the logs for more info")
    else:
        await channel.send("Database query could not be completed. Check the logs for more info")
    


bot.run(token, log_handler=handler, log_level=logging.DEBUG)