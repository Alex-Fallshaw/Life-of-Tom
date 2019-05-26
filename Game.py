import json

class Game:
    def __init__(self,json_file_path):
        json_file = open(json_file_path)
        config = json.load(json_file)
        self.scenes = []
        for scene_config in config["scenes"]:
            scene = Scene(scene_config)
            self.scenes.append(scene)
        self.current_scene = self.scenes[0]

    def play(self):
        while self.current_scene:
            next_scene_id = self.current_scene.play()
            self.current_scene = self.get_scene(next_scene_id)
        print('Thanks for playing!')
        
    def get_scene(self, next_scene_id):
        for scene in self.scenes:
            if scene.id == next_scene_id:
                return scene


class Scene:
    def __init__(self, scene_config):
        self.config = scene_config
        self.id = scene_config["id"]
        self.prompt = scene_config["prompt"]
        self.options = scene_config["options"]

    def play(self):
        print(self.prompt)
        print(self.options_str())
        answer = self.get_valid_answer()
        option_number = int(answer)
        return self.get_next_scene_from_option_number(option_number)

    def options_str(self):
        options_list = ''
        for i, option in enumerate(self.options):
            options_list += f"[{i + 1}] {option['prompt']}\n"
        return options_list

    def get_valid_answer(self):
        answer = input('Type the number of your answer: ')
        if answer == 'quit':
            sys.exit()
        while not ((int(answer) - 1) in range(len(self.options))):
            answer = input('Please type the number of your answer: ')
        return answer

    def get_next_scene_from_option_number(self, option_number):
        option = self.options[option_number - 1]
        next_scene_id = option["next_scene"]
        return next_scene_id

Game('game.json').play()
        
import sys
def ask(question):  # Plays a question in the code.
    print(question['prompt'])
    
    answer = input('Type the number of your answer: ')
    if answer == 'quit':
        sys.exit()
    while answer != '1' and answer != '2' and answer != '3':
        answer = input('Please type the number of your answer: ')
    choice = question['options'][int(answer) - 1]
    reward = choice['reward']
    print(choice['response']+"\n")
