# The Phantom v0.0.1 by The Phantasm Bot Projects

## Introduction

The Phantom is a Discord bot, which uses the Discord API to create convenient functions for the "The Phantasm" TTRPG Discord-server.

I am planning to expand the functionality so far, that other TTRPG servers can utilize it aswell

## Functions

<bold>Session planning (TODO)</bold></br>

<bold>Voting system (TODO)</bold></br>

<bold>Dice roller (WIP)</bold></br>

## Quickstart guide

To get going immediately run the `installer.sh` script

```bash
sudo chmod +x ./installer.sh

./installer.sh
```

## Install instructions

Set up your virtual environment using python3-venv:
```bash
python3 -m venv env

source ./env/bin/activate
```

Install all requirements from "requirements.txt":
```bash
python -m pip install -r "requirements.txt"
```

Lastly, set up your config file using the instructions provided withing the file and rename it (have your bots OAuth2 token ready):
```bash
mv config.yaml.template ./config.yaml
```

## Launching

Launch the bot with:
```bash
python3 -m ./app
```