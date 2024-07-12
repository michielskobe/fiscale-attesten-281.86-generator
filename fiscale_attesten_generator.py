import json
import os
import io
import datetime
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import locale

# Hardcoded gegevens

ONDERTEKENAAR_LOCATIE = 'ONDERTEKENAAR_LOCATIE'
ONDERTEKENAAR_NAAM = 'ONDERTEKENAAR_NAAM'
ONDERTEKENAAR_FUNCTIE = 'ONDERTEKENAAR_FUNCTIE'
TAKKEN_DATA = "takdata.json"
BLANCO_FISCAAL_ATTEST = "113-281-86-nl-2022.pdf"
FORMULIER_ANTWOORDEN = "Fiscaal attest (Antwoorden) - Formulierreacties 1.csv"
OUTPUT_MAP = 'out'

# Functie definities

def laad_data_takken(bestandsnaam):
    """ 
    Haalt takspecifieke kampinformatie uit een opgegeven JSON bestand.
    Pameters:
        bestandsnaam [str]: naam van het JSON bestand waar specifieke kampinformatie per tak in verzameld staat.
    Returnt een dictionary met de takspecifieke kampinformatie.
    """
    with open(bestandsnaam, 'r', encoding='utf-8') as bestand:
        return json.load(bestand)

def maak_output_mappen(takken_data, output_map):
    """
    Maakt output mappen voor de verschillende takken.
    Parameters:
        takken_data [dict]: een dictionary met de takspecifieke kampinformatie
        output_map [str]: naam van de map waar alle fiscale attesten per tak in geplaatst zulllen worden
    """
    os.makedirs(output_map, exist_ok=True)
    for tak in takken_data:
        os.makedirs(os.path.join(output_map, tak), exist_ok=True)

def laad_deelnemer_gegevens(bestandsnaam):
    """ 
    Haalt Google Formulier antwoorden uit een opgegeven CSV bestand.
    Pameters:
        bestandsnaam [str]: naam van het CSV bestand waar de antwoorden van het Google Formulier in verzameld staan.
    Returnt een DataFrame [pandas.core.frame.DataFrame] met de deelnemersinformatie.
    """
    return pd.read_csv(bestandsnaam, delimiter=',', encoding='utf-8')

def verwerk_datum(datum_string):
    """
    Zet een data in formaat DD/MM/JJJJ om naar integers.
    Parameters:
        datum_string [str]: de datum in formaat DD/MM/JJJJ
    Returnt een tuple met dag, maand en jaartal als integer.
    """
    day, month, year = datum_string.split('/')
    return int(day), int(month), int(year)

