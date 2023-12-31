# LeagueRankBot


## Description

LPCutoff is a Discord bot built in Python to help you find out how many LPs are needed to reach the Challenger or Grandmaster tiers in League of Legends.

![Screenshot_2](https://github.com/jeanhadrien/discord-bot-lol-lp-cutoff/assets/40248338/70606be6-e438-4b08-a20b-507e363da32f)

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
git clone https://github.com/jeanhadrien/discord-bot-lol-lp-cutoff
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
- queue: solo,flex
- server: euw,na,etc.

## Caching
The bot caches API results to minimize the number of calls to the Riot Games API, thereby complying with rate limits.
