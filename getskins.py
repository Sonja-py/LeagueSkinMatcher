import requests
import csv
from lcu_driver import Connector

print("fetching skin metadata...")
skins_metadata = requests.get(
    "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/skins.json"
).json()

print("fetching skinline metadata...")
skinline_metadata = requests.get(
    "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/skinlines.json"
).json()

# dict of skinline id to name
skin_map = {skin["id"]: skin for skin in skins_metadata.values()}
skinline_map = {line["id"]: line.get("name", "Unknown") for line in skinline_metadata}


# lcu connection
connector = Connector()

@connector.ready
async def connect(connection):
    print("connected to lcu")

    # get summoner name
    summoner_resp = await connection.request("GET", "/lol-summoner/v1/current-summoner")
    summoner = await summoner_resp.json()
    summoner_name = summoner["gameName"]
    
    # get owned skins
    skins_resp = await connection.request("GET", "/lol-inventory/v2/inventory/CHAMPION_SKIN")
    skins = await skins_resp.json()
    owned = [s for s in skins if s.get("owned")]

    print(f"summoner: {summoner_name}, owned skins: {len(owned)}")

    # add rows
    rows = []
    for s in owned:
        sid = s["itemId"]
        meta = skin_map.get(sid)
        if not meta:
            continue

        skin_name = meta.get("name", f"Skin {sid}")

        # its silly but the best way to get the champ name seems to be through the splash path
        splash_path = meta.get("splashPath", "")
        try:
            champion = splash_path.split("/Characters/")[1].split("/")[0]
        except IndexError:
            champion = "Unknown"

        # skinline
        skinlines_list = meta.get("skinLines")
        if not skinlines_list:
            skinline = None
        else:
            line_id = skinlines_list[0]["id"]
            skinline = skinline_map.get(line_id, None)

        rows.append([summoner_name, champion, skin_name, skinline])


    # Stoutput
    with open("owned_skins.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["SummonerName", "Champion", "Skin", "SkinLine"])
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to owned_skins.csv")
    await connector.stop()

connector.start()
