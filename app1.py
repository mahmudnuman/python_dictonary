import json
from difflib import get_close_matches

data=json.load(open("data.json"))

def translate(wrd):

    wrd=wrd.lower()

    if wrd in data:

        return data[wrd]

    elif wrd.title() in data:

        return data[wrd.title()]

    elif wrd.upper() in data:

        return data[wrd.upper()]

    elif len(get_close_matches(wrd,data.keys())) > 0: 

        yn = input( "Did You Mean %s Instead ? Enter y if Yes, or n if No:" % get_close_matches(wrd,data.keys())[0])
       
        if yn == "y":

                     return data[get_close_matches(wrd,data.keys())[0]]
        else:

            return "The Word Does Not Exist"

            

    else:

        return "The Word Does Not Exist"

word=input("Enter A Word:")

output=(translate(word))

if type(output) == list:

     for item in output:
            
        print(item)
else:

    print(output)
    