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
        # Python 'List Comprehensions' are great for this pattern
        # self.scenes = [Scene(self.store, scene_config)
        #                for scene_config in config['scenes']]

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
        # Another opportunity for List Comprehensions
        self.options = [Option(store, index, option_config)
                        for index, option_config
                        in enumerate(scene_config["options"])]

    def play(self):
        print(self.prompt.text())
        print(self.options_str())
        answer = self.get_valid_answer()
        option_number = int(answer)
        option = self.options[option_number - 1]
        option.set_consequences()
        print()
        print()
        return option.next_scene

    def options_str(self):
        options_list = '\n'
        for i, option in enumerate(self.options):
            options_list += f"[{i + 1}] {option.prompt}\n"
        return options_list
        # Another way of doing this with the new option.index:
        # (note this also fixes the trailing newline)
        # options_list = [f"[{option.index + 1}] {option.prompt}"
        #                 for option in self.options]
        # return '\n'.join(options_list)

    def get_valid_answer(self):
        answer = input('Type the number of your answer: ')
        if answer == 'quit':
            sys.exit()
        while not ((int(answer) - 1) in range(len(self.options))):
            answer = input('Please type the number of your answer: ')
        return answer


class Option:
    def __init__(self, store, index, option_config):
        self.store = store
        self.index = index
        self.next_scene = option_config['next_scene']
        self.prompt = option_config['prompt']
        if 'consequences' in option_config:
            self.consequences = option_config['consequences']
        else:
            # an empty list so we can assume we have a list in set_consequences
            self.consequences = []

    def set_consequences(self):
        for consequence in self.consequences:
            self.store.set(consequence['name'], consequence['value'])
        # Note that we could also have made the json file shorter by using
        # { "sword": 1 } instead of { "name": "sword", "value": 1 }
        # If we'd done that this would be:
        # for key in consequence.keys:
        #     self.store.set(key, consequence[key])


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
            # (See Github history for other changes by Alex's dad)
            # End part written by Alex's dad
        else:
            self.prompt_parts = []
            for part_config in prompt_config:
                part = PromptPart(store, part_config)
                self.prompt_parts.append(part)
            # Another opportunity for List Comprehensions
            # self.prompt_parts = [PromptPart(store, part_config)
            #                      for part_config in prompt_config]

    def text(self):
        full_prompt = ""
        for part in self.prompt_parts:
            full_prompt += part.text()
        return full_prompt
        # Another opportunity for a List Comprehension and a join
        # parts = [part.text() for part in self.prompt_parts]
        # return ''.join(parts)


class PromptPart:
    def __init__(self, store, part_config):
        self.store = store
        self.text_if_met = part_config['text_if_met']
        self.text_if_not_met = part_config["text_if_not_met"]

        self.requirements = []
        for requirement_config in part_config["requirements"]:
            requirement = Requirement(store, requirement_config)
            self.requirements.append(requirement)
        # Another opportunity for List Comprehensions
        # self.requirements = [Requirement(store, requirement_config)
        #                      for requirement_config
        #                      in part_config["requirements"]]

    def has_met_requirements(self):
        # Return false if any requirement is not #met(), true otherwise
        for requirement in self.requirements:
            if not requirement.met():
                return False
        return True

    def text(self):
        if self.has_met_requirements():
            return self.text_if_met
        else:
            return self.text_if_not_met


class Requirement:
    def __init__(self, store, requirement_config):
        self.store = store
        self.name = requirement_config["name"]
        self.value = requirement_config["value"]

    def met(self):
        if self.store.get(self.name) == self.value:
            return True
        else:
            return False


class Store:
    def __init__(self):
        self.store = {}

    def get(self, name):
        if name in self.store:
            return self.store[name]
        else:
            return None

    def set(self, name, value):
        self.store[name] = value


if __name__ == "__main__":
    game = Game('game.json')
    game.play()
