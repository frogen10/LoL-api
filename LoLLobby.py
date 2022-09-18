from queue import Empty
from enum import Enum
from lcu_driver import Connector, connection

class MAP_ID(Enum):
    SUMMONER_RIFT = 12
    HOWLING_ABYS = 11

class Game(Enum):
    PRACTICETOOL = -1
    DRAFT = 400
    RANKED = 420
    BLIND = 430
    FLEX = 440
    ARAM = 450
    ULT_SPELL =1400

class Role(Enum):
    SUPP = 'UTILITY'
    JGL = 'JUNGLE'
    MID = 'MIDDLE'
    ADC = 'BOTTOM'
    FILL = 'FILL'
    TOP = 'TOP'

class Lobby:
    
    async def create_classic_games(self, connection: connection, gameMode: Game, firstRole: Role, secondRole: Role)->None:
        """
        creates classic game with proper GameMode

            gameMode: switch between game modes
        """
        self.firstRole = firstRole
        self.secondRole = secondRole
        data = { 'queueId': gameMode.value }
        role = { "firstPreference": firstRole.value, "secondPreference": secondRole.value }

        await connection.request('POST', '/lol-lobby/v2/lobby', data=data)
        await connection.request('PUT', '/lol-lobby/v1/lobby/members/localMember/position-preferences', data=role)


    async def create_custom_game(self, connection: connection, mapId: int, size: int, bots= {'100':[], '200':[]}, passwd = '')-> None:
        """
        creates custom game 

            mapId: switch between maps
            size: team size
            [bots]: [{'100':[], '200':[]}] bots in game
            [passwd]: [''] password to lobby
        """

        custom = {
        'customGameLobby': {
            'configuration': {
                'gameMode': 'PRACTICETOOL',
                'mapId': mapId,
                'mutators': {'id': 1},
                'spectatorPolicy': 'AllAllowed',
                'teamSize': size},
            'lobbyName': 'PRACTICETOOL',
            'lobbyPassword': passwd},
        'isCustom': True}

        await connection.request('POST', '/lol-lobby/v2/lobby', data=custom)

        activedata = await self.connection.request('GET', '/lol-lobby/v2/lobby/custom/available-bots')
        champions = { bot['name']: bot['id'] for bot in await activedata.json() }

        for team in bots:
            if team is not Empty:
                
                for name in team:
                    bot = { 'championId': champions[name], 'botDifficulty': 'MEDIUM', 'teamId': team.Key }
                    await connection.request('POST', '/lol-lobby/v1/lobby/custom/bots', data=bot)


        