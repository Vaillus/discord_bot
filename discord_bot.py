
import os
import discord
import json

import importlib

from utils import get_params
from task_manager import TaskManager

class DiscordBot:
    def __init__(self, params= {}):
        self.server_name = None
        self.discord_token = None
        self.client = None
        self.taskman = None

        self.set_params_from_dict(params=params)
        self.set_other_params()

        self.run_bot()

    def set_params_from_dict(self, params):
        self.server_name = params.get("server_name", "")
        self.discord_token = params.get("discord_token", "")
            
    def set_other_params(self):
        self.client = discord.Client()
        self.taskman = TaskManager()

    # ================================================================

    def run_bot(self):
        self.on_ready = self.client.event(self.on_ready)
        self.on_member_join = self.client.event(self.on_member_join)
        self.on_message = self.client.event(self.on_message)

        self.client.run(self.discord_token)

    async def on_ready(self):
        print(f'{self.client.user} est descendu des cieux pour vous servir!')
        guild = discord.utils.get(self.client.guilds, name=self.server_name)
        print(
            f'{self.client.user} est connecté dans le serveur:\n'
            f'{guild.name}(id: {guild.id})'
        )

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Sont dans le nuage:\n - {members}')
    
    async def on_member_join(self, member):
        pass
        #await member.create_dm()
        #await member.dm_channel.send(
        #    f'Hi {member.name}, welcome to my Discord server!'
        #)
    
    async def on_message(self, message):
        print(f"{message.author.name} : {message.content}")
        # avoid infinite loop where the bot talks to itself.
        if message.author == self.client.user:
            return

        response = self.taskman.trigger_task(message.content.lower())
        if response:
            await message.channel.send(response)

    

if __name__ == "__main__":
    params = get_params("bot_params")
    #print(params)
    bot = DiscordBot(params)
    