import os
import re
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

if not os.path.isdir('iskljucenja'):
    os.mkdir('iskljucenja')

urls = ['https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_0_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_1_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_2_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_3_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-beograd/Dan_0_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-beograd/Dan_1_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-beograd/Dan_2_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-beograd/Dan_3_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kraljevo_Dan_0_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kraljevo_Dan_1_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kraljevo_Dan_2_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kraljevo_Dan_3_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kragujevac_Dan_0_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kragujevac_Dan_1_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kragujevac_Dan_2_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kragujevac_Dan_3_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Nis_Dan_0_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Nis_Dan_1_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Nis_Dan_2_Iskljucenja.htm',
        'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Nis_Dan_3_Iskljucenja.htm'
        ]

headers = {'User-Agent': 'Mozilla/5.0'}

iskljucenja = []
for url in urls:
    req = Request(url, headers=headers)
    page = urlopen(req)
    html = page.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    raw_data = soup.find_all('tr')
    datum = re.search(r'за датум:\s*((?:\d{2}\.\d{2}\.\d{4}\.)|(?:\d{4}-\d{2}-\d{2}))', str(raw_data), re.IGNORECASE).group(1)
    # Uraditi standardno formatiranje datuma na dd.MM.yyyy. pošto EPS koristi to za sve osim za Beograd, gde koristi yyyy-MM-dd
    print(f'Datum: {datum}')
    for row in raw_data[2:]: # preskačemo naslove kolona
        cols = row.find_all('td')
        # Quick Fix, u tabeli za Beograd ne postoji Ogranak
        # Napraviti bolje rešenje
        bg = 0
        if 'beograd' in url:
            bg = -1
            ogranak = ''
        else:
            ogranak = cols[bg].get_text(strip=True)
        opstina = cols[bg+1].get_text(strip=True)
        vreme_od = cols[bg+2].get_text(strip=True).split(' - ')[0]
        vreme_do = cols[bg+2].get_text(strip=True).split(' - ')[1]
        ulice = cols[bg+3].get_text(strip=True)

        iskljucenje = {
            'datum': datum,
            'ogranak': ogranak,
            'opstina': opstina,
            'vreme_od': vreme_od,
            'vreme_do': vreme_do,
            'ulice': ulice
        }
        iskljucenja.append(iskljucenje)

    # for i in iskljucenja:
    #     print(f'{i['opstina']}: {i['vreme_od']} - {i['vreme_do']} | {i['ulice']}')

with open('iskljucenja.json', 'w', encoding='utf-8') as f:
    json.dump(iskljucenja, f, ensure_ascii=False, indent=2)

