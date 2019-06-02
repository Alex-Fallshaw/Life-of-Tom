import json
import sys

class Game:
    def __init__(self, json_file_path):
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
        self.prompt = Prompt(scene_config["prompt"])
        self.options = scene_config["options"]

    def play(self):
        print(self.prompt.text())
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

class Prompt:
    def __init__(self, prompt_config):
        self.config = prompt_config

    def text(self):
        if type(self.config) is str:
            return self.config
        else:
            full_prompt = ""
            for part_config in self.config:
                full_prompt += self.part_text(part_config)
            return full_prompt

    def part_text(self, part):
        if part.has_met_requirements():
            return part.text_if_met
        else:
            return part.text_if_not_met

class PromptPart:
    def __init__(self, part_config):
        self.config = part_config
        self.text_if_met = part_config['text_if_met']
        self.text_if_not_met = part_config["text_if_not_met"]
        self.requirements = part_config["requirements"]

    def self.has_met_requirements(self):
        for requirement in requirements:
            if requirement.met():

class Requirement:
    def __init__(self, requirement_config):
        self.name = requirement_config['name']
        self.value = requirement_config['value']

    def met(self):
        if self.store(self.name) == self.value:
            return True
        else:
            return False
    
game = Game('game.json')
game.play()