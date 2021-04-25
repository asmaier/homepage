---
author: admin
authors: []
categories: []
date: "2005-01-01"
featured: false
image:
  caption: ""
  focal_point: ""
  preview_only: false
lastmod: "2019-09-27T21:10:55+02:00"
projects: []
slug: shell-skripte
subtitle: ""
summary: ""
tags:
- german
- computer
- linux
title: Shell-Skripte
---
<p>Um Shell-Skripte für die Bash-Shell zu schreiben sind folgende Schritte
nötig:</p>
<ol>
<li>Eine Textdatei erzeugen mit Namen
<pre> dateiname.sh</pre></li>

<li>Die erste Zeile der Textdatei muß lauten:
<pre>#!/bin/sh</pre>
Im Anschluss an diese Zeile schreibt man das
Shell-Skript. 
Aber Achtung: Bei der Angabe von Dateinamen in Skripten sollte
man immer den vollen Dateipfad angeben, sonst funktioniert das Skript nicht von
jedem Verzeichnis aus. Dies ist z.B. nötig, wenn ein Skript als Icon im
KDE-Panel gestartet werden soll.</li>

<li>Ausführen des Skripts
	<ul>
	<li>Ohne Executable-Bit wird das Skript mithilfe des <tt>sh</tt>-Kommandos
	gestartet:
	<pre>> sh dateiname.sh</pre></li>

	<li>Man kann ein Skript auch direkt ausführen, wenn man mit
	<pre>> chmod u+x dateiname.sh</pre>
	das Skript vorher ausführbar gemacht hat
	(Mehr zum <tt>chmod</tt>-Befehl gibt es 
	<a href="http://eva-marbach.net/handbuch/u-chmod.htm">hier</a>.).
	Danach kann man es direkt starten mittels
	<pre>> ./dateiname.sh</pre></li>
	</ul></li>
</ol>

<p>Mehr zur Syntax der Shell-Skript-Programmierung gibt es z.B. auf den Seiten der 
<a href="http://www.chemie.fu-berlin.de/chemnet/general/topics/scripts_sh.html">
FU Berlin</a>.</p>
