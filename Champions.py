
from typing import List


class Champions:
    def __init__(self, connection) -> None:
        self.connection =connection
        

    async def get_champions(self):
        champs= await self.connection.request('GET', '/lol-champions/v1')
        return champs
    


