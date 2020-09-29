import asyncio
import discord
from discord.ext import commands
from tokens import discord_token
from rubik_solver import utils as rubik_utils

bot = commands.Bot(command_prefix='h!')

print(bot)

async def apply_reactions(context, reactions):
    await context.clear_reactions()
    [await context.add_reaction(x) for x in reactions]

@bot.command()
async def ping(context):
    await context.send('pong')

@bot.command(aliases=['rubik'])
async def rubiksolver(context):

    instructions = "Hold the cube in front of you with the yellow face pointing upwards. Always keep the yellow face pointing upwards while inputting each side. When inputting the yellow stickers, make sure that the orange face is pointing upwards. When inputting white, make sure that the red face is pointing upwards. You can tell which face is which because the very center stickers of each side of the cube never move. They are marked in the picture below."

    stickers = ["⬜", "🟥", "🟦", "🟨", "🟩", "🟧", "❌"]

    face = 0
    index = 0
    cube = ["cuuuyuuuu", "cuuubuuuu", "cuuuruuuu", "cuuuguuuu", "cuuuouuuu", "cuuuwuuuu"]

    cube_emoji_map = {
        "x": "\n",
        "u": "❔",
        "c": "❓",
        "w": stickers[0],
        "r": stickers[1],
        "b": stickers[2],
        "y": stickers[3],
        "g": stickers[4],
        "o": stickers[5],
        "q": "❌"
    }

    cube_emoji_map_inv = {v: k for k, v in cube_emoji_map.items()}

    response = await context.send(
        embed=discord.Embed(
            title="Rubik's Cube Solver",
            type="rich",
            description="".join([cube_emoji_map[x] for x in list(''.join(l + 'x' * (n % 3 == 2) for n, l in enumerate(list(cube[face]))))])
        )
    )

    await apply_reactions(response, stickers)

    def check(reaction, user):
        return user == context.author and str(reaction.emoji) in stickers

    while face < 6:
        print(cube)
        try:
            reaction, user = await bot.wait_for('reaction_add', check=check)
        except asyncio.TimeoutError:
            await context.send("Somehow, you took longer than forever.")
        else:

            if reaction.emoji == stickers[6]:
                await context.send("Quitting Rubik's Solver.")
                break

            next = list(cube[face])
            next[index] = cube_emoji_map_inv[reaction.emoji]
            index += 1

            # skip center sticker
            if index == 4:
                index += 1
            # move to next face

            if index == 9:
                next[index] = "c"
                cube[face] = "".join(next)
                face += 1
                index = 0
            else:
                next[index] = "c"
                cube[face] = "".join(next)

            await response.edit(
                embed=discord.Embed(
                    title="Rubik's Cube Solver",
                    type="rich",
                    description="".join([cube_emoji_map[x] for x in list(''.join(l + 'x' * (n % 3 == 2) for n, l in enumerate(list(cube[face]))))])
                )
            )

            await response.remove_reaction(reaction.emoji, context.author)

    print("solving!")


bot.run(discord_token)
