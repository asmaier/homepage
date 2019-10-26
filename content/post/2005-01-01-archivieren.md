---
title: Archivieren
author: admin
date: '2005-01-01'
slug: archivieren
categories: []
tags:
  - computer
  - linux
  - old_website
  - german
subtitle: ''
summary: ''
authors: []
lastmod: '2019-09-27T21:26:30+02:00'
featured: no
image:
  caption: ''
  focal_point: ''
  preview_only: no
projects: []
---
Eine gute Einführung übers Archivieren und Komprimieren gibts in bei
<a href="http://www.oreilly.de/german/freebooks/rlinux3ger/ch072.html">
Welsh et al. 2000</a>.
Ich beschränke mich daher im weiteren auf ein paar eigene Bemerkungen.

<ul>
<li><em><tt>*.gz</tt>-Dateien entpacken:</em>
<pre>> gunzip dateiname.gz</pre>
Achtung: <tt>gunzip</tt> ersetzt die gepackte Datei (dateiname.gz)
mit der ungepackten Version (dateiname). 
Achtung2: <tt>gunzip</tt> ist ungeeignet um <tt>*.zip</tt>-Dateien
zu entpacken. <tt>gunzip</tt> unterstützt nur <tt>*.zip</tt>-Archive,
die aus genau einer Datei bestehen (siehe auch <tt>man gunzip</tt>).
Zum Entpacken von <tt>*.zip</tt>-Archiven die aus mehrerer Dateien bestehen
(was praktisch immer der Fall ist) muß man <tt>unzip</tt> verwenden.</li>

<li><em><tt>*.zip</tt>-Dateien entpacken:</em>
<pre>> unzip dateiname.zip</pre>
Dabei werden alle Dateien und Verzeichnisse ins aktuelle Verzeichnis entpackt.
Um Chaos zu vermeiden empfiehlt es sich daher vor dem Entpacken ein neues
Verzeichnis <tt>dateiname</tt> anzulegen, die Datei <tt>dateiname.zip</tt>
in dieses zu verschieben und dort erst zu entpacken. Das gleiche Vorgehen
empfiehlt sich natürlich auch für <tt>*.tar</tt>-Archive.</li>

<li><em><tt>*.tar.gz</tt>-Dateien entpacken:</em>
<pre>> tar zxvf dateiname.tar.gz</pre>
Die obige Schreibweise entspricht der sogennanten BSD-Unix-Schreibweise.
<tt>tar</tt> unterstützt auch die Standart-Schreibweise. Mit dieser
würde die obige Befehlszeile folgendermaßen aussehen:
<pre>> tar -z -x -v -f dateiname.tar.gz</pre> 
Zu beachten ist, dass die Option <tt>-f</tt> stets die letzte ist, da diese
den zu entpackenden Dateinamen angibt und daher dieser direkt im Anschluß
an die Option <tt>-f</tt> stehen muß. Die weiteren Optionen sind:
<ul>
<li><tt>-v</tt> (verbose): Damit gibt <tt>tar</tt> Informationen über den
Entpackprozess an. Kann auch mehrfach angegeben werden, dann gibt <tt>tar</tt>
immer mehr Informationen an.</li>

<li><tt>-x</tt> (extract): Sagt nur, dass die Datei hinter <tt>-f</tt> entpackt 
bzw. dearchiviert werden soll.</li>

<li><tt>-z</tt>: Gibt an, dass die Datei hinter <tt>-f</tt> zunächst mit
<tt>gunzip</tt> entpackt und dann erst weiter mit <tt>tar</tt> dearchiviert werden 
soll. Dies erspart den Extraaufruf von <tt>gunzip</tt> zum Entpacken der 
<tt>*.tar.gz</tt>-Datei. Statt <tt>-x</tt> kann man hier übrigens auch andere Optionen
und damit andere Packprogramme verwenden. Verwendet man <tt>-X</tt> wird 
<tt>uncompress</tt> (für <tt>*.tar.z</tt>-Dateien) aufgerufen, verwendet man <tt>-j</tt>
wird <tt>bunzip2</tt> (für <tt>*.tar.bz2</tt>-Dateien) benutzt.</li>
</ul>
Hinweis: Auf FAT32-Filesystemen ist zusätzlich die 
Option <tt>-m</tt> anzugeben, welche das Entpacken der Dateimodifikationszeit
verhindert, da es ansonsten beim Entpacken zu Fehlermeldungen kommt.
</li>

