import json, re
from difflib import get_close_matches
lines = open('src/all_encounters.txt').read().split('\n')
encounter_titles = [e['title'] for e in json.load(open('src/encounters.json'))]
def norm(s): return re.sub(r'[^a-z0-9]+', '', s.lower())
norm_titles = [norm(t) for t in encounter_titles]
title_to_norm = {norm(t): t for t in encounter_titles}
title_locs = []
for i, line in enumerate(lines):
    n = norm(line.strip())
    if n in title_to_norm:
        title_locs.append((i, n))
found_titles = set(ntitle for _, ntitle in title_locs)
missing_titles = [t for t in norm_titles if t not in found_titles]
print(f'Missing: {len(missing_titles)}')
for mt in missing_titles:
    close = get_close_matches(mt, [norm(line.strip()) for line in lines], n=3, cutoff=0.5)
    print(f'Wanted: {title_to_norm[mt]} | Close: {[lines[[norm(line.strip()) for line in lines].index(c)] for c in close]}')

