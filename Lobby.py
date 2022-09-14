from lcu_driver import Connector
#------------------------------------------------#
#http://www.mingweisamuel.com/lcu-schema/tool/
#------------------------------------------------#
connector = Connector()

async def get_summoner_data(connection):
    data = await connection.request('GET', '/lol-summoner/v1/current-summoner')
    summoner = await data.json()
    print(summoner)
    print(f"displayName:    {summoner['displayName']}")
    print(f"summonerId:     {summoner['summonerId']}")
    print(f"puuid:          {summoner['puuid']}")
    print("-")

async def create_draft_game(connection):
    ranked = {
            'queueId': 400
        }
    x = await connection.request('POST', '/lol-lobby/v2/lobby', data=ranked)
    print(x)

async def create_ranked_game(connection):
    ranked = {
        'queueId': 440,}
        
    await connection.request('POST', '/lol-lobby/v2/lobby', data=ranked)

async def fill_role(connection):
    role = { "firstPreference": "UTILITY", "secondPreference": "FILL" }

    x = await connection.request('PUT', '/lol-lobby/v1/lobby/members/localMember/position-preferences', data=role)
    print(x)

async def create_custom_lobby(connection):
    custom = {
        'customGameLobby': {
            'configuration': {
                'gameMode': 'PRACTICETOOL',
                'gameMutator': '',
                'gameServerRegion': '',
                'mapId': 11,
                'mutators': {'id': 1},
                'spectatorPolicy': 'AllAllowed',
                'teamSize': 5},
            'lobbyName': 'PRACTICETOOL',
            'lobbyPassword': ''},
        'isCustom': True}

    await connection.request('POST', '/lol-lobby/v2/lobby', data=custom)

async def GetTest(connection):
    x = await connection.request('GET', '/lol-lobby/v2/lobby')
    y = await connection.request('GET' '/lol-lobby/v2/lobby/invitations')
    print(x,y)

async def login(connection):
    auth = {

    }
    await connection.request('POST', '/lol-login/v1/access-token', data=auth)
#-----------------------------------------------------------------------------
# Adding bots to team1
#-----------------------------------------------------------------------------
async def add_bots_team1(connection):
    soraka = {
        'championId':16,
        'botDifficulty':'EASY',
        'teamId':'100'}
    await connection.request('POST', '/lol-lobby/v1/lobby/custom/bots', data=soraka)

#-----------------------------------------------------------------------------
# Adding bots to team2
#-----------------------------------------------------------------------------
async def add_bots_team2(connection):
    activedata = await connection.request('GET', '/lol-lobby/v2/lobby/custom/available-bots')
    champions = { bot['name']: bot['id'] for bot in await activedata.json() }

    team2 = ['Caitlyn', 'Blitzcrank', 'Darius', 'Morgana', 'Lux']

    for name in team2:
        bot = { 'championId': champions[name], 'botDifficulty': 'MEDIUM', 'teamId': '200'}
        await connection.request('POST', '/lol-lobby/v1/lobby/custom/bots', data=bot)

#-----------------------------------------------------------------------------
# websocket
#-----------------------------------------------------------------------------
@connector.ready
async def connect(connection):
    #await GetTest(connection)
    await get_summoner_data(connection)
    #await create_ranked_game(connection)
    #await fill_role(connection)
    #await create_custom_lobby(connection)
    #await add_bots_team1(connection)
    #await add_bots_team2(connection)

@connector.open
async def connected(connection):
    print("running")

@connector.close
async def close(connection):
    print("closing")


@connector.ws.register('/lol-lobby/v2/lobby', event_types=('CREATE', 'UPDATE'))
async def lobby_created(connection, event):
    print(f"Created a lobby gameId: {event.data['gameConfig']['queueId']} MapId: {event.data['gameConfig']['mapId']} \n{event.data['localMember']}")


connector.start()
#connector.loop.run_forever()