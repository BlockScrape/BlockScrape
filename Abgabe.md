## Komponenten
![plan.drawio.png](..%2F..%2FDownloads%2Fplan.drawio.png)
- Web Frontend und Backend
    - Können genutzt werden zur Erstellung von Nutzerkonten und Bestellungen (Welche Adresse, Beginn, wie oft und in welchem Intervall)
    - Frontend kommuniziert mit Backend, welches Nutzer und Bestellungsdaten im Job-User-Storage (Cassandra) ablegt
    - Verifizierung bei Login mithilfe von Auth-Service
- Auth-Service
    - Auslagerung der Verifizierung auf eigenen Service um zentralen Anlaufpunkt zu haben, falls das Ökosystem erweitert wird mit Services und Funktionen, die auch Authentifizierung benötigen (Seperation of Concerns). Außerdem um höhere Ausfallsicherheit und Skalierbarkeit zu erreichen, da unabhängig.
- Scheduling Service
    - Aufgabe
        - Abarbeitung von Bestellungen, Umwandlung in einzelne konkrete Aufträge
        - regelmäßiges Fetchen von Bestellungsdaten aus dem Job-User-Storage, und bei Bedarf Erstellung von konkreten Aufträgen(Scrape Jobs die asap ausgeführt werden sollten)
- Coin Service
    - Verwaltet Währung
    - Auslagerung in seperaten Service, da sowohl Web Backend (erstellen einer Bestellung kostet Geld) und Mining Server (zum entlohnen von minenden Usern) davon abhängig sind, und so Skalierung und Ausfallsicherheit besser gewährleistet sind.
- Mining Server und Client
    - Server vergibt zu erfüllende Scrape Aufträge an Clients
    - Clients bearbeiten Aufträge und geben Ergebnisse zurück
    - Server leitet Ergebnis an Result Storage weiter und überweist dem entsprechenden User des Mining Clients eine Entlohnung durch den Coin Service
- Result Server und Client#
    - benötigt für Auslieferung von Ergebnissen
    - Server verschickt Ergebnisse aus dem Result Storage an den für den entsprechenden Auftrag registrierten Client
    - Client speichert erhaltene Ergebnisse lokal in Dateien ab
- Result-Admin-Storage
    - benötigt bei Implementation von "ScalingGroups" um Result client bei Verbindungsaufbau an die Scaling Group zu verbinden, die die entsprechende Bestellung enthält
    - -> wegen Entscheidung zur Nicht-Implementierung von Scaling Groups nicht mehr benötigt
## Requirements
- Functional
    - anpassbares Intervall einer Bestellungen
    - anpassbare Adresse einer Bestellungen
    - anpassbares Startdatum einer Bestellung
    - Begrenzung der Wiederholungen einer Bestellung
    - Währungssystem zum Balancing von Bestellungen und Minern
    - Zwei-Faktor-Authentifizierung im Web
- Non-Functional
    - Skalierbarkeit
    - Ausfallsicherheit
    - zeitnahes Erhalten von Ergebnissen (maximal 2 min)

## Umsetzung
### Umgesetzte Architektur - Implementierung
![akt.drawio.png](..%2F..%2FDownloads%2Fakt.drawio.png)

