import json
from collections import Counter

# Cargar el JSON
with open("models.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Contar cuántas veces aparece cada name
name_counts = Counter(item["name"] for item in data)

# Mostrar solo los que están duplicados
duplicates = {name: count for name, count in name_counts.items() if count > 1}

print("🚨 Modelos duplicados por name:")
for name, count in duplicates.items():
    print(f"- {name} (aparece {count} veces)")
