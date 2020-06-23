import json
import re
import sys

orig_stdout = sys.stdout

def trello(filename):
    try:
        print("Reading :: " + filename)
        with open(filename, 'r') as myfile:
            data=myfile.read()
        if data == "":
            print("Empty JSON")
        else:
            print("Output in " + filename + ".txt")
            obj = json.loads(data)
    except IOError:
        print("File does not exist")
        return

    with open(str(filename + ".txt"), 'w') as file:
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
            card["name"] = card["name"].encode('ascii',errors='ignore').decode()
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
            filter = ["90 Day Priorities", "Product Backlog", "SPRINT GOALS", "7/4 sprint planning -59 points", "Code Review", "Testing", "items done in sprint ending 24/03- 96"]
            if list["name"] in filter :
                continue
            list["name"] = list["name"].encode('ascii',errors='ignore').decode()
            file.write("\n---\n")
            file.write(list["name"])
            file.write("\n")
            count = 0
            points = 0
            cards = []
            for card in obj["cards"]:
                if list["id"] == card["idList"]:
                    count = count + 1
                    points = points + int(card["!points"])
                    cards.append({"id": card["id"], "name": card["name"], "!points": card["!points"], "!dateCreation":card["!dateCreation"]})
            sorted_cards = sorted(cards, key=lambda k: k['!dateCreation'])
            for x in sorted_cards:
                file.write(x["name"] + " :: " + x["!points"] + " :: " + x["!dateCreation"])
                file.write("\n")

            file.write("TOTAL cards :: " + str(count))
            file.write("\n")
            file.write("TOTAL points for " + list["name"] + ":: " + str(points))


if __name__ == "__main__":
    files = ["Hes1FJVS.json", "EVRZYgQW.json", "P4KtJpAt.json"]
    for file in files:
        trello(file)
