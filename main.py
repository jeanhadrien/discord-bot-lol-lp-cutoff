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
async def rank(ctx, server="euw1"):
    try:
        all = riot.fetch_players_by_queue(server, "solo")
        extracted = riot.sort_and_extract_league_points(all)
        lp_gm = extracted[999]
        lp_chall = extracted[299]
        await ctx.send(
            f"`{server} / solo`\n"
            + "> Challenger @ "
            + str(lp_chall)
            + " LP\n"
            + "> Grandmaster @ "
            + str(lp_gm)
            + " LP"
        )
    except exceptions.RateLimitExceeded as e:
        traceback.print_exc()
        await ctx.send("API rate limit exceeded, please try again in a minute.")
    except ValueError as e:
        traceback.print_exc()
        await ctx.send(e)
    except Exception as e:
        traceback.print_exc()
        await ctx.send("An unknown error occured.")

# Run the bot
bot.run(os.environ["DISCORD_BOT_TOKEN"])
