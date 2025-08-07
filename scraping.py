import re
import json
import requests
import urllib3
from bs4 import BeautifulSoup
from datetime import datetime

from metode import *


# Umesto BeautifulSoup, može se koristiti pandas sa pandas.read_html(url)

def scrape():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Sa urllib prešao na requests jer može da radi bez verifikacije SSL sertifikata

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
        req = requests.get(url, headers=headers, verify=False)
        req.encoding = 'utf-8'
        soup = BeautifulSoup(req.text, 'html.parser')

        raw_data = soup.find_all('tr')
        datum = re.search(r'за датум:\s*((?:\d{2}\.\d{2}\.\d{4}\.)|(?:\d{4}-\d{2}-\d{2}))', str(raw_data), re.IGNORECASE).group(1)
        if re.search(r'\b\d{4}-\d{2}-\d{2}\b', str(datum)):
            datum = datetime.strptime(datum, '%Y-%m-%d').date()
        else:
            datum = datetime.strptime(datum, '%d.%m.%Y.').date()
        datum = formatiraj_datum(datum)
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

if __name__ == "__main__":
    scrape()