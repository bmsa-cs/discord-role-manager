"""
discord-role-manager

This Discord bot allows the user to quickly batch assign/remove roles
by passing a list of users as an argument.

"""


import configparser
import asyncio

from discord.ext.commands import Bot
from discord.ext import commands
from discord import Client
from discord import Embed


config = configparser.RawConfigParser()
config.read("config.ini")

bot_token = config['main']['bot_token']
bot_id = config['main']['bot_id']
bot_prefix = config['main']['bot_prefix']
listening_channels = config['main']['listening_channels'].split(",")

client = Bot(command_prefix=bot_prefix)
client.remove_command('help')

async def is_it_a_listening_channel(ctx):
    # Returns whether or not the bot should be listening to this channel.
    for c in listening_channels:
        if int(ctx.message.channel.id) == int(c):
            return True
    return False

@client.command(    name="giverole",
                    description="Assigns a role to a list of users.",
                    aliases=['gr', 'give'],
                    case_insensitive=True,
                    pass_context=True)
@commands.check(is_it_a_listening_channel)
async def give(ctx, role_id, usernames):
    """Given a role_id and a comma-separated list of users, assigns those users the role."""
    guild = ctx.guild.id
    usernames = usernames.split(',')

    #TODO: support mentions and/or nicknames?
    if len(usernames) > 0:
        for u in usernames: # For each user...
            for m in ctx.guild.members: # For each member in the server...
                 #BUG: This doesn't seem to be getting all users correctly.
                if u == m.name: #If the username equals the member name...
                    await m.add_roles(role_id)
                    await ctx.send("Assigned role to {m.name}")


@client.event
async def on_ready():
    print("Logged in as " + client.user.name)

async def valid_user(user):
    """Validates a user by checking that they're a member of the server."""
    pass

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


if __name__ == "__main__":
    client.loop.create_task(list_servers())
    client.run(bot_token)