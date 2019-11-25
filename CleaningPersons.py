import json
import xmltodict

with open("Persons.xml_cleaned.xml", 'r') as f:
    xmlString = f.read()

jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)

with open("Persons.json", 'w') as f:
    f.write(jsonString)

with open('Persons.json','r') as json_data:
    with open('PersonsClean.json','w') as json_clean:
        data = json.load(json_data)
        for i in range(len(data["GetPersonResponse"]["result"]["content"])):
            del data["GetPersonResponse"]["result"]["content"][i]["external"]
            del data["GetPersonResponse"]["result"]["content"][i]["limitedVisibility"]
            del data["GetPersonResponse"]["result"]["content"][i]["@type"]
            del data["GetPersonResponse"]["result"]["content"][i]["created"]
            del data["GetPersonResponse"]["result"]["content"][i]["modified"]
            del data["GetPersonResponse"]["result"]["content"][i]["portalUrl"]
            del data["GetPersonResponse"]["result"]["content"][i]["family"]
            del data["GetPersonResponse"]["result"]["content"][i]["type"]
            try:
                del data["GetPersonResponse"]["result"]["content"][i]["gender"]
            except KeyError:
                continue
            try:
                del data["GetPersonResponse"]["result"]["content"][i]["dateOfBirth"]
            except KeyError:
                continue
            try:
                for j in range(len(data["GetPersonResponse"]["result"]["content"][i]["organisationAssociations"][
                                           "organisationAssociation"]["jobTitle"]["term"]["localizedString"])):
                    if data["GetPersonResponse"]["result"]["content"][i]["organisationAssociations"]["organisationAssociation"]["jobTitle"]["term"]["localizedString"][j]["@locale"]=="nl_NL":
                            del data["GetPersonResponse"]["result"]["content"][i]["organisationAssociations"]["organisationAssociation"]["jobTitle"]["term"]["localizedString"][j]
            except Exception:
                continue
            try:
                del data["GetPersonResponse"]["result"]["content"][i]["nameVariant"]
            except KeyError:
                continue

        json_clean.write(json.dumps(data, indent=4, ensure_ascii=False))
#             del data["GetPersonResponse"]["result"]["content"][i]["organisationAssociations"]["organisationAssociation"]["employmentType"]
#            if data["GetPersonResponse"]["result"]["content"][i]["organisationAssociations"]["organisationAssociation"]["jobTitle"]["term"]["localizedString"][0]["@locale"]







# with open('Persons.json','r') as json_data:
#         data = json.load(json_data)
#         for i in range(len(data["GetPersonResponse"]["result"]["content"])):
#             if data["GetPersonResponse"]["result"]["content"][i]["organisationAssociations"]["organisationAssociation"]["jobTitle"]["term"]["localizedString"]:
#                 for j in range(len(data["GetPersonResponse"]["result"]["content"][i]["organisationAssociations"]["organisationAssociation"]["jobTitle"]["term"]["localizedString"])):
#                 # print (len(data["GetPersonResponse"]["result"]["content"][i]["organisationAssociations"]["organisationAssociation"]["jobTitle"]["term"]["localizedString"]))
#                     if data["GetPersonResponse"]["result"]["content"][i]["organisationAssociations"]["organisationAssociation"]["jobTitle"]["term"]["localizedString"][j]["@locale"]=="nl_NL":
#                            print(i)
#
#             else: continue
# print(len(data["GetPersonResponse"]["result"]["content"]))