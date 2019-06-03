import json
import sys


class Game:
    def __init__(self, json_file_path):
        json_file = open(json_file_path)
        config = json.load(json_file)
        self.store = Store()
        self.scenes = []
        for scene_config in config["scenes"]:
            scene = Scene(self.store, scene_config)
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
    def __init__(self, store, scene_config):
        self.store = store
        self.id = scene_config["id"]
        self.prompt = Prompt(store, scene_config["prompt"])
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
    def __init__(self, store, prompt_config):
        self.store = store
        if type(prompt_config) is str:
            # This section written by Alex's dad
            self.prompt_parts = [
                PromptPart(store, {
                    "text_if_met": prompt_config,
                    "text_if_not_met": '',
                    "requirements": []
                })
            ]
            # End part written by Alex's dad
        else:
            self.prompt_parts = []
            for part_config in prompt_config:
                part = PromptPart(store, part_config)
                self.prompt_parts.append(part)

    def text(self):
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
    def __init__(self, store, part_config):
        self.store = store
        self.text_if_met = part_config['text_if_met']
        self.text_if_not_met = part_config["text_if_not_met"]
        self.requirements = []
        for requirement_config in part_config["requirements"]:
            requirement = Requirement(store, requirement_config)
            self.requirements.append(requirement)

    def has_met_requirements(self):
        for requirement in self.requirements:
            if requirement.met():
                return True


class Requirement:
    def __init__(self, store, requirement_config):
        self.store = store
        self.name = requirement_config["name"]
        self.value = requirement_config["value"]

    def met(self):
        if self.store(self.name) == self.value:
            return True
        else:
            return False


class Store:
    def __init__(self):
        self.store = {}

    def get(self, name):
        return self.store[name]

    def set(self, name, value):
        self.store[name] = value


game = Game('game.json')
game.play()