<li><em><tt>*.tar.gz</tt>-Dateien packen:</em>
<pre>> tar zcvf verzeichnis.tar.gz verzeichnis</pre>
Zu Beachten ist hier, dass 
(im Gegensatz zu anderen Kommandos wie z.B. <tt>cp</tt> oder <tt>scp</tt>)
die zu erzeugende Datei (das Ziel) zuerst angegeben
werden muß und dann erst das zu archivierende Verzeichnis (die Quelle).
Die Optionen dazu sind die gleichen wie oben beschrieben, nur steht nun
<tt>-c</tt> dafür, dass <tt>tar</tt> jetzt archivieren soll und <tt>-z</tt>
steht dafür, dass nach der Archivierung durch <tt>tar</tt> das Archiv noch
mittels <tt>gzip</tt> komprimiert werden soll. 
</li>

<li><em><tt>*.tar.gz</tt>-Dateien erzeugen, wobei versteckte Verzeichnisse von Subversion (<tt>.svn</tt>) ausgeschlossen werden:</em>
<pre>> tar --exclude='.svn' -zcvf verzeichnis.tar.gz verzeichnis</pre>
oder in neueren <tt>tar</tt> Versionen auch mit
<pre>> tar --exclude-vcs -zcvf verzeichnis.tar.gz verzeichnis</pre>
Siehe auch 
<a href="http://www.linuxquestions.org/questions/linux-software-2/copy-svn-working-dir-without-svn-hidden-dirs-and-files-620586/">
http://www.linuxquestions.org</a>.</li>

<li><em>Entpackprozess beobachten:</em><br />
Hat man beim Aufruf des Entpackprogramms die Verbose-Option vergessen und man möchte
trotzdem wissen, ob der Entpackprozess vorangeht, kann man dies mit Hilfe von
<tt>watch</tt> erreichen. Hat man z.B. das Entpacken mehrerer 
<tt>*.iso.gz</tt>-Dateien mittels <tt>gunzip</tt> gestartet, kann man mittels
<pre>>watch ls -l *.iso</pre>
sehen, wie sich die Größe der entpackten Datei (im Abstand von zwei Sekunden,
da <tt>watch</tt> einfach alle 2 Sekunden den Befehl <tt>ls -l</tt> ausführt)
mit der Zeit entwickelt.
Hinweis: <tt>watch ll *.iso</tt> funktioniert nicht, da <tt>watch</tt> 
anscheinend nicht mit Aliasen umgehen kann.</li>

<li><em>Inhalt von <tt>*.war</tt>-Dateien anzeigen</em>
<pre>> jar -tf datei.war</pre>
<tt>war</tt>-Dateien sind übrigens keine Dateien für den 
<a href="http://de.wikipedia.org/wiki/Verteidigungsfall">Verteidigungsfall</a> sondern
sogenannte <a href="http://de.wikipedia.org/wiki/Web_Archive">Web Application Archive-Dateien</a>
abgeleitet von 
<a href="http://de.wikipedia.org/wiki/Java_Archive">Java Archive-Dateien (<tt>*.jar</tt>)</a>.
</li>

<li><em>Dateien aufteilen (splitten) und wieder zusammenfügen</em><br />
Moechte man eine sehr große Datei namens <tt>file</tt> in Teile zu je 1GB = 1024MB aufteilen, so hilft das 
<tt>split</tt>-Kommando:
<pre>> split -b 1024m file file.split</pre>
Um die so entstandenen Teile namens <tt>file.split.aa, file.split.ab, ...</tt> wieder zusammenzufuegen nutzt man <tt>cat</tt>:
<pre>> cat file.split.* > file </pre>
</li>
</ul>