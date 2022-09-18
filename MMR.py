#------------------------------------------------#
# Created by frogen10
# GitHub: https://github.com/frogen10
#------------------------------------------------#
import json
import requests, os
from varname import nameof
from Logger import Logger

_logger = Logger()
_url = {"eune" :"https://eune.whatismymmr.com/api/v1/summoner?name=", "euw": "https://euw.whatismymmr.com/api/v1/summoner?name="}

class MMR:
    def __init__(self) -> None:
        pass
    
    def get_data(self, uri: str)->None:
        tmp = requests.get(uri)
        data =tmp.json()
        _logger.LogMessage(nameof(MMR), "Loading mmr data")
        try:
            print( "RANKED: " + str(data["ranked"]["closestRank"])+ " " + str(data["ranked"]["percentile"]) + 
                "%\nNORMAL: "+str(data["normal"]["closestRank"]) + " " +str(data["normal"]["percentile"]) + 
                "%\nARAM: " +str(data["ARAM"]["closestRank"]) + " " +str(data["ARAM"]["percentile"]), end="%\n\n")
        except KeyError:
            print("Error not enough data", end="\n\n")

    def data_from_conf(self):
        y = {}
        with open("data.json", encoding= 'utf-8') as f:
            y= json.loads(f.read())

        for region in y["data"]:
            for sumName in y["data"][region]:
                print(sumName)
                url2= _url[region]+sumName
                self.get_data(url2)

    def SummonerMMR(self, name:str, region:str)->None:
        url2= _url[region]+name
        self.get_data(url2)

    
