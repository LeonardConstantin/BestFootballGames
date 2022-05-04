# BestFootballGames
Dieses Tool zeigt dem User die "interessantesten" Fussballspiele eines eingegebenen Zeitraums.
Die benötigten Imports sind:
```
pip install requests
pip install reportlab
pip install Pillow
pip install svglib
pip install DateTime
```
Das Programm errechnet für jedes Spiel einen Relevanzwert. Dieser wird recht trivial aus dem Abstand der beiden Teams und dem Tabellenplatz der beiden Teams errechnet. 
Dabei wird wie folgt vorgegangen:
1. Im ersten Schritt werden die Spiele alle auf ihren jeweiligen Wochentag verteilt. Also Mon-Son
2. Im zweiten Schritt wird der Relevanzwert (Abstand der beiden spielenden Teams) errechnet. Auf Basis diesen Wertes werden die Spiele innerhalb des Wochentages sortiert. Dabei wird DESC sortiert. Die Idee hier ist, dass Teams die in der Tabelle nahe beieinander liegen, ein attraktiveres Spiel abliefern als Teams, welche weit aus einanderliegen.
3. Im dritten Schritt werden die Spiele mit gleichem Relevanzwert so sortiert, dass die Spiele mit dem höchsten Tabellenplatz oben stehen.
Die Idee hier ist, dass Teams auf hohen Tabellenplätzen einen attraktiveren Fußball spielen, als Teams auf niedrigen Tabellenplätzen. 

#Ausblick in die Zukunft:
In den "Algorithmus" sollen weitere Faktoren wie die Punktzahl, Derbys oder auch entschiedene Meisterschaften und Do-or-Die Spiele einfließen. Außerdem sollen die Spiele so angeordnet werden, dass eine Art Kalender entsteht, welcher einem alle Tage mit den interessantesten Spielen plant, so dass man einen Watchplan herunterladen / angezeigt bekommt. 

#Syntax:
Die 2 Inputfelder müssen zwingend mit dd.mm.yyyy eingegeben werden. Auch die Punkte sind wichtig. 
Der Code läuft für Zeitintervalle von **eins** bis **sieben** Tagen. Darüber hinaus ist der Code nicht getestet und könnte ungewollte "Feature" haben.
Auch gibt es keinen zurück Button. Das Programm muss Momentan immer neu gestartet werden.

**Da die API in der gratis Version nur 10 Anfragen pro Minute zulässt und mein Code 6 Anfragen in einem Durchlauf abfragt, kann man nur 1 mal pro Minute den Code ausführen**
Vorsicht, der Fehler wird momentan noch nicht abgefangen. 

Die Klasse APP handlet das Userinterface und die Darstellung der Ergebnisse. Der restliche Code besorgt und verarbeitet die Ergebnisse. Könnte in Zukunft in einer Klasse landen  
