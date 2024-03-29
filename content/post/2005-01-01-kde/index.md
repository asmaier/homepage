---
author: admin
authors: []
date: '2005-01-01'
featured: false
image:
  caption: ''
  focal_point: ''
  preview_only: false
lastmod: '2019-09-27T21:30:50+02:00'
projects: []
slug: kde
subtitle: ''
summary: ''
tags:
- netzwerkverzeichnisse
- fish
- sicherheit
- linux
- kde
- dateiübertragung
- computer
categories:
- old_website
title: KDE
year: '2005'
languages:
- deutsch
---

<h6>Killerfeature: FISH</h6>
<p>Eines meiner liebsten Features von KDE ist die direkte Integration von Netzwerkverzeichnissen
über das <a href="http://de.wikipedia.org/wiki/FISH_(Protokoll)">FISH-Protokoll</a>.
Einfach unter Netzwerkbrowser "Netzwerkordner hinzufügen" auswählen und im folgenden Dialog
ssh auswählen 
<br />
<img src="fish1.jpg" style="margin: 1em;" alt="FISH1" /> 
<br />
und im folgenden Dialogfenster
<br />
<img src="fish2.jpg" style="margin: 1em;" alt="FISH2" />
<br />
die Daten des SSH-Servers eingeben. Aufpassen muß man nur, dass FISH anscheinend keine relativen
Verzeichnisse wie <tt>~</tt> mag. Also für das Homeverzeichnis auf dem SSH-Server immer 
<tt>/home/[benutzername]</tt> oder entsprechendes eingeben. 
Dann kann man das angegebene Verzeichnis wie ein lokales Verzeichnis benutzen,
<br />
<img src="fish4.jpg" style="margin: 1em;" alt="FISH4" />
<br />
z.B. kann man Dateien auf dem fremden Server auswählen, aber lokal über KDE drucken, ohne dass man erst per 
<tt>scp</tt> die Datei auf den eigenen Rechner kopieren muß. Oder man editiert die Datei mit dem 
bevorzugten Editor (z.B. Kate) lokal und ein Klick auf speichern speichert die Datei wieder auf dem entfernten Netzwerkverzeichnis, obwohl der Editor nativ gar kein SSH unterstützt (Reibungslos funktioniert das leider nur mit Programmen die den KDE-Dateiauswahldialog benutzen. GIMP z.B. benötigt eine lokale Kopie der Datei :-( ). Echt cool! Aber das coolste ist, dass das bei jedem Server funktioniert der SSH unterstützt, es werden keine weiteren Netzwerkprotokolle ala FTP, NFS oder SMB benötigt, welche aus Sicherheitsgründen meist geblockt sind. Daher ist die FISH-Integration in KDE eine echte
Arbeitserleichterung für alle die häufig auf Servern unterwegs sind, die aus Sicherheitsgründen nur 
SSH zulassen.
<br />
P.S.: Das Feature ist so cool, dass Google vergleichbares in MAC OS X integriert hat (siehe
<a href="http://google-code-updates.blogspot.com/2007/01/macfuse-fuse-for-mac-os-x.html">google-code-updates.blogspot.com</a>).
Die neueste Version von diesem sog. MacFUSE gibts <a href="http://code.google.com/p/macfuse/">hier</a>. Eine grafische Benutzeroberfläche dazu gibts unter <a href="http://www.macfusionapp.org/">www.macfusionapp.org</a>.
</p>

<h6>Autostart unter KDE</h6>
<p>Programme die beim Start von KDE automatisch ausgeführt werden sollen, müssen unter
<pre>~/.kde/Autostart</pre>
liegen. Am einfachsten erzeugt man über das Kontextmenü unter <tt>Neu erstellen/Verknüpfung zu Programm</tt>
einen Link zu dem aufzurufenden Programm indem man in sich öffnenden Dialogfenter im Tab <tt>Programm</tt>
den Pfad zum entsprechenden Programm unter <tt>Befehl</tt> eingibt. 
<br />
Will man mehr Kontrolle über die 
aufzurufenden Programme hilft <tt>kstart</tt> (Hilfe zu dem Befehl gibt es mit <tt>kstart --help</tt>). 
Um z.B. ein Programm nur auf nur auf der fünften Arbeitsfläche zu öffnen, kann man statt dem einfachen Pfad 
zum Programm den Befehl
<pre>kstart --desktop 5 programmname</pre>
unter <tt>Befehl</tt> eingeben. Daran sieht man auch, dass die Verküpfungen unter KDE die man über das Kontextmenü
erzeugen kann mehr sind als nur symbolische Links, wie man sie von der Kommandozeile kennt. Stattdessen steht
jede Verknüpfung für eine <tt>*.desktop</tt>-Text-Datei, die von KDE je nach Inhalt unterschiedlich interpretiert 
werden kann.
<br />
Will man auch die Reihenfolge der gestarteten Programme kontrollieren muß man ein kleines Shellskript schreiben und
als ausführbare Datei unter </tt>~/.kde/Autostart</tt> ablegen, z.B.:
<pre>
#!/bin/bash
kstart --desktop 5 thunderbird
sleep 3
kstart --desktop 6 --activate programm
</pre>
Diese Skript startet <tt>Thunderbird</tt> auf Arbeitsfläche 5, und danach das Programm <tt>programm</tt> auf 
Arbeitsfläche 6 und springt auch von Thunderbird zu dem Programm auf Arbeitsfläche 6. Der Aufruf von <tt>sleep 3</tt>
garantiert dabei, dass das zweite Programm mit 3 Sekunden Verzögerung gestartet wird. Ohne <tt>sleep</tt> erlaubt 
Thunderbird seltsamerweise nicht, dass der Focus zum zweiten Programm auf Arbeitsfläche 6 springt.
</p>

<h6>Weitere Tipps</h6>
<ul>
<li><em>Verschieben von Fenstern:</em><br />
Manchmal passiert es, dass man ausversehen ein Fenster soweit
nach oben verschoben hat, dass die Titelleiste nicht mehr
sichtbar ist. Einfaches Anklicken und Ziehen des Fensters
an der Titelleiste ist dann nicht mehr möglich. Hält man jedoch
die Taste <tt>[[Alt]]</tt> (nicht <tt>[[Alt Gr]]</tt> ) gedrückt,
so kann man das Fenster mit der linken Maustaste an einer beliebigen
Stelle greifen und so das Fenster wieder nach unten verschieben.<br />
Tipp: Weitere Befehle findet man im KDE Control Module unter
"Window Behaviour/Actions". Diese Einstellungen erreicht man auch
durch Klick auf die linke obere Ecke eines Fensters, wenn man im
sich darauf öffnenden Menü "Configure Window Behaviour..." aufruft.
</li>
<li><em>Fenster in den Hintergrund klicken</em><br />
Jedem dürfte bekannt sein, dass man durch Klicken 
mit der linken Maustaste auf die Fensterleiste
ein Fenster aktivieren und in den Vordergrund holen kann. 
Wie holt man jedoch Fenster in den Vordergrund die durch ein
anderes Fenster komplett verdeckt sind? Ganz einfach unter KDE:<br />
Durch Anklicken der Fensterleiste des gerade aktiven Fensters mit der
mittleren Maustaste wird das gerade aktive Fenster in den Hintergrund 
geschickt und eventuell verdeckte Fenster kommen zum Vorschein.
Wer das einmal ausprobiert hat, wird diese Funktion nicht mehr missen
wollen.</li>

<li><em>Taskmanager unter KDE aufrufen:</em><br />
Das Programm <tt>kpm</tt>, welches dem Taskmanager unter Windows gleicht,
kan man unter KDE mit der Tastenkombination
<pre>[[Ctrl]]-[[Esc]]</pre>
aufrufen. Durch Anklicken des Knopfes "Kill" (in dt. "Beenden")
kann man dann die markierten Prozesse beenden. Alternativ kann man
<tt>kpm</tt> auch über die Konsole mit
<pre>> kpm &amp;</pre>
oder auch das komplette Systemüberwachungsprogramm (von dem <tt>kpm</tt>
nur ein Unterprogramm ist) mittels
<pre>> ksysguard &amp;</pre>
aufrufen. Letzteres findet man auch über das Startmenü unter
"System/Überwachung/Systemüberwachung".</li>

<li><em>KDE-Taskleiste anzeigen:</em><br />
Manchmal passiert es unter KDE dass die Taskleiste sich nicht mehr einblendet, wenn
man die Maus an den unteren Bildschirmrand bewegt. In diesem Fall kann man sie mit
<tt>[[Alt]]-[[F1]]</tt> wieder hervorholen. Wenn man so wie ich keine weiteren Icons auf 
dem Bildschirm hat, kann <tt>[[Alt]]-[[F1]]</tt> daher "lebensrettend" sein, denn oft bleibt die 
Taskleiste auch nach dem Reboot verschwunden und das System ist praktisch unbedienbar.</li>

<li><em>Weitere Tastenbefehle unter KDE:</em><br />
<ul>
<li><tt>[[Ctrl]]-[[Esc]]</tt> : Taskmanager</li>
<li><tt>[[Ctrl]]-[[Alt]]-[[Esc]]</tt> : löscht Fenster in KDE (killt aber nicht
den dazugehörigen Prozess)</li>
<li><tt>[[Alt]]-[[F2]]</tt> : Analog zu "Befehl ausführen" unter Windows;
öffnet ein einzeiliges Terminal in dem man den Befehl zum Starten eines
Programmes eingeben kann</li>
<li><tt>[[Ctrl]]-[[Fx]]</tt> : Umschalten auf den virtuellen Desktop Nummer "x"</li>
<li><tt>[[Ctrl]]-[[Alt]]-[[L]]</tt> : Bildschirm sperren</li>
</ul>
Noch mehr Tastenbefehle findet man u.a. in der <a href="http://linuxwiki.de/KDE">Linuxwiki</a>.</li>

<li><em>Tastenbefehle für den X-Server:</em><br />
Die Auflösung des X-Servers zur Laufzeit (also ohne Neustart) kann mit den
Tastenkombinationen
<pre>[[Ctrl]]-[[Alt]]-[[Ziffernblock-Plus]]</pre>
bzw.
<pre>[[Ctrl]]-[[Alt]]-[[Ziffernblock-Minus]]</pre>
geändert werden. Mit der Kombination
<pre>[[Ctrl]]-[[Alt]]-[[Backspace]]</pre>
wird der X-Server <em>sofort</em> beendet. 
</li>

<li><em>Probleme mit dem Papierkorb (Trashcan):</em><br />
Es kann unter KDE passieren, dass der Papierkorb, obwohl er geleert wurde,
noch Dateien enthält, welche jedoch auf dem Desktop nicht angezeigt werden
(auch bei aktiviertem "versteckte Dateien anzeigen").
Diese Dateien muss man dann per Hand löschen. Man findet die Dateien im Papierkorb 
im eigenen Homeverzeichnis unter
<pre>.local/share/Trash/files</pre>
Mittel <tt>> rm -rf *</tt> kann man dann dort alle Dateien endgültig löschen und
damit den Papierkorb wirklich leeren.
</li>

<li><em>Kompare:</em><br />
Diese Programm findet man unter Suse Linux im Paket <tt>kdesdk3</tt>.</li>

</ul>