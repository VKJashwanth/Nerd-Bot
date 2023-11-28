from discord.ext import commands, tasks
import discord
import datetime

from dataclasses import dataclass

BOT_TOKEN = "YOUR_ID_HERE"
CHANNEL_ID = YOUR_CHANNEL_ID_HERE # <- That should be a number and not a string!
MAX_SESSION_TIME_MINUTES = 30


@dataclass
class Session:
  is_active: bool = False
  start_time: int = 0


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()


@bot.event
async def on_ready():
  print("Bot is ready!")
  channel = bot.get_channel(CHANNEL_ID)
  await channel.send("Hello! I am nerd bot")


@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
async def break_reminder():

  # ignoring the first execution of this command
  if break_reminder.current_loop == 0:
    return

  channel = bot.get_channel(CHANNEL_ID)
  await channel.send(
      f"**Take a break!** You have been using this timer for {MAX_SESSION_TIME_MINUTES} minutes."
  )


@bot.command()
async def start(ctx):
  if session.is_active:
    await ctx.send("A session is already active!")
    return

  session.is_active = True
  session.start_time = ctx.message.created_at.timestamp()
  human_readable_time = ctx.message.created_at.strftime('%H:%M:%S')
  break_reminder.start()
  await ctx.send(f"New session started at {human_readable_time}")


@bot.command()
async def stop(ctx):
  if not session.is_active:
    await ctx.send("No session is active!")
    return

  session.is_active = False
  end_time = ctx.message.created_at.timestamp()
  duration = end_time - session.start_time
  human_readable_duration = str(datetime.timedelta(seconds=duration))
  break_reminder.stop()
  await ctx.send(f"Session ended after {human_readable_duration}.")


bot.run(BOT_TOKEN)
