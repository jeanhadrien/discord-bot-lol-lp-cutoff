import os
import requests
import decorators

API_CACHE_SECONDS = 600
API_RATE_LIMIT_SECOND = 20
API_RATE_LIMIT_MINUTE = 50

QUEUES = {
    "solo": "RANKED_SOLO_5x5",
    "flex": "RANKED_FLEX_SR",
}

TIERS = ["challenger", "master", "grandmaster"]

SERVERS = {
    "br": "br1",
    "euw": "euw1",
    "eu": "euw1",
    "na": "na1",
    "jp": "jp1",
    "kr": "kr",
    "eun": "eun1",
    "la1":"la1",
    "la2":"la2",
    "la":"la1",
    "oc":"oc1",
    "ph":"ph2",
    "ru":"ru",
    "sg":"sg2",
    "th":'th2',
}


@decorators.time_based_cache(timeout=API_CACHE_SECONDS)
@decorators.rate_limited(API_RATE_LIMIT_SECOND, "second")
@decorators.rate_limited(API_RATE_LIMIT_MINUTE, "minute")
def fetch_players_by_page(server, queue, tier, page):
    if server.lower() not in SERVERS:
        raise ValueError(f"Accepted servers : {', '.join(SERVERS.keys())}")
    if queue.lower() not in QUEUES:
        raise ValueError(f"Accepted queues : {', '.join(QUEUES.keys())}")
    if tier.lower() not in TIERS:
        raise ValueError(f"Accepted tiers : {', '.join(TIERS)}")
    url = f"https://{SERVERS[server]}.api.riotgames.com/lol/league-exp/v4/entries/{QUEUES[queue]}/{tier.upper()}/I?page={page}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": os.getenv["RIOT_API_KEY"],
    }
    try:
        print(f"Fetching page {page} of {tier} in {queue} ({server})")
        resp = requests.get(url, headers=headers)
        result = resp.json()
        print(len(result))
        return result
    except Exception as error:
        print(f"{error}")


@decorators.time_based_cache(timeout=API_CACHE_SECONDS)
def fetch_players_by_tier(server, queue, tier):
    all_players = []
    page = 1
    while True:
        fetched_players = fetch_players_by_page(server, queue, tier, page)
        if (
            not fetched_players
            or len(fetched_players) == 0
            or (tier == "MASTER" and page > 5)
        ):
            break
        all_players.extend(fetched_players)
        page += 1
    return all_players


@decorators.time_based_cache(timeout=API_CACHE_SECONDS)
def fetch_players_by_queue(server, queue):
    all_players = []
    for tier in ["CHALLENGER", "GRANDMASTER", "MASTER"]:
        fetched_players = fetch_players_by_tier(server, queue, tier)
        if fetched_players:
            all_players.extend(fetched_players)
    return all_players


def parse_rank_data(all_players):
    # Sort the all_players list by the leaguePoints key in descending order
    gm_count = sum(1 for d in all_players if "tier" in d and d["tier"] == "GRANDMASTER")
    chall_count = sum(
        1 for d in all_players if "tier" in d and d["tier"] == "CHALLENGER"
    )
    sorted_players = sorted(all_players, key=lambda x: x["leaguePoints"], reverse=True)

    # Extract the leaguePoints from the sorted list into a new list
    lps = [player["leaguePoints"] for player in sorted_players]

    return {"lps": lps, "gm_count": gm_count, "chall_count": chall_count}

