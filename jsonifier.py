### JSONIFIER
# this takes in the version number, and some feedback, and eventually uses
# chatgpt to generate the next generation game.



prompt = '''
I'm doing an experiment on whether AIs can create cogent video games. I will give you an initial python file, and it will be your job to add features based on user feedback. You will be sent a json file in the following format:
{
    "files":{
    "put file name here..." : "put the file content here...",
    "put file2 name here..." : "put the file2 content here..."
    }
    "feedback" : "user feedback goes here..."
}
You will respond in the same format.
The only additional library you may use is the openAI api. If you do use this api, place a comment ### PUT API KEY HERE ### where the api key is needed. The game should be a cyberpunk text-based adventure. The files can be txt, py or JSON. Here is the JSON:
'''

import json
version = input("What version to start with?")

mypath="Version " + str(int(version)) 
feedback=input("What feedback would you give?")

#https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]



files={}
i=0
for f in onlyfiles:
    files[f] = open(mypath+"\\"+f,'r').read()





combined = {"files":files, "feedback":feedback}
print(json.dumps(combined))




from openai import OpenAI
client = OpenAI()

initial_prompt = prompt + "\n" + str(json.dumps(combined))

finish_reason="length"

incomplete_response=""

GPT_messages =[{"role": "system", "content": "You are a helpful assistant designed to output JSON."},{"role": "user", "content":initial_prompt}]


while True:
    
    ## NOTE: GPT-3.5 just gives up in the middle of completions for some reason. 
    ## It doesn't even run out of tokens or anything- it just gives up! because
    ## of that, running gpt-3.5 will crash this program, despite openAI swearing
    ## that it will always produce valid json, as long as token count permits.
    response = client.chat.completions.create(
        #model="gpt-3.5-turbo-1106",
        model="gpt-3.5-turbo-0125",  
        #model="gpt-4-turbo-preview", ## Unfortunately, this prompt is too complicated for gpt 3.5
        response_format={ "type": "json_object" },
        messages=GPT_messages,
        max_tokens=None
    )

    finish_reason = response.choices[0].finish_reason
    print("finish reason:", finish_reason)
    incomplete_response += response.choices[0].message.content#.replace("```json","").replace("```","")

    GPT_messages+=[{"role":"assistant","content":response.choices[0].message.content}]#, {"role":"user","content":"continue"}]
    
    ## GPT3.5 is broken, so I have to manually verifiy whether it's valid JSON
    if(finish_reason == "stop"):
        try:
            print(incomplete_response)
            json_response = json.loads(incomplete_response)
            break
        except ValueError:
            finish_reason="length"



json_response = json.loads(incomplete_response)


new_mypath= "Version "+str(int(version)+1)

import os

if not os.path.exists(new_mypath):
    os.makedirs(new_mypath)

for f in json_response["files"]:
    newfile = open(new_mypath + "\\"+f, "w")
    newfile.write(str(json_response["files"][f]))
    newfile.close()




