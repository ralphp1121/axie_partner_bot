import os
import discord
import json
import requests

client = discord.Client()
my_secret = os.environ['TOKEN']

ronin = {'karl':'ronin:0e2b59addf4e324b3a0c26b62280aa270d00f729','reynald':'ronin:84eca762ecdd0c388c3c9a70baf4b9317241f390', 'mylene':'ronin:3bd8d200ef6d1b82f7c2ddfe6d89fedc5283354c','janjan':'ronin:a5fd8015eb88bac5fbffc074449585307de8f724', 'janrae':'ronin:752e5f460768fb0f6cadd24f06b23ce34976dc37', 'keo':'ronin:55ba81d5f2e6cdaafc56387e5b8c6f4763e7ee78', 'tracy':'ronin:3e69081f866520b56e2684e14e76243406960e78', 'jinky':'ronin:16e2a8e8ea64f3bafae970549f205925afb7f000'}

scholars = ["mylene", "jinky", "janjan", "janrae", "keo", "karl", "tracy", "reynald"]

def get_current_slp(ronin_id):
  response = requests.get("https://api.lunaciaproxy.cloud/_earnings/"+ronin_id)
  json_data = json.loads(response.text)
  curr_slp = json_data['earnings']['slp_inventory']
  return curr_slp

def get_next_withdraw(ronin_id):
  response = requests.get("https://api.lunaciaproxy.cloud/_earnings/"+ronin_id)
  json_data = json.loads(response.text)
  next_withdraw = json_data['earnings']['next_claim']
  return next_withdraw

@client.event 
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if msg.startswith('$help'):
    await message.channel.send("This is our very own Axie Bot" + ":robot:")
    await message.channel.send("Refer to the commands below on how to use this bot")
    await message.channel.send("1. type $partners to see your username needed for other bot commands")
    await message.channel.send("2. type $earnings <your username> to see your current SLP and next withdrawal date")
    await message.channel.send("For any issue or help needed with this bot, contact Kuya Ralph")

  if msg.startswith('$earnings'):
    get_user_id = msg.split("$earnings ",1)[1]
    get_ronin_id = ronin[get_user_id]
    get_slp = get_current_slp(get_ronin_id)
    get_withdraw = get_next_withdraw(get_ronin_id)

    await message.channel.send("Current SLP : " + str(get_slp) + " " + ":moneybag:")
    await message.channel.send("Next Withdraw Schedule : " + get_withdraw + " " + ":atm:")

  if msg.startswith('$partners'):
    await message.channel.send(scholars)  

client.run(my_secret)