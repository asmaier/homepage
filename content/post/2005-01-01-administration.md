---
author: admin
authors: []
date: '2005-01-01'
featured: false
image:
  caption: ''
  focal_point: ''
  preview_only: false
lastmod: '2019-09-27T21:28:39+02:00'
projects: []
slug: administration
subtitle: ''
summary: ''
tags:
- superuser
- x-programme
- root-rechte
- passwortänderung
- linux
- administratorrechte
- computer
categories:
- old_website
title: Administration
year: '2005'
languages:
- deutsch
---

<p>Hier stehen Dinge, die man nur als Administrator (Root) bzw.
Superuser ausführen kann.</p>
<ul>
<li><em>Administratorrechte bekommen:</em><br />
Sitzt man vor einem Linux-Rechner kann man sich sehr einfach(!) Root-Rechte
verschaffen. Dazu muß man nur im Bootmanager als Option
<pre> init=/bin/bash </pre>
eingeben. Das System bootet dann ohne(!!) nach dem Passwort zu fragen in eine
bash-shell mit Root-Rechten. Jetzt gibt man einfach
<pre>> passwd</pre>
ein und gibt ein neues Passwort ein. Damit hat man das Root-Passwort neu gesetzt
und damit sofort Root-Rechte auf diesem Rechner.</li>

<li><em>Als Administrator/Superuser das Passwort eines anderen Benutzers neu setzen</em><br />
Als Superuser kann man sich zwar jederzeit mittels <tt>sudo -i -u [Benutzername]</tt> als
Benutzer <tt>[Benutzername]</tt> anmelden, aber versucht man dann das Passwort mittels <tt>passwd</tt>
neu zu setzen, wird man nach dem alten Passwort des Benutzers <tt>[Benutzername]</tt> gefragt,
das man wahrscheinlich nicht kennt. Viel einfacher und ohne das Passwort des Benutzers zu kennen,
setzt man das Passwort als Administrator/Superuser neu:
<pre>
> passwd [Benutzername]
</pre>
</li>

<li><em>Passwortänderung beim nächten Login erzwingen:</em><br />
Will man, dass ein Benutzer beim nächsten Login sein Passwort neu setzt, so benutzt man
<pre>
> passwd -e [Benutzername]
</pre>
Dies ist auch nützlich, wenn man gerade einen neuen Benutzeraccount angelegt hat und dem
Benutzer ein initiales Passwort per Email senden möchte, dass er nur für den ersten Login
verwenden soll. Setzt man unmittelbar nach der Erzeugung des Account 
<tt> passwd -e [Benutzername]</tt>, so ist der Benutzer gezwungen bereits beim ersten Login
ein neues Passwort zu setzen. Mehr dazu bei 
<a href="http://theos.in/desktop-linux/tip-that-matters/how-do-i-force-linux-to-change-forcefully-user-password/">Hakuna Matata:How do I force linux to change (forcefully) user password?</a>.
</li>

<li><em>Als Superuser X-Programme ausführen:</em><br />
Mit dem üblichen <tt>su</tt>-Befehl kann man keine X-Programme
(Programme mit grafischer Benutzeroberfläche) ausführen,
da die entsprechenden Rechte nicht automatisch gesetzt werden.
Unter Suse gibt es dafür folgenden Befehl:
<pre>> sux</pre>
Nach Eingabe des Superuserpassworts kann man dann ohne Probleme
auch Programme mit grafischer Benutzeroberfläche mit Superuserrechten
aus der Kommandozeile starten.</li>

<li><em>Einem Benutzer in die sudoers-Liste aufnehmen:</em><br />
Frei nach <a href="http://de.wikipedia.org/wiki/Sudo">Wikipedia/Sudo</a>:
Man benutzt <tt>sudo</tt> anstelle von <tt>su</tt>, um bestimmten Benutzern die Möglichkeit zu geben, 
gewisse Programme mit den Rechten eines anderen Benutzers (meistens Root) ausführen zu können, ohne 
das Root-Passwort weitergeben zu müssen. Die Sicherheitsrichtlinien sind bei Linux in der Datei /etc/sudoers gespeichert, 
die nur vom Superuser root editiert werden darf.<br />
Um also für einen Benutzer <tt>sudo</tt> freizuschalten, editiert man als root die sudoers-Datei
<pre>
> jpico /etc/sudoers
</pre>
Folgende Zeilen müssen hinzugefügt werden, um einem Benutzer <tt>[username]</tt> Zugriff auf alle Befehle mittels 
<tt>sudo</tt> zu geben:
<pre>
[username] ALL=(ALL) ALL
</pre>
Unter Suse Linux wird der Benutzer beim Ausführen von <tt>sudo</tt> jedoch trotzdem standardmäßig nach dem
root-Passwort gefragt. Um das zu verhindern muß man zwei Zeilen wie folgt auskommentieren
<pre>
#Defaults targetpw    # ask for the password of the target user i.e. root
#%users ALL=(ALL) ALL # WARNING! Only use this together with 'Defaults targetpw'!
</pre>
Jetzt fragt <tt>sudo</tt> wie gewünscht beim Ausführen nach dem Benutzerpasswort und nicht nach dem
root-Passwort.
</li>

