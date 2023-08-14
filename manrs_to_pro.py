import json
from types import SimpleNamespace

participants = []

more_than_one_as = 0
total_ases = 0
with open("manrs.json") as manrs_file:
    manrs_content = manrs_file.read()
    manrs_object = json.loads(manrs_content, object_hook=lambda manrs_content: SimpleNamespace(**manrs_content))
    
    for participant in manrs_object.participants:
       
        total_ases += len(participant.ASNs)
        participants.append(participant)
        if len(participant.ASNs) > 1:
            more_than_one_as+= 1


print(len(participants))
print(more_than_one_as, "ISPs with >1 as")
print(total_ases, "ases in total")