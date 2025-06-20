import json, re, pyassimp
from pathlib import Path

# Files containing categories
files = {
    'bones': 'Resources/Models/FBX/SkeletalSystem100.fbx',
    'muscles': 'Resources/Models/FBX/MuscularSystem100.fbx',
    'joints': 'Resources/Models/FBX/Joints100.fbx'
}

all_names = set()
for category, path in files.items():
    with pyassimp.load(path) as scene:
        for mesh in scene.meshes:
            all_names.add(mesh.name)

# Load translations English -> French
translations = {}
with open('Resources/Translations0.txt', encoding='utf-8') as f:
    header = f.readline().strip().split(';')
    eng_idx = header.index('English')
    fr_idx = header.index('Français')
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split(';')
        if len(parts) <= max(eng_idx, fr_idx):
            continue
        translations[parts[eng_idx]] = parts[fr_idx]

# Orientation words
orientation_en = {'l': 'Left', 'r': 'Right'}
orientation_fr = {'l': 'gauche', 'r': 'droite'}

result = {}
for name in sorted(all_names):
    base = re.sub(r'\.[0-9]+$', '', name)
    suffix = ''
    side_en = ''
    side_fr = ''
    if base.endswith('.l') or base.endswith('.r'):
        side = base[-1]
        side_en = orientation_en.get(side, '')
        side_fr = orientation_fr.get(side, '')
        base = base[:-2]
    en_base = base
    fr_base = translations.get(base, base)
    english = f"{side_en} {en_base}".strip()
    french = f"{fr_base} {side_fr}".strip()
    result[name] = {'en': english, 'fr': french}

with open('structures_anatomiques.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
