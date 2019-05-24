import discord
from discord.ext import commands
import os

from dotenv import load_dotenv
load_dotenv()

# Role id of 'Role Manager'
ROLE_MANAGER_ROLE_ID = int(os.getenv('ROLE_MANAGER_ROLE_ID'))

# Role id of bottom which the bot can manage roles
BOTTOM_ROLE_ID = int(os.getenv('BOTTOM_ROLE_ID'))

class RoleManage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def is_bot():
        def check_bot(ctx):
            return not ctx.author.bot
        return commands.check(check_bot)

    @commands.command(name='list')
    @is_bot()
    async def _list(self, ctx):
        sender = ctx.author
        roles = ctx.guild.roles

        role_manager_role = ctx.guild.get_role(ROLE_MANAGER_ROLE_ID)
        bottom_role = ctx.guild.get_role(BOTTOM_ROLE_ID)

        # Role のポジション
        # いじれる Role を範囲指定する
        index_role_manager = role_manager_role.position
        index_bottom = bottom_role.position

        # +1 しないと境界用の役職も入ってしまう
        controllable_roles = roles[index_bottom + 1:index_role_manager]
        controllable_roles.reverse()

        # 発言者が既に取得している役職名
        role_names_member_has_already = set(role.name for role in sender.roles)

        # Bot が制御可能な役職名
        controllable_role_names = set(role.name for role in controllable_roles)

        # 発言者が既に持っている制御可能な役職名リスト
        controllable_role_names_member_has_already = list(controllable_role_names & role_names_member_has_already)

        # 発言者が持っていない制御可能な役職名を抽出する
        controllable_role_names_member_not_has_yet = list(controllable_role_names - role_names_member_has_already)

        embed_message = discord.Embed(title=f'{sender.name} 様が移動できるできる役職', description='\'\'の中身をそのまま引数に渡すんだにゃ')
        embed_message.add_field(name='取得可能な役職名', value=controllable_role_names_member_not_has_yet, inline=False)
        embed_message.add_field(name='外すことが可能な役職名', value=controllable_role_names_member_has_already, inline=False)

        await ctx.send(content=None, embed=embed_message)


def setup(bot):
    bot.add_cog(RoleManage(bot))