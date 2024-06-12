# Pulsar
Eine auf Python-basierende Grafikschnittstelle für den Kommandozeilenschnittstellenclienten [Nebula Mesh Netzwerk](https://github.com/slackhq/nebula) für Windows und MacOS.


Detaillierte Dokumentation befindet sich im Wiki

Pulsar wird von JS Prodüksiyon Ltd. Şti entwickelt und gewartet. und wird unter der GNU GPL v3.0 präsentiert.

Dieses Dokument ist auch in [Englisch (English)](README.md) und [Türkisch (Türkçe)](README_tr.md) verfügbar.

Dieses Dokument wurde zuletzt am 2024-06-12 aktualisiert.


## Nebula-Version
Nebula-Client-Binärversion 1.8.2

## Begründung für Pulsar
So schön das Nebula-Mesh-Netzwerk auch ist, es erfordert einiges an technischem Know-how, um es zu implementieren. Viele Benutzer sind technisch nicht versiert genug, um die Kommandozeilenschnittstellen-Befehle zu handhaben, die zum ordnungsgemäßen Ausführen von Nebula erforderlich sind. Da wir mehrere solcher Benutzer in unserer Gesellschaft haben, fanden wir es nötig, eine einfache Grafikschnittstelle zu schreiben, die es dem Benutzer ermöglicht, sich mit dem Nebula-Netzwerk zu verbinden. Das Setup erfordert ein wenig Hilfe von der IT-Abteilung, aber sobald es läuft, sollte es ziemlich einfach zu bedienen sein. 


## Betriebssystem-Kompatibilität

| Betriebssystem     | Quellencode    | Compiliert         |
| ------------------ | ------------   | ------------------ |
| Windows 11         | Funktioniert   | Funktioniert       |
| Windows 10         | Nicht getestet | Funktioniert       |
| Windows 7          | Nicht getestet | Funktioniert nicht |
| MacOS 13.6 (Intel) | Funktioniert   | Funktioniert       |
| MacOS 14.2 (M1)    | Funktioniert teilweise | Funktioniert teilweise |

Technisch gesehen sollte Pulsar in jedem Betriebssystem funktionieren, auf dem Python 3.11 und dem Nebula-Client laufen. Obwohl wir nicht in der Lage sind, alle Plattformen zu testen, kann diese Anwendung unter Berücksichtigung der Systemanforderungen von Python 3.11, PyQT 6.7 und Nebula auf den folgenden Betriebssystemen ausgeführt werden:

* **Windows:** 11, 10
* **macOS:** Sonoma 14, Ventura 13, Monterey 12, Big Sur 11

Da wir diese Anwendung nicht unter Linux gebrauchen werden, haben wir diese Funktionalität nicht hinzugefügt. Wenn Sie es jedoch forken und dort zum Laufen bringen möchten, dürfen Sie dies gerne tun.

PyQT 6- und Mac M1-Chipsatz-Inkompatibilitäten führen dazu, dass das Öffnen des Systemdateiauswahldialogs und das Einfügen in Textfelder fehlschlägt. Die Anwendung funktioniert jedoch, wenn die erforderlichen Informationen von Hand eingegeben werden. [Detaillierte Informationen befinden sich im Wiki](https://github.com/JS-Produksiyon/pulsar/wiki/Usage#issues-with-pulsar-on-macos-on-m-series-chips).

> Bitte beachten Sie, dass wir zurzeit _der MacOS-Version_ von Pulsar _nur die allernötigste Zeit widmen_, da eine völlig Funktionsfähige Windows-Version für unseren internen Gebrauch wichtiger ist.


## Installation
### Compilierte Releases
Sie können compilierte Versionen für Pulsar, die unter Windows und MacOS funktionieren, finden, indem Sie die Seite [Releases](releases/) besuchen.

Laden Sie die neueste Version herunter, entpacken Sie die Datei an einem Ort Ihrer Wahl und führen Sie die ausführbare Datei aus. Pulsar muss nicht installiert werden, um verwendet zu werden.

Sie können manuell einen Verknüpfungslink zu Pulsar zum Startmenü in Windows oder zum Launcher in MacOS hinzufügen

### Quelle
Pulsar benötigt Python 3.11, um ausgeführt zu werden.

Sie können den Quellcode von Pulsar auf Ihren Computer klonen, indem Sie eine Kommandoschnittstelle (PowerShell in Windows oder Terminal unter MacOS) mit dem Befehl `git clone https://github.com/JS-Produksiyon/pulsar.git` öffnen. 

Erstellen Sie nach dem Klonen eine virtuelle Umgebung: `python3.11 -m venv venv`

Aktivieren Sie die virtuelle Umgebung in Windows mit `venv\Scripts\Activate.ps1` oder verwenden Sie `source venv/bin/activate` unter MacOS.

Installieren Sie die erforderlichen Pakete mit `pip install -r requirements.txt`

Sobald die Anforderungen installiert sind, führen Sie das Programm mit dem Befehl `python src/pulsar.py` aus.


## Verwendung
Aufgrund der Tatsache, dass der Nebula Kommandozeilenschnittstellenclient Superuser-Zugriff erfordert, versucht Pulsar automatisch, seine Berechtigungen zu erhöhen, entweder mit einer UAC-Eingabeaufforderung unter Windows oder mit der Abfrage Ihres Passworts unter MacOS.

Beim ersten Start von Pulsar müssen Sie die erforderliche Nebula-Konfigurationsdatei (`.yaml`) auswählen. Sobald Sie diese ausgewählt haben, klicken Sie auf _Speichern_ und Sie sollten sofort eine Verbindung zum Nebula-Netzwerk herstellen können, indem Sie auf die große grüne Schaltfläche klicken.

> Die IT-Abteilung muss die Nebula-CA-Datei sowie den privaten Schlüssel und die Zertifikatsdateien des Benutzers zusammen mit der `.yaml`-Konfigurationsdatei  bereitstellen.

Das Schließen des Pulsar-Fensters beendet das Programm nicht. Das Programm wir beendet, indem Sie entweder auf die Schaltfläche _Pulsar schließen_ klicken oder mit der rechten Maustaste auf das Pulsar-Symbol in der Taskleiste klicken (Windows) oder indem Sie auf das Pulsar-Symbol in der Menüleiste klicken (MacOS) und _Beenden_ auswählen. 

Darüber hinaus bietet Pulsar die Möglichkeit, Einträge zur lokalen  `hosts`-Datei hinzuzufügen, um einen einfachen domainnamenbasierten Zugriff auf die verschiedenen Ressourcen zu ermöglichen, auf die der Benutzer zugreifen muss.

> Diese IP-Adressen-/Hostnamenpaare im `hosts`-Dateiformat müssen von der IT-Abteilung bereitgestellt werden.


## Warum heißt die App "Pulsar"?
Das Nebula-Mesh-Netzwerk-Tool ist nach den himmlisch leuchtenden Gasen benannt, die viele Sterne enthalten. Ein Mesh-Netzwerk ist eher amorph und enthält auch viele Knotenpunkte. Diese Anwendung ermöglicht es, dass sich ein Knotenpunkt mit dem Netzwerk verbindet, ähnlich wie ein Stern im Nebula existiert. Und weil es einen Puls aussendet, um sich zu verbinden, schien das Bild des Pulsars, eines magnetisierten Neutronensterns, der mit einer bestimmten Frequenz pulsiert, ein passendes Bild zu sein. Daher verwenden Sie Pulsar, um sich mit dem Nebula zu verbinden. Viel Spaß!
