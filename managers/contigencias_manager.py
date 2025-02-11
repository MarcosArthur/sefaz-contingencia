import json

class ContigenciasManager:
    def __init__(self, filename):
        self.filename = filename

    def load_contigencias(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_contigencias(self, contigencias):
        with open(self.filename, 'w') as f:
            json.dump(contigencias, f, indent=4)
