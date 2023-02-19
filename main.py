import os
import shutil


def get_data_from_source(path):
    lines = []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    first_name = lines[3].split('first-name:')[1].split('\n')[0].strip()
    last_name = lines[4].split('last-name:')[1].split('\n')[0].strip()
    email = lines[5].split('email:')[1].split('\n')[0].strip().replace('"', '')
    phone = lines[6].split('phone:')[1].split('\n')[0].strip().replace('"', '')

    work = lines[8].split('work:')[1].split('\n')[0].strip().replace('"', '')
    home = "[[" + lines[9].split('home:')[1].split('\n')[0].strip().replace('"', '').title() + "]]"

    summary = lines[11].split('summary:')[1].split('\n')[0].strip().replace('"', '')

    birthday = lines[13].split("📅")[1].split('\n')[0].strip() if "📅" in lines[13] else ""
    return {"first_name": first_name, "last_name": last_name, "email": email, "phone": phone, "work": work,
            "home": home,
            "summary": summary, "birthday": birthday}


template_path = r"F:\SHARED\OBSIDIAN VAULT\001 Templates\004 Workbench\Templates\20 Me\26 Contacts\Contact.md"


def create_contact(data):
    new_contact_path = r"F:\SHARED\OBSIDIAN VAULT\004 Workbench\20 Me\26 Contacts\{}.md".format(
        data['first_name'] + " " + data['last_name'])
    shutil.copyfile(template_path, new_contact_path)

    with open(new_contact_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    lines = [line.replace("{{VALUE:First Name}}", data['first_name']) for line in lines]
    lines = [line.replace("{{VALUE:Last Name}}", data['last_name']) for line in lines]

    lines = [line.replace("Email:: ", "Email:: " + data['email']) for line in lines]
    lines = [line.replace("Phone:: ", "Phone:: " + data['phone']) for line in lines]
    lines = [line.replace("Work:: ", "Work:: " + data['work']) for line in lines]
    lines = [line.replace("Home:: ", "Home:: " + data['home']) for line in lines]
    lines = [line.replace("Summary:: ", "Summary:: " + data['summary']) for line in lines]
    lines[-1] = f"- [ ] Birthday {data['first_name'] + ' ' + data['last_name']} ⏫ 🔁 every year 📅 {data['birthday']}"

    with open(new_contact_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)


if __name__ == '__main__':
    folder_path = r"F:\SHARED\OBSIDIAN VAULT\004 Workbench\20 Me\26 Contacts"
    for file in os.listdir(folder_path):
        if file.endswith(".md"):
            data = get_data_from_source(os.path.join(folder_path, file))
            create_contact(data)
            print(data)
