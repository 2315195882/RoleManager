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
            # 登録されていないサブコマンドが実行されたとき
            self.HELP_EMBED_MESSAGE.title = '登録されたサブコマンドを利用して欲しいにゃ!'
            self.HELP_EMBED_MESSAGE.description = 'このわかりやすいヘルプをよく読むにゃ。'
            self.HELP_EMBED_MESSAGE.color = discord.Color.red()
            await ctx.send(content=None, embed=self.HELP_EMBED_MESSAGE)

    @role.group(name='list')
    @is_bot()
    async def _list(self, ctx):
        controllable_roles_list_dic = get_controllable_roles_list_dict(ctx.author, ctx.guild)

        # TODO: lambda 式と map の利用
        controllable_role_names_member_has_already = []
        for role in controllable_roles_list_dic['has_already']:
            controllable_role_names_member_has_already.append(role.name)

        controllable_role_names_member_not_has_yet = []
        for role in controllable_roles_list_dic['has_not_yet']:
            controllable_role_names_member_not_has_yet.append(role.name)

        embed_message = discord.Embed(title=f'{ctx.author.name} が操作できるできる役職は以下のとおりですにゃ', description='\'\'の中身をそのまま引数に渡すんだにゃ')
        embed_message.add_field(name='取得可能な役職名', value=controllable_role_names_member_not_has_yet, inline=False)
        embed_message.add_field(name='外すことが可能な役職名', value=controllable_role_names_member_has_already, inline=False)
        embed_message.color = discord.Color.green()

        await ctx.send(content=None, embed=embed_message)

    @role.group(name='get')
    @is_bot()
    async def _get(self, ctx, *target_role_name):
        EMBED_MESSAGE = discord.Embed()
        if len(target_role_name) == 0:
            # 引数がない
            EMBED_MESSAGE.title = '引数に役職名を指定するにゃ!!'
            EMBED_MESSAGE.description = '使い方がわからない場合は !role help を実行してみるといいにゃ。'
            EMBED_MESSAGE.color = discord.Color.red()
            await ctx.send(content=None, embed=EMBED_MESSAGE)
        elif len(target_role_name) > 1:
            # 引数が2つ以上ある(一括付与は認めていない)
            EMBED_MESSAGE.title = '引数はひとつだけだにゃ!!'
            EMBED_MESSAGE.description = '使い方がわからない場合は !role help を実行してみるといいにゃ。'
            EMBED_MESSAGE.color = discord.Color.red()
            await ctx.send(content=None, embed=EMBED_MESSAGE)
        else:
            # sender が持っていない役職の名前一覧
            controllable_role_names_member_not_has_yet = []
            controllable_roles_member_has_not_yet      = get_controllable_roles_list_dict(ctx.author, ctx.guild)['has_not_yet']
            for role in controllable_roles_member_has_not_yet:
                controllable_role_names_member_not_has_yet.append(role.name)

            # sender がすでに持っている役職の名前一覧
            controllable_role_names_member_has_already = []
            controllable_roles_member_has_already      = get_controllable_roles_list_dict(ctx.author, ctx.guild)['has_already']
            for role in controllable_roles_member_has_already:
                controllable_role_names_member_has_already.append(role.name)

            # Role Manager が操作可能な役職の名前一覧
            controllable_role_names = []
            controllable_roles      = get_controllable_roles_list_dict(ctx.author, ctx.guild)['controllable']
            for role in controllable_roles:
                controllable_role_names.append(role.name)

            if target_role_name[0] in controllable_role_names_member_has_already:
                # 指定した役職をすでに持っている
                EMBED_MESSAGE.title = f'その役職は {ctx.author.name} がすでに持っている役職だにゃ!'
                EMBED_MESSAGE.description = '!role list を確認するといいにゃ。'
                EMBED_MESSAGE.color = discord.Color.red()
                await ctx.send(content=None, embed=EMBED_MESSAGE)

            elif target_role_name[0] not in controllable_role_names:
                # 指定した役職が存在してなかった
                EMBED_MESSAGE.title = 'その役職は存在しないか、吾輩がいじれるものじゃないにゃ!'
                EMBED_MESSAGE.description = '!role list を確認するか、OJI に聞くといいにゃ。'
                EMBED_MESSAGE.color = discord.Color.red()
                await ctx.send(content=None, embed=EMBED_MESSAGE)

            else:
                # 指定した役職が存在しており、Role Manager が付与できるものだった
                target_role_index = controllable_role_names_member_not_has_yet.index(target_role_name[0])
                target_role = controllable_roles_member_has_not_yet[target_role_index]
                await ctx.author.add_roles(target_role, reason = 'Role Manager によって付与されました。')

                EMBED_MESSAGE.title = f'{target_role.name} を付与したにゃ!'
                EMBED_MESSAGE.color = discord.Color.green()
                await ctx.send(content=None, embed=EMBED_MESSAGE)


def setup(bot):
    bot.add_cog(RoleManage(bot))

def get_controllable_roles_list_dict(sender, guild):
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
    roles_member_has_already = sender.roles

    # 発言者が既に持っている制御可能な役職リスト
    controllable_roles_member_has_already = [role for role in roles_member_has_already  if role in controllable_roles]

    # 発言者が持っていない制御可能な役職リスト
    controllable_roles_member_has_not_yet = [role for role in controllable_roles if role not in roles_member_has_already]

    return {
        'controllable': controllable_roles,
        'has_already': controllable_roles_member_has_already,
        'has_not_yet': controllable_roles_member_has_not_yet
    }