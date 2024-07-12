# Fiscale attesten generator

## Vereisten

Het gebruik van deze code vereist een beperkte kennis van Python en git. 

### De repository clonen

```bash
$ git clone git@github.com:michielskobe/fiscale-attesten-281.86-generator.git
$ cd fiscale-attesten-281.86-generator
```

### Python packages intalleren

Dit Python-script gebruikt pandas, PyPDF2 en reportlab. Het volgende commando installeert deze met behulp van pip:

```bash
$ pip install -r requirements.txt
```

### Bestanden en gegevens updaten

Dit Python-script maakt gebruik van een aantal bestanden om de fiscale attesten te genereren. De gegevens in deze bestanden moeten up-to-date gebracht worden met de gegevens van het afgelopen kamp. Daarnaast moet ook de informatie van de persoon die het attest zal ondertekenen aangepast worden.

* __TAKKEN\_DATA (takdata.json):__ Dit is een json bestand met volgende info per tak:

|Info          |Uitleg                                      |
|:-------------|:-------------------------------------------|
|`startdag`    |De startdatum van kamp voor deze tak        |
|`einddag`     |De einddatum van kamp voor deze tak         |
|`aantal_dagen`|Aantal dagen dat deze tak mee was op kamp   |
|`dagtarief`   |Dagtarief in €/dag                          |
|`tot_bedrag`  |Totaal bedrag = aantal dagen * dagtarief    |

* __BLANCO\_FISCAAL\_ATTEST (113-281-86-nl-2022.pdf):__ Dit is het modelattest dat gebruikt wordt. Dit kan best vervangen worden door een exemplaar waarbij ook de eerste pagina is ingevuld.

* __FORMULIER\_ANTWOORDEN (Fiscaal attest (Antwoorden) - Formulierreacties 1.csv):__ Dit is een CSV bestand met de informatie van de kampgangers die ingevuld moet worden in Vak II van het attest. Deze CSV is automatisch gegenereerd met een Google Formulier dat door de ouders ingevuld wordt. Google Forms laat niet toe om een formulier te downloaden, maar Google-Forms-template.pdf geeft een beeld van het gebruikte formulier. Je kan altijd contact opnemen met mij en dan bezorg ik je een kopie van het formulier waaruit je de vragen vervolgens kan exporteren.

* __ONDERTEKENAAR\_LOCATIE:__ Hier zet je de locatie van de persoon die de attesten zal ondertekenen.

* __ONDERTEKENAAR\_NAAM__: Hier zet je de naam van de persoon die de attesten zal ondertekenen.
 
* __ONDERTEKENAAR\_FUNCTIE:__ Hier zet je de functie van de persoon die de attesten zal ondertekenen.

* __OUTPUT\_MAP:__ Dit is de map waar de gegenereerde attesten in zullen verschijnen. Deze is bij default ingesteld op 'out'.

## Attesten genereren

Wanneer aan alle vereisten voldaan is, kan het script uitgevoerd worden. Dit kan met het volgende commando:

```bash
$ python Fiscale_attesten_generator.py                  
```

Wanneer het script correct is uitgevoerd, zal je een bevestigingsboodschap zien. Er is een map *out* aangemaakt, die de mappen *kapoenen*, *kawellen*, en *jogis* bevat. Hier zitten de verschillende attesten per tak gesorteerd. Let wel, dit zijn de takken zoals ze waren ingedeeld in het afgelopen scoutsjaar waarvoor je de attesten genereert.

## Attesten gebruiken

Vervolgens kan je de attesten ondertekenen en doormailen naar de ouders. 
