import json


class Stimulation:
    def __init__(self, filename):
        with open(filename, 'r') as infile:
            self.json_keys = json.load(infile)
