import requests
from config import URL, Streamer


def api_reader():
    FACEIT = str(URL) + str(Streamer)
    r = requests.get(FACEIT)
    data = r.json()
    iElo = data['elo']
    acEloToday = data['todayEloDiff']
    iRank = data['lvl']
    iStreak = data['stats']['lifetime']['Current Win Streak']
    for data in data['latestMatches']:
        acResult = data['result'][0]
        acScore = data['teamScore']
        acKd = data['kd']
        acMap = data['map'][3:]
        break
    return iElo, acEloToday, iRank, acResult, acScore, acKd, acMap, iStreak
