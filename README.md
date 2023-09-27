# Blockscrape

- ## Requirements
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

## Nutzung

Um die Server-Dienste zu starten: (in /Blockscrape)
```
docker compose up --build -d
```
<br>

Die Clients müssen seperat gestartet werden : (in /mining/client oder /result/client)
Vorher sollte allerdings ein User und eine Bestellung erstellt werden.
```
docker compose up --build -d
```

### Erstellung User und Bestellung
![img.png](ReadMeBilder%2Fimg.png)
Initiale Seite (Standardmäßig Port 99)
![img_1.png](ReadMeBilder%2Fimg_1.png)
Registrierung eines Users
<br>Hier müssen alle Felder einschließlich der Checkbox ausgefüllt sein
![img_2.png](ReadMeBilder%2Fimg_2.png)
Bei erstmaliger Registrierung öffnet sich ein Fenster mit den 2FA Daten
<br> Hier wird der QR-Code und der Secret Key angezeigt
<br> Diese müssen in eine 2FA App (getestet mit Google Auth) eingetragen werden
<br> Danach muss der entstehende Code einmalig zur Validierung, dass die Daten korrekt eingetragen wurden, übermittelt werden
<br> Danach landet man wieder auf der Login Seite
![img_3.png](ReadMeBilder%2Fimg_3.png)
Bei jeder weiteren Anmeldung muss der 2FA Code aus der APP eingegeben werden
![img_4.png](ReadMeBilder%2Fimg_4.png)
Bei erfolgreicher Anmeldung landet man auf der Startseite
Links in der Navbar, bzw. mobil im Burger Menü, befinden sich die Punkte:
- Your Orders
- Jegger Coins

<br>
Unter "Your Orders" können Bestellungen erstellt werden und alle bisherigen Bestellungen eingesehen werden
<br>
Unter "Jegger Coins" kann der aktuelle Coin Stand eingesehen werden und zu Testzwecken auch Coins hinzugefügt werden

![img_5.png](ReadMeBilder%2Fimg_5.png)

In der Tabelle stehen alle bisherigen Bestellungen
<br> Mit Hilfe des Plus-Buttons kann eine neue Bestellung erstellt werden
![img_6.png](ReadMeBilder%2Fimg_6.png)

Hier müssen folgende Daten eingetragen werden:
- Name
- URL (mit http:// oder https://)
- Request Method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS) (Standardmäßig GET)
- Intervall zwischen Wiederholungen (in Sekunden)
- Wiederholungen (Anzahl der Wiederholungen)
- Startdatum (Datum und Uhrzeit)
- Checkbox

Folgende Daten sind optional:
- Request Body (JSON)
- Request Header (JSON)

Getestet wurden Get APIs, welche JSONs zurückgeben, es kann somit bei anderen Optionen zu Problemen kommen

Pro Wiederholung muss ein Coin vorhanden sein

![img_7.png](ReadMeBilder%2Fimg_7.png)
Unter "Jegger Coins" kann der aktuelle Coin Stand eingesehen werden und zu Testzwecken auch Coins hinzugefügt werden

![img_8.png](ReadMeBilder%2Fimg_8.png)
![img_9.png](ReadMeBilder%2Fimg_9.png)
![img_10.png](ReadMeBilder%2Fimg_10.png)

Die komplette Website ist responsive und kann somit auch auf mobilen Geräten verwendet werden
Zusätzlich besitzt diese einen Darkmode, welcher über den Mond/Sonne in der Navbar aktiviert/deaktiviert werden kann

![img_11.png](ReadMeBilder%2Fimg_11.png)
Öffnet man eine Order, sieht man dessen Informationen, darunter die UUID
<br> Dieser wird für den Result Client benötigt


### Anpassungen Docker Compose Mining/Result Client

![img_12.png](ReadMeBilder%2Fimg_12.png)

In der Docker Compose müssen folgende Daten gesetzt werden:
- Mining_server_url mit Protokoll (http:// oder https://) und Port
- Server_path dieser ist für den Traefik relevant (standardmäßig /miningServer/socket.io)
- user (username) wird der falsche User eingetragen, werden die Coins einem anderen Account gutgeschrieben
funktionieren würde es aber

![img_13.png](ReadMeBilder%2Fimg_13.png)
In der Docker Compose müssen folgende Daten gesetzt werden:
- Result_server_url mit Protokoll (http:// oder https://) und Port
- Server_path dieser ist für den Traefik relevant (standardmäßig /resultServer/socket.io)
- job_id diese ist die UUID der Order
- output_dir hier wird der Ordner angegeben, in welchem die Ergebnisse gespeichert werden sollen, die Daten werden im Container gespeichert, wenn dies nicht gewünscht ist, muss noch ein Volume angegeben werden


### Infos
Der Dienst funktioniert auch mit nur einem User und einem Miner
<br> In diesem Fall mined man seinen eigenen Auftrag
