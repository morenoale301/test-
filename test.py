import json

from bs4 import BeautifulSoup

def find_elements(bs_content, structure):
    
    circuit = bs_content.find(structure)
    elements = [tag.name for tag in circuit.find_all() if "list" in tag.name]
    total_components = {}
    for element in elements:
        components = circuit.find(element)
        components = circuit.find_all(element.replace("_list",""))
        total_components[element.replace("_list","")] = {}
        if components is not None:
            for component in components:
                tags = [(tag.name,tag.text) for tag in component.find_all()]
                for i in range(len(tags)):
                    tag_name = tags[i][0]
                    tag_value = tags[i][1]
                    if i == 0:
                        total_components[element.replace("_list","")][tag_value] = {}
                    else:
                        total_components[element.replace("_list","")][tags[0][1]][tag_name] = tag_value

    with open(structure + ".json", "w") as file:
        json.dump(total_components, file, indent=2) 

def main(archieve):
    
    with open(archieve, "r") as file:
        content = file.readlines()
        content = "".join(content)

        bs_content = BeautifulSoup(content,"lxml")

    find_elements(bs_content,"powerflow")
    find_elements(bs_content,"assert")
    find_elements(bs_content,"tape")

archieve = "ejemplo.xml"
main(archieve)