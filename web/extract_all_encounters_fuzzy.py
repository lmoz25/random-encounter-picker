import json, re
from difflib import get_close_matches
lines = open('src/all_encounters.txt').read().split('\n')
encounter_titles = [e['title'] for e in json.load(open('src/encounters.json'))]
def norm(s): return re.sub(r'[^a-z0-9]+', '', s.lower())
norm_titles = [norm(t) for t in encounter_titles]
title_to_norm = {norm(t): t for t in encounter_titles}
# Find all lines that match a normalized title
title_locs = []
for i, line in enumerate(lines):
    n = norm(line.strip())
    if n in title_to_norm:
        title_locs.append((i, n))
found_titles = set(ntitle for _, ntitle in title_locs)
missing_titles = [t for t in norm_titles if t not in found_titles]
# Try fuzzy matching for missing titles
for mt in missing_titles:
    close = get_close_matches(mt, [norm(line.strip()) for line in lines], n=1, cutoff=0.7)
    if close:
        idx = [norm(line.strip()) for line in lines].index(close[0])
        title_locs.append((idx, mt))
title_locs = sorted(title_locs, key=lambda x: x[0])
encounter_bodies = {}
for idx, (start, ntitle) in enumerate(title_locs):
    end = title_locs[idx+1][0] if idx+1 < len(title_locs) else len(lines)
    title = title_to_norm[ntitle]
    body = '\n'.join(lines[start+1:end]).strip()
    encounter_bodies[title] = body
json.dump(encounter_bodies, open('src/encounter_texts.json', 'w'), indent=2)

