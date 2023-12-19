import os
    
class PromptTemplate():
    def __init__(self, path_elements):
        self.path_elements = path_elements
        self.path_elements[-1] = self.path_elements[-1] + '.txt'
        self.path = os.path.join(*self.path_elements)
        self.path = f'../prompt_template/{self.path}'
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
            
        data = [str(i) for i in data]
        for count, i in enumerate(data):
            prompt = self.content.replace(f'<INPUT {count}>', i)
            
        return prompt.strip()