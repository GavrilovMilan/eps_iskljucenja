import re
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


urls = ['https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_0_Iskljucenja.htm'#,
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_1_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_2_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_3_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-beograd/Dan_0_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-beograd/Dan_1_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-beograd/Dan_2_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-beograd/Dan_3_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kraljevo_Dan_0_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kraljevo_Dan_1_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kraljevo_Dan_2_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kraljevo_Dan_3_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kragujevac_Dan_0_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kragujevac_Dan_1_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kragujevac_Dan_2_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Kragujevac_Dan_3_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Nis_Dan_0_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Nis_Dan_1_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Nis_Dan_2_Iskljucenja.htm',
        # 'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Nis_Dan_3_Iskljucenja.htm'
        ]

headers = {'User-Agent': 'Mozilla/5.0'}

for url in urls:
    req = Request(url, headers=headers)
    page = urlopen(req)
    html = page.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())

    # print(soup.get_text())
    # print(soup.find_all('tr'))

    raw_data = soup.find_all('tr')
    datum = re.search(r'за датум:\s*(\d{2}\.\d{2}\.\d{4}\.)', str(raw_data), re.IGNORECASE).group(1)
    # datum = datum.group(1)
    print(f'Datum: {datum}')
    iskljucenja = []
    for row in raw_data[2:]: # preskačemo naslove kolona
        cols = row.find_all('td')
        ogranak = cols[0].get_text(strip=True)
        opstina = cols[1].get_text(strip=True)
        vreme_od = cols[2].get_text(strip=True).split(' - ')[0]
        vreme_do = cols[2].get_text(strip=True).split(' - ')[1]
        ulice = cols[3].get_text(strip=True)
        iskljucenje = {
            'ogranak': ogranak,
            'opstina': opstina,
            'vreme_od': vreme_od,
            'vreme_do': vreme_do,
            'ulice': ulice
        }
        iskljucenja.append(iskljucenje)

    # for i in iskljucenja:
    #     print(f'{i['opstina']}: {i['vreme_od']} - {i['vreme_do']} | {i['ulice']}')

    with open('iskljucenja/iskljucenja.json', 'w', encoding='utf-8') as f:
        json.dump(iskljucenja, f, ensure_ascii=False, indent=2)

