import discord
import random
import sqlite3
import os
from discord.ext import commands

app = commands.Bot(command_prefix='%%')
con = sqlite3.connect(os.getcwd()+"/Members.db", isolation_level= None)
cur = con.cursor()
'''
cur.execute("CREATE TABLE IF NOT EXISTS IronHorse(id INTEGER PRIMARY KEY AUTOINCREMENT, nickname TEXT, force INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS DarkHour(id INTEGER PRIMARY KEY AUTOINCREMENT, nickname TEXT, force INTEGER)")
'''

@app.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(app.user.name)
    print(os.getcwd())
    print('connection was succesful')
    await app.change_presence(status=discord.Status.online, activity=discord.Game("Division2 지원"))


@app.command()
async def 레이드생성(ctx, tablename):
    cur.execute('SELECT * FROM sqlite_master WHERE name = "'+tablename+'"')
    rows = cur.fetchall()
    if rows:
        await ctx.send('이미'+tablename+'테이블이 존재합니다.')
    else:
        cur.execute("CREATE TABLE IF NOT EXISTS "+tablename+" (id INTEGER PRIMARY KEY AUTOINCREMENT, nickname TEXT, force INTEGER)")
        await ctx.send('레이드 테이블이 생성되었습니다.')

@app.command()
async def 레이드목록(ctx):
    cur.execute('SELECT * FROM sqlite_master WHERE type = "table"')
    rows = cur.fetchall()
    str = ''
    for row in rows:
        if row[1] != 'sqlite_sequence':
            str += row[1] + '\n'
    if str != '':
        embed = discord.Embed(title='',
                              description='직접 생성한 레이드 목록을 표시합니다.',
                              color=0xAA6633)
        embed.add_field(name='레이드 목록', value=str, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send('레이드가 존재하지 않습니다.')

@app.command()
async def 레이드삭제(ctx, tablename):
    cur.execute('SELECT * FROM sqlite_master WHERE name = "'+tablename+'"')
    rows = cur.fetchall()
    if rows:
        con.execute("DROP TABLE "+tablename)
        await ctx.send(tablename+'을 삭제하였습니다.')
    else:
        await ctx.send(tablename+'레이드 테이블이 존재하지 않습니다.')

@app.command()
async def 레이드초기화(ctx, tablename):
    cur.execute('SELECT * FROM sqlite_master WHERE name = "'+tablename+'"')
    rows = cur.fetchall()
    if rows:
        con.execute("DELETE FROM "+tablename).rowcount
        await ctx.send(tablename+'을 삭제하였습니다.')
    else:
        await ctx.send(tablename+'레이드 테이블이 존재하지 않습니다.')

@app.command()
async def 레이드참가(ctx, tablename, nickname, force):
    cur.execute('SELECT * FROM sqlite_master WHERE name = "'+tablename+'"')
    rows = cur.fetchall()
    if rows:
        cur.execute('SELECT * FROM ' + tablename + ' WHERE nickname = "' + nickname + '"')
        user = cur.fetchone()
        cur.execute('SELECT * FROM ' + tablename + ' WHERE force = "' + str(1) + '"')
        force_bool = cur.fetchone()
        if user is None:
            if force == 'y':
                if force_bool is None:
                    cur.execute('INSERT INTO '+tablename+' (nickname, force) VALUES(?, ?)', (nickname, 1))
                    await ctx.send(nickname+'님이 '+tablename+'의 레이드에 참여하였습니다.')
                else:
                    await ctx.send("이미 공대장이 존재합니다.")
            else:
                cur.execute('INSERT INTO ' + tablename + ' (nickname, force) VALUES(?, ?)', (nickname, 0))
                await ctx.send(nickname+'님이 '+tablename+'의 레이드에 참여하였습니다.')
        else:
            await ctx.send(nickname + "님은 이미 레이드에 참여하였습니다.")
    else:
        await ctx.send(tablename + '레이드 테이블이 존재하지 않습니다.')

@app.command()
async def 레이드취소(ctx, tablename, nickname):
    cur.execute('SELECT * FROM sqlite_master WHERE name = "' + tablename + '"')
    rows = cur.fetchall()
    if rows:
        cur.execute('SELECT * FROM ' + tablename + ' WHERE nickname = "' + nickname + '"')
        user = cur.fetchone()
        if user is None:
            await ctx.send(nickname+'님이 레이드에 참여하지 않았습니다.')
        else:
            cur.execute("DELETE FROM "+tablename+" WHERE nickname = '" + nickname + "'")
            await ctx.send(nickname + "님이 철마 레이드 참여를 취소하였습니다.")
    else:
        await ctx.send(tablename + '레이드 테이블이 존재하지 않습니다.')

@app.command()
async def 레이드인원(ctx, tablename):
    cur.execute('SELECT * FROM sqlite_master WHERE name = "' + tablename + '"')
    rows = cur.fetchall()
    if rows:
        embed = discord.Embed(title='',
                              description='',
                              color=0xAA6633)
        cur.execute('SELECT * FROM '+tablename)
        raid_rows = cur.fetchall()
        raid_list = ''
        for row in raid_rows:
            raid_list += row[1]
            if row[2] == 1:
                raid_list += ' (공대장)'
            raid_list += '\n'
        embed.add_field(name=tablename, value=raid_list, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(tablename + '레이드 테이블이 존재하지 않습니다.')


'''
@app.command()
async def 레이드참가(ctx, nickname, raid_type, force):
    if raid_type == "철마":
        cur.execute("SELECT * FROM IronHorse WHERE nickname = '"+nickname+"'")
        user = cur.fetchone()
        cur.execute("SELECT * FROM IronHorse WHERE force = "+str(1)+"")
        force_bool = cur.fetchone()
        if user is None:
            if force == "y":
                if force_bool is None:
                    await ctx.send(nickname+"님이 철마 레이드에 참여하였습니다.")
                    cur.execute("INSERT INTO IronHorse (nickname, force) VALUES(?, ?)", (nickname, 1))
                else:
                    await ctx.send("이미 공대장이 존재합니다.")
            else:
                await ctx.send(nickname + "님이 철마 레이드에 참여하였습니다.")
                cur.execute("INSERT INTO IronHorse (nickname, force) VALUES(?, ?)", (nickname, 0))
        else:
            await ctx.send(nickname+"님은 이미 레이드에 참여하였습니다.")
    else:
        cur.execute("SELECT * FROM DarkHour WHERE nickname = '" + nickname + "'")
        user = cur.fetchone()
        cur.execute("SELECT * FROM DarkHour WHERE force = " + str(1) + "")
        force_bool = cur.fetchone()
        if user is None:
            if force == "y":
                if force_bool is None:
                    await ctx.send(nickname + "님이 철마 레이드에 참여하였습니다.")
                    cur.execute("INSERT INTO DarkHour (nickname, force) VALUES(?, ?)", (nickname, 1))
                else:
                    await ctx.send("이미 공대장이 존재합니다.")
            else:
                await ctx.send(nickname + "님이 철마 레이드에 참여하였습니다.")
                cur.execute("INSERT INTO DarkHour (nickname, force) VALUES(?, ?)", (nickname, 0))
        else:
            await ctx.send(nickname + "님은 이미 레이드에 참여하였습니다.")


@app.command()
async def 레이드인원(ctx):
    embed = discord.Embed(title='레이드 인원',
                          description='',
                          color=0xAA6633)
    ironhorse_txt = ""
    index = 0
    cur.execute("SELECT COUNT(*) FROM IronHorse")
    count = cur.fetchone()
    if count[0] != 0:
        cur.execute("SELECT * FROM IronHorse")
        while index < count[0]:
            user = cur.fetchone()
            ironhorse_txt += user[1] + "\n"
            index = index + 1
        embed.add_field(name='철마 레이드 (' + str(count[0]) + "/8)", value=ironhorse_txt, inline=False)
        
    darkhour_txt = ""
    index = 0
    cur.execute("SELECT COUNT(*) FROM DarkHour")
    count = cur.fetchone()
    if count[0] != 0:
        cur.execute("SELECT * FROM DarkHour")
        while index < count[0]:
            user = cur.fetchone()
            darkhour_txt += user[1] + "\n"
            index = index + 1
        embed.add_field(name='칠흑 레이드 (' + str(count[0]) + "/8)", value=darkhour_txt, inline=False)

    await ctx.send(embed=embed)

@app.command()
async def 레이드취소(ctx, nickname, raid_type):
    if raid_type == "철마":
        cur.execute("SELECT * FROM IronHorse WHERE nickname = '" + nickname + "'")
        user = cur.fetchone()
        if user is None:
            await ctx.send(nickname + "님은 레이드에 참여하지 않았습니다.")
        else:
            cur.execute("DELETE FROM IronHorse WHERE nickname = '"+nickname+"'")
            await ctx.send(nickname + "님이 철마 레이드 참여를 취소하였습니다.")
    else:
        cur.execute("SELECT * FROM DarkHour WHERE nickname = '" + nickname + "'")
        user = cur.fetchone()
        if user is None:
            await ctx.send(nickname + "님은 레이드에 참여하지 않았습니다.")
        else:
            cur.execute("DELETE FROM DarkHour WHERE nickname = '"+nickname+"'")
            await ctx.send(nickname + "님이 칠흑 레이드 참여를 취소하였습니다.")
            
@app.command()
async def 레이드초기화(ctx, raid_type):
    if raid_type == "철마":
        con.execute("DELETE FROM IronHorse").rowcount
        con.commit()
        await ctx.send("철마 레이드가 초기화되었습니다.")
    else:
        con.execute("DELETE FROM DarkHour").rowcount
        con.commit()
        await ctx.send("칠흑 레이드가 초기화되었습니다.")
'''

@app.command()
async def 버전체크(ctx):
    await ctx.send("Version 3.0")


@app.command()
async def 가위바위보(ctx, hand):
    answer = random.randrange(1,4)
    result = ''
    # 가위 : 1
    # 바위 : 2
    # 보 : 3
    if hand == '가위':
        if answer == 1:
            result = '비겼습니다.'
        elif answer == 2:
            result = '졌습니다...'
        else:
            result = '이겼습니다!!!'
    elif hand == '바위':
        if answer == 1:
            result = '이겼습니다!!!'
        elif answer == 2:
            result = '비겼습니다.'
        else:
            result = '졌습니다...'
    else:
        if answer == 1:
            result = '졌습니다...'
        elif answer == 2:
            result = '이겼습니다!!!'
        else:
            result = '비겼습니다.'

    embed = discord.Embed(title='가위바위보',
                          description='',
                          color=0xAA6633)
    embed.add_field(name='플레이어', value=hand, inline=False)

    bot = ''
    if answer == 1:
        bot = '가위'
    elif answer == 2:
        bot = '바위'
    else:
        bot = '보'

    embed.add_field(name='봇', value=bot, inline=False)
    embed.add_field(name='결과', value=result, inline=False)

    await ctx.send(embed=embed)

@app.command()
async def 인원뽑기(ctx, *text):
    index = random.randrange(0, len(text))
    await ctx.send("총 "+str(len(text))+"명 중에 뽑힌 인원은 "+text[index]+"님입니다.")

@app.command()
async def 로그(ctx):
    await ctx.send(os.getcwd())
    await ctx.send(os.path.realpath("Members.db"))

@app.command()
async def 도움(ctx):
    embed = discord.Embed(title='BLACKCLAW Bot 도움말',
                          description='레이드 이름, 닉네임 등 필드마다 공백이 들어가선 안됩니다. ex) 칠흑의 시간(X), 칠흑의_시간 (O)',
                          color=0xAA6633)
    embed.add_field(name='%%레이드생성 [레이드 이름]', value='[레이드 이름]의 레이드 테이블을 생성합니다.', inline=False) # 레이드생성(ctx, tablename)
    embed.add_field(name='%%레이드목록', value='생성된 모든 레이드들을 조회합니다.', inline=False) # 레이드목록(ctx)
    embed.add_field(name='%%레이드삭제 [레이드 이름]', value='[레이드 이름]를 삭제합니다. 안의 데이터 모두 삭제됩니다.', inline=False) # 레이드삭제(ctx, tablename):
    embed.add_field(name='%%레이드초기화 [레이드 이름]', value='[레이드 이름]를 초기화합니다. 테이블은 삭제되지 않고 안의 데이터만 삭제됩니다.', inline=False) # 레이드초기화(ctx, tablename):
    embed.add_field(name='%%레이드참가 [레이드 이름] [닉네임] [(공대장 여부)y/n]', value='[레이드 이름] 레이드에 참여합니다. y/n로 공대장 여부를 확인하시면 되며 공대장은 2명 이상 참여하실 수 없습니다.', inline=False) # 레이드참가(ctx, tablename, nickname, force):
    embed.add_field(name='%%레이드취소 [레이드 이름] [닉네임]', value='[레이드 이름]에서 해당 유저의 데이터를 삭제합니다.', inline=False) # 레이드취소(ctx, tablename, nickname):
    embed.add_field(name='%%레이드인원 [레이드 이름]', value='[레이드 이름]에 참여한 모든 유저를 조회합니다. 공대장 여부도 확인가능합니다.', inline=False) # 레이드인원(ctx, tablename):
    embed.add_field(name='%%가위바위보 [가위/바위/보]', value='봇과 가위바위보를 합니다.', inline=False)
    embed.add_field(name='%%인원뽑기 [인원1] [인원2] [인원3] ...', value='뒤 입력한 인원들 중 랜덤으로 1명 지정됩니다.', inline=False)
    embed.add_field(name='%%버전체크', value='현재 봇 버전을 체크합니다.', inline=False)
    await ctx.send(embed=embed)

app.run('ODY1OTA3NjUyNDQ2MjU3MTYy.YPK1WA.yvlV3Wic3XE5lPCyF7mhrc-dpp0')