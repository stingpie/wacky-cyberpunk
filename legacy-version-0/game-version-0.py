## CYBERPUNK ADVENTURE!!

import helper_functions as hf


character_files={"Ravenette description":"ravenette-desc.txt",
                 "Ravenette":"ravenette-dialog.txt",
                 "Nullbird description":"nullbird-desc.txt",
                 "Nullbird":"nullbird-dialog.txt"}

character_dialogs={}
character_descriptions={}
for name, file in character_files.items():
    if "description" in name:
        character_descriptions[name.split()[0]] = open(file, "r").readlines()
    else:
        character_dialogs[name] = open(file, "r").readlines()
    


rooms = {"patio":{"adjacent rooms":["kitchen"],"characters":["Nullbird"]},
         "kitchen":{"adjacent rooms":["garage", "patio"], "characters":[""]},
         "garage":{"adjacent rooms":["kitchen"], "characters":["Ravenette"]}}

player_location = "kitchen"




while True:
    player_command = input()

    if(player_command.startswith("look")):
        hf.describe_room(player_location, rooms, character_descriptions)

    if(player_command.startswith("go")):
        if(player_command.split()[-1] in rooms[player_location]["adjacent rooms"]):
            player_location = player_command.split()[-1]

    if(player_command.startswith("talk")):
        if(player_command.split()[-1] in rooms[player_location]["characters"]):
            hf.speak_to(player_command.split()[-1], character_dialogs)

    if(player_command.startswith("quit") or player_command.startswith("exit()")):
        break


