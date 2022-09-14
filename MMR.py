import json
import requests, os
url = {"eune" :"https://eune.whatismymmr.com/api/v1/summoner?name=", "euw": "https://euw.whatismymmr.com/api/v1/summoner?name="}

class MMR:
    def __init__(self) -> None:
        pass
    def get_data(self, uri: str)->None:
        tmp = requests.get(uri)
        data =tmp.json()
        try:
            print( "ranked: " + str(data["ranked"]["closestRank"])+ " " + str(data["ranked"]["percentile"]) + "%\nnormal: "+str(data["normal"]["closestRank"]) + " " +str(data["normal"]["percentile"])+ "%\nARAM: " +str(data["ARAM"]["closestRank"]) + " " +str(data["ARAM"]["percentile"]), end="%\n\n")
        except KeyError:
            print("Error not enough data", end="\n\n")

    def data_from_conf(self):
        y = {}
        with open("data.json", encoding= 'utf-8') as f:
            y= json.loads(f.read())

        for i in y["data"]:
            for j in y["data"][i]:
                print(j)
                url2= url[i]+j
                self.get_data(url2)

    def SummonerMMR(self, name:str, region:str)->None:
        url2= url[region]+name
        self.get_data(url2)

    
