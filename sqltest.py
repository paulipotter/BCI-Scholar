import json

def testjson(calf_list):
    print("About to start CSV export...")
    with open("result.json","w") as f:
        json.dump(calf_list,f, sort_keys = True, indent = 4, separators = (',',':'))
        #for calf in calf_list:
         #   jsonData = json.dump(calf_list[calf])