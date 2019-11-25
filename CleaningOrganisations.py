import json
import xmltodict

with open("Organisations.xml", 'r') as f:
    xmlString = f.read()

jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)

with open("Organisations.json", 'w') as f:
    f.write(jsonString)


with open('Organisations.json','r') as json_data:
    with open('OrganisationsClean.json','w') as json_clean:
        data = json.load(json_data)
        for i in range(len(data["GetOrganisationResponse"]["result"]["content"])):
            del data["GetOrganisationResponse"]["result"]["content"][i]["external"]
            del data["GetOrganisationResponse"]["result"]["content"][i]["limitedVisibility"]
            del data["GetOrganisationResponse"]["result"]["content"][i]["@type"]
            del data["GetOrganisationResponse"]["result"]["content"][i]["created"]
            del data["GetOrganisationResponse"]["result"]["content"][i]["modified"]
            del data["GetOrganisationResponse"]["result"]["content"][i]["portalUrl"]
            del data["GetOrganisationResponse"]["result"]["content"][i]["family"]
            del data["GetOrganisationResponse"]["result"]["content"][i]["type"]
            del data["GetOrganisationResponse"]["result"]["content"][i]["nameVariant"]
            try:
                for j in range(len(data["GetOrganisationResponse"]["result"]["content"][i]["typeClassification"]["term"]["localizedString"])):
                    if data["GetOrganisationResponse"]["result"]["content"][i]["typeClassification"]["term"]["localizedString"][j]["@locale"] == "nl_NL":
                        del data["GetOrganisationResponse"]["result"]["content"][i]["typeClassification"]["term"]["localizedString"][j]
            except Exception:
                continue
        json_clean.write(json.dumps(data,indent=4,ensure_ascii=False))