def genereer_pdf(deelnemer, volgnummer, tak_info, tak, kind_info, schuldenaar_info, output_locatie):
    """
    Vult het fiscale attest op basis van de meegevenen informatie en slaat dit op als pdf.
    Parameters:
        deelnemer [pandas.core.series.Series]: een één-dimentionale rij met de informatie van een deelnemer
        volgnummer [int]: een automatisch gegenereerd volgnummer dat aan het attest wordt toegekend
        tak_info [dict]: een dictionary met de takspecifieke kampinformatie
        tak [str]: de naam van de tak van de deelnemer
        kind_info [dict]: een dictionary met de informatie van het kind
        schuldenaar_info [dict]: een dictionary met de informatie van de schuldenaar
        output_locatie [str]: naam van de map waar het fiscale attesten in geplaatst zal worden

    """

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFillColorRGB(0, 0, 0)

    can.drawString(80 * mm, 268 * mm, str(volgnummer + 1))
    can.drawString(45 * mm, 252 * mm, schuldenaar_info['achternaam'])
    can.drawString(53 * mm, 246 * mm, schuldenaar_info['voornaam'])
    can.drawString(55 * mm, 232.5 * mm, str(schuldenaar_info['rijksregisternummer']).zfill(11))
    can.drawString(45 * mm, 224 * mm, schuldenaar_info['adres_straat'])
    can.drawString(177 * mm, 224 * mm, str(schuldenaar_info['adres_huisnummer']))
    can.drawString(51 * mm, 217.5 * mm, str(schuldenaar_info['adres_postcode']))
    can.drawString(101.5 * mm, 217.5 * mm, schuldenaar_info['adres_gemeente'])
    can.drawString(45 * mm, 202 * mm, kind_info['achternaam'])
    can.drawString(52 * mm, 195 * mm, kind_info['voornaam'])
    can.drawString(55 * mm, 181.5 * mm, str(kind_info['rijksregisternummer']).zfill(11))
    can.drawString(61 * mm, 173 * mm, str(kind_info['geboorte_dag']).zfill(2))
    can.drawString(68.5 * mm, 173 * mm, str(kind_info['geboorte_maand']).zfill(2))
    can.drawString(76 * mm, 173 * mm, str(kind_info['geboorte_jaar']))
    can.drawString(45 * mm, 166.5 * mm, kind_info['adres_straat'])
    can.drawString(177 * mm, 166.5 * mm, str(kind_info['adres_huisnummer']))
    can.drawString(51 * mm, 160 * mm, str(kind_info['adres_postcode']))
    can.drawString(101.5 * mm, 160 * mm, kind_info['adres_gemeente'])
    can.drawString(62 * mm, 131.5 * mm, str(kind_info['periode_start_dag']).zfill(2))
    can.drawString(69.5 * mm, 131.5 * mm, str(kind_info['periode_start_maand']).zfill(2))
    can.drawString(77 * mm, 131.5 * mm, str(kind_info['periode_start_jaar']))
    can.drawString(62 * mm, 126.5 * mm, str(kind_info['periode_einde_dag']).zfill(2))
    can.drawString(69.5 * mm, 126.5 * mm, str(kind_info['periode_einde_maand']).zfill(2))
    can.drawString(77 * mm, 126.5 * mm, str(kind_info['periode_einde_jaar']))
    can.drawString(107 * mm, 128 * mm, str(kind_info['dag_aantal']))
    can.drawString(125 * mm, 128 * mm, f"€ {float(kind_info['prijs_per_dag']):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    can.drawString(155 * mm, 128 * mm, f"€ {float(kind_info['prijs_totaal']):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    can.drawString(155 * mm, 85 * mm, f"€ {float(kind_info['prijs_totaal']):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    can.drawString(81 * mm, 65 * mm, ONDERTEKENAAR_LOCATIE)
    can.drawString(157 * mm, 65 * mm, datetime.datetime.now().strftime("%d"))
    can.drawString(165 * mm, 65 * mm, datetime.datetime.now().strftime("%m"))
    can.drawString(178 * mm, 65 * mm, datetime.datetime.now().strftime("%y"))
    can.drawString(116 * mm, 35 * mm, ONDERTEKENAAR_NAAM)
    can.drawString(130 * mm, 29 * mm, ONDERTEKENAAR_FUNCTIE)
    can.save()

    packet.seek(0)
    ingevuld_fiscaal_attest = PdfReader(packet)
    pdf = PdfReader(BLANCO_FISCAAL_ATTEST)
    p1, p2, p3 = pdf.pages[0], pdf.pages[1], pdf.pages[2]
    p2.merge_page(ingevuld_fiscaal_attest.pages[0])

    pdf_writer = PdfWriter()
    pdf_writer.add_page(p1)
    pdf_writer.add_page(p2)
    pdf_writer.add_page(p3)

    with open(output_locatie, 'wb') as output_bestand:
        pdf_writer.write(output_bestand)

def verwerk_deelnemers(deelnemer_gegevens, takken_data, output_map):
    """
    Genereert de attesten op basis van de deelnemers - en takinformatie en slaat deze op als pdf.
    Parameters:
        deelnemers_gegevens [pandas.core.frame.DataFrame]: een DataFrame met de deelnemersinformatie
        takken_data [dict]: een dictionary met de takspecifieke kampinformatie
        output_map [str]: naam van de map waar alle fiscale attesten per tak in geplaatst zulllen worden
    """
    tak_map = {
        'Kapoenen': 'kapoenen',
        'Kawellen': 'kawellen',
        "Jogi's": 'jogis'
    }
    for volgnummer, deelnemer in deelnemer_gegevens.iterrows():
        kind_info = {
            'achternaam': deelnemer['Achternaam van het kind?'].capitalize(),
            'voornaam': deelnemer['Voornaam van het kind?'].capitalize(),
            'rijksregisternummer': deelnemer['Rijksregisternummer van het kind?'],
            'geboorte_datum': deelnemer['Geboortedatum van het kind?'].split('/'),
            'adres_straat': deelnemer['Straat van het kind?'].capitalize(),
            'adres_huisnummer': deelnemer['Huisnummer van het kind?'],
            'adres_postcode': deelnemer['Postcode van het kind?'],
            'adres_gemeente': deelnemer['Gemeente/stad van het kind?']
        }
        kind_info['geboorte_dag'], kind_info['geboorte_maand'], kind_info['geboorte_jaar'] = verwerk_datum(deelnemer['Geboortedatum van het kind?'])
        
        if deelnemer['Is het adres van het kind hetzelfde als dat van de schuldenaar?'] == "Ja":
            schuldenaar_info = {
                'achternaam': deelnemer['Achternaam van de schuldenaar?'].capitalize(),
                'voornaam': deelnemer['Voornaam van de schuldenaar?'].capitalize(),
                'rijksregisternummer': deelnemer['Rijksregisternummer van de schuldenaar?'],
                'adres_straat': kind_info['adres_straat'],
                'adres_huisnummer': kind_info['adres_huisnummer'],
                'adres_postcode': kind_info['adres_postcode'],
                'adres_gemeente': kind_info['adres_gemeente']
            }
        else:
            schuldenaar_info = {
                'achternaam': deelnemer['Achternaam van de schuldenaar?.1'].capitalize(),
                'voornaam': deelnemer['Voornaam van de schuldenaar?.1'].capitalize(),
                'rijksregisternummer': deelnemer['Rijksregisternummer van de schuldenaar?.1'],
                'adres_straat': deelnemer['Straat van de schuldenaar?'].capitalize(),
                'adres_huisnummer': deelnemer['Huisnummer van de schuldenaar?'],
                'adres_postcode': deelnemer['Postcode van de schuldenaar?'],
                'adres_gemeente': deelnemer['Gemeente/stad van de schuldenaar?'].capitalize()
            }

        tak = tak_map.get(deelnemer['Tak van het kind tijdens de kampperiode waarvoor dit attest opgesteld wordt?'])
        if not tak:
            continue

        tak_info = takken_data[tak]
        kind_info.update({
            'periode_start_dag': verwerk_datum(tak_info['startdag'])[0],
            'periode_start_maand': verwerk_datum(tak_info['startdag'])[1],
            'periode_start_jaar': verwerk_datum(tak_info['startdag'])[2],
            'periode_einde_dag': verwerk_datum(tak_info['einddag'])[0],
            'periode_einde_maand': verwerk_datum(tak_info['einddag'])[1],
            'periode_einde_jaar': verwerk_datum(tak_info['einddag'])[2]
        })

        periode_start_datum = datetime.datetime(kind_info['periode_start_jaar'], kind_info['periode_start_maand'], kind_info['periode_start_dag'])
        periode_einde_datum = datetime.datetime(kind_info['periode_einde_jaar'], kind_info['periode_einde_maand'], kind_info['periode_einde_dag'])
        leeftijdsgrens_datum = datetime.datetime(kind_info['geboorte_jaar'] + 14, kind_info['geboorte_maand'], kind_info['geboorte_dag'])

        if (leeftijdsgrens_datum > periode_einde_datum):
            kind_info['dag_aantal'] = tak_info['aantal_dagen']
            if deelnemer['Heeft u afgelopen kampperiode gebruik gemaakt van de mogelijkheid tot verminderd lidgeld?'] == "Ja":
                kind_info['prijs_per_dag'] = float(tak_info['dagtarief'])/2
                kind_info['prijs_totaal'] = int(tak_info['tot_bedrag'])/2
            else:
                kind_info['prijs_per_dag'] = tak_info['dagtarief']
                kind_info['prijs_totaal'] = tak_info['tot_bedrag']
        elif (leeftijdsgrens_datum > periode_start_datum):
            kind_info['dag_aantal'] =(leeftijdsgrens_datum - periode_start_datum).days
            if deelnemer['Heeft u afgelopen kampperiode gebruik gemaakt van de mogelijkheid tot verminderd lidgeld?'] == "Ja":
                kind_info['prijs_per_dag'] = float(tak_info['dagtarief'])/2
            else:
                kind_info['prijs_per_dag'] = float(tak_info['dagtarief'])
            kind_info['prijs_totaal'] = kind_info['prijs_per_dag'] * kind_info['dag_aantal']
        else:
            continue

        output_locatie = os.path.join(output_map, tak, f"{volgnummer + 1}_{kind_info['voornaam']}_{kind_info['achternaam']}.pdf")
        genereer_pdf(deelnemer, volgnummer, tak_info, tak, kind_info, schuldenaar_info, output_locatie)

def genereer_fiscale_attesten(bestandsnaam_json, bestandsnaam_csv, output_locatie):
    takken_data = laad_data_takken(bestandsnaam_json)
    maak_output_mappen(takken_data, output_locatie)
    deelnemer_gegevens = laad_deelnemer_gegevens(bestandsnaam_csv)
    verwerk_deelnemers(deelnemer_gegevens, takken_data, output_locatie)


# Main 

if __name__ == "__main__":
    try:         
        genereer_fiscale_attesten(TAKKEN_DATA, FORMULIER_ANTWOORDEN, OUTPUT_MAP)
    except:         
        print("Er is iets misgegaan bij het genereren van de fiscale attesten. Controleer of de juiste bestanden zijn meegegeven en probeer opnieuw.")     
    else:         
        print("De fiscale attesten zijn succesvol gegenereerd. Je kan ze terugvinden in", os.getcwd() + "/" + OUTPUT_MAP)
