
def describe_room(player_location, rooms, character_descriptions):
    print("You are in the "+player_location+".")
    room_to_describe = rooms[player_location]

    print("Adjacent to this room are " +" or ".join(room_to_describe["adjacent rooms"]))
    
    for character in room_to_describe["characters"]:
        if(character!=""):
            description = character_descriptions[character]
            for line in description:
                print(line)
        else:
            print("There is no one in here, besides you.")

def speak_to(character, dialogs):
    for line in dialogs[character]:
        print(line)
