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
        self.HELP_EMBED_MESSAGE = discord.Embed(title = '吾輩は Role Manger である!', description='わからないことがあったら OJI に聞くにゃ！')
        self.HELP_EMBED_MESSAGE.add_field(name='!role help', value='Role Manager の使い方(このメッセージ)を表示するにゃ!', inline=False)
        self.HELP_EMBED_MESSAGE.add_field(name='!role list', value='あなたが自身に付与 or 自身から外せる役職の一覧を表示するにゃ!\nこれより下のコマンドにはこれで表示された役職名を入力てほしいにゃ。', inline=False)
        self.HELP_EMBED_MESSAGE.add_field(name='!role get \{役職名\}', value='\{役職名\} に与えた役職を取得するにゃ!', inline=False)
        self.HELP_EMBED_MESSAGE.add_field(name='!role remove \{役職名\}', value='\{役職名\} に与えられた役職をあなたから外すにゃ!', inline=False)

    def is_bot():
        def check_bot(ctx):
            return not ctx.author.bot
        return commands.check(check_bot)


    @commands.group(name='role')
    @is_bot()
    async def role(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(content=None, embed=self.HELP_EMBED_MESSAGE)

    @role.group(name='list')
    @is_bot()
    async def _list(self, ctx):
        controllable_roles_list_dic = get_controllable_roles_list_dic(ctx.author, ctx.guild)

        controllable_role_names_member_has_already = controllable_roles_list_dic['has_already']
        controllable_role_names_member_not_has_yet = controllable_roles_list_dic['has_not_yet']

        embed_message = discord.Embed(title=f'{ctx.author.name} 様が移動できるできる役職', description='\'\'の中身をそのまま引数に渡すんだにゃ')
        embed_message.add_field(name='取得可能な役職名', value=controllable_role_names_member_not_has_yet, inline=False)
        embed_message.add_field(name='外すことが可能な役職名', value=controllable_role_names_member_has_already, inline=False)

        await ctx.send(content=None, embed=embed_message)

    @role.group(name='get')
    @is_bot()
    async def _get(self, ctx):
        await ctx.send('`!role get` を実行したにゃ!')

def setup(bot):
    bot.add_cog(RoleManage(bot))

def get_controllable_roles_list_dic(sender, guild):
    roles = guild.roles

    role_manager_role = guild.get_role(ROLE_MANAGER_ROLE_ID)
    bottom_role       = guild.get_role(BOTTOM_ROLE_ID)

    # Role のポジション
    # いじれる Role を範囲指定する
    index_role_manager = role_manager_role.position
    index_bottom       = bottom_role.position

    # +1 しないと境界用の役職も入ってしまう
    controllable_roles = roles[index_bottom + 1:index_role_manager]
    # @everyone から順番に取ってくるので反転
    # sort をかけてもいいかも
    controllable_roles.reverse()

    # 発言者が既に取得している役職名
    role_names_member_has_already = set(role.name for role in sender.roles)

    # Bot が制御可能な役職名
    controllable_role_names = set(role.name for role in controllable_roles)

    # 発言者が既に持っている制御可能な役職名リスト
    controllable_role_names_member_has_already = list(controllable_role_names & role_names_member_has_already)

    # 発言者が持っていない制御可能な役職名を抽出する
    controllable_role_names_member_has_not_yet = list(controllable_role_names - role_names_member_has_already)

    return {
        'has_already':  controllable_role_names_member_has_already,
        'has_not_yet': controllable_role_names_member_has_not_yet
    }