<li><em><tt>sudo</tt> benutzen:</em><br />
Um sich als anderer Benutzer <tt>[username] </tt> einzuloggen:
<pre>> sudo -i -u [username] </pre>
Um sich als <tt>root</tt> einzuloggen:
<pre>> sudo -i </pre>
Letzterer Befehl ist äquivalent zu <tt>sudo su -</tt>.
Will man eine Shell mit <tt>root</tt>-Rechten, jedoch ohne die Umgebungsvariablen der aktuellen Umgebung zu verlieren, so benutzt man
<pre>> sudo -s </pre>
Letzteres funktioniert jedoch nur, wenn in der Datei <tt>/etc/sudoers</tt> die eventuell vorhandene Zeile
<pre>Defaults    env_reset</pre>
auskommentiert(!) ist.
Mehr zum <tt>sudo</tt>-Kommando gibt es unter 
<a href="https://help.ubuntu.com/community/RootSudo">RootSudo(help.ubuntu.com)</a>.
</li>

<li><em>Graphische (X-Window) Programme ueber <tt>sudo</tt> aufrufen:</em><br />
Das naive Aufrufen graphischer Programme aus einer <tt>sudo</tt>-Shell scheitert meist,
da notwendige Umgebungsvariablen nicht gesetzt sind. Insbesondere wird vom Betriebssystem oft die <tt>XAUTHORITY</tt>-Variable nicht gesetzt, weswegen auch nach einem <tt>sudo -s</tt> die X-Window-Ausgabe nicht funktioniert, obwohl sie in der Umgebung des vorherigen Benutzers durchaus funktioniert hat. Man muß daher leider die <tt>XAUTHORITY</tt>-Variable manuell setzen
<pre>
> export XAUTHORITY=$HOME/.Xauthority
> sudo -s
> xclock
</pre>
Will man jedoch eine Login-Shell, so muß man zusaetzlich noch die <tt>DISPLAY</tt>-Variable setzten und zwar auf den Wert den sie fuer den Benutzer <tt>[username]</tt> hatte von dem aus man <tt>sudo</tt> aufgerufen hat
<pre>
> echo $DISPLAY
localhost:11.0
> echo $HOME
/home/[username]
> sudo -i
> export DISPLAY=localhost:11.0
> export XAUTHORITY=/home/[username]/.Xauthority
> xclock
</pre>
</li>

<li><em>Daemonen (Dienste) unter Suse Linux neustarten:</em><br />
Manchmal hilft ein Neustart eines Hintergrundprozesses (auch Daemon,
bzw. Dienst genannt) um die seltsamsten Probleme zu lösen.
Den SSH-Server z.B startet man unter Suse 9.3 mit der Kommandozeile
<pre>
> rcsshd restart
</pre>
neu.</li>

<li><em id="mac">Eigene MAC Adresse herausfinden:</em>
<pre>
> sudo /sbin/ifconfig
eth0      Link encap:Ethernet  HWaddr [MAC-Adresse]
...
</pre> 
wobei <tt>[MAC-Adresse]</tt> die gesuchte MAC-Adresse der ersten eingebauten Netzwerkkarte ist. 
Braucht man die WLAN MAC-Adresse steht diese oft unter Punkt <tt>eth1</tt>.
</li>

<li><em>Herausfinden, welche Computer online in einem Subnetz sind:</em>
<pre>
> nmap -sP 123.123.123.*
</pre>
Wird derselbe Befehl nicht als root aufgerufen, findet <tt>nmap</tt>
eventuell nicht alle Computer.</li>

<li><em>Herausfinden, welches Betriebssystem hinter einer bestimmten IP-Nummer steckt:</em>
<pre>
> nmap -O 123.123.123.*
</pre></li>

<li><em><a id="lsof">Herausfinden, welcher Benutzer und welcher Prozess auf Dateien in einem Verzeichnis zugreift:</a></em>
<pre>
> lsof /pfad/verzeichnis
</pre>
<tt>lsof</tt> steht dabei für "list open files" 
(siehe auch <a href="http://www.uwsg.iu.edu/UAU/advcomm/lsof.html">UnixforAdvancedUsers</a>).</li>

<li><em>Alle Dateien eines bestimmten Benutzers finden:</em>
<pre>
> sudo find / -user [user]
</pre>
<p>Der Befehl funktioniert natürlich nur, wenn der Benutzer <tt>[user]</tt> existiert. Mehr Infos gibts
bei <a href="http://www.cyberciti.biz/faq/how-do-i-find-all-the-files-owned-by-a-particular-user-or-group/">
www.cyberciti.biz</a>.</p></li>

<li><em>Eine Datei schreibschützen (so dass selbst <tt>root</tt> die Datei nicht verändern kann):</em>
<pre>
> chattr +i [readonly]
</pre>
<p>
Mit diesem Befehl kann man sicherstellen, dass die Datei <tt>[readonly]</tt> niemals überschrieben werden kann,
auch nicht von <tt>root</tt> selbst. Allerdings kann man als <tt>root</tt> den Schutz 
natürlich wieder entfernen. Das ist nützlich, um sicherzustellen, dass bestimmte Dateien 
(z.B. <tt>/etc/passwd</tt> und andere Systemdateien) auch bei Systemupdates nicht überschrieben werden 
können. Das ganze funktioniert wohl nur auf ext2/3/4 Dateisystemen. Da der Befehl relativ wenig bekannt ist
wird er auch von einigen RootKits benutzt um das Beseitigen des RootKits zu erschweren. Mehr Infos über den Befehl
gibts bei <a href="http://linuxhelp.blogspot.com/2005/11/make-your-files-immutable-which-even.html">
linuxhelp.blogspot.com</a>.</p></li>

