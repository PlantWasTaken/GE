import json

n = []

with open(r"C:\Users\Max\Desktop\Osrs bot\Grand exchange\bank.json", "r") as jsonFile:
    data = json.load(jsonFile)



with open(r"C:\Users\Max\Desktop\Osrs bot\Grand exchange\bank.json", "w") as jsonFile:
    for i in range(3):
        data["items"]['slot' + str(i+1)]['Item'] = "hi"
        data['items']['slot' + str(i+1)]['Price'] = i
    json.dump(data, jsonFile, indent=4)