import discord, os
from discord.ext import commands
from dotenv import load_dotenv
import exceptions
import traceback
import riot

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialize the bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot event for when it is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.command()
async def rank(ctx, queue="solo", server="euw"):
    try:
        all = riot.fetch_players_by_queue(server, queue)
        data = riot.parse_rank_data(all)
        msg = rank_message(data, server, queue)
        await ctx.send(msg)
    except exceptions.RateLimitExceeded as e:
        traceback.print_exc()
        await ctx.send("API rate limit exceeded, please try again in a minute.")
    except ValueError as e:
        traceback.print_exc()
        await ctx.send(e)
    except Exception as e:
        traceback.print_exc()
        await ctx.send("An unknown error occured.")


def rank_message(data, server, queue):
    if data["chall_count"] == 0 and data["gm_count"] == 0:
        return "Not enough players on server."
    lp_chall = data["lps"][data["chall_count"] - 1]
    lp_gm = data["lps"][data["chall_count"] + data["gm_count"] - 1]
    return (
        f"`{server} / {queue}`\n"
        + "> Challenger @ "
        + str(lp_chall)
        + f" LP (top {data['chall_count']})\n"
        + "> Grandmaster @ "
        + str(lp_gm)
        + f" LP (top {data['gm_count'] + data['chall_count']} )\n"
    )


# Run the bot
bot.run(os.getenv["DISCORD_BOT_TOKEN"])
