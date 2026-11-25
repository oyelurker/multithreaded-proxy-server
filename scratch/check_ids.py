import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

called_ids = set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", content))
qs_ids = set(re.findall(r"querySelector(?:All)?\(['\"]#([a-zA-Z0-9_\-]+)['\"]\)", content))
all_needed = called_ids | qs_ids

existing_ids = set(re.findall(r"id=['\"]([^'\"]+)['\"]", content))

missing = all_needed - existing_ids
print(f"Total needed IDs: {len(all_needed)}")
print(f"Missing IDs ({len(missing)}):")
for m in sorted(list(missing)):
    print(" -", m)
