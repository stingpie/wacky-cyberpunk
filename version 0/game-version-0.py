

import helper_functions as hf  

## a list of all the actions a player can take.
actions ={
            "look" : hf.examine,
            "pick up" : hf.take_item,
            "go" : hf.move_player,
            "use" : hf.use_item,
            "talk" : hf.talk_to,
            "speak" :hf.talk_to
            }


import json

characters = json.loads(open('characters.json','r').read())
items = json.loads(open('items.json','r').read())
dialog = json.loads(open('dialog.json','r').read())
rooms = json.loads(open('rooms.json','r').read())

player_location = "patio"
player_inventory=[] ## This should hold all the items the player has grabbed.
player_flags=["None"] ## This keeps track of dialog and the state of quests. 



while True:
    player_command = input()
    game_state = {
                    "characters":characters, 
                    "items":items,
                    "dialog":dialog,
                    "rooms":rooms,
                    "p_loc": player_location,
                    "p_inv": player_inventory,
                    "p_flags": player_flags
                }
                
  
    for action in actions:  ## scan through all possible actions
        if(player_command.startswith(action)):  ## if the player has entered a command that is a valid action,
            game_state = actions[action](game_state, player_command) ## execute that action, and update the game state.
    
    characters = game_state["characters"] 
    items = game_state["items"]
    dialog = game_state["dialog"]
    rooms = game_state["rooms"]
    player_location = game_state["p_loc"]
    player_inventory = game_state["p_inv"]
    player_flags= game_state["p_flags"]
    
    
    
    
