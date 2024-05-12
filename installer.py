import yaml

token = input('Please paste your Discord API token here: ')

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

config['app']['discord_api']['token'] = token

with open('config.yaml', 'w') as file:
    yaml.dump(config, file)