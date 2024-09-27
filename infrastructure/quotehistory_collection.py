import json
from models.quotehistory import Quotehistory

class QuotehistoryCollection:
    FILENAME = "quotehistory.json"
    API_KEYS = ["Symbol", "Precision", "TradeAmountStep"]

    def __init__(self):
        self.quotehistory_dict = {}

    def LoadQuotehistory(self, path):
        self.quotehistory_dict = {}
        fileName = f"{path}/{self.FILENAME}"
        with open(fileName, "r") as f:
            data = json.loads(f.read())
            for k,v in data.items():
                self.quotehistory_dict[k] = Quotehistory.FromApiObject(v)
    
    def CreateFile(self, data, path):
        if data is None:
            print("Quotehistory file creation failed")
            return
        
        quotehistory_dict = {}
        for i in data:
            key = i['Symbol']
            quotehistory_dict[key] = { k: i[k] for k in self.API_KEYS }

        fileName = f"{path}/{self.FILENAME}"
        with open(fileName, "w") as f:
            f.write(json.dumps(quotehistory_dict, indent=2))

    def PrintQuotehistory(self):
        [print(k,v) for k,v in self.quotehistory_dict.items()]
        print(len(self.quotehistory_dict.keys()), "quotehistory")
        

quotehistoryCollection = QuotehistoryCollection()