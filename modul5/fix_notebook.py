import json

# Wczytaj notebook
with open('2.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Napraw strukturę wiadomości w komórce 5
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if "'type': \"text\"" in source:
            # Napraw problematyczną linię
            fixed_source = []
            for line in cell['source']:
                if "'type': \"text\"" in line:
                    line = line.replace("'type': \"text\"", '"type": "text"')
                fixed_source.append(line)
            cell['source'] = fixed_source

# Zapisz naprawiony notebook
with open('2.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("Notebook został naprawiony!") 