#------------------------------------------------#
#http://www.mingweisamuel.com/lcu-schema/tool/
#------------------------------------------------#
from lcu_driver import Connector
#from Champions import Champions
from MMR import MMR
from LoLLobby import Game, Lobby, Role
connector = Connector()
exec = []
class Main:

    def __init__(self) -> None:
        self.mmr = MMR()
        self.lobby = Lobby()

    async def fetch(self, query):
        data = await query.json()
        try:
            return data['httpStatus']
        except:
            return data
            

    async def get_summoner_data(self, connection):
        activedata = await connection.request('GET', '/lol-summoner/v1/current-summoner')
        data = await self.fetch(activedata)
        if data is int:
            print(f"Error to read bot {data}")
            return data
        summonerId, summonerName, summonerPuuid = data['summonerId'], data['displayName'], data['puuid']
        print(f"displayName:    {summonerId}")
        print(f"summonerId:     {summonerName}")
        print(f"puuid:          {summonerPuuid}")
        print('-')
        self.mmr.SummonerMMR(summonerName, 'euw') #todo check region

    async def bot_data(self, connection):
        activedata = await connection.request('GET', '/lol-lobby/v2/lobby/custom/available-bots')
        data = await self.fetch(activedata)
        if data is int:
            print(f"Error to read bot {data}")
            return data
        champions = { bot['name']: bot['id'] for bot in data }
        print(champions)
        return champions
    
    def set_game(self, gameMode: Game, firstRole: Role, secondRole: Role):
        self.gameMode = gameMode
        self.firstRole = firstRole
        self.secondRole = secondRole
    
    async def create_classic_game(self, connection):
        await self.lobby.create_classic_games(connection, self.gameMode, self.firstRole, self.secondRole)
    

@connector.open
async def connected(connection):
    print("Running...\nPrepering functions...")

@connector.ready
async def connect(connection):
    for i in exec:
        await i(connection)

if __name__ == '__main__':
    main = Main()
    exec.append(main.get_summoner_data)
    main.set_game(Game.RANKED, Role.SUPP, Role.MID)
    exec.append(main.create_classic_game)
    #ecec.append(main.bot_data)
    connector.start()


