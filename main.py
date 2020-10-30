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
import discord.utils


config = configparser.RawConfigParser()
config.read("config.ini")

bot_token = config['main']['bot_token']
bot_id = config['main']['bot_id']
bot_prefix = config['main']['bot_prefix']
listening_channels = config['main']['listening_channels'].split(",")

client = Bot(command_prefix=bot_prefix)
client.remove_command('help')

async def is_it_a_listening_channel(ctx):
    """Returns whether or not the bot should be listening to this channel."""
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
    usernames = usernames.split(',')
    role = discord.utils.get(ctx.guild.roles, id=int(role_id))
    if role:
        print(role)
    else:
        await ctx.send("Unable to find role!")
        return


    #TODO: support mentions and/or nicknames?
    if len(usernames) > 0:
        for u in usernames: # For each user...
            member = None
            name = None
            discriminator = None
            if '#' in u: # split the discriminator.
                name, discriminator = u.split('#')
                # member = discord.utils.get(ctx.guild.members, name=name, discriminator=int(discriminator))
            else:
                name = u
                # BUG: discord.utils.get() isn't working? have to use loop below with fetch_members.
                # member = discord.utils.get(ctx.guild.members, name=name)
            async for m in ctx.guild.fetch_members(limit=None):
                if m.name == name:
                    print("Member found: {}".format(m.name))
                    await m.add_roles(role)
                    await ctx.send("Assigned role to {}#{}".format(m.name, m.discriminator))


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