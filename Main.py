#------------------------------------------------#
# Created by frogen10
# GitHub: https://github.com/frogen10
#------------------------------------------------#

#------------------------------------------------#
# API endpoint checker
# http://www.mingweisamuel.com/lcu-schema/tool/
#------------------------------------------------#
import json
from unicodedata import name
from lcu_driver import Connector
from varname import nameof

from Logger import Logger
from Champions import Champions
from MMR import MMR
from LoLLobby import *
from Logger import Logger

_connector = Connector()
_logger =  Logger()
_exec = []
_summonerId = 0

class Main:

    def __init__(self) -> None:
        self.mmr = MMR()
        self.lobby = Lobby()
        self.region = 'unknown'

    async def fetch(self, query):
        '''
        Check if data is recived
        
        :query: activedata from lcu-driver request
        '''
        data = await query.json()
        _logger.LogMessage(nameof(Main), str(data))
        try:
            return data['httpStatus']
        except:
            return data

    async def get_client_data(self, connection):
        '''
        Get Summoner data and MMR
        '''
        _logger.LogMessage(nameof(Main), "Getting summoner data")
        activedata = await connection.request('GET', '/lol-client-config/v3/client-config/lol')
        data = await self.fetch(activedata)
        try:
            int(data)
            _logger.LogError(nameof(Main), data)
            return data
        except:
            self.set_region(data['game_client_settings']['redge_urls']['public']['loadouts'])

    def set_region(self, data)->None:
        
        if 'euw' in data:
            self.region = 'euw'
        elif 'eune' in data:
            self.region = 'eune'
        _logger.LogMessage(nameof(Main), f"Region set to: {self.region}")
        print(f"Region: {self.region}")


    async def get_summoner_data(self, connection):
        '''
        Get Summoner data and MMR
        '''
        _logger.LogMessage(nameof(Main), "Getting summoner data")
        activedata = await connection.request('GET', '/lol-summoner/v1/current-summoner')
        data = await self.fetch(activedata)
        if data is int:
            _logger.LogError(nameof(Main), data)
            return
        global _summonerId
        try:
            _summonerId, summonerName, summonerPuuid = data['summonerId'], data['displayName'], data['puuid']
        
        except:
            _logger.LogReadDataError(nameof(Main), "Wrong endpoint!")
            return
        
        print(f"summonerId:     {_summonerId}")
        print(f"displayName:    {summonerName}")
        print(f"puuid:          {summonerPuuid}")
        print('-')
        self.mmr.SummonerMMR(summonerName, self.region) #todo check region

    async def bot_data(self, connection):
        '''
        Get info about avaliable bots
        '''
        activedata = await connection.request('GET', '/lol-lobby/v2/lobby/custom/available-bots')
        data = await self.fetch(activedata)
        if data is int:
            _logger.LogReadDataError(nameof(Main), data)
            return data
        champions = { bot['name']: bot['id'] for bot in data }
        print(champions)
        return champions

    async def champion_data(self, connection):
        '''
        Get info about avaliable bots
        '''
        activedata = await connection.request('GET', '/lol-champ-select/v1/picable-champion-ids')
        data = await self.fetch(activedata)
        if data is int:
            _logger.LogReadDataError(nameof(Main), data)
            return data
        champions = { bot['name']: bot['id'] for bot in data }
        print(champions)
        return champions

    def set_game(self, gameMode: Game, firstRole: Role, secondRole: Role):
        '''
        Sets lobby type and roles
        '''
        _logger.LogMessage(nameof(Main), "Set up a game values")
        self.gameMode = gameMode
        self.firstRole = firstRole
        self.secondRole = secondRole
    
    async def create_classic_game(self, connection):
        '''
        Creates lobby with roles
        '''
        await self.lobby.create_classic_games(connection, self.gameMode, self.firstRole, self.secondRole)
    

@_connector.open
async def connected(connection):
    print("Running...\nPrepering functions...")
    _logger.LogMessage(nameof(Main), "Running...\nPrepering functions...")

@_connector.ready
async def connect(connection):
    _logger.LogMessage(nameof(Main), "Ready")
    for i in _exec:
        await i(connection)

@_connector.ws.register('/lol-lobby/v2/lobby', event_types=('CREATE',))
async def lobby_created(connection, event):
    _logger.LogMessage(nameof(Main) , f"Created a lobby gameId: {event.data['gameConfig']['queueId']} MapId: {event.data['gameConfig']['mapId']} \n{event.data['localMember']}")

@_connector.ws.register('/lol-lobby/v2/lobby/localMember', event_types=('UPDATE',))
async def lobby_created(connection, event):
    _logger.LogMessage(nameof(Main) ,f"Updated a lobby gameId: {event.data}")

@_connector.ws.register('/lol-champ-select/v1/session', event_types=('UPDATE',))
async def lobby_created(connection, event):
    _logger.LogMessage(nameof(Main) ,f"Updated a champ select: {event.data}")

if __name__ == '__main__':
    main = Main()
    _exec.append(main.get_client_data)
    _exec.append(main.get_summoner_data)
    main.set_game(Game.RANKED, Role.SUPP, Role.MID)
    _exec.append(main.create_classic_game)
    
    _connector.start()


