# AI Content Describer per NVDA

Questo add-on permette di ottenere descrizioni dettagliate di immagini, controlli dell'interfaccia utente e altri contenuti visivamente inaccessibili.

Sfruttando le capacità multimodali di modelli di IA avanzati e di algoritmi di visione artificiale, puntiamo a fornire descrizioni dei contenuti della migliore qualità possibile e ad aumentare l'autonomia in generale. Per maggiori informazioni sui modelli utilizzati, consulta la sezione corrispondente di questo documento.

## Funzionalità

* Descrivere l'oggetto con il focus, l'oggetto del navigatore, l'intero schermo, oppure scattare una foto con la fotocamera integrata
* Descrivere qualsiasi immagine copiata negli appunti, che si tratti di un'immagine in un'email o di un percorso in Esplora file di Windows
* Copiare negli appunti un'immagine dell'oggetto con il focus, dell'oggetto del navigatore o dell'intero schermo, per incollarla in altre app
* Indicare se il volto dell'utente è posizionato al centro dell'inquadratura, tramite algoritmi di visione artificiale (non richiede un accesso API a pagamento)
* Usare i modelli supportati per controllare l'applicazione attiva con azioni del mouse e della tastiera, per attività che potrebbero essere inaccessibili
* Gratuito per impostazione predefinita, con la possibilità di aggiungere la propria chiave API per avere più modelli
* Supporta diversi provider (GPT di OpenAI e il livello gratuito di Pollinations, Gemini di Google, Mistral Large 4, Claude di Anthropic, Grok di xAI, Kimi di Moonshot AI, vivo BlueLM Vision tramite NVDA-CN, Datalab Chandra 2, Ollama, llama.cpp, LiteLLM Proxy e Seer)
* Supporta un'ampia varietà di formati, tra cui PNG (.png), JPEG (.jpeg e .jpg), WEBP (.webp) e GIF non animate (.gif)
* Memorizza facoltativamente le risposte nella cache per risparmiare la quota API
* Per un uso avanzato, è possibile personalizzare il prompt e il numero di token per adattare le informazioni alle proprie esigenze
* Fare domande di approfondimento e allegare altre immagini
* Rendering Markdown per accedere facilmente alle informazioni strutturate (basta attivare l'impostazione "Apri ogni risultato in una finestra navigabile" e aggiungere, ad esempio, "rispondi in Markdown" alla fine dei prompt)

## Casi d'uso

Questo progetto nasce da alcune motivazioni principali.

NVDA è in grado di eseguire il riconoscimento ottico dei caratteri (OCR) senza componenti aggiuntivi, e questo ha cambiato molte cose. Se devi estrarre il testo da un'immagine o da un documento PDF, è lo strumento che fa per te.

Tuttavia, l'OCR può analizzare solo i dati che *potrebbero* essere testo. Non riesce a considerare il contesto, gli oggetti e le relazioni rappresentati in quelle immagini. E Internet ne è pieno. Loghi, ritratti, meme, icone, grafici, diagrammi, grafici a barre o a linee... e chi più ne ha più ne metta. Sono ovunque, e di solito non in un formato che gli utenti di screen reader possano interpretare.
Fino a poco tempo fa, si dipendeva interamente dagli autori dei contenuti per le descrizioni con testo alternativo. Anche se restano indispensabili, è difficile negare che un alto livello di qualità sia l'eccezione e non la regola.

Ora le possibilità sono quasi infinite. Potresti:

* Visualizzare il desktop o una finestra specifica per capire la disposizione delle icone quando insegni ad altri
* Ottenere informazioni dettagliate sullo stato di giochi, macchine virtuali e così via quando l'audio è insufficiente o non disponibile
* Capire cosa mostra un grafico
* Decifrare screenshot o condivisioni dello schermo in Zoom o Microsoft Teams
* Chiedere a un modello supportato di aiutarti a usare un'app inaccessibile o a completare un'attività nella finestra in primo piano
* Assicurarti che il tuo volto guardi bene verso la fotocamera e che lo sfondo sia professionale prima di registrare video o partecipare a riunioni online

## Modelli

* [Pollinations](https://pollinations.ai/): il team di Pollinations.AI offre generosamente l'accesso gratuito a GPT4 per questo progetto, quindi gli utenti non devono fornire una propria chiave API. Tieni presente che il servizio si è rivelato poco affidabile e consigliamo vivamente di usare le tue chiavi per sfruttare appieno questo progetto.
* [Modelli GPT di OpenAI](https://platform.openai.com/docs/models): richiede una chiave API di OpenAI. Comprende la famiglia GPT-5.4 (5.4 e 5.4 mini), la famiglia GPT-5.5 (5.5 e 5.5 pro), la famiglia GPT-6 (6 Astra e 6 Luna) e la famiglia GPT-6.1 (6.1 Sol e 6.1 Terra). Il controllo del computer è supportato dalle famiglie GPT-5.4, GPT-5.5, GPT-6 e GPT-6.1.
* [Google Gemini](https://deepmind.google/models/gemini/), inclusi i modelli 2.5 Flash, 2.5 Flash-Lite, 2.5 Pro, 3.1 Flash-Lite, 3.1 Pro Preview, 3.5 Flash, 3.5 Flash-Lite, 3.6 Flash, 3.7 Flash, 3.8 Flash, 4 Hydrogen, 4 Argon e 4 Carbon.
* [Anthropic Claude](https://docs.anthropic.com/claude/docs/vision), inclusi Claude 4.5 (Sonnet, Opus), 4.6 (Sonnet, Opus), 4.7 Opus, 4.8 Opus, 5 (Sonnet, Opus, Fable), 5.1 Fable, 5.2 Fable e 5.5 (Haiku, Sonnet, Opus). Tutti supportano il controllo del computer.
* [Mistral Large 4](https://docs.mistral.ai/models/mistral-large-4-0)
* [xAI Grok](https://docs.x.ai/developers/models), inclusi Grok 4.20 (senza ragionamento), 4.3, 4.5, 4.6 e 4.7.
* [Kimi](https://platform.kimi.ai/docs/guide/use-kimi-vision-model), i modelli multimodali di Moonshot AI, inclusi Kimi K3 e Kimi K2.6.
* vivo BlueLM Vision: un modello multimodale di vivo, accessibile tramite un account NVDA-CN gratuito. Vedi la sezione di configurazione più avanti.
* [Datalab Chandra 2](https://github.com/datalab-to/chandra): modello di visione e OCR all'avanguardia di Datalab, specializzato in layout di documenti complessi, tabelle, moduli, scrittura a mano, grafici e matematica. Supporta l'API cloud gestita di Datalab (su [datalab.to](https://www.datalab.to)) o installazioni self-hosted tramite vLLM (con `chandra_vllm` o endpoint `/v1` compatibili con OpenAI).
* [Ollama (instabile)](https://ollama.com/)
* [llama.cpp (estremamente instabile e lento a seconda dell'hardware, testato con i modelli llava-v1.5/1.6, BakLLaVA, Obsidian e MobileVLM 1.7B/3B)](https://github.com/ggerganov/llama.cpp)
* [LiteLLM Proxy](https://docs.litellm.ai/docs/proxy/quick_start): accedi a più modelli di IA tramite un server proxy unificato. Richiede l'URL di un server proxy LiteLLM e, a seconda della configurazione del proxy, una chiave API. Compare come "LiteLLM Proxy" nella finestra di configurazione dei modelli. Supporta la selezione dinamica del modello e le domande di approfondimento. Compatibile con tutti i formati (PNG, JPEG, WEBP, GIF).
* [Seer](https://github.com/recursia-lab/Seer): esegue PaliGemma2 in locale tramite il demone Seer. Non servono né una chiave API né una connessione a Internet. Nota: è un modello che genera solo didascalie. Prompt e domande di approfondimento non sono supportati.

Segui le istruzioni riportate di seguito per far funzionare ciascuno di questi modelli.

## Per iniziare

Scarica l'ultima versione dell'add-on da [questo link](https://github.com/cartertemm/AI-content-describer/releases/latest/). Apri il file su un computer con NVDA installato e procedi con l'installazione seguendo le indicazioni.

Al primo avvio di NVDA con l'add-on, ti verrà chiesto di scaricare alcune librerie aggiuntive. Consulta la sezione `Dipendenze` di questo documento per i dettagli.

Dalla versione 2025.06.05, l'uso di GPT4 è gratuito grazie alla generosità della comunità di PollinationsAI.

Se hai le risorse e l'interesse per provare altri modelli, puoi sempre usare la tua chiave API e ridurre le richieste ai loro server. In caso contrario, passa pure direttamente alla sezione `Utilizzo` di questo documento.

Segui le istruzioni riportate di seguito per ottenere una chiave API da un provider supportato.

### Quale modello usare?

In passato fornivamo consigli sulle opzioni più economiche e di qualità più alta, ma il panorama cambia così rapidamente che non è più possibile tenerli aggiornati.

In breve, la maggior parte dei modelli all'avanguardia è ormai abbastanza precisa per quasi tutti gli usi quotidiani, quindi scegli il provider che conosci meglio.

Quasi tutti cercano un equilibrio tra precisione e costo. La [classifica LLM arena](https://lmarena.ai/leaderboard) (in particolare la categoria vision) misura l'accuratezza, mentre il [calcolatore dei prezzi LLM](https://www.llm-prices.com/) riporta i prezzi.

Se vuoi usare il controllo del computer, scegli uno dei modelli OpenAI o Anthropic supportati elencati sopra. L'accesso gratuito a Pollinations è utile per le descrizioni di immagini, ma non supporta il controllo del computer.

### Ottenere una chiave API da OpenAI:

1. Vai alla [pagina delle chiavi API di OpenAI](https://platform.openai.com/account/api-keys)
2. Se non hai ancora un account, creane uno. Se ce l'hai, accedi.
3. Nella pagina delle chiavi API, fai clic per creare una nuova chiave segreta. Copiala negli appunti.
4. Ricarica l'account con almeno 1 $
5. Nella finestra delle impostazioni di NVDA, scorri fino alla categoria AI Content Describer, scegli "gestisci modelli (alt+m)", seleziona uno qualsiasi dei modelli OpenAI (ad esempio "GPT-6.1 Sol") come provider, spostati con Tab nel campo della chiave API e incolla la chiave appena generata.

Al momento della stesura, OpenAI concede ai nuovi account sviluppatore dei crediti utilizzabili per tre mesi, dopodiché vanno persi. Trascorso questo periodo, dovrai acquistare crediti. Un uso tipico non dovrebbe mai superare 5,00 $ al mese. Come riferimento, la versione originale di questo add-on è stata sviluppata spendendo poco meno di un dollaro. Puoi sempre accedere al tuo account OpenAI e fare clic su "usage" per vedere la tua quota.

### Ottenere una chiave API da Google

1. Per prima cosa devi creare un progetto Google Workspace andando sulla [console di Google Cloud](https://console.cloud.google.com/projectcreate). Assicurati di aver effettuato l'accesso al tuo account Google.
2. Scegli un nome di lunghezza compresa tra quattro e trenta caratteri, ad esempio "Gemini" o "NVDA add-on"
3. Vai alla [pagina delle chiavi API di Google AI Studio](https://makersuite.google.com/app/apikey)
4. Fai clic su "create API key"
5. Nella finestra delle impostazioni di NVDA, scorri fino alla categoria AI Content Describer, scegli "gestisci modelli (alt+m)", seleziona "Google Gemini" come provider, spostati con Tab nel campo della chiave API e incolla la chiave appena generata.

### Ottenere una chiave API da Anthropic

1. Accedi alla [console di Anthropic](https://console.anthropic.com/login).
2. Fai clic sul tuo profilo -> API keys.
3. Fai clic su Create Key.
4. Inserisci un nome per la chiave, ad esempio "AIContentDescriber", poi fai clic su "Create Key" e copia il valore che compare. È questo il valore da incollare nel campo della chiave API nella categoria AI Content Describer della finestra delle impostazioni di NVDA -> gestisci modelli -> qualsiasi modello Claude (ad esempio "Claude 5 Sonnet").
5. Se non l'hai già fatto, acquista almeno 5 $ di crediti nella [pagina dei piani di Anthropic](https://console.anthropic.com/settings/plans).

### Ottenere una chiave API da Mistral

1. Accedi o crea un account MistralAI dalla [pagina di accesso di MistralAI](https://auth.mistral.ai/ui/login).
2. Se crei un account o accedi per la prima volta, aggiungi un workspace come richiesto, indicando un nome e accettando i termini e le condizioni.
3. Dopo l'accesso, seleziona "API keys" dal menu.
4. Fai clic su "create a new key" e copiala negli appunti. È questo il valore da incollare nel campo della chiave API nella categoria AI Content Describer della finestra delle impostazioni di NVDA -> gestisci modelli -> Mistral Large 4.
5. Ricarica l'account, se necessario.

### Ottenere una chiave API da Kimi (Moonshot AI)

1. Accedi o crea un account sulla [piattaforma per sviluppatori Kimi](https://platform.kimi.ai/).
2. Dopo l'accesso, apri la sezione delle chiavi API della console e crea una nuova chiave.
3. Copia la chiave negli appunti. È questo il valore da incollare nel campo della chiave API nella categoria AI Content Describer della finestra delle impostazioni di NVDA -> gestisci modelli -> Kimi K3 (o un altro modello Kimi).
4. Ricarica l'account, se necessario.


### Attivare il modello VIVO BlueLM Vision tramite NVDA-CN

Questo servizio è offerto gratuitamente grazie a una collaborazione tra VIVO (vivo.com.cn) e la comunità cinese di NVDA (NVDACN). Offre un riconoscimento multimodale di alta qualità ed è il modello consigliato per tutti gli utenti, soprattutto per chi inizia.

Per usare questo modello serve solo un account NVDA-CN gratuito.

1.  Crea un account: vai alla pagina di registrazione di NVDA-CN: [https://nvdacn.com/admin/register.php](https://nvdacn.com/admin/register.php).
    * **Nota**: al momento la pagina è in cinese. Ti consigliamo di usare la funzione di traduzione integrata nel browser per compilare il modulo.
    * Ti verranno chiesti un nome utente, una password e un indirizzo email valido. Conserva la password in un luogo sicuro, perché il recupero automatico della password non è ancora disponibile.
2.  Verifica l'email: cerca nella posta in arrivo l'email di verifica e fai clic sul link che contiene per attivare l'account.
3.  Configura l'add-on:
    * Apri la finestra delle impostazioni di NVDA e vai alla categoria "AI Content Describer".
    * Seleziona il pulsante "Gestisci modelli".
    * Dall'elenco dei provider, scegli "vivo BlueLM Vision (NVDA-CN)".
    * Inserisci il nome utente e la password di NVDA-CN nei campi corrispondenti.
    * Fai clic su OK per salvare le credenziali.

Ora puoi usare il modello VIVO. Per qualsiasi problema relativo all'account, puoi contattare il team di NVDA-CN all'indirizzo `support@nvdacn.com`.


### Configurare Ollama

Al momento è l'opzione preferita per un'installazione locale.

Anche se l'integrazione con Ollama è stata testata più a fondo di llama.cpp, resta meno stabile rispetto a una chiamata a un'API ed è noto che si comporti in modo strano con alcune configurazioni, fino a causare crash su computer che non hanno i requisiti necessari.
Come minimo, quando la provi per la prima volta, salva tutti i documenti e qualsiasi cosa importante prima di continuare, nel caso dovesse capitare anche a te.

Per prima cosa, assicurati di riuscire a interagire con il modello con capacità visive che preferisci tramite l'interfaccia a riga di comando. I passaggi sono i seguenti:

1. Scarica il programma di installazione di Ollama per Windows dalla pagina dei [download di Ollama](https://ollama.com/download).
2. Esegui il programma di installazione. Si occuperà di scaricare tutte le dipendenze necessarie al tuo computer.
3. Trova il modello che vuoi usare. Un elenco è disponibile su ollama.com -> models -> vision, oppure [direttamente qui](https://ollama.com/search?c=vision).
4. Scarica e avvia il modello aprendo un prompt dei comandi e digitando `ollama run [model_name]`, sostituendo ovviamente "[model_name]" con quello scelto al passaggio 3. Ad esempio, `ollama run llama3.2-vision`.
5. Se il processo è andato a buon fine, ti troverai in una shell interattiva in cui puoi scrivere domande e ricevere risposte dal modello, una specie di ChatGPT locale (e limitato). Provalo facendo una domanda (qualsiasi) per vedere se funziona, poi digita "/bye" per uscire da questa interfaccia.
6. Tornato nella finestra della console, digita `ollama list`. La prima colonna mostrerà un nome come "llama3.2-vision:latest".
7. Vai nelle impostazioni di AI Content Describer -> gestisci modelli -> Ollama. Nel campo del nome del modello, inserisci questo valore e fai clic su OK -> OK. È tutto pronto! Passa a Ollama nel sottomenu dei modelli e dovrebbe funzionare dopo qualche istante.

### Configurare llama.cpp

Al momento questo provider presenta diversi bug e i risultati possono variare. Andrebbe usato solo da utenti esperti interessati a eseguire modelli locali self-hosted e che dispongono dell'hardware adatto.

1. Scarica llama.cpp. Al momento della stesura, questa [pull request](https://github.com/ggerganov/llama.cpp/pull/5882) rimuove le capacità multimodali, quindi dovrai usare l'[ultima versione che le supporta](https://github.com/ggerganov/llama.cpp/releases/tag/b2356).
Se usi una scheda grafica Nvidia con supporto CUDA, scarica questi binari precompilati:
[llama-b2356-bin-win-cublas-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/llama-b2356-bin-win-cublas-cu12.2.0-x64.zip) e [cudart-llama-bin-win-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/cudart-llama-bin-win-cu12.2.0-x64.zip)
I passaggi per altre schede grafiche non sono trattati qui, ma si trovano nel readme di llama.cpp.
2. Estrai entrambi i file nella stessa cartella.
3. Trova su Huggingface le versioni quantizzate dei modelli che vuoi usare. Per LLaVA 1.6 Vicuna 7B: [llava-v1.6-vicuna-7b.Q4_K_M.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/llava-v1.6-vicuna-7b.Q4_K_M.gguf) e [mmproj-model-f16.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/mmproj-model-f16.gguf)
4. Metti questi file nella cartella con gli altri binari di llama.cpp.
5. Da un prompt dei comandi, esegui il binario del server llava.cpp, passando i file .gguf del modello e del proiettore multimodale (come segue):
```
server.exe -m llava-v1.6-vicuna-7b.Q4_K_M.gguf --mmproj mmproj-model-f16.gguf
```
6. Nella finestra delle impostazioni di NVDA, scorri fino alla categoria AI Content Describer, scegli "gestisci modelli (alt+m)", seleziona "llama.cpp" come provider, spostati con Tab nel campo dell'URL di base e inserisci l'endpoint mostrato nella console (per impostazione predefinita "http://localhost:8080").
7. In alternativa, puoi saltare alcuni di questi passaggi ed eseguire llama.cpp su un server remoto più potente del tuo computer, quindi inserire quell'endpoint.

### Configurare LiteLLM Proxy

LiteLLM Proxy offre un'interfaccia unificata per accedere a più modelli di IA tramite un unico endpoint, semplificando la gestione dei modelli e consentendo di passare facilmente da un provider all'altro.

1. Configura un server proxy LiteLLM seguendo la [documentazione del proxy LiteLLM](https://docs.litellm.ai/docs/proxy/quick_start). Puoi eseguire il proxy in locale o usare un server remoto.
2. In locale, il modo più rapido per iniziare è:
```
pip install 'litellm[proxy]'
litellm --model gpt-4o
```
Questo avvia un server proxy su `http://localhost:4000` che inoltra le richieste a GPT-4o di OpenAI.
3. Per l'uso in produzione, crea un file `config.yaml` per configurare più modelli e l'autenticazione. Consulta la [guida alla configurazione di LiteLLM](https://docs.litellm.ai/docs/proxy/configs) per i dettagli.
4. Nella finestra delle impostazioni di NVDA, scorri fino alla categoria AI Content Describer, scegli "gestisci modelli (alt+m)" e seleziona "LiteLLM Proxy" come provider.
5. Inserisci l'URL del server proxy nel campo dell'URL di base (ad esempio "http://localhost:4000" in locale, oppure l'URL del tuo server remoto).
6. Se il proxy richiede l'autenticazione, inserisci la chiave API nel campo della chiave API. Altrimenti lascialo vuoto.
7. Fai clic sul pulsante "Elenco modelli" per recuperare i modelli disponibili dal proxy, poi seleziona dall'elenco a discesa il modello che vuoi usare.
8. Regola le altre impostazioni, come il prompt, il numero massimo di token e il timeout, secondo le tue esigenze, poi fai clic su OK.

Nota: i modelli disponibili e le loro capacità dipendono dalla configurazione del proxy LiteLLM. Assicurati che il proxy sia configurato con modelli dotati di capacità visive per la descrizione delle immagini.

### Configurare Seer

Seer esegue PaliGemma2 sul tuo computer senza bisogno di una chiave API o di una connessione al cloud. Tieni presente che è un modello che genera solo didascalie: prompt e domande di approfondimento non sono supportati.

1. Installa il [demone Seer](https://github.com/recursia-lab/Seer). È disponibile un programma di installazione con un solo comando per Windows (.bat) e Linux/macOS (.sh).
2. Nella finestra delle impostazioni di NVDA, vai alla categoria AI Content Describer, scegli "gestisci modelli (alt+m)" e seleziona "Seer (requires installation)".
3. L'URL di base predefinito è `http://127.0.0.1:11435`. Lascialo così, a meno che tu non abbia cambiato la porta del demone.
4. Fai clic su OK. Il demone deve essere in esecuzione prima di richiedere una descrizione.

### Configurare Datalab Chandra 2

Datalab Chandra 2 è un modello all'avanguardia per l'analisi di documenti e l'OCR, specializzato in layout complessi, tabelle, moduli, scrittura a mano, grafici e formule matematiche. Si può usare tramite l'API cloud gestita di Datalab, un container on-premise o un'istanza vLLM self-hosted.

#### Opzione A: usare l'API cloud di Datalab (consigliato)
1. Registra un account su [datalab.to](https://www.datalab.to). I nuovi account ricevono crediti di prova gratuiti.
2. Vai alla [pagina delle chiavi API](https://www.datalab.to/app/keys) e genera una chiave API.
3. Nella finestra delle impostazioni di NVDA, vai alla categoria AI Content Describer, scegli "gestisci modelli (alt+m)" e seleziona "Datalab Chandra 2".
4. Inserisci la chiave API nel campo "Chiave API".
5. L'URL di base è impostato per impostazione predefinita su `https://www.datalab.to/api/v1/convert`. Puoi regolare la modalità di elaborazione (`fast`, `balanced` o `accurate`) in base alle tue esigenze.
6. Fai clic su OK. Il modello sarà ora disponibile nel menu di AI Content Describer.

#### Opzione B: self-hosted con vLLM
1. Avvia il tuo server vLLM locale con Chandra 2 (ad esempio con `chandra_vllm` o `vllm serve datalab-to/chandra-ocr-2`). Per impostazione predefinita, il server è in esecuzione su `http://localhost:8000/v1`.
2. In Impostazioni di NVDA -> AI Content Describer -> Gestisci modelli -> "Datalab Chandra 2", inserisci l'endpoint locale nel campo "URL di base" (ad esempio `http://localhost:8000/v1`).
3. Imposta il nome del modello se è diverso da quello predefinito (`datalab-to/chandra-ocr-2`), lascia vuota la chiave API (o fornisci un bearer token se l'autenticazione è attiva) e fai clic su OK.

## Utilizzo

Per impostazione predefinita sono assegnati sei tasti di scelta rapida:

* NVDA+shift+i: apre un menu che chiede se descrivere il focus attuale, l'oggetto del navigatore, la fotocamera fisica o l'intero schermo, oppure controllare il computer con l'IA.
* NVDA+shift+u: descrive con l'IA il contenuto dell'oggetto del navigatore attuale.
* NVDA+shift+y: descrive con l'IA l'immagine (o il percorso di un file immagine) presente negli appunti.
* NVDA+shift+j: descrive la posizione del tuo volto nell'inquadratura della fotocamera selezionata. Se hai più fotocamere collegate, apri il menu di AI Content Describer (NVDA+shift+i) e scegli quella da usare con la voce "seleziona fotocamera" nel sottomenu del rilevamento del volto.
* NVDA+alt+c: apre la finestra di conversazione con l'IA per fare domande di approfondimento.
* NVDA+control+shift+p: mette in pausa o riprende una sessione di controllo del computer attiva.

Sette gesti non sono assegnati:

* Descrivere con l'IA il contenuto dell'elemento che ha il focus.
* Fare uno screenshot e descriverlo con l'IA.
* Scattare una foto con la fotocamera selezionata e descriverla con l'IA.
* Annullare la sessione di controllo del computer attiva.
* Fare uno screenshot dell'oggetto con il focus e copiarlo negli appunti.
* Fare uno screenshot dell'oggetto del navigatore attuale e copiarlo negli appunti.
* Fare uno screenshot dell'intero schermo e copiarlo negli appunti.

I tre comandi di copia si trovano anche nel sottomenu "Copia immagine negli appunti" del menu NVDA+shift+i. Non inviano nulla a un servizio di IA. Usali per incollare una cattura in Be My AI o in un'altra app non supportata da questo add-on. La copia sostituisce il contenuto precedente degli appunti.

Puoi personalizzarli in qualsiasi momento dalla finestra dei gesti e tasti di immissione.

### Fare domande di approfondimento su una descrizione

A volte la risposta dell'IA non basta. Forse l'immagine è di bassa qualità, incompleta o contiene dettagli indesiderati. Forse vuoi concentrarti solo su una certa parte o scattare una foto più nitida senza perdere il contesto.
Dopo aver ricevuto una descrizione, puoi premere NVDA+alt+c o selezionare "Continua con la descrizione precedente" dal menu contestuale di AI Content Describer (NVDA+shift+i). Per impostazione predefinita, il focus si trova nel campo del messaggio.
Per aggiungere un'altra immagine, lascia aperta la finestra della conversazione e usa l'add-on come fai di solito. Quando viene acquisita un'immagine (dalla fotocamera, da un controllo di sistema, da uno screenshot e così via), ti verrà chiesto se vuoi allegarla alla sessione corrente o avviarne una nuova.

### Controllo del computer

Il controllo del computer permette ad AI Content Describer di gestire l'applicazione attiva con il mouse e la tastiera dopo che hai descritto un'attività. Può aiutare con attività difficili o inaccessibili da svolgere manualmente.

Dato che questa funzione dà a un modello di IA il controllo del tuo computer, usala con attenzione. L'add-on chiede il consenso prima di iniziare, annuncia le azioni mentre avvengono e chiede conferma prima delle azioni potenzialmente rischiose. Sei tu il responsabile di ciò che fa, quindi tieni d'occhio la sessione ed evita di usarla per lavori delicati o difficili da annullare.

Puoi mettere in pausa o riprendere il controllo del computer in qualsiasi momento con `NVDA+Control+Shift+P`. Durante la pausa, l'add-on non passa all'azione successiva finché non riprendi.

L'add-on usa dei toni per indicare lo stato del controllo. Un segnale acustico acuto indica che il modello sta prendendo o riprendendo il controllo. Un segnale grave indica che il controllo è in pausa, perché l'hai messo in pausa tu o perché il modello ha bisogno di un tuo intervento. Un breve segnale di errore grave indica che la sessione si è interrotta a causa di un errore dell'API.

Durante una sessione di controllo, il modello annuncia cosa sta per fare prima di inviare l'input. Non succede nulla finché l'annuncio non è terminato, a meno che tu non prema `Control` per interromperlo e lasciare che l'azione proceda prima.

Se il modello non sa come completare un'azione, ha bisogno di altre informazioni o ti restituisce il turno per altri motivi, la sessione va in pausa e la finestra Controllo del computer passa in primo piano. Scrivi lì un messaggio per continuare la conversazione, oppure chiudi la finestra per terminare la sessione.

Questa funzione funziona solo con i modelli che forniscono uno strumento di controllo del computer: GPT-5.4, GPT-5.4 mini, GPT-5.5, GPT-5.5 pro, GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna, Claude 4.5 Sonnet, Claude 4.5 Opus, Claude 4.6 Sonnet, Claude 4.6 Opus, Claude 4.7 Opus, Claude 4.8 Opus, Claude 5 Sonnet, Claude 5 Opus, Claude 5 Fable, Claude 5.1 Fable, Claude 5.2 Fable, Claude 5.5 Haiku, Claude 5.5 Sonnet e Claude 5.5 Opus. Gli altri modelli possono descrivere immagini, ma non forniscono le azioni strutturate di mouse e tastiera necessarie per il controllo del computer.

Per usare il controllo del computer:

1. Configura e seleziona uno dei modelli supportati.
2. Apri l'applicazione o la finestra su cui vuoi che lavori il modello.
3. Premi `NVDA+shift+i`, poi scegli "Controlla il computer...".
4. Scrivi l'attività da eseguire e premi Invia.
5. Leggi la richiesta di consenso. Se autorizzi la sessione, tieni d'occhio le azioni e approva o annulla le eventuali richieste per azioni rischiose.

Nota: questa funzione va considerata in fase beta e stiamo lavorando attivamente per renderne l'implementazione più solida.

## Dipendenze

Alcune delle librerie necessarie a questo add-on sono troppo grandi per essere incluse nel pacchetto. Al primo avvio di NVDA con l'add-on installato, ti verrà chiesto se vuoi scaricarle. Seleziona sì, attendi la fine del download e NVDA si riavvierà.

Il download è un file zip di circa 35-70 MB, a seconda della versione di NVDA. Proviene dalla pagina [libs-release](https://github.com/cartertemm/AI-content-describer/releases/tag/libs-release) di questo repository. Se GitHub non è raggiungibile, l'add-on propone di provare un mirror fornito dalla comunità cinese di NVDA.

Lo zip contiene:

* [NumPy](https://numpy.org/): calcoli su array, richiesto da OpenCV.
* [OpenCV](https://opencv.org/) (`cv2`): individua il tuo volto nelle immagini della webcam per la funzione di rilevamento del volto.
* [Pillow](https://python-pillow.org/) (`PIL`): acquisisce gli screenshot e li converte in immagini leggibili dai modelli di IA.
* [Markdown](https://python-markdown.github.io/): mostra le descrizioni con la formattazione, come titoli, elenchi e tabelle.
* [pygrabber](https://github.com/andreaschiavinato/python_grabber): elenca le webcam presenti sul computer.
* Alcuni moduli della libreria standard di Python che NVDA non include (`html`, `xml`, `pathlib`, `secrets` e `_markupbase`). Sono necessari alle librerie elencate sopra.

I file vengono salvati in una cartella chiamata `aic-py-` seguito dalla versione di Python di NVDA, ad esempio `aic-py-3.13`. Questa cartella si trova nella cartella di configurazione utente di NVDA, di solito `%APPDATA%\nvda`. Ogni versione di Python ha la sua cartella, quindi l'add-on scarica di nuovo le librerie quando una nuova versione di NVDA cambia la versione di Python. Disinstallando l'add-on viene eliminata la cartella relativa alla versione di Python attuale di NVDA.

Se il download non funziona, puoi installare le librerie manualmente. Scarica `aic-py-3.13.zip` (o il file per la versione di Python del tuo NVDA) dalla pagina libs-release, estrailo nella cartella di configurazione utente di NVDA e riavvia NVDA.

## Compilare l'add-on

Per creare il pacchetto dell'add-on dai sorgenti, ti serviranno:

* una distribuzione di Python (si consiglia la 3.7 o successiva). Consulta il [sito web di Python](https://www.python.org) per i programmi di installazione per Windows. Tieni presente che al momento la preparazione del codice sorgente di NVDA e dei moduli di terze parti inclusi richiede la versione a 32 bit di Python 3.7.
* Scons - [Sito web](https://www.scons.org/) - versione 4.3.0 o successiva. Puoi installarlo tramite PIP. `pip install scons`
* Markdown 3.3.0 o successivo. `pip install markdown`

Poi apri il terminale che preferisci:

```
git clone https://github.com/cartertemm/AI-content-describer.git
cd AI-content-describer
scons
```

Al termine del comando `scons`, nella cartella principale di questo repository verrà creato un file *.nvda-addon pronto per i test e la pubblicazione.

Se aggiungi altre stringhe da tradurre, è importante rigenerare il file .pot in questo modo:

```
scons pot
```

## Come tradurre?

Su un computer Windows:

* scarica [poedit](https://poedit.net/). È il programma che userai per tradurre ogni messaggio dall'inglese.
* scarica il file .pot con tutte le stringhe [qui](https://raw.githubusercontent.com/cartertemm/AI-content-describer/main/AIContentDescriber.pot)
* Apri il file appena scaricato in poedit. Fai clic su "Crea nuova traduzione" nella finestra che compare, poi seleziona la lingua di destinazione.
* Traduci il testo di origine nella lingua di destinazione e inseriscilo nel campo della traduzione. Per un aiuto in più, puoi fare clic con il tasto destro sulla voce dell'elenco -> occorrenze nel codice, poi salire di una riga per leggere il commento che inizia con "# Translators: ". Questi commenti sono riportati anche tutti insieme nel file .pot.
* Al termine, fai clic su file -> salva o premi ctrl+s, poi scegli dove salvare i nuovi file .mo e .po. Sono questi i file da inviarmi via email o da allegare a una pull request.
* Traduci il contenuto di readme.md (questo file). Allega anche quello!

## Contributi

Tutti i contributi sono molto apprezzati e verranno riconosciuti.
Le seguenti persone hanno lavorato all'add-on.

* [Cary Rowen](https://github.com/cary-rowen): ha reso l'add-on utilizzabile per gli utenti cinesi tramite il mirroring delle dipendenze e ha aggiunto il supporto per il provider Vivo Blue
* [Mazen](https://github.com/mzanm): implementazione di Markdown e altri contributi al codice
* [Kostenkov-2021](https://github.com/Kostenkov-2021): traduzione russa
* [Nidza07](https://github.com/nidza07): traduzione serba
* [Heorhii Halas](nvda.translation.uk@gmail.com) e [George-br](https://github.com/George-br): traduzione ucraina
* [Umut Korkmaz](umutkork@gmail.com): traduzione turca
* [Platinum_Hikari](urbain_onces.0r@icloud.com): traduzione francese
* [Lukas](https://4sensegaming.cz): traduzione ceca
* [Michaela](https://technologiebezzraku.sk): traduzione slovacca
* [loginerror](https://github.com/theloginerror): traduzione polacca

Hai un problema? Segnalalo nell'[issue tracker](https://github.com/cartertemm/AI-content-describer/issues)

Hai un suggerimento per una nuova funzionalità? Apri una segnalazione anche per quello e potremo discutere di come implementarla. Le pull request senza una issue associata verranno esaminate, ma probabilmente richiederanno più tempo a tutti, soprattutto se decido che la nuova correzione o funzionalità deve funzionare in modo diverso da quanto proposto.

Le traduzioni sono accolte a braccia aperte. Più persone possono accedere a questa potente tecnologia, meglio è!

Se non hai un account Github o preferisci non usarlo, puoi [mandarmi un'email](mailto:carter@ctemm.me) - carter (at) ctemm (dot) me.

Grazie per il supporto!
