import json
import xmltodict
import codecs

sourcefile = "publications1_15000.xml"
jsonfile = "publications1_15000.json"
cleanedfile = "publications1_15000Clean.json"

with open(sourcefile, 'r', encoding="utf8") as f:
    xmlString = f.read()
print("read file")

jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)
print("dumped in string")

with open(jsonfile, 'w') as f:
    f.write(jsonString)
print("written in file")

with open(jsonfile,'r', encoding="utf8") as json_data:
    with open(cleanedfile,'w', encoding="utf8") as json_clean:
        print("start data load")
        data = json.load(json_data)
        print("data loaded...")
        selectedData = {"GetPublicationResponse": {"result": {"content":[]}}}
        for i in range(len(data["GetPublicationResponse"]["result"]["content"])):
            temp = {}
            temp["created"] = data["GetPublicationResponse"]["result"]["content"][i]["created"]
            temp["modified"] = data["GetPublicationResponse"]["result"]["content"][i]["modified"]
            temp["type"] = data["GetPublicationResponse"]["result"]["content"][i]["type"]
            temp["title"] = data["GetPublicationResponse"]["result"]["content"][i]["title"]
            temp["portalUrl"] = data["GetPublicationResponse"]["result"]["content"][i]["portalUrl"]
            temp["typeClassification"] = data["GetPublicationResponse"]["result"]["content"][i]["typeClassification"]
            temp["publicationCategory"] = data["GetPublicationResponse"]["result"]["content"][i]["publicationCategory"]
            temp["persons"] = data["GetPublicationResponse"]["result"]["content"][i]["persons"]
            temp["organisations"] = data["GetPublicationResponse"]["result"]["content"][i]["organisations"]
            temp["publicationStatuses"] = data["GetPublicationResponse"]["result"]["content"][i]["publicationStatuses"]
            try:
                temp["citations"] = data["GetPublicationResponse"]["result"]["content"][i]["citations"]
            except KeyError:
                continue
            try:
                del temp["publicationStatuses"]["publicationStatus"]["publicationStatus"]
                del temp["organisations"]["association"]["external"]
                del temp["organisations"]["association"]["organisation"]["@uuid"]
                del temp["organisations"]["association"]["organisation"]["@rendering"]
                del temp["organisations"]["association"]["organisation"]["family"]
                del temp["organisations"]["association"]["organisation"]["typeClassification"]
            except TypeError:
                continue
            selectedData["GetPublicationResponse"]["result"]["content"].append(temp)
        json_clean.write(json.dumps(selectedData,indent=4,ensure_ascii=False))
        print('done')

