# Doplnok Popis obsahu pomocou AI pre NVDA

Tento doplnok umožňuje získať podrobné popisy obrázkov, ovládacích prvkov používateľského rozhrania a ďalšieho neprístupného vizuálneho obsahu.

S využitím multimodálnych schopností pokročilých modelov umelej inteligencie a algoritmov počítačového videnia sa snažíme poskytovať najlepšie možné popisy obsahu svojho druhu a zvýšiť tak vašu nezávislosť od pomoci vidiacich. Ďalšie informácie o použitých modeloch nájdete v príslušnej časti tohto dokumentu.

## Funkcie

* Popis objektu, ktorý má práve fokus, aktuálne prezeraného objektu, celej obrazovky alebo snímky z pripojenej kamery.
* Popis akéhokoľvek obrázka, ktorý ste skopírovali do schránky, či už sa jedná o obrázok z e-mailu alebo napr. cestu v prieskumníkovi Windows.
* Zistenie, či sa tvár užívateľa nachádza uprostred záberu, pomocou algoritmov počítačového videnia (nevyžaduje platený prístup k žiadnemu rozhraniu API)
* Podpora viacerých poskytovateľov modelov (GPT4 od OpenAI, Gemini od Googlu, Claude 3 od Anthropic a llama.cpp).
* Podpora pre širokú škálu formátov obrázkov, vrátane PNG (.png), JPEG (.jpeg a .jpg), WEBP (.webp) a neanimovaného GIF (.gif).
* Voliteľné ukladanie odpovedí do medzipamäte pre úsporu kvóty API
* Pre pokročilé použitie si môžete nastaviť pokyn a počet tokenov tak, aby ste získané informácie prispôsobili svojim potrebám.
* Vykresľovanie vo formáte Markdown pre ľahký prístup k štruktúrovaným informáciám (stačí na konci vášho pokynu uviesť napr. „odpovedz vo formáte Markdown“).

## Možnosti využitia

Tento projekt mal niekoľko hlavných motivácií.

NVDA dokáže už v základnej inštalácii vykonávať optické rozpoznávanie znakov (OCR), čo je obrovský pokrok. Pokiaľ sa snažíte získať text z obrázku alebo dokumentu PDF, potom hľadáte práve túto funkciu.

OCR však dokáže analyzovať iba dáta, ktoré *môžu* obsahovať text. Nedokáže objasniť kontext, predmety, ktoré sa na obrázkoch môžu nachádzať, a vzťahy medzi nimi. Tých je internet plný. Logá, portréty, mémy, ikony, grafy, diagramy, stĺpcové/čiarové grafy... Na čo si spomeniete. Sú všade a obvykle nie sú vo formáte, ktorý by používatelia čítača obrazovky dokázali interpretovať.
Donedávna sme sa neochvejne spoliehali na to, že autori obsahu budú poskytovať alternatívne textové popisy. Aj keď je to stále nutnosť, ťažko zmeníme skutočnosť, že vysoký štandard kvality býva skôr výnimkou, nie pravidlom.

Teraz máte možnosti takmer neobmedzené. Môžete napr:

* Vizualizovať si plochu alebo konkrétne okno, aby ste pochopili rozmiestnenie jednotlivých ikon pri školení ostatných.
* Získať podrobné informácie z videohier, virtuálnych počítačov atď. v prípade nedostatočného alebo chýbajúceho ozvučenia.
* Zistiť, čo je zobrazené v grafe
* Pochopiť snímky obrazovky alebo zdieľanie obrazovky v online komunikačných aplikáciách, ako je Zoom alebo Microsoft Teams
* Pred natáčaním videí alebo účasťou na online stretnutiach sa uistiť, že sa vaša tvár nachádza zreteľne v zábere kamery a že pozadie vyzerá profesionálne.

## Modely