Aufgrund fehlender Funktionen zur Nutzung von mehreren ineinander verschachtelten
Scaling, wurde die Architektur etwas abgeändert. Bei der neuen Architektur werden
die Services (Mining Server, Result Server, Scheduling Server) nicht mehr miteinander
gescaled, sondern einzeln. Dies hat zur Folge, dass ein zusätzlicher Scheduling-Managing
Service benötigt wird. Zu diesem bauen die Scheduling-Services eine Socket Verbindung auf.
Bei jeder neuen Verbindung oder einem Verbindungsabbruch bekommt jeder Scheduling-Service
die Gesamtanzahl aller aktiven Services und eine Nummer innerhalb dieser Anzahl zugewiesen.
Dadurch werden die Jobs in der Cassandra gleichmäßig auf die Scheduling-Services verteilt.
<br><br>
Für eine bessere Übertragung der Scraping Ergebnissen zwischen Mining und Result Server, 
wurde statt Pub/Sub-Redis, RabbitMQ verwendet. Dies hat den Vorteil, dass ohne Probleme
mehrere Result Server verwendet werden können. Außerdem ist es möglich, dass mehrere 
Mining-Server auf denselben Channel Daten schicken können.
<br><br>
Für die Verbindung nach außen war ein Nginx-Reverse-Proxy vorgesehen. Dieser wurde jedoch
nicht verwendet, da es Probleme mit dem Round Robin Load-Balacing System von Docker gab.
Für die Website war dies kein Problem, allerdings für den Mining- und Result-Client.
Diese bauen mit dem jeweiligen Server eine Socket Verbindung auf, um die Daten zu verteilen.
Allerdings kann durch Round-Robin keine feststehende Session verwendet werden. Um dieses
Problem zu lösen, wird Traefik verwendet. Dieser kann mit Docker umgehen und die Verbindungen
für Mining- und Result-Client nach Sessions auf unterschiedliche Server leiten. Dies ermöglicht
eine Skalierbarkeit der Mining- und Result-Server.
<br><br>
Für die Authentifizierung auf der Website wird ein Authentifizierungsservice verwendet.
Dieser ist voll skalierbar, da er keine Daten speichert. Die Daten werden in einer zentralen
Cassandra abgelegt. Diese ist theoretisch auch skalierbar.
<br><br>
Der Backend-Service verarbeitet alle Anfragen, welche von der Website kommen. Bei jeder
Anfrage User-Anfrage wird der Auth-Service angefragt, ob der User validiert ist. Da der
Backend-Service als Datenspeicher ebenfalls die Cassandra verwendet, ist dieser auch 
skalierbar.
<br><br>
Der Coin-Service verwaltet wie geplant die anfallenden Abbuchungen. Bei der Bestellung
wird pro Wiederholung ein Coin berechnet. Pro gescrapte Website bekommt der User einen
Coin gutgeschrieben. Für Testzwecke kann sich aktuell ein User im Frontend Coins zuschreiben.
Dieser Service ist ebenfalls skalierbar, da er keine Daten speichert.
<br><br>
Das Frontend wird von einem NGINX Server ausgeliefert und ist somit auch skalierbar.
<br><br>
Bei jedem Punkt, welcher "Theoretisch Ja" ist, wurde die Skalierbarkeit des benutzten
Dienstes nicht direkt implementiert, allerdings unterstützen die Dienste diese Funktion.

| Service | Skalierbarkeit |
| --- |----------------|
| Auth-Service | Ja             |
| Backend-Service | Ja             |
| Cassandra | Theoretisch Ja |
| Coin-Service | Ja             |
| Frontend | Ja             |
| Mining-Server | Ja             |
| RabbitMQ | Theoretisch Ja |
| Result-Server | Ja             |
| Scheduling-Manager | Nein           |
| Scheduling-Server | Ja             |
| Scheduling Queue (Redis) | Theoretisch Ja |
| Traefik | Theoretisch Ja |

### Schwierigkeiten

- Verwendung von SocketIO und Load-Balancing via Docker und Nginx
- Zuteilung der Jobs auf die Scheduling-Services
- Testen der Funktionen und Skalierbarkeit -> Authentifizierung Funktionen (2FA) eingebaut, welche die Zeit für einen neuen Test verlängert haben
- Firewall-Probleme vor allem auf privatem Linux Rechner -> System wurde auf einem Ubuntu 22.04 LTS Server getestet, dort ohne Probleme


### Alternativen

- Services eventuell etwas zusammenfassen
- andere DB verwenden (z.B. statt Cassandra ScyllaDB)
- Verwendung von Kubernetes


## Reflektion
- was würden wir jetzt anders machen
    - erst checken ob NGINX auch Sticky-Sessions in der kostenlosen Variante unterstützt bevor man NGINX für die gesamte Architektur als Proxy festlegt und implementiert (um nicht nachher nochmal alles auf Traefik umbauen zu müssen)
- größte Herausforderungen
    - Load Balancing von SocketIO Verbindungen, Anfragen eines SocketIO Clients müssen immer an den gleichen SocketIO Server gelangen -> Sticky Sessions -> war Umbau von NGINX auf Traefik nötig, da NGINX Sticky Sessions nicht in der Open Source Variante unterstützt.
    - Aufteilen von Bestellungen auf mehrere Scheduling Services -> ein Management-Service wurde nötig um Bestellungen bestimmen Scheduling-Services zuzuordnen