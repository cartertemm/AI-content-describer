# Doplnok Popis obsahu pomocou AI pre NVDA

Tento doplnok umožňuje získať podrobné popisy obrázkov, ovládacích prvkov používateľského rozhrania a ďalšieho neprístupného vizuálneho obsahu.

S využitím multimodálnych schopností pokročilých modelov umelej inteligencie a algoritmov počítačového videnia sa snažíme poskytovať najlepšie možné popisy obsahu svojho druhu a zvýšiť tak vašu nezávislosť. Ďalšie informácie o použitých modeloch nájdete v príslušnej časti tohto dokumentu.

## Funkcie

* Popis objektu, ktorý má práve fokus, aktuálne prezeraného objektu, celej obrazovky alebo snímky zo vstavanej kamery
* Popis akéhokoľvek obrázka, ktorý ste skopírovali do schránky, či už sa jedná o obrázok z e-mailu alebo cestu v Prieskumníkovi Windows
* Skopírovanie obrázka objektu pod fokusom, prezeraného objektu alebo celej obrazovky do schránky, aby ste ho mohli vložiť do iných aplikácií
* Zistenie, či sa tvár používateľa nachádza uprostred záberu, pomocou algoritmov počítačového videnia (nevyžaduje platený prístup k žiadnemu rozhraniu API)
* Ovládanie aktívnej aplikácie pomocou myši a klávesnice podporovanými modelmi, napríklad pri úlohách, ktoré by inak mohli byť neprístupné
* Štandardne zadarmo, pre prístup k ďalším modelom môžete voliteľne pridať vlastný kľúč API
* Podpora viacerých poskytovateľov (GPT od OpenAI a bezplatná úroveň Pollinations, Gemini od Googlu, Mistral Large 4, Claude od Anthropic, Grok od xAI, Kimi od Moonshot AI, vivo BlueLM Vision cez NVDA-CN, Datalab Chandra 2, Ollama, llama.cpp, LiteLLM Proxy a Seer)
* Podpora širokej škály formátov, vrátane PNG (.png), JPEG (.jpeg a .jpg), WEBP (.webp) a neanimovaného GIF (.gif)
* Voliteľné ukladanie odpovedí do medzipamäte pre úsporu kvóty API
* Pre pokročilé použitie si môžete nastaviť pokyn a počet tokenov tak, aby ste získané informácie prispôsobili svojim potrebám
* Možnosť klásť doplňujúce otázky a prikladať ďalšie obrázky
* Vykresľovanie vo formáte Markdown pre ľahký prístup k štruktúrovaným informáciám (stačí zapnúť nastavenie „otvárať výsledky v prehľadávateľnom dialógu“ a na koniec svojho pokynu uviesť napr. „odpovedz vo formáte Markdown“)

## Možnosti využitia

Tento projekt mal niekoľko hlavných motivácií.

NVDA dokáže už v základnej inštalácii vykonávať optické rozpoznávanie znakov (OCR), čo je obrovský pokrok. Pokiaľ sa snažíte získať text z obrázku alebo dokumentu PDF, potom hľadáte práve túto funkciu.

OCR však dokáže analyzovať iba dáta, ktoré *môžu* obsahovať text. Nedokáže objasniť kontext, predmety, ktoré sa na obrázkoch môžu nachádzať, a vzťahy medzi nimi. Tých je internet plný. Logá, portréty, mémy, ikony, grafy, diagramy, stĺpcové/čiarové grafy... Na čo si spomeniete. Sú všade a obvykle nie sú vo formáte, ktorý by používatelia čítača obrazovky dokázali interpretovať.
Donedávna sme sa neochvejne spoliehali na to, že autori obsahu budú poskytovať alternatívne textové popisy. Aj keď je to stále nutnosť, ťažko zmeníme skutočnosť, že vysoký štandard kvality býva skôr výnimkou, nie pravidlom.

Teraz máte možnosti takmer neobmedzené. Môžete napr.:

* Vizualizovať si plochu alebo konkrétne okno, aby ste pochopili rozmiestnenie jednotlivých ikon pri školení ostatných
* Získať podrobné informácie o stave hier, virtuálnych počítačov atď. v prípade nedostatočného alebo chýbajúceho ozvučenia
* Zistiť, čo je zobrazené v grafe
* Pochopiť snímky obrazovky alebo zdieľanie obrazovky v aplikáciách Zoom alebo Microsoft Teams
* Požiadať podporovaný model, aby vám pomohol ovládať neprístupnú aplikáciu alebo dokončiť úlohu v okne v popredí
* Pred natáčaním videí alebo účasťou na online stretnutiach sa uistiť, že sa pozeráte zreteľne do kamery a že pozadie vyzerá profesionálne

## Modely

