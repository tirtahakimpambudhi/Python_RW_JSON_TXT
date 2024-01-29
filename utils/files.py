import json
import os.path





class Files :
    def __init__ (self):
        pass

    def read_file_json(self,filename):
        try:
            filepath = os.path.join(os.getcwd(), "database", filename)
            with open(filepath) as json_file:
                menu = json.load(json_file)
                return menu
        except Exception as err:
            print(f"Error : {err}")
