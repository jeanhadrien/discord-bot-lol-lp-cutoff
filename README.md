# LeagueRankBot


## Description

LPCutoff is a Discord bot built in Python to help you find out how many LPs are needed to reach the Challenger or Grandmaster tiers in League of Legends.

## Features
- !rank command to check LP cutoff
- Supports all servers
- Caches API calls to reduce spam

## Installation
### Prerequisites
- Python 3.8 or higher
- pip
- Discord API Token
- Riot Games API Token
### Steps
Clone the repository
```
git clone https://github.com/yourusername/LeagueRankBot.git
```

Navigate to the project folder
```
cd LeagueRankBot
```

Install required packages
```
pip install -r requirements.txt
```
Add your Discord and Riot Games API tokens to a `.env` file
```
DISCORD_BOT_TOKEN=XXX
RIOT_API_KEY=XXX
```

Run the bot
```
python main.py
```

## Usage

`!rank <queue> <server>`
- queue: solo,tft
- server: euw1,na1,etc.

## Caching
The bot caches API results to minimize the number of calls to the Riot Games API, thereby complying with rate limits.