* [Pollinations](https://pollinations.ai/): Tím, ktorý stojí za Pollinations.AI, veľkoryso sponzoruje pre tento projekt bezplatný prístup ku GPT4, takže používatelia nemusia zadávať vlastný kľúč API. Majte na pamäti, že pri tejto službe boli pozorované chyby, a preto dôrazne odporúčame používať vlastné kľúče, aby ste z tohto projektu získali maximum.
* [Modely GPT od OpenAI](https://platform.openai.com/docs/models): Vyžaduje kľúč API od OpenAI. Zahŕňa rad GPT-5.4 (5.4 a 5.4 mini), rad GPT-5.5 (5.5 a 5.5 pro), rad GPT-6 (6 Astra a 6 Luna) a rad GPT-6.1 (6.1 Sol a 6.1 Terra). Ovládanie počítača podporujú rady GPT-5.4, GPT-5.5, GPT-6 a GPT-6.1.
* [Google Gemini](https://deepmind.google/models/gemini/), vrátane modelov 2.5 Flash, 2.5 Flash-Lite, 2.5 Pro, 3.1 Flash-Lite, 3.1 Pro Preview, 3.5 Flash, 3.5 Flash-Lite, 3.6 Flash, 3.7 Flash, 3.8 Flash, 4 Hydrogen, 4 Argon a 4 Carbon.
* [Anthropic Claude](https://docs.anthropic.com/claude/docs/vision), vrátane Claude 4.5 (Sonnet, Opus), 4.6 (Sonnet, Opus), 4.7 Opus, 4.8 Opus, 5 (Sonnet, Opus, Fable), 5.1 Fable, 5.2 Fable a 5.5 (Haiku, Sonnet, Opus). Všetky tieto modely podporujú ovládanie počítača.
* [Mistral Large 4](https://docs.mistral.ai/models/mistral-large-4-0)
* [xAI Grok](https://docs.x.ai/developers/models), vrátane Grok 4.20 (bez uvažovania), 4.3, 4.5, 4.6 a 4.7.
* [Kimi](https://platform.kimi.ai/docs/guide/use-kimi-vision-model), multimodálne modely od Moonshot AI, vrátane Kimi K3 a Kimi K2.6.
* vivo BlueLM Vision: multimodálny model od spoločnosti vivo, dostupný prostredníctvom bezplatného účtu NVDA-CN. Pozrite si časť o nastavení nižšie.
* [Datalab Chandra 2](https://github.com/datalab-to/chandra): Špičkový model na rozpoznávanie obrazu a OCR od spoločnosti Datalab, špecializovaný na zložité rozloženia dokumentov, tabuľky, formuláre, ručne písaný text, grafy a matematiku. Podporuje spravované cloudové API spoločnosti Datalab (na [datalab.to](https://www.datalab.to)) alebo vlastné nasadenie cez vLLM (pomocou `chandra_vllm` alebo koncových bodov `/v1` kompatibilných s OpenAI).
* [Ollama (nestabilná)](https://ollama.com/)
* [llama.cpp (extrémne nestabilný a pomalý v závislosti od vášho hardvéru, testované pri práci s modelmi llava-v1.5/1.6, BakLLaVA, Obsidian a MobileVLM 1.7B/3B)](https://github.com/ggerganov/llama.cpp)
* [LiteLLM Proxy](https://docs.litellm.ai/docs/proxy/quick_start): Prístup k viacerým modelom AI cez jednotný proxy server. Vyžaduje adresu URL proxy servera LiteLLM a v závislosti od konfigurácie proxy aj kľúč API. V dialógu konfigurácie modelov sa zobrazuje ako „LiteLLM Proxy“. Podporuje dynamický výber modelu a doplňujúce otázky. Je kompatibilný so všetkými formátmi (PNG, JPEG, WEBP, GIF).
* [Seer](https://github.com/recursia-lab/Seer): Spúšťa model PaliGemma2 lokálne pomocou démona Seer. Nevyžaduje kľúč API ani pripojenie na internet. Poznámka: ide o model, ktorý vie iba vytvárať popisky. Pokyny ani doplňujúce otázky nie sú podporované.

Pre sprevádzkovanie jednotlivých modelov postupujte podľa nižšie uvedených pokynov.

## Ako začať

Stiahnite si najnovšiu verziu doplnku z [tohto odkazu](https://github.com/cartertemm/AI-content-describer/releases/latest/). Otvorte stiahnutý súbor v počítači, kde máte nainštalované NVDA, a pokračujte v inštalácii podľa zobrazených pokynov.

Pri prvom spustení NVDA s týmto doplnkom budete požiadaní o stiahnutie niekoľkých ďalších knižníc. Podrobnosti nájdete v časti `Závislosti` tohto dokumentu.

Od verzie 2025.06.05 je používanie GPT4 zadarmo vďaka veľkorysosti komunity okolo PollinationsAI.

Ak máte prostriedky a záujem vyskúšať ďalšie modely, môžete vždy použiť vlastný kľúč API a znížiť tak počet požiadaviek na ich servery. Ak nie, pokojne preskočte na časť `Použitie` tohto dokumentu.

Podľa nižšie uvedených pokynov získajte kľúč API od niektorého z podporovaných poskytovateľov.

### Ktorý model mám použiť?

Predtým sme odporúčali najlacnejšie a najkvalitnejšie možnosti, ale situácia sa mení tak rýchlo, že nie je možné tieto odporúčania udržiavať aktuálne.

Stručne povedané: väčšina špičkových modelov je dnes dostatočne presná pre väčšinu bežných situácií, takže si vyberte poskytovateľa, ktorého poznáte.

Väčšina ľudí hľadá rovnováhu medzi presnosťou a cenou. [Rebríček LLM arena](https://lmarena.ai/leaderboard) (konkrétne kategória vision) meria správnosť, zatiaľ čo [kalkulačka cien LLM](https://www.llm-prices.com/) prehľadne uvádza ceny.

Ak chcete používať ovládanie počítača, vyberte niektorý z podporovaných modelov od OpenAI alebo Anthropic uvedených vyššie. Bezplatný prístup cez Pollinations je užitočný na popisy obrázkov, ale ovládanie počítača nepodporuje.

### Ako získať API kľúč od OpenAI:

1. Prejdite na [stránku s kľúčmi API od OpenAI](https://platform.openai.com/account/api-keys)
2. Ak ešte nemáte účet, vytvorte si ho. Ak áno, prihláste sa.
3. Na stránke API keys kliknite na tlačidlo na vytvorenie nového tajného kľúča. Skopírujte ho do schránky.
4. Na svoj účet vložte aspoň 1 dolár
5. V dialógovom okne nastavenia NVDA prejdite do kategórie Popis obsahu pomocou AI, potom vyberte „Spravovať modely (alt+m)“, ako poskytovateľa vyberte ktorýkoľvek model od OpenAI (napríklad „GPT-6.1 Sol“), klávesom tab prejdite do políčka API kľúč a vložte sem práve vytvorený kľúč.

V čase, keď bol tento dokument vytvorený, vydávala OpenAI novým vývojárskym účtom kredity, ktoré je možné používať po dobu troch mesiacov, potom prepadnú. Po uplynutí tejto lehoty si budete musieť kredity zakúpiť. Zvyčajná spotreba by nikdy nemala presiahnuť 5,00 USD mesačne. Pre predstavu, pôvodná verzia tohto doplnku bola vyvinutá za necelý dolár. Kedykoľvek sa môžete prihlásiť k svojmu účtu OpenAI a kliknutím na „usage“ zistiť stav svojej kvóty.

### Ako získať API kľúč od Googlu

1. Najprv je potrebné vytvoriť projekt Google Workspace v [konzole Google Cloud](https://console.cloud.google.com/projectcreate). Uistite sa, že ste prihlásení k svojmu účtu Google.
2. Zadajte názov v rozsahu štyroch až tridsiatich znakov, napríklad „Gemini“ alebo „NVDA add-on“.
3. Prejdite na [stránku s kľúčmi API v Google AI Studiu](https://makersuite.google.com/app/apikey)
4. Kliknite na tlačidlo „create API key“
5. V dialógovom okne nastavenia NVDA prejdite do kategórie Popis obsahu pomocou AI, potom vyberte „Spravovať modely (alt+m)“, ako poskytovateľa vyberte „Google Gemini“, klávesom tab prejdite do políčka API kľúč a vložte sem práve vygenerovaný kľúč.

### Ako získať API kľúč od Anthropic

1. Prihláste sa do [konzoly Anthropic](https://console.anthropic.com/login).
2. Kliknite na svoj profil -> API keys.
3. Kliknite na tlačidlo Create Key.
4. Zadajte názov kľúča, napríklad „AIContentDescriber“, potom kliknite na „Create Key“ a skopírujte hodnotu, ktorá sa zobrazí. Túto hodnotu vložíte do políčka API kľúč v kategórii Popis obsahu pomocou AI v dialógovom okne Nastavenia NVDA -> Spravovať modely -> ktorýkoľvek model Claude (napríklad „Claude 5 Sonnet“).
5. Ak ste tak ešte neurobili, zakúpte si kredity v hodnote aspoň 5 USD na [stránke Plans od Anthropic](https://console.anthropic.com/settings/plans).

### Ako získať API kľúč od Mistralu

1. Prihláste sa k účtu MistralAI alebo si ho vytvorte na [prihlasovacej stránke MistralAI](https://auth.mistral.ai/ui/login).
2. Ak si účet vytvárate alebo sa prihlasujete prvýkrát, pridajte podľa výzvy pracovný priestor, zadajte jeho názov a prijmite zmluvné podmienky.
3. Po prihlásení vyberte v ponuke položku „API keys“.
4. Kliknite na „create a new key“ a skopírujte kľúč do schránky. Túto hodnotu vložíte do políčka API kľúč v kategórii Popis obsahu pomocou AI v dialógovom okne Nastavenia NVDA -> Spravovať modely -> Mistral Large 4.
5. V prípade potreby si na účet vložte kredit.

### Ako získať API kľúč od Kimi (Moonshot AI)

1. Prihláste sa k účtu na [vývojárskej platforme Kimi](https://platform.kimi.ai/) alebo si ho vytvorte.
2. Po prihlásení otvorte v konzole časť s kľúčmi API a vytvorte nový kľúč.
3. Skopírujte kľúč do schránky. Túto hodnotu vložíte do políčka API kľúč v kategórii Popis obsahu pomocou AI v dialógovom okne Nastavenia NVDA -> Spravovať modely -> Kimi K3 (alebo iný model Kimi).
4. V prípade potreby si na účet vložte kredit.


### Aktivácia modelu VIVO BlueLM Vision cez NVDA-CN

Táto služba je k dispozícii zadarmo vďaka partnerstvu medzi spoločnosťou VIVO (vivo.com.cn) a čínskou komunitou NVDA (NVDACN). Poskytuje kvalitné multimodálne rozpoznávanie a je to odporúčaný model pre všetkých používateľov, najmä pre začiatočníkov.

Na používanie tohto modelu potrebujete iba bezplatný účet NVDA-CN.

1.  Vytvorenie účtu: Prejdite na registračnú stránku NVDA-CN: [https://nvdacn.com/admin/register.php](https://nvdacn.com/admin/register.php).
    * **Poznámka**: Stránka je zatiaľ iba v čínštine. Na vyplnenie formulára odporúčame použiť vstavanú funkciu prekladu vo vašom prehliadači.
    * Budete požiadaní o používateľské meno, heslo a platnú e-mailovú adresu. Heslo si bezpečne uložte, pretože automatické obnovenie hesla zatiaľ nie je k dispozícii.
2.  Overenie e-mailu: Vo svojej schránke vyhľadajte overovací e-mail a kliknutím na odkaz v ňom aktivujte účet.
3.  Konfigurácia doplnku:
    * Otvorte dialógové okno nastavenia NVDA a prejdite do kategórie „Popis obsahu pomocou AI“.
    * Vyberte tlačidlo „Spravovať modely“.
    * V zozname poskytovateľov zvoľte „vivo BlueLM Vision (NVDA-CN)“.
    * Do príslušných polí zadajte svoje používateľské meno a heslo k NVDA-CN.
    * Kliknutím na OK prihlasovacie údaje uložte.

Teraz môžete model VIVO používať. S akýmikoľvek problémami s účtom sa môžete obrátiť na tím NVDA-CN na adrese `support@nvdacn.com`.


### Ako nastaviť Ollama

Toto je v súčasnosti preferovaná možnosť pre lokálnu prevádzku.

Hoci integrácia Ollama bola testovaná dôkladnejšie ako llama.cpp, stále je menej stabilná ako volanie API a v niektorých konfiguráciách sa správa zvláštne, a to až po pády na počítačoch, ktoré nespĺňajú požadované parametre.
Keď túto možnosť skúšate prvýkrát, uložte si pre istotu všetky dokumenty a všetko dôležité, než budete pokračovať.

Najprv sa uistite, že dokážete so zvoleným modelom s podporou obrazu komunikovať cez príkazový riadok. Postup je nasledujúci:

1. Stiahnite si inštalačný súbor Ollama pre Windows zo stránky [Ollama downloads](https://ollama.com/download).
2. Spustite tento inštalačný súbor. Postará sa o stiahnutie všetkých závislostí, ktoré bude váš počítač potrebovať.
3. Nájdite model, ktorý chcete použiť. Zoznam nájdete na ollama.com -> models -> vision, alebo [priamo tu](https://ollama.com/search?c=vision).
4. Stiahnite a spustite tento model tak, že otvoríte príkazový riadok a napíšete `ollama run [model_name]`, pričom „[model_name]“ samozrejme nahradíte modelom zvoleným v kroku 3. Napríklad `ollama run llama3.2-vision`.
5. Ak všetko prebehlo úspešne, ocitnete sa v interaktívnom prostredí, kde môžete písať otázky a dostávať odpovede od modelu, niečo ako lokálny (a obmedzený) ChatGPT. Vyskúšajte ho tak, že sa na niečo opýtate, a potom napíšte „/bye“ na ukončenie tohto rozhrania.
6. Späť v okne konzoly napíšte `ollama list`. V prvom stĺpci uvidíte názov ako „llama3.2-vision:latest“.
7. Prejdite do nastavení Popisu obsahu pomocou AI -> Spravovať modely -> Ollama. Do políčka názov modelu zadajte túto hodnotu a kliknite na OK -> OK. Hotovo! V podponuke modelov prepnite na Ollama a po chvíli by malo všetko fungovať.

### Ako nastaviť llama.cpp

Tento poskytovateľ je v súčasnej dobe trochu chybný a vaše skúsenosti sa môžu líšiť. O sprevádzkovanie modelu by sa mali pokúšať naozaj len pokročilí používatelia so záujmom o prevádzkovanie lokálnych self-hosted modelov a s hardvérom, ktorý na to potrebujú.

1. Stiahnite si llama.cpp. V čase vytvorenia tohto dokumentu tento [pull request](https://github.com/ggerganov/llama.cpp/pull/5882) odstraňuje podporu pre multimodálne schopnosti, takže budete chcieť použiť [poslednú verziu s touto podporou](https://github.com/ggerganov/llama.cpp/releases/tag/b2356).
Ak používate grafickú kartu Nvidia s podporou CUDA, stiahnite si tieto predpripravené binárne súbory:
[llama-b2356-bin-win-cublas-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/llama-b2356-bin-win-cublas-cu12.2.0-x64.zip) a [cudart-llama-bin-win-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/cudart-llama-bin-win-cu12.2.0-x64.zip)
Popis krokov potrebných na prácu s inou grafickou kartou je nad rámec tohto dokumentu, ale nájdete ho v readme súbore pre llama.cpp.
2. Obidva súbory rozbaľte do rovnakého priečinka.
3. Z Huggingface si stiahnite kvantizované súbory modelov, ktoré chcete použiť. Pre LLaVA 1.6 Vicuna 7B: [llava-v1.6-vicuna-7b.Q4_K_M.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/llava-v1.6-vicuna-7b.Q4_K_M.gguf) a [mmproj-model-f16.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/mmproj-model-f16.gguf)
4. Tieto súbory vložte do priečinka s ostatnými spustiteľnými súbormi llama.cpp.
5. Z príkazového riadka spustite server llama.cpp a odovzdajte mu súbory .gguf pre model a multimodálny projektor (podľa nasledujúceho príkladu):
```
server.exe -m llava-v1.6-vicuna-7b.Q4_K_M.gguf --mmproj mmproj-model-f16.gguf
```
6. V dialógovom okne nastavenia NVDA prejdite do kategórie Popis obsahu pomocou AI, potom zvoľte „Spravovať modely (alt+m)“, ako poskytovateľa vyberte „llama.cpp“, klávesom tab prejdite do políčka Adresa URL a zadajte koncový bod zobrazený v konzole (predvolená hodnota je „http://localhost:8080“).
7. Prípadne môžete niektoré z týchto krokov vynechať a spustiť llama.cpp na vzdialenom serveri s vyšším výkonom, než má váš lokálny počítač, a zadať namiesto toho jeho koncový bod.

### Ako nastaviť LiteLLM Proxy

LiteLLM Proxy poskytuje jednotné rozhranie na prístup k viacerým modelom AI cez jediný koncový bod, čo zjednodušuje správu modelov a umožňuje ľahké prepínanie medzi poskytovateľmi.

1. Nastavte proxy server LiteLLM podľa [dokumentácie LiteLLM proxy](https://docs.litellm.ai/docs/proxy/quick_start). Proxy môžete prevádzkovať lokálne alebo použiť vzdialený server.
2. Pri lokálnej prevádzke najrýchlejšie začnete takto:
```
pip install 'litellm[proxy]'
litellm --model gpt-4o
```
Tým sa na adrese `http://localhost:4000` spustí proxy server, ktorý preposiela požiadavky na model GPT-4o od OpenAI.
3. Na produkčné nasadenie vytvorte súbor `config.yaml` s konfiguráciou viacerých modelov a overovania. Podrobnosti nájdete v [sprievodcovi konfiguráciou LiteLLM](https://docs.litellm.ai/docs/proxy/configs).
4. V dialógovom okne nastavenia NVDA prejdite do kategórie Popis obsahu pomocou AI, potom zvoľte „Spravovať modely (alt+m)“ a ako poskytovateľa vyberte „LiteLLM Proxy“.
5. Do políčka Adresa URL zadajte adresu svojho proxy servera (napr. „http://localhost:4000“ pre lokálnu prevádzku alebo adresu vášho vzdialeného servera).
6. Ak proxy vyžaduje overenie, zadajte kľúč do políčka API kľúč. Ak nie, nechajte políčko prázdne.
7. Kliknutím na tlačidlo „Vypísať modely“ načítajte dostupné modely z proxy a potom v rozbaľovacom zozname vyberte model, ktorý chcete použiť.
8. Podľa potreby upravte ďalšie nastavenia, ako je pokyn, maximálny počet tokenov a časový limit, a potom kliknite na OK.

Poznámka: Dostupné modely a ich schopnosti závisia od konfigurácie vašej LiteLLM proxy. Na popisy obrázkov sa uistite, že je proxy nakonfigurovaná s modelmi, ktoré podporujú prácu s obrazom.

### Ako nastaviť Seer

Seer spúšťa model PaliGemma2 priamo na vašom počítači, bez kľúča API a bez pripojenia ku cloudu. Majte na pamäti, že ide o model, ktorý vie iba vytvárať popisky; pokyny ani doplňujúce otázky nie sú podporované.

1. Nainštalujte [démona Seer](https://github.com/recursia-lab/Seer). K dispozícii je inštalátor spúšťaný jediným príkazom pre Windows (.bat) a Linux/macOS (.sh).
2. V dialógovom okne nastavenia NVDA prejdite do kategórie Popis obsahu pomocou AI, zvoľte „Spravovať modely (alt+m)“ a vyberte „Seer (vyžaduje inštaláciu)“.
3. Predvolená adresa URL je `http://127.0.0.1:11435`. Ponechajte ju bez zmeny, pokiaľ ste nezmenili port démona.
4. Kliknite na OK. Skôr než požiadate o popis, démon musí byť spustený.

### Ako nastaviť Datalab Chandra 2

Datalab Chandra 2 je špičkový model na spracovanie dokumentov a OCR, špecializovaný na zložité rozloženia, tabuľky, formuláre, ručne písaný text, grafy a matematické vzorce. Dá sa používať cez spravované cloudové API spoločnosti Datalab, kontajner prevádzkovaný na vlastnej infraštruktúre alebo vlastnú inštanciu vLLM.

#### Možnosť A: Cloudové API spoločnosti Datalab (odporúčané)
1. Zaregistrujte si účet na [datalab.to](https://www.datalab.to). Nové účty dostanú skúšobné kredity zadarmo.
2. Prejdite na [stránku s kľúčmi API](https://www.datalab.to/app/keys) a vygenerujte kľúč API.
3. V dialógovom okne nastavenia NVDA prejdite do kategórie Popis obsahu pomocou AI, zvoľte „Spravovať modely (alt+m)“ a vyberte „Datalab Chandra 2“.
4. Do políčka „API kľúč“ zadajte svoj kľúč API.
5. Adresa URL je štandardne `https://www.datalab.to/api/v1/convert`. Režim spracovania (`fast`, `balanced` alebo `accurate`) môžete upraviť podľa svojich potrieb.
6. Kliknite na OK. Model bude teraz k dispozícii v ponuke Popisu obsahu pomocou AI.

#### Možnosť B: Vlastná prevádzka s vLLM
1. Spustite lokálny server vLLM s modelom Chandra 2 (napr. pomocou `chandra_vllm` alebo `vllm serve datalab-to/chandra-ocr-2`). Štandardne server beží na adrese `http://localhost:8000/v1`.
2. V nastaveniach NVDA -> Popis obsahu pomocou AI -> Spravovať modely -> „Datalab Chandra 2“ zadajte do políčka „Adresa URL“ svoj lokálny koncový bod (napr. `http://localhost:8000/v1`).
3. Ak sa názov modelu líši od predvoleného (`datalab-to/chandra-ocr-2`), nastavte ho, políčko API kľúč nechajte prázdne (alebo zadajte bearer token, ak je zapnuté overovanie) a kliknite na OK.

## Použitie

Štandardne je priradených šesť klávesových skratiek:

* NVDA+shift+i: Zobrazí sa ponuka s otázkou, či chcete popísať aktuálny objekt pod fokusom, aktuálny prezeraný objekt, snímku z fyzickej kamery, celú obrazovku, alebo ovládať počítač pomocou AI.
* NVDA+shift+u: Popíše obsah aktuálne prezeraného objektu pomocou AI.
* NVDA+shift+y: Popíše obrázok (alebo cestu k súboru s obrázkom) v schránke pomocou AI.
* NVDA+shift+j: Popíše umiestnenie tváre v zábere vybranej kamery. Ak máte pripojených viac kamier, prejdite do ponuky doplnku (NVDA+shift+i) a vyberte tú, ktorú chcete použiť, pomocou položky „vybrať kameru“ v podponuke detekcia tváre.
* NVDA+alt+c: Otvorí dialóg konverzácie s AI, kde môžete klásť doplňujúce otázky.
* NVDA+control+shift+p: Pozastaví alebo obnoví prebiehajúcu reláciu ovládania počítača.

Sedem klávesových skratiek v predvolenom stave nie je priradených:

* Popísať obsah objektu pod fokusom pomocou AI.
* Urobiť snímku obrazovky a potom ju popísať pomocou AI.
* Urobiť snímku pomocou vybranej kamery a potom ju popísať pomocou AI.
* Zrušiť prebiehajúcu reláciu ovládania počítača.
* Urobiť snímku aktuálneho objektu pod fokusom a skopírovať ju do schránky.
* Urobiť snímku aktuálneho prezeraného objektu a skopírovať ju do schránky.
* Urobiť snímku celej obrazovky a skopírovať ju do schránky.

Tieto tri príkazy na kopírovanie nájdete aj v podponuke „Kopírovať obrázok do schránky“ v ponuke NVDA+shift+i. Neodosielajú nič žiadnej službe AI. Použite ich, keď chcete snímku vložiť do Be My AI alebo inej aplikácie, ktorú tento doplnok nepodporuje. Skopírovaný obrázok nahradí predchádzajúci obsah schránky.

Neváhajte si ich kedykoľvek prispôsobiť v dialógu Klávesové príkazy.

### Doplňujúce otázky k popisu

Niekedy odpoveď, ktorú od AI dostanete, nestačí. Obrázok môže mať nízku kvalitu, môže byť neúplný alebo obsahovať nežiaduce detaily. Možno sa chcete zamerať len na určitú časť alebo urobiť ostrejšiu snímku bez straty kontextu.
Po prijatí popisu môžete stlačiť NVDA+alt+c alebo v kontextovej ponuke Popisu obsahu pomocou AI (NVDA+shift+i) vybrať „Doplňujúca otázka k predchádzajúcemu popisu“. Štandardne je fokus v políčku na správu.
Ak chcete pridať ďalší obrázok, nechajte okno konverzácie otvorené a používajte doplnok ako obvykle. Keď urobíte snímku (či už z kamery, ovládacieho prvku, snímku obrazovky atď.), budete vyzvaní, či ju chcete priložiť k aktuálnej relácii, alebo začať novú.

### Ovládanie počítača

Ovládanie počítača umožňuje doplnku Popis obsahu pomocou AI ovládať aktívnu aplikáciu myšou a klávesnicou potom, čo popíšete úlohu. To môže pomôcť s úlohami, ktoré je ťažké alebo nemožné prístupne dokončiť ručne.

Keďže tým dávate modelu AI kontrolu nad svojím počítačom, používajte túto funkciu opatrne. Doplnok si pred spustením vyžiada súhlas, priebežne hlási vykonávané akcie a pred potenciálne rizikovými akciami sa opýta. Za to, čo vykoná, zodpovedáte vy, preto reláciu sledujte a nepoužívajte ju na citlivú prácu alebo prácu, ktorú je ťažké vrátiť späť.

Ovládanie počítača môžete kedykoľvek pozastaviť alebo obnoviť klávesovou skratkou `NVDA+Control+Shift+P`. Počas pozastavenia doplnok nepokračuje ďalšou akciou, kým ho neobnovíte.

Doplnok stav ovládania signalizuje tónmi. Vysoké pípnutie znamená, že model preberá alebo znovu preberá kontrolu. Nízke pípnutie znamená, že ovládanie bolo pozastavené, buď preto, že ste ho pozastavili vy, alebo preto, že model potrebuje vašu odpoveď. Krátke nízke chybové pípnutie znamená, že relácia skončila kvôli chybe API.

Počas prebiehajúcej relácie ovládania model pred odoslaním vstupu oznámi, čo sa chystá urobiť. Kým toto oznámenie nedohovorí, nič sa nestane, pokiaľ oznámenie neprerušíte klávesom `Control` a nenecháte akciu prebehnúť skôr.

Ak si model nie je istý, ako akciu dokončiť, potrebuje viac informácií alebo vám inak odovzdá slovo, relácia sa pozastaví a do popredia sa prenesie dialóg Ovládanie počítača. Napíšte doň doplňujúcu správu a pokračujte v konverzácii, alebo dialóg zatvorte a reláciu ukončite.

Táto funkcia funguje iba s modelmi, ktoré poskytujú nástroj na ovládanie počítača: GPT-5.4, GPT-5.4 mini, GPT-5.5, GPT-5.5 pro, GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna, Claude 4.5 Sonnet, Claude 4.5 Opus, Claude 4.6 Sonnet, Claude 4.6 Opus, Claude 4.7 Opus, Claude 4.8 Opus, Claude 5 Sonnet, Claude 5 Opus, Claude 5 Fable, Claude 5.1 Fable, Claude 5.2 Fable, Claude 5.5 Haiku, Claude 5.5 Sonnet a Claude 5.5 Opus. Ostatné modely vedia popisovať obrázky, ale neposkytujú štruktúrované akcie myši a klávesnice potrebné na ovládanie počítača.

Ako používať ovládanie počítača:

1. Nastavte a vyberte niektorý z podporovaných modelov.
2. Otvorte aplikáciu alebo okno, s ktorým má model pracovať.
3. Stlačte `NVDA+shift+i` a zvoľte „Ovládať počítač...“.
4. Napíšte úlohu, ktorú chcete vykonať, a stlačte Odoslať.
5. Prezrite si žiadosť o súhlas. Ak reláciu povolíte, sledujte vykonávané akcie a rizikové akcie schváľte alebo zrušte.

Poznámka: Túto funkciu považujte za beta verziu. Aktívne pracujeme na tom, aby bola implementácia spoľahlivejšia.

## Závislosti

Niektoré knižnice, ktoré tento doplnok potrebuje, sú príliš veľké na to, aby boli súčasťou balíčka doplnku. Namiesto toho sa vás NVDA pri prvom spustení s nainštalovaným doplnkom opýta, či ich chcete stiahnuť. Vyberte Áno, počkajte na dokončenie sťahovania a NVDA sa reštartuje.

Sťahuje sa súbor zip s veľkosťou približne 35 až 70 MB v závislosti od vašej verzie NVDA. Pochádza zo stránky [libs-release](https://github.com/cartertemm/AI-content-describer/releases/tag/libs-release) tohto repozitára. Ak GitHub nie je dostupný, doplnok ponúkne stiahnutie zo zrkadla, ktoré poskytuje čínska komunita NVDA.

Súbor zip obsahuje:

* [NumPy](https://numpy.org/): výpočty s poľami, vyžaduje ho OpenCV.
* [OpenCV](https://opencv.org/) (`cv2`): vyhľadáva vašu tvár v obraze z webovej kamery pre funkciu detekcie tváre.
* [Pillow](https://python-pillow.org/) (`PIL`): robí snímky obrazovky a prevádza ich na obrázky, ktoré modely AI dokážu prečítať.
* [Markdown](https://python-markdown.github.io/): zobrazuje popisy s formátovaním, napríklad s nadpismi, zoznamami a tabuľkami.
* [pygrabber](https://github.com/andreaschiavinato/python_grabber): vypisuje webové kamery pripojené k vášmu počítaču.
* Niekoľko modulov zo štandardnej knižnice Pythonu, ktoré NVDA neobsahuje (`html`, `xml`, `pathlib`, `secrets` a `_markupbase`). Potrebujú ich vyššie uvedené knižnice.

Súbory sa ukladajú do priečinka s názvom `aic-py-`, za ktorým nasleduje verzia Pythonu v NVDA, napríklad `aic-py-3.13`. Tento priečinok sa nachádza vo vašom priečinku s používateľskou konfiguráciou NVDA, zvyčajne `%APPDATA%\nvda`. Každá verzia Pythonu má vlastný priečinok, takže doplnok knižnice stiahne znova, keď nové vydanie NVDA zmení verziu Pythonu. Odinštalovaním doplnku sa vymaže priečinok pre aktuálnu verziu Pythonu v NVDA.

Ak sťahovanie nefunguje, môžete knižnice nainštalovať sami. Stiahnite si `aic-py-3.13.zip` (alebo súbor pre verziu Pythonu vo vašom NVDA) zo stránky libs-release, rozbaľte ho do priečinka s používateľskou konfiguráciou NVDA a reštartujte NVDA.

## Zostavenie doplnku

Na vytvorenie balíčka doplnku zo zdrojových kódov budete potrebovať:

* distribúciu jazyka Python (odporúčame verziu 3.7 alebo novšiu). Inštalačné programy pre systém Windows nájdete na [webových stránkach Pythonu](https://www.python.org). Upozorňujeme, že v súčasnosti príprava zdrojového kódu NVDA a obsiahnutých modulov tretích strán vyžaduje 32-bitovú verziu Pythonu 3.7.
* Scons - [Webové stránky](https://www.scons.org/) - verzia 4.3.0 alebo novšia. Môžete ho nainštalovať prostredníctvom PIP. `pip install scons`
* Markdown 3.3.0 alebo novší. `pip install markdown`

Potom otvorte vybraný terminál:

```
git clone https://github.com/cartertemm/AI-content-describer.git
cd AI-content-describer
scons
```

Po dokončení príkazu `scons` bude do koreňového adresára tohto repozitára umiestnený súbor *.nvda-addon pripravený na testovanie a vydanie.

Ak pridáte ďalšie reťazce, ktoré je potrebné preložiť, je dôležité znova zostaviť súbor .pot:

```
scons pot
```

## Ako doplnok preložiť

Na počítači so systémom Windows:

* stiahnite si [poedit](https://poedit.net/). Pomocou tohto programu preložíte jednotlivé reťazce z angličtiny.
* stiahnite si súbor .pot so všetkými reťazcami [tu](https://raw.githubusercontent.com/cartertemm/AI-content-describer/main/AIContentDescriber.pot)
* Otvorte práve stiahnutý súbor v programe poedit. V zobrazenom okne kliknite na tlačidlo „Vytvoriť nový preklad“ a vyberte cieľový jazyk.
* Prejdite a preveďte obsah zdrojového textu do cieľového jazyka a potom ho vložte do poľa pre preklad. Ak chcete získať ďalšiu nápovedu, neváhajte kliknúť pravým tlačidlom myši na položku zoznamu -> výskyty kódu, potom prejdite o riadok vyššie a prečítajte si komentár začínajúci slovami „# Translators: “. Tieto komentáre sú navyše sprístupnené na jednom mieste v súbore .pot.
* Po dokončení kliknite na Súbor -> Uložiť alebo stlačte klávesovú skratku ctrl+s a potom vyberte miesto, kam sa nový súbor .mo a .po uloží. Tieto súbory mi pošlite e-mailom alebo priložte v pull requeste.
* Preložte obsah súboru readme.md (tento súbor). Priložte ho tiež!

## Spolupracovníci

Všetku vašu spoluprácu si veľmi vážim a uvediem ju tu.
Na doplnku sa podieľali:

* [Cary Rowen](https://github.com/cary-rowen): sprevádzkoval doplnok pre čínskych používateľov pomocou zrkadlenia závislostí, pridal podporu poskytovateľa Vivo Blue
* [Mazen](https://github.com/mzanm): implementácia Markdownu, ďalšie príspevky do kódu
* [Kostenkov-2021](https://github.com/Kostenkov-2021): ruský preklad
* [Nidza07](https://github.com/nidza07): srbský preklad
* [Heorhii Halas](nvda.translation.uk@gmail.com) a [George-br](https://github.com/George-br): ukrajinský preklad
* [Umut Korkmaz](umutkork@gmail.com): turecký preklad
* [Platinum_Hikari](urbain_onces.0r@icloud.com): francúzsky preklad
* [Lukas](https://4sensegaming.cz): český preklad
* [Michaela](https://technologiebezzraku.sk): slovenský preklad

Narazili ste na problém? Popíšte ho v [issue trackeri](https://github.com/cartertemm/AI-content-describer/issues)

Máte návrh na novú funkciu? Vytvorte ticket aj pre ňu a môžeme sa dohodnúť na jej implementácii. Pull requesty bez priradených issues budú preskúmané, ale pravdepodobne zaberú všetkým viac času, najmä ak sa rozhodnem, že nová oprava alebo funkcia musí fungovať inak, ako ste pôvodne navrhovali.

Preklady uvítam s otvoreným náručím. Čím viac ľudí bude mať k tejto skvelej technológii prístup, tým lepšie!

Pokiaľ nemáte Github alebo ho radšej nepoužívate, môžete mi [poslať e-mail](mailto:carter@ctemm.me) - carter (zavináč) ctemm (bodka) me.

Ďakujem za vašu podporu!
