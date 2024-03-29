


def examine(game_state, command): ## Examine a room, character, or an item. 
    name_to_examine = " ".join(command.split()[1:]) ## get the name of the thing the player wants to examine
    
    if(name_to_examine==""): ## if the player has just typed 'look'
        describe_room(game_state, game_state["p_loc"]) ## tell the player about the room they are in
        return game_state
        
    if (name_to_examine in game_state["rooms"]): ## if the player wants to examine a room
        if(name_to_examine == game_state["p_loc"]): ## if the player is examining the room they are currently in.
            describe_room(game_state, name_to_examine)  ## describe the room.
            return game_state
        else: ## otherwise,
            print("You aren't in the "+name_to_examine+"!") ## tell the player they aren't in that room.
            return game_state
    
    if(name_to_examine in game_state["items"]): ## if the player wants to examine an item
        if(name_to_examine in game_state["rooms"][game_state["p_loc"]]["Items"] or name_to_examine in game_state["p_inv"]): ## if the player is examining an item in the room or in their inventory
            describe_item(game_state, name_to_examine) ## describe the item
            return game_state
        else: ## otherwise,
            print("You can't see a "+ name_to_examine +" in here.") ## tell the player that they can't see that item.
            return game_state
            
    if(name_to_examine in game_state["characters"]): ## if the player wants to examine a character
        if(name_to_examine in game_state["rooms"][game_state["p_loc"]]["Characters"]): ## if the player is in the same room as the character
            describe_character(game_state, name_to_examine) # describe the character
            return game_state
        else: ## otherwise,
            print("You don't see "+name_to_examine+" in here.") ## tell the player they can't see the character in this room.
            return game_state
    ## If the name to examine isn't an item, character, or room,
    print("What? What's a " + name_to_examine + "?") ## Tell the player
    return game_state
    
    
def describe_item(game_state, item_to_examine):
    print("This is a "+item_to_examine+". "+ game_state["items"][item_to_examine]["Description"])


def describe_room(game_state, room_to_examine):
    print("This is a "+room_to_examine+". "+ game_state["rooms"][room_to_examine]["Description"])
    print("Connected to this room is " + " and ".join(game_state["rooms"][room_to_examine]["Adjacent rooms"]))
    if(len(game_state["rooms"][room_to_examine]["Items"])>0):
        print("There is a "+ " and ".join(game_state["rooms"][room_to_examine]["Items"]) )
    if(len(game_state["rooms"][room_to_examine]["Characters"])>0):
        print(" and ".join(game_state["rooms"][room_to_examine]["Characters"]) + " is here.")
    
    
def describe_character(game_state, character_to_examine):
    print("This is "+character_to_examine+". "+ game_state["characters"][character_to_examine])
    
    
def take_item(game_state, command):
    item_to_grab = " ".join(command.split()[1:]) ## get the name of the item the player wants to pick up.
    if(item_to_grab in game_state["rooms"][game_state["p_loc"]]["Items"]): ## if the item the player wants to pick up is inside the room
        game_state["p_inv"] += [item_to_grab] ## add the item to the players inventory
        game_state["rooms"][game_state["p_loc"]]["Items"].remove(item_to_grab) ## remove the item from the room.
        print("You grabbed the "+item_to_grab+".") ## tell the player they grabbed that item.
        
        game_state["p_flags"] +=["[ITEM] HAS "+item_to_grab] ## add a flag saying that the player has picked up the item.
        return game_state
    else: ## otherwise,
        print("There isn't a "+item_to_grab+" in here!") ## tell the player they can't grab that item
        return game_state   
        
def move_player(game_state, command):
    destination = " ".join(command.split()[1:]) ## get the name of the room the player wants to go to.
    if(destination in game_state["rooms"][game_state["p_loc"]]["Adjacent rooms"]): ## if the destination is adjecent to the player's current location
        game_state["p_loc"] = destination ## move the player to that room.
        print("You go to a "+destination+".") ## tell the player they succeded.
        return game_state
    else:
        print("You can't walk through walls!") ## tell the player that they failed.
        return game_state
        
def use_item(game_state, command): ## TODO: finish this function so that the player can use items.
    return game_state
    
    
def meets_requirements(player_flags, required_flags, prevent_flags):
    for val in required_flags:
        if not val in player_flags:
            return False
    for val in prevent_flags:
        if val in player_flags:
            return False
    return True

    

def print_dialog(game_state, room_dialog):

    responses = ["a"]
    conversation_history=[]
    while len(responses)!=0:
        dialog=None
        
        ## check to see if the player has any flags which allow different dialog options
        for i in range(len(room_dialog)): ## for each dialog tree the character has in this room
            dialog_tree = room_dialog[i]
            if( not (dialog_tree in conversation_history) and meets_requirements(game_state["p_flags"], dialog_tree["Requirements"], dialog_tree["Disqualifiers"])): ## if the player meets all of the requirements for this dialog tree
                dialog = dialog_tree
                break
                
        if(dialog==None):
            flags_copy = game_state["p_flags"][:]
            for flag in flags_copy:
                if(flag.startswith("[TEMP]")):
                    game_state["p_flags"].remove(flag)
            return game_state
            
            
        conversation_history += [dialog_tree]
        responses = dialog["Response options"]
    
        
    
        print(dialog["Dialog"])
        
        if(len(responses)==0):
            flags_copy = game_state["p_flags"][:]
            for flag in flags_copy:
                if(flag.startswith("[TEMP]")):
                    game_state["p_flags"].remove(flag)
                    
            return game_state
        
        for i in range(len(responses)):
            print(str(i)+". "+ responses[i][0])
        
        player_choice = int(input())

        
        game_state["p_flags"] += responses[player_choice][1]
        
    flags_copy = game_state["p_flags"][:]
    for flag in flags_copy:
        if(flag.startswith("[TEMP]")):
            game_state["p_flags"].remove(flag)
                
    return game_state

    


def talk_to(game_state, command): 
    character = " ".join(command.split()[1:]) ## get the name of the character the player wants to talk to.

    if(character in game_state["rooms"][game_state["p_loc"]]["Characters"] or ( any(["[CHARACTER] "+character in game_state["items"][item]["Properties"] for item in game_state["p_inv"]]))): ## if the character is in the room
        room_dialog = game_state["dialog"][character][game_state["p_loc"]] ## all the dialog options for the character in this room.
        return print_dialog(game_state, room_dialog)
    else:
        print(character + " isn't in here!")
             
    return game_state
            
            



def combine(game_state, command):
    first_item = command[command.find("combine")+7:command.find("with")].strip()
    second_item = command[command.find("with")+5:].strip()
    
    if(first_item in game_state["p_inv"] and second_item in game_state["p_inv"]):
        for p in game_state["items"][first_item]["Properties"]:
            if p.startswith("[COMBINE]") and second_item in p:
                game_state["p_inv"].remove(first_item)
                game_state["p_inv"].remove(second_item)
                game_state["p_inv"] += [p[p.find(">")+1:]]
                break
    return game_state
    
def check_inv(game_state, command):
    print("You have "+", ".join( str(item) for item in game_state["p_inv"]))
    return game_state
    
def help(game_state, command):
    print("You can talk [character], take [item], go [room], look [room], look [item], look [character], combine [item1] with [item2], inv")
    return game_state