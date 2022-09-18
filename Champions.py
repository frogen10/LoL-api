#------------------------------------------------#
# Created by frogen10
# GitHub: https://github.com/frogen10
#------------------------------------------------#

from typing import List


class Champions:
    def __init__(self, championId: int) -> None:
        self.championId = championId
        self.champions = []

    async def get_champions(self):
        activedata = await self.connection.request('GET', f'/lol-champions/v1/inventories/{self.summonerId}/champions')
        data = await activedata.json()
        print(data)