<li><em>Bildschirmsperre (mit Passwort) abschalten:</em><br />
Manchmal kommt es vor, dass die Bildschirmsperre unter KDE abstürzt oder
man das Passwort nicht mehr richtig eingeben kann. Dies passiert z.B. wenn 
man unter Suse 9.3 und KDE ein Passwort mit lateinischen Zeichen hat, 
jedoch auf russische Tastaturbelegung umgeschaltet hat kurz bevor die
Bildschirmsperre kommt. Da man dann die Tastaturbelegung nicht mehr 
ändern kann (siehe dazu auch <a href="http://bugs.kde.org/show_bug.cgi?id=102149">bugs.kde.org</a>), 
kann man das Passwort mit den lateinischen Buchstaben nicht 
mehr eingeben und sich auch nicht mehr einloggen. Einzige Möglichkeit ist 
dann noch die Deaktivierung der Bildschirmsperre als <tt>root</tt>.
Eingeloggt als <tt>root</tt> findet man die Bildschrimsperre mit
<pre>
> ps aux | grep kdesktop_lock
pechvogel 14161 0.0 0.1 2700 704 pts/11 S 14:35
</pre>
Mittels
<pre>
> kill 14161
</pre>
kann man jetzt die Bildschirmsperre für den Benutzer <tt>pechvogel</tt>
"abschießen", so dass derjenige wieder mit seiner noch laufenden
"Session" weiterarbeiten kann.</li>

<li><em>Computer über Terminalkommando herunterfahren:</em><br />
Will man das System <em>sofort</em> herunterfahren, so kann man dass
mittels
<pre>
> sux
> halt </pre>
oder
<pre>
> poweroff</pre>
erreichen. Der Befehl <tt>halt</tt> ist dabei die Abkürzung für
<tt>shutdown -h now</tt> und <tt>poweroff</tt> steht für
<tt>halt -p</tt>. Wenn man es weniger eilig hat, kann man das System
z.B. in 2 Minuten mit dem Befehl
<pre>> shutdown -h +2</pre>
herunterfahren. Will man nur neustarten benutzt man am besten
<pre>
> reboot
</pre>
which is an alias for <tt>shutdown -r now</tt>.

</li>

<li><em>System an einem bestimmmten Tag herunterfahren:</em><br />
Mit dem Befehl <tt>shutdown</tt> allein ist es nicht möglich, den
Computer an einem bestimmten Datum herunterzufahren, da
<tt>shutdown</tt> nur Uhrzeitangaben, jedoch keine Datumsangaben
(Tage, Monate, Jahre...) erlaubt. Daher muß man <tt>at</tt> benutzen,
z.B.:
<pre>
> sux
> at 05:00 30.08.05
at> halt
at> [[Ctrl]]-[[d]]
>
</pre>
Dieser Befehl (<tt>[[Ctrl]]-[[d]]</tt> steht dabei für die abschließende Tastenkombination
<tt>Ctrl-d</tt> ) fährt das System am 30.08.2005 um 5 Uhr früh herunter.
Eventuelle Ausgaben werden als Mail an <tt>root@computername.domainname</tt> geschickt.
</li>

<li><em>Scratch-Partition einrichten:</em><br />
Um allen Benutzern auf einem Computer die Möglichkeit zu geben temporär
Daten auf dem lokalen Computer abzulegen, ist es üblich sogenannte
Scratch-Partitionen (oder ein Scratch-Verzeichnis) anzulegen. Um ein
Scratch-Verzeichnis anzulegen kann man z.B. folgendermaßen vorgehen:
<pre>
> sux
> cd /
> mkdir scratch
> chmod a+rwx scratch
</pre>
Der letze Befehl gibt dabei allen Benutzern Lese- und Schreibrechte.
Das Executable-Bit <tt>x</tt> zusätzlich ist wichtig, damit auch alle
Benutzer in das Verzeichnis mittels <tt>cd</tt> wechseln können.</li>

<li><em>Windows-Partition unter Linux mounten:</em>
<pre>> mount /dev/hdc1 /mnt -t vfat -o umask=000, exec </pre>
Dabei steht <tt>vfat</tt> für das Dateisystem FAT32, <tt>umask=000</tt> gibt allen Benutzern 
Lese- und Schreibrechte und <tt>exec</tt> erlaubt das Ausführen von Programmen
von dem gemounteten Dateisystem. Soll das Laufwerk immer beim booten gemountet werden,
sieht ein entsprechender Eintrag in die Datei <tt>/etc/fstab</tt> folgendermaßen aus:
<pre>
/dev/sda7  /windows/E  vfat  users,gid=users, umask=0000,exec,utf8=true  0  0
</pre>
Erläuterung zum umask-code:<br />
Die erste 0 zeigt einfach an, dass eine Octal-Zahl folgt, die zweite Zahl steht für die Rechte
des <tt>user</tt>, die dritte für die rechte der <tt>group</tt> und die vierte für <tt>others</tt>.
Die Kodierung ist dabei folgendermaßen:
keine Leserechte <tt>r</tt>=4, keine Schreibrechte <tt>w</tt>=2 und keine Ausführbarkeit <tt>x</tt>=1,
sodass z.B. alle Rechte für <tt>others</tt> ausgeschlossen sind, wenn die entsprechende Zahl 4+2+1=7 ist. 
Alle möglichen Kombinationen entnehme man folgender Tabelle:
<table border="1" style="margin:auto;">
<tr><td> 0 </td><td> 1 </td><td> 2 </td><td> 3 </td><td> 4 </td><td> 5 </td><td> 6 </td><td> 7 </td></tr>
<tr><td>rwx</td><td>rw-</td><td>r-x</td><td>r--</td><td>-wx</td><td>-w-</td><td>--x</td><td>---</td></tr>
</table>
Mehr dazu findet man auch auf
<a href="http://gentoo-wiki.com/HOWTO_Mount_Windows_partitions_(DOS,_FAT,NTFS)#uid.2Cgid:_mount_as_.28user.2Cgroup.29">
gentoo-wiki.com
</a> und <a href="http://de.opensuse.org/SDB%3ADOS_Mount%2C_Schreibrechte_f%C3%BCr_alle">de.opensuse.org</a>.
</li>

