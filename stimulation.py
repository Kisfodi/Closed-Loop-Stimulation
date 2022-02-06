import json
import pickle
import os
from retinotopic_mapping import DisplayLogAnalysis

class Stimulation:
    def __init__(self, pathname):
        self.pathname = pathname
        self.json_path = self.pathname.replace('.pkl', '.json')
        self.filename,self.extension = os.path.splitext(self.pathname)
        if ("pkl" in self.extension):
            self.log = DisplayLogAnalysis.DisplayLogAnalyzer(self.pathname)
            self.log.stim_block_extractor()
            self.log.save_to_json()
            self.load_json()
        elif ("json" in self.extension):
             self.load_json()

        # self.stim_type = self.log['stim_parameters']['stim_type']
        # if ('CombinedStimuli' in self.stim_type):
        #     self.indices = self.log['iteration_indices']
        # elif ("DriftingGratingCircle" in self.stim_type):
        #     self.indices = self.log['direction_indices']
        # else:
        #     self.indices = []
        #     print("Not implemented yet!!!")
    def load_json(self):
        with open (self.json_path) as json_file:
            self.log = json.load(json_file)