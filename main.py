import os
import discord
import json
import requests
from datetime import datetime
from pytz import timezone
import pytz
import math

client = discord.Client()
my_secret = os.environ['TOKEN']

# List of all scholars and ronin addresses
ronin = {'karl':'ronin:0e2b59addf4e324b3a0c26b62280aa270d00f729','reynald':'ronin:84eca762ecdd0c388c3c9a70baf4b9317241f390', 'mylene':'ronin:3bd8d200ef6d1b82f7c2ddfe6d89fedc5283354c','janjan':'ronin:a5fd8015eb88bac5fbffc074449585307de8f724', 'janrae':'ronin:752e5f460768fb0f6cadd24f06b23ce34976dc37', 'keo':'ronin:55ba81d5f2e6cdaafc56387e5b8c6f4763e7ee78', 'tracy':'ronin:3e69081f866520b56e2684e14e76243406960e78', 'jinky':'ronin:16e2a8e8ea64f3bafae970549f205925afb7f000'}

# List of scholar names to be used for the bot commands
scholars = ["mylene", "jinky", "janjan", "janrae", "keo", "karl", "tracy", "reynald"]

# Get the SLP based on the ronin address
def get_current_slp(ronin_id):
  response = requests.get("https://api.lunaciaproxy.cloud/_earnings/"+ronin_id)
  json_data = json.loads(response.text)
  curr_slp = json_data['earnings']['slp_inventory']
  return curr_slp

# Get next withdrawal date
def get_next_withdraw(ronin_id):
  response = requests.get("https://api.lunaciaproxy.cloud/_earnings/"+ronin_id)
  json_data = json.loads(response.text)
  next_withdraw = json_data['earnings']['next_claim']
  return next_withdraw

# Get the earnings average and tier
def get_allocation(ronin_id):
  response = requests.get("https://api.lunaciaproxy.cloud/_earnings/"+ronin_id)
  json_data = json.loads(response.text)

  # Manipulate date/time
  # Reference: https://towardsdatascience.com/basic-datetime-operations-in-python-2d706be82c63

  last_withdraw_timestamp = json_data['earnings']['last_claimed']
  last_withdraw_date = datetime.fromtimestamp(last_withdraw_timestamp)

  # Set the timezone to 'Asia/Singapore'
  # Reference: https://www.kite.com/python/answers/how-to-convert-timezones-in-python
  local_tz = pytz.timezone('Asia/Singapore')

  diff_date = datetime.now().astimezone(local_tz)-last_withdraw_date.astimezone(local_tz)
  diff_date_str = str(diff_date)
  diff_date_int = int(diff_date_str[0:2])

  curr_slp = get_current_slp(ronin_id)

  slp_average = int(curr_slp/diff_date_int)

# Return output for daily average SLP and current tier
  if slp_average >= 126:
    alloc = "Daily SLP Average: "+str(slp_average)+" at 55% earnings, yon oh, lufet!"+":flame:"
    return alloc
  elif slp_average < 126 and slp_average > 75:
    alloc = "Daily SLP Average: "+str(slp_average)+" at 50% earnings, good job, go go go lang!"+":sunglasses:"
    return alloc
  else:
    alloc = "Daily SLP Average: "+str(slp_average)+" at 40% earnings, konting push pa!"+":muscle:"
    return alloc

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
    get_alloc = get_allocation(get_ronin_id)

    await message.channel.send("Current SLP : " + str(get_slp) + " " + ":moneybag:")
    await message.channel.send("Next Withdraw Schedule : " + get_withdraw + " " + ":atm:")
    #await message.channel.send(get_alloc)

  if msg.startswith('$partners'):
    await message.channel.send(scholars)  

client.run(my_secret)