<li><em>USB-Disk unter Linux als FAT32 formatieren:</em><br />
Als root oder Superuser eingeben (siehe auch <a href="http://www.linux-club.de/viewtopic.php?t=59075">www.linuxclub.de</a>):
<pre>> mkfs.vfat -F 32 /dev/[laufwerk]</pre>
oder
<pre>> mkdosfs -F 32 /dev/[laufwerk]</pre>
Das Laufwerk bekommt man unter KDE auf Suse Linux heraus, indem man das Icon des USB-Sticks auf dem Desktop
rechtsklickt und im Menü->Eigenschaften wählt.</li>

<li><em>Disketten formatieren unter Linux:</em><br />
Falls man an einem Computer sitzt der noch ein Diskettenlaufwerk besitzt
<pre>> mformat a:</pre>
Dies formatiert eine Diskette mit dem DOS-FAT Dateisystem. Für weitere Informationen siehe
<a href="http://de.opensuse.org/SDB:Disketten_formatieren_unter_Linux">SDB:Disketten formatieren unter Linux</a>.</li>

<li><em>Unterschied zwischen <tt>user</tt> und <tt>users</tt> beim mounten:</em><br />
Es besteht ein subtiler (und in den <tt>man</tt>-Pages schlecht erklärter) Unterschied
zwischen den Optionen <tt>user</tt> und <tt>users</tt>, die man beim mounten von Laufwerken
angeben kann:<br />
Die Option <tt>user</tt> erlaubt es, dass jeder Benutzer ein Laufwerk mounten darf; aber nur der
Benutzer, welcher das Laufwerk gemountet hat, darf es auch wieder unmounten. Die Option
<tt>users</tt> erlaubt es hingegen, dass jeder Benutzer, egal ob er das Laufwerk gemountet hat
oder nicht, dieses wieder unmounten darf.</li>

<li><em>Detaillierte <tt>Yast2</tt>-Fehlermeldungen lesen:</em><br />
Sämtliche Fehler, die bei der Benutzung von <tt>Yast2</tt> auftreten, werden detailliert
im Yast2-Logfile mitprotokolliert. Lesen kann man dieses unter Suse Linux mit
<pre>
> less /var/log/Yast2/y2log
</pre></li>

<li><em>NIS-User mit <tt>Yast2</tt> verwalten</em><br />
Unter Suse kann man über <tt>Yast2</tt> nicht nur die lokalen Benutzer, sondern auf dem NIS-Server
auch die NIS-Benutzer verwalten. Dazu muß ein NIS-Server konfiguriert und gestartet sein.
Jedoch erkennt das Benutzerverwaltungsmodul von <tt>Yast2</tt> nicht immer, wenn ein NIS-Server
läuft, so dass es die Verwaltung der NIS-Benutzer nicht erlaubt. Einzige Abhilfe in diesem Fall ist
mittels
<pre>
> /usr/lib/yp/ypinit -m
</pre>
im Verzeichnis <tt>/var/yp</tt> den Server manuell neu zu initialisieren. Erst danach erkennt 
<tt>Yast2</tt> wieder, dass ein NIS-Server läuft und erlaubt die NIS-Benutzerverwaltung.
</li>

<li><em>RPM-Pakete von Kommandozeile über Yast2 installieren:</em><br />
Obwohl es zunächst unsinnig klingen mag, ist es manchmal von Vorteil
<pre>> kdesu /opt/kde3/share/apps/krpmview/setup_temp_source *.rpm</pre>
Dies entspricht der Aktion "Mit Yast installieren", welche man per Rechtsklick auf ein 
RPM im Kontextmenü des Konqueror findet. Es funktioniert auch mit mehreren RPMs.</li> 

<li><em>RPM-Pakete von Kommandozeile ohne Yast2 installieren:</em>
<pre>
> rpm -Uhv [paketname].rpm
</pre>
Die Option <tt>-U</tt> steht dabei für Upgrade, welches nach der Installation alle älteren 
installierten Versionen von <tt>[paketname]</tt> entfernt. <tt>-h</tt> steht für "hash marks",
welches zur Fortschrittsanzeige beim Installieren 50 "hash marks" anzeigt. Die Option <tt>-v</tt>
steht für "verbose" und sorgt u.a. dafür, dass die "hash marks" etwas schöner angezeigt werden.
</li>
<li><em>Herausfinden, welche Version eines Pakets installiert ist:</em>
<pre>
> rpm -q [paketname] 
</pre>
<li><em>Herausfinden, wohin die Dateien eines Pakets installiert werden:</em>
<pre>
> rpm -q -l [paketname] 
</pre>
</li>

