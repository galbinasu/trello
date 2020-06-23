import json
import re

if __name__ == "__main__":

    with open('Trello Central Board JSON.json', 'r') as myfile:
        data=myfile.read()
    obj = json.loads(data)

    # # Add points
    # for card in obj["cards"]:
    #     last_open_index = card["name"].rfind("(")
    #     first_close_index = card["name"][last_open_index:].find(")")
        
    #     if (last_open_index != -1) and (first_close_index != -1):
    #         value = card["name"][last_open_index+1:last_open_index+first_close_index]
    #         if value.isdigit():
    #             pass
    #         else:
    #             value = "0"
    #     else:
    #         value = "0"
    #     card["!points"] = value

    # Add points regex
    for card in obj["cards"]:
        card["!points"] = "0"
        card["!dateCreation"] = "0"
        for value in re.findall('\(([^)]+)', card["name"]):
            if value.isdigit():
                card["!points"] = value

    # Add dateCreation
    for action in obj["actions"]:
        if action["type"] == "createCard":
            for card in obj["cards"]:
                if card["id"] == action["data"]["card"]["id"]:
                    card["!dateCreation"]=action["date"]
                

    for list in obj["lists"]:
        print "---"
        print list["name"]
        points = 0
        cards = []
        for card in obj["cards"]:
            if list["id"] == card["idList"]:
                points = points + int(card["!points"])
                cards.append({"id": card["id"], "name": card["name"], "!points": card["!points"], "!dateCreation":card["!dateCreation"]})
        sorted_cards = sorted(cards, key=lambda k: k['!dateCreation'])
        for x in sorted_cards:
            print x["name"] + " :: " + x["!points"] + " :: " + x["!dateCreation"]
        print "TOTAL points for " + list["name"] + ":: " + str(points)

    # with open('file.json', 'w') as file:
    #     file.write(json.dumps(obj))