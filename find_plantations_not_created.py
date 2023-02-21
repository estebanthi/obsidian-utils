import os
import re


notes_path = r"F:\SHARED\OBSIDIAN VAULT\10 Wiki\12 Notes"
plantations_path = r"F:\SHARED\OBSIDIAN VAULT\10 Wiki\13 Plantations"

ignore_list = [
    "Anemometric Circuit - 20230126111008",
    "Compilation - 20230213030315"
]


def get_all_plantations_referenced(notes_path):
    plantations = []
    for file in os.listdir(notes_path):
        with open(os.path.join(notes_path, file), 'r', encoding='utf-8') as f:
            content = f.read()
            plantation_line = re.findall(r'Plantations:: (.*)', content)
            if plantation_line:
                plantation_line = plantation_line[0]
                plantations.extend(plantation_line.split(","))
    plantations = [plantation.strip() for plantation in plantations if plantation.strip()]
    plantations = [plantation.split("|")[0].replace("[", "").replace("]", "") for plantation in plantations]
    plantations = list(set(plantations))
    return plantations


def get_all_plantations_created(plantations_path):
    return [file.replace(".md", "") for file in os.listdir(plantations_path)]


if __name__ == "__main__":
    plantations_referenced_in_notes = get_all_plantations_referenced(notes_path)
    plantations_referenced_in_plantations = get_all_plantations_referenced(plantations_path)
    plantations_referenced = list(set(plantations_referenced_in_notes + plantations_referenced_in_plantations))
    plantations_referenced = [plantation for plantation in plantations_referenced if plantation not in ignore_list]

    plantations_created = get_all_plantations_created(plantations_path)
    plantations_not_created = [plantation for plantation in plantations_referenced if plantation not in plantations_created]
    print(len(plantations_not_created))
    for plantation in sorted(plantations_not_created):
        print(plantation)