* [GPT4 vision](https://platform.openai.com/docs/guides/vision)
* [Google Gemini pre vision](https://blog.google/technology/ai/google-gemini-ai/)
* [Claude 3 (Haiku, Sonett a Opus)](https://docs.anthropic.com/claude/docs/vision)
* [llama.cpp (extrémne nestabilný a pomalý, v závislosti na vašom hardvéri, testované pri práci s modelmi llava-v1.5/1.6, BakLLaVA, Obsidian a MobileVLM 1.7B/3B)](https://github.com/ ggerganov/flama.cpp)

Pre sprevádzkovanie jednotlivých modelov postupujte podľa nižšie uvedených pokynov.

## Ako začať

Stiahnite si najnovšiu verziu doplnku z [tohto odkazu](https://github.com/cartertemm/AI-content-describer/releases/latest/). Otvorte stiahnutý súbor v počítači, kde máte nainštalované NVDA, a potom podľa nižšie uvedených pokynov získajte kľúč API od niektorého z podporovaných poskytovateľov modelov.
Pokiaľ si nie ste istí, ktorý model použiť, vývojári a testeri tohto doplnku sa zhodujú na tom, že Gemini aktuálne ponúka rozumnejšie ceny, zatiaľ čo OpenAI zrejme poskytuje vyššiu mieru presnosti rozpoznávania. Claude 3 haiku je najlacnejšou a najrýchlejšou možnosťou, ale jeho kvalita je sporná.
Tieto výsledky sú samozrejme veľmi závislé od danej úlohy, takže odporúčame experimentovať s rôznymi modelmi a pokynmi, aby ste zistili, čo vám funguje najlepšie.

### Ako získať API kľúč od OpenAI:

1. Prejdite na stránku https://platform.openai.com/account/api-keys
2. Ak ešte nemáte účet, vytvorte si ho. Ak áno, prihláste sa.
3. Na stránke API keys kliknite na tlačidlo „Create new secret key“. Skopírujte ho do schránky.
4. Na svoj užívateľský účet vložte aspoň 1 dolár
5. V dialógovom okne nastavenia NVDA prejdite do kategórie Popis obsahu pomocou AI, potom vyberte „Spravovať modely (alt+m)“, ako poskytovateľa vyberte „GPT4 Vision“, klávesom tab prejdite do políčka API kľúč a vložte sem práve vytvorený kľúč.

V čase, keď bol tento dokument vytvorený, začala OpenAI k novým vývojárskym účtom vydávať kredity zadarmo, ktoré je možné používať po dobu troch mesiacov, potom prepadnú. Po uplynutí tejto lehoty si budete musieť kredity zakúpiť. Zvyčajná spotreba by nikdy nemala presiahnuť 5,00 USD mesačne. Pre predstavu, pôvodná verzia tohto doplnku bola vyvinutá za necelý dolár. Kedykoľvek sa môžete prihlásiť k svojmu účtu OpenAI a kliknutím na „usage“ zistiť, koľko kreditov vám ešte zostáva.

### Ako získať API kľúč od Googlu

1. Najprv je potrebné vytvoriť Google Workspace projekt pomocou tohto odkazu. Uistite sa, že ste prihlásení k svojmu účtu. https://console.cloud.google.com/projectcreate
2. Zadajte názov v rozsahu štyroch až tridsiatich znakov, napríklad „gemini“ alebo „NVDA add-on“.
3. Prejdite na túto adresu: https://makersuite.google.com/app/apikey
4. Kliknite na tlačidlo „create API key“
5. V dialógovom okne nastavenia NVDA prejdite do kategórie Popis obsahu pomocou AI, potom vyberte „Spravovať modely (alt+m)“, ako poskytovateľa vyberte „Google Gemini“, klávesom tab prejdite do políčka API kľúč a vložte sem práve vygenerovaný kľúč.

### Ako získať API kľúč od Anthropic

1. Prihláste sa do [konzoly Anthropic](https://console.anthropic.com/login).
2. Kliknite na Your profile -> API keys.
3. Kliknite na tlačidlo Create key.
4. Zadajte názov kľúča, napríklad „AIContentDescriber“, potom kliknite na „Create Key“ a skopírujte hodnotu, ktorá sa zobrazí. Túto hodnotu vložíte do políčka API kľúč v kategórii Popis obsahu pomocou AI v dialógovom okne Nastavenia NVDA -> Spravovať modely -> Claude 3.
5. Ak ste tak ešte neurobili, zakúpte si kredity v hodnote aspoň 5 USD na stránke Plans na adrese https://console.anthropic.com/settings/plans.

### Ako nastaviť llama.cpp

Tento poskytovateľ je v súčasnej dobe trochu chybný a vaše skúsenosti sa môžu líšiť. O sprevádzkovanie modelu by sa mali pokúšať naozaj len pokročilí používatelia so záujmom o prevádzkovanie lokálnych self-hosted modelov as hardvérom, ktorý na to potrebujú.

1. Stiahnite si llama.cpp. V čase vytvorenia tohto dokumentu tento [pull request](https://github.com/ggerganov/llama.cpp/pull/5882) odstraňuje podporu pre multimodálne schopnosti, takže vy budete chcieť použiť [poslednú verziu s touto podporou](https: //github.com/ggerganov/llama.cpp/releases/tag/b2356).
Ak používate grafickú kartu Nvidia s podporou CUDA, stiahnite si tieto predpripravené binárne súbory:
[llama-b2356-bin-win-cublas-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/llama-b2356-bin-win-cublas- cu12.2.0-x64.zip) a [cudart-flama-bin-win-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/cudart-llama -bin-win-cu12.2.0-x64.zip).
Popis krokov potrebných pre sprevádzkovanie tohto modelu s inou grafickou kartou je nad rámec tohto dokumentu, ale nájdete ho v readme súbore pre llama.cpp.
2. Obidva súbory rozbaľte do rovnakého priečinka.
3. Z Huggingface si stiahnite kvantifikované súbory modelov, ktoré chcete použiť. Pre LLaVA 1.6 Vicuna 7B: [llava-v1.6-vicuna-7b.Q4_K_M.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/llava- v1.6-vicuna-7b.Q4_K_M.gguf) a [mmproj-model-f16.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/mmproj -model-f16.gguf).
4. Tieto súbory vložte do priečinka s ostatnými spustiteľnými súbormi llama.cpp.
5. Z príkazového riadka spustite server llama.cpp a odovzdajte mu súbory .gguf pre model a multimodálny projektor (podľa nasledujúcich pokynov):
`server.exe -m llava-v1.6-vicuna-7b.Q4_K_M.gguf --mmproj mmproj-model-f16.gguf`
6. V dialógovom okne nastavenia NVDA prejdite do kategórie Popis obsahu pomocou AI, potom zvoľte „Spravovať modely (alt+m)“, ako poskytovateľa vyberte „llama.cpp“, klávesom tab prejdite do políčka Adresa URL a zadajte koncový bod zobrazený v konzole (predvolená hodnota je „http://localhost:8080“).
7. Prípadne môžete niektoré z týchto krokov vynechať a spustiť llama.cpp na vzdialenom serveri s vyšším výkonom, než má váš lokálny počítač, a zadať príslušný koncový bod podľa neho.

## Použitie

Štandardne sú priradené štyri klávesové skratky:

* NVDA+shift+i: Zobrazí sa ponuka s otázkou, či chcete popísať aktuálny objekt pod fokusom, aktuálny prezeraný objekt, snímku z pripojenej kamery, alebo celú obrazovku.
* NVDA+shift+u: Popíše obsah aktuálne prezeraného objektu.
* NVDA+shift+y: Popíše obrázok (alebo cestu k súboru s obrázkom) v schránke.
* NVDA+shift+j: Popíše umiestnenie tváre v zábere vybranej kamery. Ak máte pripojených viac kamier, prejdite do ponuky doplnku (NVDA+shift+i) a vyberte tú, ktorú chcete použiť, pomocou položky „vybrať kameru“ v podponuke detekcia tváre.

Tri klávesové skratky v predvolenom stave nie sú priradené:

* Popísať obsah objektu pod fokusom.
* Urobiť snímku obrazovky a potom ju popísať.
* Urobiť snímku pomocou vybranej kamery a potom ju popísať.

Neváhajte si ich kedykoľvek prispôsobiť v dialógu Klávesové príkazy.

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

Po dokončení príkazu `scons` bude do koreňového adresára umiestnený súbor *.nvda-addon.

Ak pridáte ďalšie reťazce, ktoré je potrebné preložiť, je dôležité znova zostaviť súbor .pot:

```
scons pot
```

## Ako doplnok preložiť

Na počítači so systémom Windows:

* stiahnite si [poedit](https://poedit.net/). Pomocou tohto programu preložíte jednotlivé reťazce z angličtiny.
* stiahnite si súbor .pot so všetkými reťazcami [tu](https://raw.githubusercontent.com/cartertemm/AI-content-describer/main/AIContentDescriber.pot).
* Otvorte práve stiahnutý súbor v programe poedit. V zobrazenom okne kliknite na tlačidlo „Vytvoriť nový preklad“ a vyberte cieľový jazyk.
* Prejdite a preveďte obsah zdrojového textu do cieľového jazyka a potom ho vložte do poľa pre preklad. Ak chcete získať ďalšiu nápovedu, neváhajte kliknúť pravým tlačidlom myši na položku zoznamu -> výskyty kódu, potom prejdite o riadok vyššie a prečítajte si komentár začínajúci slovami „# Translators: „. Tieto komentáre sú navyše sprístupnené na jednom mieste v súbore .pot.
* Po dokončení kliknite na Súbor -> Uložiť alebo stlačte klávesovú skratku ctrl+s a potom vyberte miesto, kam sa nový súbor .mo a .po uloží. Tieto súbory mi pošlite e-mailom alebo priložte v pull requeste.
* Preložte obsah súboru readme.md (tento súbor). Priložte ho tiež!

## Spolupracovníci

Všetku vašu spoluprácu si veľmi vážim a uvediem ju tu.
Na doplnku sa podieľali:

* [Mazen](https://github.com/mzanm)
* [Kostenkov-2021](https://github.com/Kostenkov-2021)
* [nidza07](https://github.com/nidza07)
* [Heorhii Halas](nvda.translation.uk@gmail.com)

Narazili ste na problém? Popíšte ho v [issue trackeri](https://github.com/cartertemm/AI-content-describer/issues)

Máte návrh na novú funkciu? Vytvorte ticket aj pre ňu a môžeme sa dohodnúť na jej implementácii. Pull requesty bez priradených issues budú preskúmané, ale pravdepodobne zaberú viac času, najmä ak sa rozhodnem, že nová oprava alebo funkcia musí fungovať inak, ako ste pôvodne navrhovali.

Preklady uvítam s otvoreným náručím. Čím viac ľudí bude mať k tejto skvelej technológii prístup, tým lepšie!

Pokiaľ nemáte Github alebo ho radšej nepoužívate, môžete mi [poslať e-mail](mailto:cartertemm@gmail.com) - cartertemm (zavináč) gmail (bodka) com (len v angličtine).

Ďakujem za vašu podporu!