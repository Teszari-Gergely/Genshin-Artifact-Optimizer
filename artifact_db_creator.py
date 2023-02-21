import csv

artifact_types = ['Flower', 'Quill', 'Goblet', 'Watch', 'Crown']
bonus_names = {'ATK', 'DEF', 'HP', 'Elemental mastery', 'Energy recharge', 'CRIT rate', 'CRIT DMG'}

artifacts = []

while True:
    new_artifact = {}
    print("Enter artifact details:")
    new_artifact['Type'] = input("Type (Flower, Quill, Goblet, Watch, Crown): ")
    if new_artifact['Type'] not in artifact_types:
        print("Invalid artifact type. Please try again.")
        continue

    new_artifact['Name'] = input("Name: ")
    new_artifact['Memory Group'] = input("Memory Group: ")
    try:
        new_artifact['Quality'] = int(input("Quality (1-5): "))
        if new_artifact['Quality'] not in range(1, 6):
            print("Quality must be between 1 and 5. Please try again.")
            continue
    except ValueError:
        print("Quality must be an integer. Please try again.")
        continue

    try:
        new_artifact['Level'] = int(input("Level (0-16): "))
        if new_artifact['Level'] not in range(0, 17):
            print("Level must be between 0 and 16. Please try again.")
            continue
    except ValueError:
        print("Level must be an integer. Please try again.")
        continue

    new_artifact['Bonuses'] = {}
    for bonus_name in bonus_names:
        bonus_value = input(f"{bonus_name}: ")
        if not bonus_value:
            bonus_value = 0
        else:
            try:
                bonus_value = int(bonus_value)
            except ValueError:
                try:
                    bonus_value = float(bonus_value.strip("%")) / 100
                except ValueError:
                    print("Bonus value must be a number or a percentage. Please try again.")
                    break

        new_artifact['Bonuses'][bonus_name] = bonus_value

    if not any(isinstance(value, (int, float)) for value in new_artifact['Bonuses'].values()):
        print("At least one bonus must have a definite number or a percentage value. Please try again.")
        continue

    if all(value == 0 for value in new_artifact['Bonuses'].values()):
        print("At least one bonus must be present. Please try again.")
        continue

    artifacts.append(new_artifact)

    end_input = input("Type 'end' to finish, or press enter to add another artifact: ")
    if end_input == 'end':
        break

if not artifacts:
    print("No artifacts added.")
else:
    with open('artifacts.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Type', 'Name', 'Memory Group', 'Quality', 'Level'] + list(bonus_names))
        for artifact in artifacts:
            bonuses = [artifact['Bonuses'].get(bonus_name, 0) for bonus_name in bonus_names]
            writer.writerow([artifact['Type'], artifact['Name'], artifact['Memory Group'], artifact['Quality'],
                             artifact['Level']] + bonuses)
        print("Artifacts saved to artifacts.csv.")
