# Doplnìk Popis obsahu pomocí AI pro NVDA

Tento doplnìk umožòuje získat podrobné popisy obrázkù, ovládacích prvkù uživatelského rozhraní a dalšího nepøístupného vizuálního obsahu.

S využitím multimodálních schopností pokroèilých modelù umìlé inteligence a algoritmù poèítaèového vidìní se snažíme poskytovat nejlepší možné popisy obsahu svého druhu a zvýšit tak vaši nezávislost na pomoci vidících. Další informace o použitých modelech naleznete v pøíslušné èásti tohoto dokumentu.

## Funkce

* Popis objektu, který má právì fokus, aktuálnì prohlíženého objektu, celé obrazovky nebo snímku z pøipojené kamery.
* Popis jakéhokoli obrázku, který jste zkopírovali do schránky, a už se jedná o obrázek z e-mailu nebo napø. cestu v prùzkumníku Windows.
* Zjištìní, zda se tváø uživatele nachází uprostøed zábìru, pomocí algoritmù poèítaèového vidìní (nevyžaduje placený pøístup k žádnému rozhraní API)
* Podpora více poskytovatelù modelù (GPT4 od OpenAI, Gemini od Googlu, Claude 3 od Anthropic a llama.cpp).
* Podpora pro širokou škálu formátù obrázkù, vèetnì PNG (.png), JPEG (.jpeg a .jpg), WEBP (.webp) a neanimovaného GIF (.gif).
* Volitelné ukládání odpovìdí do mezipamìti pro úsporu kvóty API
* Pro pokroèilé použití si mùžete nastavit pokyn a poèet tokenù tak, abyste získané informace pøizpùsobili svým potøebám.
* Vykreslování ve formátu Markdown pro snadný pøístup ke strukturovaným informacím (staèí na konci vašeho pokynu uvést napø. „odpovìz ve formátu Markdown“).

## Možnosti využití

Tento projekt mìl nìkolik hlavních motivací.

NVDA dokáže už ve výchozí instalaci provádìt optické rozpoznávání znakù (OCR), což je obrovský pokrok. Pokud se snažíte získat text z obrázku nebo dokumentu PDF, pak hledáte právì tuto funkci.

OCR však dokáže analyzovat pouze data, která *mohou* obsahovat text. Nedokáže objasnit kontext, pøedmìty, které se na obrázcích mohou nacházet, a vztahy mezi nimi. Tìch je internet plný. Loga, portréty, memy, ikony, grafy, diagramy, sloupcové/øádkové grafy... Na co si vzpomenete. Jsou všude a obvykle nejsou ve formátu, který by uživatelé odeèítaèe obrazovky dokázali interpretovat.
Donedávna jsme neochvìjnì spoléhali na to, že autoøi obsahu budou poskytovat alternativní textové popisy. I když je to stále nutností, tìžko zmìníme skuteènost, že vysoký standard kvality bývá spíš jen výjimkou, nikoli pravidlem.

Nyní máte možnosti témìø neomezené. Mùžete napø:

* Vizualizovat si plochu nebo konkrétní okno, abyste pochopili rozmístìní jednotlivých ikon pøi školení ostatních.
* Získat podrobné informace z videoher, virtuálních poèítaèù atd. v pøípadì nedostateèného nebo chybìjícího ozvuèení.
* Zjistit, co je zobrazeno v grafu
* Pochopit snímky obrazovky nebo sdílení obrazovky v online komunikaèních aplikacích, jako je Zoom nebo Microsoft Teams
* Pøed natáèením videí nebo úèastí na online schùzkách se ujistit, že se váš oblièej nachází zøetelnì v zábìru kamery a že pozadí vypadá profesionálnì.

## Modely

