# Sammlung und Auswertung der Daten für Bürgermeister*innen in Baden-Württemberg

Diese Software sammelt die Wahlergebnisse der jeweils letzten Bürgermeister*innenwahlen 
in allen Gemeinden und Städten in Baden-Württemberg von der [Webseite des Staatsanzeigers für BW](https://www.staatsanzeiger.de/staatsanzeiger/wahlen/buergermeisterwahlen/).

Die so gesammelten Daten sind nur so gut und vollständig wie die Daten auf dieser Webseite. 
Im Oktober 2020 waren 1049 von 1101 Städten und Gemeinden gelistet.

**Achtung:** Die Datensäuberung nach dem Download ist nicht ganz vollständig. Mehr als die Hälfte 
der Einträge auf der Webseite haben das selbe Format und lassen sich zuverlässig parsen. Einige "Fehler" 
lassen sich auch auffangen, aber den Rest muss man zuletzt von Hand nachbessern.


## Installation

Vorraussetzungen:

* Python3.7 oder höher
* Python-pip
* *Optional:* virtualenv

```bash
git clone https://github.com/dketterer/buergermeister_innen-bw.git
cd buergermeister_innen-bw
virtualenv -p python3.7 venv
source venv/bin/activate 
pyhon setup.py install
```

## Verwendung

```bash
bbw --save buergermeister_innen.csv
```

## Auswertung

In einem [Jupyter Notebook](notebooks/demo.ipynb) finden sich beispielhafte 
datenjournalistische Auswertungen.

**Benutzung:**

Das Notebook starten: `jupyter notebook`

Den Link aus der Konsole im Browser öffnen.

## Funktionsweise

Der Crawler holt sich aus der [Übersichtsseite](https://www.staatsanzeiger.de/staatsanzeiger/wahlen/buergermeisterwahlen/) die Liste der Städt und Gemeinden zu denen Daten verfügbar sind 
und besucht dann im nächsten Schritt jede Seite zu der Gemeinde. Diese ganzen HTML-Dateien werden dann lokal in `.html` 
zwischengespeichert.

Nach dem Download wird aus dem HTML automatisch die Information zur Bürgermeister*innenwahl herausgefiltert.

## License

GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007
