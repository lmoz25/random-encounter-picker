import pdfplumber, json
encounters = []
with pdfplumber.open('Road_Encounters.pdf') as pdf:
    pages = pdf.pages[1:4]
    for page in pages:
        for line in page.extract_text().split('\n'):
            if line.strip() and line.strip()[0].isdigit():
                parts = line.strip().split(' ', 2)
                if len(parts) == 3:
                    num, title, rest = parts
                    rest_parts = rest.strip().rsplit(' ', 1)
                    if len(rest_parts) == 2 and rest_parts[1].isdigit():
                        title = title + ' ' + rest_parts[0]
                        page_num = rest_parts[1]
                    else:
                        title = title + ' ' + rest.strip()
                        page_num = None
                    encounters.append({'number': int(num), 'title': title.strip(), 'page': int(page_num) if page_num else None})
with open('encounters.json', 'w') as f:
    json.dump(sorted(encounters, key=lambda x: x['number']), f, indent=2)

