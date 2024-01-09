import os
import copy
    
class PromptTemplate():
    def __init__(self, path_elements):
        self.path_elements = path_elements
        self.path_elements[-1] = self.path_elements[-1] + '.txt'
        self.path = os.path.join(*self.path_elements)
        
        current_script_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_script_path)
        parent_directory = os.path.dirname(current_directory)
        self.path = os.path.join(parent_directory, 'prompt_template', *self.path_elements)
        
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                self.content = f.read()
        else:
            self.content = None
            
    def render(self, data=None):
        if data == None:
            return self.content
        if (type(data) == type("string")):
            data = [data]
        
        prompt = copy.deepcopy(self.content)
        data = [str(i) for i in data]
        for count, i in enumerate(data):
            prompt = prompt.replace(f'<INPUT {count}>', i)
            
        return prompt.strip()