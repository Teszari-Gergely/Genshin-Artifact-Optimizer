import csv
from typing import List, Tuple, Dict

BONUSES = {'ATK', 'DEF', 'HP', 'Elemental mastery', 'Energy recharge', 'CRIT rate', 'CRIT DMG'}

class Artifact:
    def __init__(self, artifact_type: str, name: str, group: str, quality: int, level: int, bonuses: Dict[str, float]):
        self.type = artifact_type
        self.name = name
        self.group = group
        self.quality = quality
        self.level = level
        self.bonuses = bonuses
    
    def __str__(self):
        return f"\nType: {self.type}, Name: {self.name}, Level: {self.level}, Bonuses: {self.bonuses}\n"
    
    def has_bonus(self, bonus_name: str) -> bool:
        return bonus_name in self.bonuses
    
    def get_bonus_value(self, bonus_name: str) -> float:
        return self.bonuses.get(bonus_name, 0.0)

def read_artifacts_from_csv(filename: str) -> List[Artifact]:
    artifacts = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            artifact_type = row['Type']
            name = row['Name']
            group = row['Group']
            quality = int(row['Quality'])
            level = int(row['Level'])
            bonuses = {}
            for bonus_name in BONUSES:
                bonus_value = row.get(bonus_name, '0')
                if bonus_value.endswith('%'):
                    bonus_value = float(bonus_value[:-1]) / 100.0
                else:
                    bonus_value = float(bonus_value)
                bonuses[bonus_name] = bonus_value
            artifacts.append(Artifact(artifact_type, name, group, quality, level, bonuses))
    return artifacts

def select_best_artifacts(artifacts: List[Artifact]) -> List[Artifact]:
    artifact_sets = []
    for flower in filter(lambda x: x.type == 'Flower', artifacts):
        for quill in filter(lambda x: x.type == 'Quill', artifacts):
            for goblet in filter(lambda x: x.type == 'Goblet', artifacts):
                for watch in filter(lambda x: x.type == 'Watch', artifacts):
                    for crown in filter(lambda x: x.type == 'Crown', artifacts):
                        if len({flower, quill, goblet, watch, crown}) == 5:
                            if flower.has_bonus('HP') and quill.has_bonus('ATK') and goblet.has_bonus('DEF'):
                                group_counts = {}
                                for artifact in {flower, quill, goblet, watch, crown}:
                                    if artifact.group in group_counts:
                                        group_counts[artifact.group] += 1
                                    else:
                                        group_counts[artifact.group] = 1
                                max_group_count = max(group_counts.values())
                                if max_group_count >= 2:
                                    artifact_sets.append({flower, quill, goblet, watch, crown})
    if not artifact_sets:
        return []
    else:
        return sorted(artifact_sets, key=lambda x: sum([artifact.quality for artifact in x]), reverse=True)[0]

# Test the code
artifacts = read_artifacts_from_csv('artifacts.csv')
best_artifacts = select_best_artifacts(artifacts)
if best_artifacts:
    for artifact in best_artifacts:
        print(artifact)
