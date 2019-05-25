import json

class Game:
    def __init__(self,json_file_path):
        json_file = open(json_file_path)
        config = json.load(json_file)
        self.config = config

    def play(self):
        print(self.config)

Game('game.json').play()
        