* [GPT4 vision](https://platform.openai.com/docs/guides/vision)
* [Google Gemini pro vision](https://blog.google/technology/ai/google-gemini-ai/)
* [Claude 3 (Haiku, Sonett a Opus)](https://docs.anthropic.com/claude/docs/vision)
* [llama.cpp (extrémnì nestabilní a pomalý, v závislosti na vašem hardwaru, testováno pøi práci s modely llava-v1.5/1.6, BakLLaVA, Obsidian a MobileVLM 1.7B/3B)](https://github.com/ggerganov/llama.cpp)

Pro zprovoznìní jednotlivých modelù postupujte podle níže uvedených pokynù.

## Jak zaèít

Stáhnìte si nejnovìjší verzi doplòku z [tohoto odkazu](https://github.com/cartertemm/AI-content-describer/releases/latest/). Otevøete stažený soubor v poèítaèi, kde máte nainstalované NVDA, a poté podle níže uvedených pokynù získejte klíè API od nìkterého z podporovaných poskytovatelù modelù.
Pokud si nejste jisti, který model použít, vývojáøi a testeøi tohoto doplòku se shodují na tom, že Gemini aktuálnì nabízí rozumnìjší ceny, zatímco OpenAI zøejmì poskytuje vyšší míru pøesnosti rozpoznávání. Claude 3 haiku je nejlevnìjší a nejrychlejší možností, ale jeho kvalita je sporná.
Tyto výsledky jsou samozøejmì velmi závislé na daném úkolu, takže doporuèujeme experimentovat s rùznými modely a pokyny, abyste zjistili, co vám funguje nejlépe.

### Jak získat API klíè od OpenAI:

1. Pøejdìte na stránku https://platform.openai.com/account/api-keys
2. Pokud ještì nemáte úèet, vytvoøte si ho. Pokud ano, pøihlaste se.
3. Na stránce API keys kliknìte na tlaèítko „Create new secret key“. Zkopírujte jej do schránky.
4. Na svùj uživatelský úèet vložte alespoò 1 dolar
5. V dialogovém oknì nastavení NVDA pøejdìte do kategorie Popis obsahu pomocí AI, poté vyberte „Spravovat modely (alt+m)“, jako poskytovatele vyberte „GPT4 Vision“, klávesou tab pøejdìte do políèka API klíè a vložte sem právì vytvoøený klíè.

V dobì, kdy byl tento dokument vytvoøen, zaèala OpenAI k novým vývojáøským úètùm vydávat kredity zdarma, které lze používat po dobu tøí mìsícù, poté propadají. Po uplynutí této lhùty si budete muset kredity zakoupit. Obvyklá spotøeba by nikdy nemìla pøesáhnout 5,00 USD mìsíènì. Pro pøedstavu, pùvodní verze tohoto doplòku byla vyvinuta za necelý dolar. Kdykoli se mùžete pøihlásit ke svému úètu OpenAI a kliknutím na „usage“ zjistit, kolik kreditù vám ještì zbývá.

### Jak získat API klíè od Googlu

Nejprve je tøeba vytvoøit si Google Workspace projekt pomocí tohoto odkazu. Ujistìte se, že jste pøihlášeni ke svému úètu. https://console.cloud.google.com/projectcreate
2. Zadejte název v rozsahu ètyø až tøiceti znakù, napøíklad „gemini“ nebo „NVDA add-on“.
3. Pøejdìte na tuto adresu: https://makersuite.google.com/app/apikey
4. Kliknìte na tlaèítko „create API key“
5. V dialogovém oknì nastavení NVDA pøejdìte do kategorie Popis obsahu pomocí AI, poté vyberte „Spravovat modely (alt+m)“, jako poskytovatele vyberte „Google Gemini“, klávesou tab pøejdìte do políèka API klíè a vložte sem právì vygenerovaný klíè.

### Jak získat API klíè od Anthropic

1. Pøihlaste se do [konzole Anthropic](https://console.anthropic.com/login).
2. Kliknìte na Your profile -> API keys.
3. Kliknìte na tlaèítko Create key.
4. Zadejte název klíèe, napøíklad „AIContentDescriber“, poté kliknìte na „Create Key“ a zkopírujte hodnotu, která se zobrazí. Tuto hodnotu vložíte do políèka API klíè v kategorii Popis obsahu pomocí AI v dialogovém oknì Nastavení NVDA -> Spravovat modely -> Claude 3.
5. Pokud jste tak ještì neuèinili, zakupte si kredity v hodnotì alespoò 5 USD na stránce Plans na adrese https://console.anthropic.com/settings/plans.

### Jak nastavit llama.cpp

Tento poskytovatel je v souèasné dobì ponìkud chybový a vaše zkušenosti se mohou lišit. O zprovoznìní tohoto modelu by se mìli pokoušet opravdu jen pokroèilí uživatelé se zájmem o provozování lokálních self-hosted modelù a s hardwarem, který k tomu potøebují.

1. Stáhnìte si llama.cpp. V dobì vytvoøení tohoto dokumentu tento [pull request](https://github.com/ggerganov/llama.cpp/pull/5882) odstraòuje podporu pro multimodální schopnosti, takže vy budete chtít použít [poslední verzi s touto podporou](https://github.com/ggerganov/llama.cpp/releases/tag/b2356).
Pokud používáte grafickou kartu Nvidia s podporou CUDA, stáhnìte si tyto pøedpøipravené binární soubory:
[llama-b2356-bin-win-cublas-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/llama-b2356-bin-win-cublas-cu12.2.0-x64.zip) a [cudart-llama-bin-win-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/cudart-llama-bin-win-cu12.2.0-x64.zip).
Popis krokù pro zprovoznìní tohoto modelu s jinou grafickou kartou je nad rámec tohoto dokumentu, ale najdete jej v readme souboru pro llama.cpp.
2. Oba tyto soubory rozbalte do stejné složky.
3. Z Huggingface si stáhnìte kvantifikované soubory modelù, které chcete použít. Pro LLaVA 1.6 Vicuna 7B: [llava-v1.6-vicuna-7b.Q4_K_M.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/llava-v1.6-vicuna-7b.Q4_K_M.gguf) a [mmproj-model-f16.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/mmproj-model-f16.gguf).
4. Tyto soubory vložte do složky s ostatními spustitelnými soubory llama.cpp.
5. Z pøíkazového øádku spuste server llama.cpp a pøedejte mu soubory .gguf pro model a multimodální projektor (podle následujících pokynù):
`server.exe -m llava-v1.6-vicuna-7b.Q4_K_M.gguf --mmproj mmproj-model-f16.gguf`
6. V dialogovém oknì nastavení NVDA pøejdìte do kategorie Popis obsahu pomocí AI, poté zvolte „Spravovat modely (alt+m)“, jako poskytovatele vyberte „llama.cpp“, klávesou tab pøejdìte do políèka Adresa URL a zadejte koncový bod zobrazený v konzoli (výchozí hodnota je „http://localhost:8080“).
7. Pøípadnì mùžete nìkteré z tìchto krokù vynechat a spustit llama.cpp na vzdáleném serveru s vyšším výkonem, než má váš lokální poèítaè, a zadat pøíslušný koncový bod podle toho.

## Použití

Ve výchozím nastavení jsou pøiøazeny ètyøi klávesové zkratky:

* NVDA+shift+i: Zobrazí se nabídka s dotazem, zda chcete popsat aktuální objekt pod fokusem, aktuální prohlížený objekt, snímek z pøipojené kamery, nebo celou obrazovku.
* NVDA+shift+u: Popíše obsah aktuálnì prohlíženého objektu.
* NVDA+shift+y: Popíše obrázek (nebo cestu k souboru s obrázkem) ve schránce.
* NVDA+shift+j: Popíše umístìní tváøe v zábìru vybrané kamery. Pokud máte pøipojeno více kamer, pøejdìte do nabídky doplòku (NVDA+shift+i) a vyberte tu, kterou chcete použít, pomocí položky „vybrat kameru“ v podnabídce detekce tváøe.

Tøi klávesové zkratky ve výchozím stavu pøiøazeny nejsou:

* Popsat obsah objektu pod fokusem.
* Poøídit snímek obrazovky a poté jej popsat.
* Poøídit snímek pomocí vybrané kamery a poté jej popsat.

Neváhejte si je kdykoli pøizpùsobit v dialogu  Klávesové pøíkazy.

## Sestavení doplòku

K vytvoøení balíèku doplòku ze zdrojových kódù budete potøebovat:

* distribuci jazyka Python (doporuèujeme verzi 3.7 nebo novìjší). Instalaèní programy pro systém Windows naleznete na [webových stránkách Pythonu](https://www.python.org). Upozoròujeme, že v souèasné dobì pøíprava zdrojového kódu NVDA a obsažených modulù tøetích stran vyžaduje 32bitovou verzi Pythonu 3.7.
* Scons - [Webové stránky](https://www.scons.org/) - verze 4.3.0 nebo novìjší. Mùžete jej nainstalovat prostøednictvím PIP. `pip install scons`
* Markdown 3.3.0 nebo novìjší. `pip install markdown`

Poté otevøete vybraný terminál:

```
git clone https://github.com/cartertemm/AI-content-describer.git
cd AI-content-describer
scons
```

Po dokonèení pøíkazu `scons` bude do koøenového adresáøe umístìn soubor *.nvda-addon.

Pokud pøidáte další øetìzce, které je tøeba pøeložit, je dùležité znovu sestavit soubor .pot:

```
scons pot
```

## Jak doplnìk pøeložit

Na poèítaèi se systémem Windows:

* stáhnìte si [poedit](https://poedit.net/). Pomocí tohoto programu pøeložíte jednotlivé øetìzce z angliètiny.
* stáhnìte si soubor .pot se všemi øetìzci [zde](https://raw.githubusercontent.com/cartertemm/AI-content-describer/main/AIContentDescriber.pot).
* Otevøete právì stažený soubor v programu poedit. V zobrazeném oknì kliknìte na tlaèítko „Vytvoøit nový pøeklad“ a vyberte cílový jazyk.
* Projdìte a pøeveïte obsah zdrojového textu do cílového jazyka a poté jej vložte do pole pro pøeklad. Chcete-li získat další nápovìdu, neváhejte kliknout pravým tlaèítkem myši na položku seznamu -> výskyty kódu, poté pøejdìte o øádek výše a pøeètìte si komentáø zaèínající slovy „# Translators: „. Tyto komentáøe jsou navíc zpøístupnìny na jednom místì v souboru .pot.
* Po dokonèení kliknìte na Soubor -> Uložit nebo stisknìte klávesovou zkratku ctrl+s a poté vyberte místo, kam se nový soubor .mo a .po uloží. Tyto soubory mi pošlete e-mailem nebo pøiložte v pull requestu.
* Pøeložte obsah souboru readme.md (tento soubor). Pøiložte ho také!

## Spolupracovníci

Veškeré vaší spolupráce si velice vážím a uvedu ji zde.
Na doplòku se podíleli:

* [Mazen](https://github.com/mzanm)
* [Kostenkov-2021](https://github.com/Kostenkov-2021)
* [nidza07](https://github.com/nidza07)
* [Heorhii Halas](nvda.translation.uk@gmail.com)

Narazili jste na problém? Popište ho v [issue trackeru](https://github.com/cartertemm/AI-content-describer/issues)

Máte návrh na novou funkci? Vytvoøte pro ni také ticket a mùžeme se domluvit na její implementaci. Pull requesty bez pøiøazených issues budou pøezkoumány, ale pravdìpodobnì zaberou více èasu, zejména pokud se rozhodnu, že nová oprava nebo funkce musí fungovat jinak, než jak jste pùvodnì navrhovali.

Pøeklady uvítám s otevøenou náruèí. Èím více lidí bude mít k této skvìlé technologii pøístup, tím lépe!

Pokud nemáte Github nebo ho radìji nepoužíváte, mùžete mi [poslat e-mail](mailto:cartertemm@gmail.com) - cartertemm (zavináè) gmail (teèka) com (pouze v angliètinì).

Dìkuji za vaši podporu!