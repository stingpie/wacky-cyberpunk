


def examine(game_state, command): ## Examine a room, character, or an item. 
    name_to_examine = " ".join(command.split()[1:]) ## get the name of the thing the player wants to examine
    
    
    
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
    print("This is a "+item_to_examine+". "+ game_state["items"][item_to_examine])


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
    
    
def meets_requirements(player_flags, required_flags):
    for val in required_flags:
        if not val in player_flags:
            return False
    return True

    

def print_dialog(game_state, room_dialog):

    responses = ["a"]
    
    while len(responses)!=0:
        dialog=None
        
        ## check to see if the player has any flags which allow different dialog options
        for i in range(len(room_dialog)): ## for each dialog tree the character has in this room
            dialog_tree = room_dialog[i]
            if( meets_requirements(game_state["p_flags"], dialog_tree["Requirements"]) and dialog_tree["Responded"]==0): ## if the player meets all of the requirements for this dialog tree         
                dialog = dialog_tree
                room_dialog[i]["Responded"]+=1
                break
                
        if(dialog==None):
            return game_state
                
        responses = dialog["Response options"]
    
        
    
        print(dialog["Dialog"])
        
        if(len(responses)==0):
            return game_state
        
        for i in range(len(responses)):
            print(str(i)+". "+ responses[i][0])
        
        player_choice = int(input())

        
        game_state["p_flags"] += responses[player_choice][1]
    return game_state

    


def talk_to(game_state, command): 
    character = " ".join(command.split()[1:]) ## get the name of the character the player wants to talk to.
    if(character in game_state["rooms"][game_state["p_loc"]]["Characters"]): ## if the character is in the room

        room_dialog = game_state["dialog"][character][game_state["p_loc"]] ## all the dialog options for the character in this room.
        return print_dialog(game_state, room_dialog)
        
                

            
            
            