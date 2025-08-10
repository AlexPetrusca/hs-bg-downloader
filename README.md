# Hearthstone Battlegrounds Image Downloader

This script downloads high-quality images of all cards currently available in Hearthstone Battlegrounds. 

This includes images for all:
- Heroes
- Minions (grouped by tier, 1-7)
- Tavern Spells
- Quests
- Quest Rewards
- Trinkets (grouped by lesser and greater)
- Anomalies

Images links are fetched from Blizzard's Hearthstone API and downloaded directly from Blizzard's CDN. These are the same images found on Blizzards official page for [Hearthstone Battlegrounds](https://hearthstone.blizzard.com/en-us/battlegrounds).

### How to Use

> [!IMPORTANT]
> Calling Blizzard's API requires [setting up a client](https://develop.battle.net/documentation/guides/getting-started). This script expects a Client ID and Client Secret as input.

1. Clone this repo and open it in a terminal.
2. Install requirements with `pip3 install -r requirements.txt`.
3. Pass your Client ID and Client Secret as environment variables to the script. Create a file named `.env` with content:
```
BLIZZARD_CLIENT_ID="<client_id>"
BLIZZARD_CLIENT_SECRET="<client_secret>"
```
4. Run the script with `python3 downloader.py`.
5. Images are written to `out` folder in the same directory.
