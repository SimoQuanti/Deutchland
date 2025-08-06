# Deutschland

Deutschland è un semplice videogioco per imparare il tedesco che gira su PC (Windows, ma anche su altri sistemi dotati di Python 3). L’obiettivo è rendere più interattivo lo studio della lingua tedesca attraverso esercizi con punteggio, progressivi e personalizzati. Questo gioco parte dal lessico del settore magazzino e introduce gradualmente nuove parole e nozioni grammaticali, tra cui gli articoli determinativi/indeterminativi, le forme plurali e il verbo **sein** (essere).

## Funzionalità principali

- **Livelli progressivi:** ogni livello introduce un piccolo gruppo di vocaboli nuovi. Per superare un livello occorre ottenere almeno l’80 % di risposte corrette. Quando si supera il livello vengono sbloccate nuove parole e concetti grammaticali.
- **Spiegazioni:** ogni vocabolo nuovo è accompagnato dalla sua traduzione italiana, dall’articolo determinativo corretto, dal plurale e da una breve spiegazione. Le regole grammaticali sono spiegate in italiano con esempi.
- **Esercizi a scelta multipla:** le domande propongono traduzioni italiane o forme singolari/plurali e richiedono di scegliere la risposta tedesca corretta. Dopo ogni domanda viene fornito un feedback immediato con la risposta giusta e una spiegazione.
- **Sezione di ripasso giornaliero:** una volta al giorno puoi avviare una sessione di ripasso che pesca casualmente i vocaboli e le regole già studiate nei giorni precedenti. Questo ti aiuta a mantenere la memoria attiva anche mentre continui ad avanzare nei livelli.
- **Salvataggio del progresso:** i tuoi progressi (livello raggiunto, punteggio, parole apprese e data dell’ultimo ripasso) vengono salvati automaticamente in un file JSON (`progress.json`) all’interno della cartella del gioco.

## Requisiti

- **Python 3.8 o superiore** installato sul sistema. Non sono necessarie librerie esterne: il gioco utilizza solo la libreria standard e viene eseguito interamente nel terminale.

## Avvio del gioco

1. Apri un terminale e spostati nella cartella del progetto:

   ```
   cd src
   ```

2. Avvia il gioco con:

   ```
   python3 game.py
   ```

Sul primo avvio verrà creato un file `progress.json` con il tuo progresso iniziale. Se desideri ricominciare da capo puoi cancellare manualmente questo file.

## Struttura del codice

- `game.py` contiene l’implementazione principale del gioco (logica degli esercizi, gestione dei livelli, interfaccia a riga di comando e salvataggio del progresso).
- `data.py` definisce le liste di vocaboli e di argomenti grammaticali utilizzati nei vari livelli. Ogni voce comprende singolare, plurale, articolo corretto, traduzione italiana ed eventuale spiegazione.
- `progress.json` viene creato automaticamente alla prima esecuzione per salvare stato e punteggi.

## Fonti

Alcune regole e forme usate nel gioco sono state verificate con risorse affidabili:

- Gli articoli determinativi dipendono dal genere del sostantivo: **der** per i nomi maschili, **die** per i femminili e **das** per i neutri. Al plurale si usa sempre **die**【579445628222420†L117-L134】.
- Le forme plurali e gli articoli dei vocaboli principali sono tratti da dizionari online, ad esempio **der Gabelstapler – die Gabelstapler**【59630982256329†L128-L184】, **das Lager – die Lager/Läger**【79702443002764†L129-L184】, **die Palette – die Paletten**【18485698920483†L128-L186】, **der Lagerarbeiter – die Lagerarbeiter**【144059179125449†L128-L180】, **das Regal – die Regale**【933059004205608†L18-L23】, **die Kiste – die Kisten**【912261064037591†L14-L22】, **das Paket – die Pakete**【724579430065651†L18-L22】, **die Waage – die Waagen**【8612395697889†L127-L134】 e **die Verpackung – die Verpackungen**【725387443235402†L128-L134】.
- Le principali regole per gli articoli sono descritte nel blog Lingoda, che spiega come **der**, **die** e **das** corrispondano rispettivamente ai generi maschile, femminile e neutro e che al plurale si usi **die**【579445628222420†L117-L134】. Il gioco include esercizi per riconoscere i generi e applicare correttamente l’articolo.
- Le coniugazioni del verbo **sein** al presente sono riportate su ThoughtCo: *ich bin* (io sono), *du bist* (tu sei), *er/sie/es ist* (egli/ella/esso è), *wir sind* (noi siamo), *ihr seid* (voi siete), *sie sind* (essi sono), *Sie sind* (Lei è)【583649228292794†L158-L174】.

## Licenza

Questo progetto è distribuito sotto la licenza MIT. Puoi usarlo, modificarlo e distribuirlo liberamente, ma senza alcuna garanzia.
