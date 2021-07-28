# Ubersicht

GMIT ermöglicht es einer Organisation, Angebote von wiederverwendbaren Materialien zu verfolgen, den Materialbestand zu verwalten und verschiedene Berichte und Ergebnisse zu erstellen.

Diese Berichte enthalten EcoCost-Berichte. Es wird eine API bereitgestellt, um Informationen zu Drittanbieterdiensten wie Restado bereitzustellen.

## Login

https://gmit.material-mafia.net/accounts/login/

## Logout

Klicken Sie auf Ihren Benutzernamen in der oberen rechten Ecke einer beliebigen Seite und klicken Sie auf "Logout".

## Angebote

Externe Nutzer können der Materialmafia Material oder Gegenstände anbieten.

https://gmit.material-mafia.net/offer/

Einige Informationen werden gesammelt.

Für den administrativen Benutzer von GMIT erscheinen die Angebote hier:

https://gmit.material-mafia.net/dashboard/offers/

Angebote können auf angenommen, abgelehnt oder anstehend eingestellt werden.

https://gmit.material-mafia.net/dashboard/offers/
https://gmit.material-mafia.net/dashboard/pending/
https://gmit.material-mafia.net/dashboard/accepted/
https://gmit.material-mafia.net/dashboard/rejected/

Angebote können in der Datenbank in Materialien umgewandelt werden, indem Sie auf den Button "Objekt aus Diesem Angebote Erstellen" klicken.

Angebote können auch gelöscht werden.

## Materialen

### Material Erstellen

Materialien können auf vier Arten erstellt werden

#### Durch manuelle Eingabe aller Informationen

Klicken Sie auf neues Material erstellen und geben Sie alle Informationen ein.

#### Indem Sie ein Angebot annehmen und daraus ein Material machen, wie oben erwähnt

Angebote können in der Datenbank in Materialien umgewandelt werden, indem Sie auf den Button "Objekt aus Diesem Angebote Erstellen" klicken.

#### Durch Klonen eines Elements aus der KnowledgeBase

Klicken Sie auf neues Material erstellen, wählen Sie einen Artikel aus der KnowledgeBase aus und klicken Sie auf Klonen.

#### Durch Klonen eines bestehenden Materials

Besuchen Sie ein vorhandenes Material und klicken Sie auf "Klonen" im Admin-Bereich in der rechten Spalte.

### Material info (Info zum Material)

Hier kann der Benutzer alle ihm bekannten Informationen zum Material eingeben. Du solltest eine "Einheit" für das Material auswählen und eine Stuckanzahl eingeben. Stuckanzahl kann leer gelassen werden, wenn der Betrag unbekannt ist.

Die mit Restado geteilten Felder sind in der Benutzeroberfläche deutlich gekennzeichnet.

### Material Admin

#### KnowlegeBase

Durch Anklicken des Kontrollkästchens "Benutzen in KnowledgeBase" bestätigen Sie, dass das Material als eine Art Vorlage zum Erstellen anderer Materialien zur Verfügung steht.

#### Klonen

Über diese Schaltfläche kann direkt ein neues Material aus dem aktuellen Material geklont werden. Sie werden sofort auf die Infoseite für dieses Material weitergeleitet. Sie können auch sehen, welche Materialien aus diesem Material geklont wurden und welches Material (falls vorhanden) die Vorlage für das aktuelle Material war.

#### Löschen

Über den Button "Löschen" kann ein Material gelöscht werden.

Gelöschte Materialien finden Sie hier: https://gmit.material-mafia.net/dashboard/deleted/

#### Archivieren

Über diese Schaltfläche kann ein Material an das Archiv gesendet werden. MAterials können danach ausarchiviert werden. Archivierte Materialien finden Sie hier:

https://gmit.material-mafia.net/dashboard/archived/

### Restado

Materialien können auf Restado, einer Partner-Website, angezeigt werden. Durch Klicken auf die Schaltfläche stellen Sie das Material über die restado-API zur Verfügung.

### Verkaufen

Nachdem ein Material verkauft wurde, sollte es in der Rubrik Verkaufen als gebraucht verkauft gekennzeichnet werden.

Der Benutzer kann den Preis, zu dem er den Artikel verkauft hat, und die Anzahl der verkauften Einheiten eingeben.

Sie klicken dann auf Bestatigen.

Der Verkauf wird protokolliert.

Wenn der Benutzer das gesamte Material verkauft, wird das Material als verkauft markiert und weitere Verkaufsaktionen können nicht durchgeführt werden.

Wenn der Benutzer nur einen Teil des Materials verkauft hat, wird das Material geklont, der Klon wird als verkauft markiert und die Stückzahl für das aktuelle Material wird um die verkaufte Anzahl reduziert.

Bitte beachten Sie, dass wenn die Stückanzahl leer ist, der Benutzer das Material immer wieder verkaufen und weiterverkaufen kann. Dies soll Situationen Rechnung tragen, in denen die genaue Menge des Materials nicht bekannt ist, aber dennoch ein Verkauf stattfindet (z. B.: eine sehr lange Stoffrolle usw.).

### Bilder

Bilder können hinzugefügt, gelöscht oder als "Hauptbild" festgelegt werden. Das Hauptbild wird für die Verwendung für Drittanbieterdienste wie Restado empfohlen.

### Bemerkungen

Diese Kommentare sind nur für den internen Gebrauch bestimmt. Sie können alles sein, was der Administrator wünscht.

### Vorherige Aktionen

Ein vollständiges Protokoll aller Aktionen, die mit dem aktuellen Material durchgeführt wurden, finden Sie hier.

## Geber

TODO

## Bericht

2 Berichte sind verfügbar:

1) Eine Gesamtbuchhaltung aller Materialien in der Datenbank, als CSV-Datei.
2) Eine monatliche Aufschlüsselung der verkauften Artikel und der damit verbundenen Ökokosten.

Beide Berichte sind auf jeder Seite oben verfügbar:

1) Inventarbericht herunterladen
2) Monatlicher Bericht herunterladen