</ul>

<h6>Kopieren für Fortgeschrittene</h6>
<p>Wer jemals ein komplettes Home-Verzeichnis für z.B. Backup-Zwecke mittels <tt>cp -R </tt> kopiert hat,
wird erstaunt feststellen, dass nicht alle Dateien kopiert wurden und auch die Rechte der Dateien 
eventuell nicht den ursprünglichen Rechten entsprechen. Ein ziemliches Desaster, wenn man diese Kopie
für Backup-Zwecke verwenden wollte. Die Lösung dafür ist</p>
<pre>
> sudo cp -a -T source dest
</pre>
<p>Die Option <tt>-a</tt> ist equivalent zu <tt>-r -p -d</tt>, kopiert also rekursiv, erhält dabei die Rechte
und erhält auch Links. Die Option <tt>-T</tt> behandelt das Ziel <tt>dest</tt> wie eine Datei, d.h. falls
<tt>dest</tt> noch nicht existiert, wird es angelegt (mehr zu dieser Option unter
<a href="http://www.gnu.org/software/coreutils/manual/html_node/Target-directory.html#Target-directory">
http://www.gnu.org/software/coreutils</a>)
. Eine vergleichbare Lösung ist (siehe
<a href="http://superuser.com/questions/26586/copy-directory-contents-using-cp-command">superuser.com</a>):</p>
<pre>
> sudo cp -a source/. dest
</pre>
<p>Für den Fall, dass man auf einem sehr alten Unix-System arbeitet, das vielleicht nicht alle genannten 
<tt>cp</tt>-Optionen unterstützt, gibt es auch noch die Möglichkeit das Quellverzeichnis in eine <tt>tar</tt>-Datei
zu packen und am Zielort wieder zu entpacken (das ganze funktioniert auch über <tt>ssh</tt>), siehe
<a href="http://www.tech-recipes.com/rx/513/copy-entire-contents-of-a-directory-and-preserve-permissions/">
www.tech-recipes.com</a>. Will man nur versteckte Dateien (<tt>.*</tt>) kopieren, stößt man mit dem
Standardpatternmatching an Grenzen, denn <tt>.*</tt> gilt auch für <tt>..</tt>. Auch dabei kann <tt>tar</tt> helfen,
siehe <a href="http://serverfault.com/questions/3154/recursively-copying-hidden-files-linux">serverfault.com</a>.
</p>

<h6>Netzwerkinterface unter Suse/Ubuntu konfigurieren</h6>
<p>Unter Suse konfiguriert man Netzwerkarten usw. am besten über Yast2. Will man
dennoch über die Kommandozeile arbeiten wird man feststellen, dass die unter Debian/Ubuntu
verbreitete Konfigurationsdatei <tt>/etc/network/interfaces</tt> unter Suse nicht existiert
(siehe <a href="http://lilypond.org/blog/janneke/openSUSE-HOWTO">openSUSE-HOWTO</a>)
. Unter Suse wird für jedes 
Netzwerkinterface eine eigene Datei der Form <tt>ifcfg-*</tt> unter <tt>/etc/sysconfig/network/</tt> angelegt.
Informationen über das Format dieser Datei gibt es mit <tt>man ifcfg</tt> und z.B. bei 
<a href="http://www.fibel.org/linux/lfo-0.6.0/node478.html">www.fibel.org</a>. Wie man unter Ubuntu eine Netzwerkarte
einrichtet wird bei 
<a href="https://help.ubuntu.com/9.04/serverguide/C/network-configuration.html">Ubuntu Server Guide</a> und in den
<a href="http://manpages.ubuntu.com/manpages/jaunty/en/man5/interfaces.5.html">Ubuntu ManPages</a>
erklärt. Für eine Netzwerkarte mit dynamischer IP-Adresse schreibt man in <tt>/etc/network/interfaces</tt>:</p>
<pre>
auto eth0
iface eth0 inet dhc
</pre>
<p>Für eine Netzwerkarte mit statischer IP-Adresse z.B.:</p>
<pre>
auto eth0
iface eth0 inet static
address 123.456.10.225
netmask 255.255.255.0
gateway 123.456.10.254
</pre>

<h6>Init-Skripte für Suse Linux schreiben</h6>
<p>Init-Skript sind bash-Skripten, die benutzt werden sollten um einen Hintergrund-Dienst (Dämon,Service) 
zu kontrollieren (starten, stoppen,neustarten). Sie werden auch vom Betriebsystem genutzt um einen Dienst
beim Start des System automatisch zu starten. Normalerweise werden sie in <tt>/etc/init.d</tt> als 
ausführbare Dateien ohne Suffix (z.B. <tt>/etc/init.d/sshd</tt>) gespeichert.
Mit Suse wird ein Beispiel-Init-Skript mitgeliefert, das als Ausgangspunkt für eigene Init-Skripte dienen
kann. Es liegt unter</p>
<pre>
/etc/init.d/skeleton
</pre>
<p>Eine ausführliche Anleitung zum Erstellen eigener Init-Skripten findet man bei
<a href="http://developer.novell.com/wiki/index.php/Writing_Init_Scripts">Novell Developer - Writing_Init_Scripts</a>.
Mit</p> 
<pre>
> sudo /sbin/chkconfig -a newservice
</pre>
<p>kann man einen Dienst beim Betriebssystem registrien, so dass er automatisch gestartet wird. In welchen Runlevels
er gestartet wird, wird im Init-Skript definiert. Eine Übersicht über alle Dienste bekommt man mit</p>
<pre>
> sudo /sbin/chkconfig -l
</pre>
<p>Mehr über <tt>chkconfig</tt> steht bei 
<a href="http://www.easylinux.de/Artikel/ausgabe/2007/01/126-chkconfig/">easyLinux - Mit den Dienern reden</a>.
</p>

<h6>Umgang mit ISO-Images unter Linux</h6>
<p>Ein ISO-Image einfach zu dekomprimieren wie unter Windows scheint unter Linux nicht möglich zu sein.
Stattdessen muss man als root(!)-User das Image als virtuelles Laufwerk mounten</p>
<pre>
> mkdir /mnt/iso
> mount -r -t iso9660 -o loop Datei.iso /mnt/iso
</pre>
<p>Dabei bedeutet <tt>-r</tt>, dass von diesem Laufwerk nur gelesen werden kann und die Angabe 
<tt>-t iso9660</tt> spezifiziert das genaue Dateisystem, kann aber oft auch weggelassen werden.</p>
<p>Jetzt kann man auch als normaler Benutzer das Iso-Image Verzeichnis z.B. ins aktuelle Verzeichnis kopieren</p>
<pre>
> cp -v -r /mnt/iso .
</pre>
<p>Jetzt hat man die Daten vom aktuellen Verzeichnis ausgehend im Unterverzeichnis <tt>iso</tt>.
Von dort aus kann man die Daten weiterverarbeiten oder auch das <tt>iso</tt>-Verzeichnis anders komprimieren.
Allerdings kann man das kopierte Verzeichnis <tt>iso</tt> nicht unmittelbar löschen, da es von einer
(virtuellen) CD kopiert wurde und die Rechte noch einer nichtbeschreibbaren CD entsprechen. Daher muss man erst
mit</p>
<pre>
> chmod -R a+w iso
</pre>
<p>die Rechte entsprechend anpassen, dann kann man das Verzeichnis wieder löschen mit</p>
<pre>
> rm -r iso
</pre>
<p>Um das ISO-Image wieder zu unmounten muss man als root eingeben</p>
<pre>
> umount /mnt/iso
> rm -r /mnt/iso
</pre>
<p>Kommt bei <tt>umount</tt> der Fehler</p>
<pre>umount: /mnt/iso: device is busy</pre>
<p> so muss man sicherstellen, dass kein anderer Benutzer oder Programm gerade auf das Laufwerk
zugreift (z.B. ein Terminal-Fenster, welches gerade auf <tt>/mnt/iso</tt> verweist). Dies kann man mit dem 
<tt>lsof</tt>-Kommando (siehe <a href="#lsof">oben</a>) überprüfen.</p>
<p>Aber eine Frage nach dieser ganzen Prozedur bleibt: Warum nur kann man ein ISO-Image unter Linux nicht einfach 
wie ein Archiv als normaler Benutzer entpacken? Aber das wäre wahrscheinlich zu einfach.</p>

<h6>NFS-Server unter Suse Linux 9.3 einrichten</h6>
<p>Ein Network File System (NFS) Server einzurichten ist unter Suse 9.3 nicht schwer.
Jedoch kann es einige Probleme mit der Suse Firewall geben die einen viel Zeit kosten
können, daher hier diese Kurzanleitung zur NFS-Server-Installation:</p>
<ol>
<li>Yast2 aufrufen und unter Network Services das NFS-Server-Modul aufrufen.</li>
<li>Den NFS-Server durch anklicken von <tt>Start NFS-Server</tt> aktivieren und
<tt>Open Port in Firewall</tt> auswählen. Ansonsten funktioniert später garnichts.
Dann weiter zum nächsten Dialog gehen.</li>
<li>Im nächsten Dialog muß man nun durch Auswahl von <tt>Add directory</tt> das
per NFS zu verteilende Verzeichnis angeben. Im darauffolgenden Eingabefenster
kann man als <tt>Host wildcard</tt> <tt>*</tt> übernehmen, aber damit erlaubt
man wirklich jedem, dass NFS-Laufwerk zu mounten. Es ist sicherer dies z.B. nur
für Rechner des eigenen Subnetzes zu erlauben. Man sollte daher für 
<tt>Host wildcard</tt> z.B.
<pre>
192.168.0.0/255.255.255.0
</pre>
eintragen. Als Optionen sollte man
<pre>
ro,root_squash,async
</pre>
setzen. Die Option <tt>ro</tt> erlaubt dabei nur lesenden Zugriff auf
das freigegebene Verzeichnis, <tt>root_squash</tt> (wörtl. "Wurzel zerquetschen")
verhindert, dass jemand mit Rootrechten auf einem fremden Rechner, der das NFS-Laufwerk
eingebunden hat, diese Rootrechte auch auf dem NFS-Laufwerk hat und <tt>async</tt>
erlaubt einen schnelleren Zugriff und Datentransfer (ist allerdings etwas
anfälliger für Fehler als <tt>sync</tt>).</li>
<li>Durch Anklicken von <tt>Finish</tt> wird der NFS-Server gestartet.</li>
</ol>
<p>Die Clientrechner sollten nun in der Lage sein, dass freigegebene Verzeichnis zu
sehen und einzubinden. Oft ist dies jedoch noch nicht der Fall.
Dann sollte man zunächst mit Rootrechten vom Client aus überprüfen, ob der Portmapper Daemon auf 
dem Server läuft:</p>
<pre>
> rpcinfo -p servername
</pre>
Dieser Befehl sollte eigentlich eine Liste anzeigen, die so ähnlich
aussieht:
<pre>
program vers proto   port
...
100003    2   udp   2049  nfs
100003    3   udp   2049  nfs
100003    2   tcp   2049  nfs
100003    3   tcp   2049  nfs
...
</pre>
Passiert jedoch garnichts, so handelt es sich um ein Problem mit der
Firewall auf dem Server. Vermutlich wurde <tt>Open Port in Firewall</tt>
vergessen auszuwählen. Wenn stattdessen die Fehlermeldung
<pre>
RPC: Program not registered
</pre>
erscheint, so sollte man die Dateien <tt>/etc/hosts.allow</tt> bzw.
<tt>/etc/hosts.deny</tt> überprüfen. In <tt>/etc/hosts.allow</tt>
sollte man folgende Dienste erlauben, falls man
ansonsten in <tt>/etc/hosts.deny</tt> alle Dienste erst einmal 
generell verboten hat:
<pre>
portmap: 192.168.0.0/255.255.255.0 :ALLOW
mountd: 192.168.0.0/255.255.255.0 :ALLOW
lockd: 192.168.0.0/255.255.255.0 :ALLOW
rquotad: 192.168.0.0/255.255.255.0 :ALLOW
statd: 192.168.0.0/255.255.255.0 :ALLOW
</pre>
<p>Mehr dazu findet man auch in der 
<a href="http://www.faqs.org/docs/Linux-HOWTO/NFS-HOWTO.html">Linux-NFS-HOWTO</a>

Funktioniert der <tt>rpcinfo</tt>-Befehl jedoch ohne Probleme und
der Clientrechner findet die Freigaben immer noch nicht, so hilft es häufig
die Suse Firewall auf dem Server ab- und dann wieder anzuschalten. Dann funktioniert
seltsamerweise oft alles wieder wie es soll. <br />
Mehr zum Thema NFS findet man abgesehen vom oben erwähnten 
Linux-NFS-HOWTO auch auf deutsch unter <a href="http://linuxwiki.de/NFS">linuxwiki.de</a>.</p>

<h6>Subversion (SVN) einrichten</h6>
<p>Das Versionskontrollsystem Subversion (SVN) einzurichten lohnt sich nicht nur für Gruppen von Entwicklern
sondern auch für den einzelnen Programmierer, denn mit SVN hat man praktisch eine Zeitmaschine (wie es die
SVN Entwickler selbst ausdrücken), die es einem erlaubt sämtliche(!) Änderungen (d.h. auch das Überschreiben
und Umbenennen von Dateien und Verzeichnissen u.ä.) an einem Projekt transparent zu verfolgen und gegebenenfalls
rückgängig zu machen. Wäre jedes Filesystem ein Versionskontrollsystem gäbe es nie mehr Datenverlust durch das 
unbeabsichtigte Überschreiben von Dateien, vor dem auch Techniken wie die Verwendung von "Trashcans" in
modernen Betreibsystemen nicht schützen. Aber es soll hier nicht diskutiert werden, warum es sowas nützliches wieder
nicht gibt, sondern die Installation von SVN dargestellt werden. <br />
Die Installation von SVN ist im Prinzip in der ausführliche offiziellen 
<a href="http://svnbook.red-bean.com/">Onlineanleitung</a> zu SVN beschrieben. Jedoch liegt der Schwerpunkt
eher auf der Installation im Zusammenhang mit dem WebDAV-Module für Apache. Will man jedoch nicht extra
Apache laufen lassen und stattdessen SVN einfach über SSH bedienen sind einige Fallstricke bezüglich
Benutzerrechten zu umschiffen. Dies wird recht übersichtlich bei 
<a href="http://www.linux-fuer-alle.de/doc_show.php?docid=230&amp;catid=3">Linux-fuer-alle</a> erklärt
und soll hier nochmal zusammengefasst und ergänzt werden:</p>
<ol>
<li>Zunächst muß man Subversion auf dem Server installieren, auf dem man das Repository
(die Ablage für die Dateien, die versionskontrolliert werden sollen) anlegen möchte. 
Dies macht man am besten mit <tt>Yast2</tt>.</li>
<li>Dann sollte man eine neue Benutzergruppe (Name z.B. <tt>svn</tt>) im System anlegen.
Alle Benutzer, die später Subversion verwenden wollen, müssen Mitglieder dieser Gruppe werden.
Am einfachsten erledigt man das wieder mit <tt>Yast2</tt> indem man unter "Security and Users" 
das Module "Edit and create groups" aufruft (Ob man das "lokal" auf dem Rechner macht, auf dem
das Repository liegt, oder "global" auf dem eventuell vorhandenen NIS-Server ist eigentlich egal,
aber mit einer globalen Gruppe ist es später leichter, das Repository auf einen anderen Rechner
zu verschieben). Nach Aufruf von "Add" (eventuell sollte man vorher unter "Set Filter"
"NIS Groups" oder "System Groups" auswählen, damit man später auch die "globalen" Benutzer sieht)
gibt man "Group Name" und "Group ID" (diese sollte > 500 sein, andernfalls gibts Probleme) und
wählt die zugehörigen Mitglieder aus. Danach kann man das ganze durch Drücken von "Accept" und "Finish"
abschließen.</li>
<li>Damit sich die verschiedenen Benutzer nicht gegenseitig aussperren, weil die gesendeten
Dateien die falschen Benutzungsrechte haben, muß man auf dem Repository-Server den
Befehl <tt>/usr/bin/svnserve</tt> durch ein Wrapper-Skript ersetzen, welches automatisch
die richtigen Rechte für alle empfangenen Dateien setzt. Dazu sollte man den
Orginalbefehl umbenennen:
<pre>
> mv svnserve svnserv
</pre>
und stattdessen folgendes Skript anlegen:
<pre>
> pico svnserve
#!/bin/bash
umask 002            #Everything is allowed for user and the group,
                     #nothing is allowed for others.
/usr/bin/svnserv $*
</pre>
Nicht vergessen, dass Skript für alle ausführbar zu machen:
<pre>
> chmod a+x svnserve
</pre></li>
<li>Jetzt muß man das Repository anlegen, z.B. kann man mit Rootrechten ein neues Verzeichnis im
Wurzelverzeichnis des Repository-Servers anlegen:
<pre>
> cd /
> mkdir subversion
</pre>
Will man erlauben, dass auch Benutzer der Gruppe <tt>svn</tt> neue Repositories innerhalb des Verzeichnises
<tt>subversion</tt> anlegen können, so muß man noch die Gruppenzugehörigkeit und die Schreibrechte dieses 
Verzeichnisses anpassen:
<pre>
> chown root.svn subversion/
> chmod g+w subversion/
</pre>
Hat man den letzten Schritt getan, kann man die folgenden mit einem Benutzer aus der Gruppe <tt>svn</tt>
durchfuehren, ansonsten muß man weiter mit Root-Rechten arbeiten.
<pre>
> cd subversion
> mkdir projektname
</pre>
Das Unterverzeichnis <tt>projektname</tt> ist nur zur Übersicht, da man sicher mehr als nur
ein Projekt mit Subversion verwalten möchte. Dieses Unterverzeichnis muß man nun zu einem
Repository erklären (subversion legt dazu dort einige Unterverzeichnisse und Dateien an):
<pre>
> svnadmin create --fs-type fsfs projektname
</pre>
Die Option <tt>--fs-type fsfs</tt> stellt dabei sicher, dass Subversion als Speichersystem
einfach das Filesystem verwendet und nicht die veraltete Berkley Database (DB), die eigentlich
nur Nachteile hat (siehe 
<a href="http://svnbook.red-bean.com/nightly/en/svn.reposadmin.html#svn.reposadmin.basics.backends">
Repository Administration</a> im Online Manual). Ich wundere mich, warum sie immer
noch in der Defaulteinstellung verwendet wird.</li>
<li>Nun muß man die Zugriffsrechte auf das Repository so anpassen, dass später alle
Mitglieder der angelegten Gruppe <tt>svn</tt> Zugriff darauf haben:
<pre>
> chgrp -R svn projektname
</pre>
Alle anderen haben im Repository nichts verloren:
<pre>
> chmod -R o-rwx projektname
</pre>
Die Gruppenmitglieder sollen natürlich auch schreiben dürfen:
<pre>
> chmod -R g+rw projektname
</pre>
Um sicherzustellen, dass die Logfiles, welche Subversion anlegt auch problemlos geschrieben
werden können ist noch folgende Rechteänderung nötig:
<pre>
> chmod g+s projektname/db
</pre></li>
<li>Nun muss man nur noch die Konfiguration des Repositories etwas anpassen.
Dazu sollte man in der Datei <tt>/subversion/projektname/conf/svnserve.conf</tt>
folgendes eintragen:
<pre>
[general]            #Diese Zeile darf nicht weggelassen werden.
anon-access = none
auth-access = write
realm = projektname
</pre></li>
<li>Falls noch nicht geschehen kann man jetzt Subversion mit <tt>Yast2</tt>
auch auf den Clientrechnern installieren. Von einem Clientrechner aus kann
man jetzt, wenn man zur Benutzergruppe <tt>svn</tt> gehört, das Repository
mit Daten füllen:
<pre>
svn import dirname svn+ssh://[svnserver]/subversion/projektname/dirname -m "Original Version"
</pre>
Dabei steht <tt>dirname</tt> z.B. für das Verzeichnis in dem das Projekt
(inklusive Sourcecode, Makefiles, Bilder, Readme usw., Subversion verwaltet alles!)
bisher auf dem Clientrechner lag. <tt>[svnserver]</tt> steht für die Adresse
des Servers, auf dem das Repository eingerichtet wurde und mit
der Option <tt>-m</tt> hat man die Möglichkeit kurze Notizen zu dem
gerade eingerichtet Projekt zu geben.
Noch ein Tipp zum Schluß: Falls aus unerfindlichen Gründen beim Datenimport
plötzlich <tt>vim</tt> startet, so kann man diesen mit Eingabe von
<tt>:quit[[Enter]]</tt> beenden. Die darauf folgende Frage muß man dann mit
<tt>c(ontinue)</tt> beantworten. Dann startet der Datenimport aber wirklich.
</li>
</ol>