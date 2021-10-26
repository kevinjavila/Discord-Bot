import discord
import os
import requests
import json
from replit import db
import keep_alive

client = discord.Client()

# Using CoinGecko API
def loop():
  response = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd")
  json_data = json.loads(response.text)
  # This loop will store keys and values inside of Replit's Database
  for i in range(len(json_data)):
    db[json_data[i]["id"]] = json_data[i]["current_price"]

# Checking the value of the coin
def get_coin(coin):
  if coin in db.keys():
    return db[coin]

# Checking if the coin is in the CoinGecko API
def exists(coin):
  if coin in db.keys():
    return "Yes I do."
  return "Unfortunately, I do not."

# triggered when client has logged on 
@client.event
async def on_ready():
  print("You have logged in as {}".format(client))


# triggered each time a message is received
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  # Needs to loop through API data before getting any input so that database will be full
  loop()

  # Setting the user's input to new variable for readability
  user_input = message.content.lower()

  # Will give the price of a given coin at the moment
  if user_input[1:] in db.keys():
    value = get_coin(user_input[1:])
    await message.channel.send("The price of {} is ${} at the moment.".format(message.content, value))

  # Will list all the coins available within the API
  if user_input.startswith("$ls"):
    coin_lst = [i for i in db.keys()]
    await message.channel.send(coin_lst)

  # Will confirm if the coin is in the database
  if message.content.startswith("$support "):
    supported = message.content.split("$support ", 1)[1].lower()
    await message.channel.send(exists(supported))


keep_alive.keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)



