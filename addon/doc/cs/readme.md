# Doplněk Popis obsahu pomocí AI pro NVDA

Tento doplněk umožňuje získat podrobné popisy obrázků, ovládacích prvků uživatelského rozhraní a dalšího nepřístupného vizuálního obsahu.

S využitím multimodálních schopností pokročilých modelů umělé inteligence a algoritmů počítačového vidění se snažíme poskytovat nejlepší možné popisy obsahu svého druhu a zvýšit tak vaši nezávislost. Další informace o použitých modelech naleznete v příslušné části tohoto dokumentu.

## Funkce

* Popis objektu, který má právě fokus, aktuálně prohlíženého objektu, celé obrazovky nebo snímku z vestavěné kamery
* Popis jakéhokoli obrázku, který jste zkopírovali do schránky, ať už se jedná o obrázek z e-mailu nebo cestu v Průzkumníku Windows
* Zkopírování obrázku objektu pod fokusem, prohlíženého objektu nebo celé obrazovky do schránky, abyste ho mohli vložit do jiných aplikací
* Zjištění, zda se tvář uživatele nachází uprostřed záběru, pomocí algoritmů počítačového vidění (nevyžaduje placený přístup k žádnému rozhraní API)
* Ovládání aktivní aplikace pomocí myši a klávesnice podporovanými modely, například u úkolů, které by jinak mohly být nepřístupné
* Ve výchozím nastavení zdarma, pro přístup k dalším modelům můžete volitelně přidat vlastní klíč API
* Podpora více poskytovatelů (GPT od OpenAI a bezplatná úroveň Pollinations, Gemini od Googlu, Mistral Large 4, Claude od Anthropic, Grok od xAI, Kimi od Moonshot AI, vivo BlueLM Vision přes NVDA-CN, Datalab Chandra 2, Ollama, llama.cpp, LiteLLM Proxy a Seer)
* Podpora široké škály formátů, včetně PNG (.png), JPEG (.jpeg a .jpg), WEBP (.webp) a neanimovaného GIF (.gif)
* Volitelné ukládání odpovědí do mezipaměti pro úsporu kvóty API
* Pro pokročilé použití si můžete nastavit pokyn a počet tokenů tak, abyste získané informace přizpůsobili svým potřebám
* Možnost klást doplňující otázky a přikládat další obrázky
* Vykreslování ve formátu Markdown pro snadný přístup ke strukturovaným informacím (stačí zapnout nastavení „Otevírat každý výsledek v procházitelném dialogu“ a na konec svého pokynu uvést např. „odpověz ve formátu Markdown“)

## Možnosti využití

Tento projekt měl několik hlavních motivací.

NVDA dokáže už ve výchozí instalaci provádět optické rozpoznávání znaků (OCR), což je obrovský pokrok. Pokud se snažíte získat text z obrázku nebo dokumentu PDF, pak hledáte právě tuto funkci.

OCR však dokáže analyzovat pouze data, která *mohou* obsahovat text. Nedokáže objasnit kontext, předměty, které se na obrázcích mohou nacházet, a vztahy mezi nimi. Těch je internet plný. Loga, portréty, memy, ikony, grafy, diagramy, sloupcové/čárové grafy... Na co si vzpomenete. Jsou všude a obvykle nejsou ve formátu, který by uživatelé odečítače obrazovky dokázali interpretovat.
Donedávna jsme neochvějně spoléhali na to, že autoři obsahu budou poskytovat alternativní textové popisy. I když je to stále nutností, těžko změníme skutečnost, že vysoký standard kvality bývá spíš jen výjimkou, nikoli pravidlem.

Nyní máte možnosti téměř neomezené. Můžete např.:

* Vizualizovat si plochu nebo konkrétní okno, abyste pochopili rozmístění jednotlivých ikon při školení ostatních
* Získat podrobné informace o stavu her, virtuálních počítačů atd. v případě nedostatečného nebo chybějícího ozvučení
* Zjistit, co je zobrazeno v grafu
* Pochopit snímky obrazovky nebo sdílení obrazovky v aplikacích Zoom nebo Microsoft Teams
* Požádat podporovaný model, aby vám pomohl ovládat nepřístupnou aplikaci nebo dokončit úkol v okně na popředí
* Před natáčením videí nebo účastí na online schůzkách se ujistit, že se díváte zřetelně do kamery a že pozadí vypadá profesionálně

## Modely

* [Pollinations](https://pollinations.ai/): Tým, který stojí za Pollinations.AI, velkoryse sponzoruje pro tento projekt bezplatný přístup ke GPT4, takže uživatelé nemusí zadávat vlastní klíč API. Mějte na paměti, že u této služby byly pozorovány chyby, a proto důrazně doporučujeme používat vlastní klíče, abyste z tohoto projektu získali maximum.
* [Modely GPT od OpenAI](https://platform.openai.com/docs/models): Vyžaduje klíč API od OpenAI. Zahrnuje řadu GPT-5.4 (5.4 a 5.4 mini), řadu GPT-5.5 (5.5 a 5.5 pro), řadu GPT-6 (6 Astra a 6 Luna) a řadu GPT-6.1 (6.1 Sol a 6.1 Terra). Ovládání počítače podporují řady GPT-5.4, GPT-5.5, GPT-6 a GPT-6.1.
* [Google Gemini](https://deepmind.google/models/gemini/), včetně modelů 2.5 Flash, 2.5 Flash-Lite, 2.5 Pro, 3.1 Flash-Lite, 3.1 Pro Preview, 3.5 Flash, 3.5 Flash-Lite, 3.6 Flash, 3.7 Flash, 3.8 Flash, 4 Hydrogen, 4 Argon a 4 Carbon.
* [Anthropic Claude](https://docs.anthropic.com/claude/docs/vision), včetně Claude 4.5 (Sonnet, Opus), 4.6 (Sonnet, Opus), 4.7 Opus, 4.8 Opus, 5 (Sonnet, Opus, Fable), 5.1 Fable, 5.2 Fable a 5.5 (Haiku, Sonnet, Opus). Všechny tyto modely podporují ovládání počítače.
* [Mistral Large 4](https://docs.mistral.ai/models/mistral-large-4-0)
* [xAI Grok](https://docs.x.ai/developers/models), včetně Grok 4.20 (bez uvažování), 4.3, 4.5, 4.6 a 4.7.
* [Kimi](https://platform.kimi.ai/docs/guide/use-kimi-vision-model), multimodální modely od Moonshot AI, včetně Kimi K3 a Kimi K2.6.
* vivo BlueLM Vision: multimodální model od společnosti vivo, dostupný prostřednictvím bezplatného účtu NVDA-CN. Viz část o nastavení níže.
* [Datalab Chandra 2](https://github.com/datalab-to/chandra): Špičkový model pro rozpoznávání obrazu a OCR od společnosti Datalab, specializovaný na složitá rozvržení dokumentů, tabulky, formuláře, ručně psaný text, grafy a matematiku. Podporuje spravované cloudové API společnosti Datalab (na [datalab.to](https://www.datalab.to)) nebo vlastní nasazení přes vLLM (pomocí `chandra_vllm` nebo koncových bodů `/v1` kompatibilních s OpenAI).
* [Ollama (nestabilní)](https://ollama.com/)
* [llama.cpp (extrémně nestabilní a pomalý v závislosti na vašem hardwaru, testováno při práci s modely llava-v1.5/1.6, BakLLaVA, Obsidian a MobileVLM 1.7B/3B)](https://github.com/ggerganov/llama.cpp)
* [LiteLLM Proxy](https://docs.litellm.ai/docs/proxy/quick_start): Přístup k více modelům AI přes jednotný proxy server. Vyžaduje adresu URL proxy serveru LiteLLM a v závislosti na konfiguraci proxy také klíč API. V dialogu konfigurace modelů se zobrazuje jako „LiteLLM Proxy“. Podporuje dynamický výběr modelu a doplňující otázky. Je kompatibilní se všemi formáty (PNG, JPEG, WEBP, GIF).
* [Seer](https://github.com/recursia-lab/Seer): Spouští model PaliGemma2 lokálně pomocí démona Seer. Nevyžaduje klíč API ani připojení k internetu. Poznámka: jde o model, který umí pouze vytvářet popisky. Pokyny ani doplňující otázky nejsou podporovány.

Pro zprovoznění jednotlivých modelů postupujte podle níže uvedených pokynů.

## Jak začít

Stáhněte si nejnovější verzi doplňku z [tohoto odkazu](https://github.com/cartertemm/AI-content-describer/releases/latest/). Otevřete stažený soubor v počítači, kde máte nainstalované NVDA, a pokračujte v instalaci podle zobrazených pokynů.

Při prvním spuštění NVDA s tímto doplňkem budete požádáni o stažení několika dalších knihoven. Podrobnosti najdete v části `Závislosti` tohoto dokumentu.

Od verze 2025.06.05 je používání GPT4 zdarma díky velkorysosti komunity kolem PollinationsAI.

Pokud máte prostředky a zájem vyzkoušet další modely, můžete vždy použít vlastní klíč API a snížit tak počet požadavků na jejich servery. Pokud ne, klidně přeskočte na část `Použití` tohoto dokumentu.

Podle níže uvedených pokynů získejte klíč API od některého z podporovaných poskytovatelů.

### Který model mám použít?

Dříve jsme doporučovali nejlevnější a nejkvalitnější možnosti, ale situace se mění tak rychle, že není možné tato doporučení udržovat aktuální.

Stručně řečeno: většina špičkových modelů je dnes dostatečně přesná pro většinu běžných situací, takže si vyberte poskytovatele, kterého znáte.

Většina lidí hledá rovnováhu mezi přesností a cenou. [Žebříček LLM arena](https://lmarena.ai/leaderboard) (konkrétně kategorie vision) měří správnost, zatímco [kalkulačka cen LLM](https://www.llm-prices.com/) přehledně uvádí ceny.

Pokud chcete používat ovládání počítače, vyberte některý z podporovaných modelů od OpenAI nebo Anthropic uvedených výše. Bezplatný přístup přes Pollinations je užitečný pro popisy obrázků, ale ovládání počítače nepodporuje.

### Jak získat API klíč od OpenAI:

1. Přejděte na [stránku s klíči API od OpenAI](https://platform.openai.com/account/api-keys)
2. Pokud ještě nemáte účet, vytvořte si ho. Pokud ano, přihlaste se.
3. Na stránce API keys klikněte na tlačítko pro vytvoření nového tajného klíče. Zkopírujte jej do schránky.
4. Na svůj účet vložte alespoň 1 dolar
5. V dialogovém okně nastavení NVDA přejděte do kategorie Popis obsahu pomocí AI, poté vyberte „Spravovat modely (alt+m)“, jako poskytovatele vyberte kterýkoli model od OpenAI (například „GPT-6.1 Sol“), klávesou tab přejděte do políčka API klíč a vložte sem právě vytvořený klíč.

V době, kdy byl tento dokument vytvořen, vydávala OpenAI novým vývojářským účtům kredity, které lze používat po dobu tří měsíců, poté propadají. Po uplynutí této lhůty si budete muset kredity zakoupit. Obvyklá spotřeba by nikdy neměla přesáhnout 5,00 USD měsíčně. Pro představu, původní verze tohoto doplňku byla vyvinuta za necelý dolar. Kdykoli se můžete přihlásit ke svému účtu OpenAI a kliknutím na „usage“ zjistit stav své kvóty.

### Jak získat API klíč od Googlu

1. Nejprve je třeba vytvořit projekt Google Workspace v [konzoli Google Cloud](https://console.cloud.google.com/projectcreate). Ujistěte se, že jste přihlášeni ke svému účtu Google.
2. Zadejte název v rozsahu čtyř až třiceti znaků, například „Gemini“ nebo „NVDA add-on“.
3. Přejděte na [stránku s klíči API v Google AI Studiu](https://makersuite.google.com/app/apikey)
4. Klikněte na tlačítko „create API key“
5. V dialogovém okně nastavení NVDA přejděte do kategorie Popis obsahu pomocí AI, poté vyberte „Spravovat modely (alt+m)“, jako poskytovatele vyberte „Google Gemini“, klávesou tab přejděte do políčka API klíč a vložte sem právě vygenerovaný klíč.

### Jak získat API klíč od Anthropic

1. Přihlaste se do [konzole Anthropic](https://console.anthropic.com/login).
2. Klikněte na svůj profil -> API keys.
3. Klikněte na tlačítko Create Key.
4. Zadejte název klíče, například „AIContentDescriber“, poté klikněte na „Create Key“ a zkopírujte hodnotu, která se zobrazí. Tuto hodnotu vložíte do políčka API klíč v kategorii Popis obsahu pomocí AI v dialogovém okně Nastavení NVDA -> Spravovat modely -> kterýkoli model Claude (například „Claude 5 Sonnet“).
5. Pokud jste tak ještě neučinili, zakupte si kredity v hodnotě alespoň 5 USD na [stránce Plans od Anthropic](https://console.anthropic.com/settings/plans).

### Jak získat API klíč od Mistralu

1. Přihlaste se k účtu MistralAI nebo si ho vytvořte na [přihlašovací stránce MistralAI](https://auth.mistral.ai/ui/login).
2. Pokud si účet vytváříte nebo se přihlašujete poprvé, přidejte podle výzvy pracovní prostor, zadejte jeho název a přijměte smluvní podmínky.
3. Po přihlášení vyberte v nabídce položku „API keys“.
4. Klikněte na „create a new key“ a zkopírujte klíč do schránky. Tuto hodnotu vložíte do políčka API klíč v kategorii Popis obsahu pomocí AI v dialogovém okně Nastavení NVDA -> Spravovat modely -> Mistral Large 4.
5. V případě potřeby si na účet vložte kredit.

### Jak získat API klíč od Kimi (Moonshot AI)

1. Přihlaste se k účtu na [vývojářské platformě Kimi](https://platform.kimi.ai/) nebo si ho vytvořte.
2. Po přihlášení otevřete v konzoli část s klíči API a vytvořte nový klíč.
3. Zkopírujte klíč do schránky. Tuto hodnotu vložíte do políčka API klíč v kategorii Popis obsahu pomocí AI v dialogovém okně Nastavení NVDA -> Spravovat modely -> Kimi K3 (nebo jiný model Kimi).
4. V případě potřeby si na účet vložte kredit.


### Aktivace modelu VIVO BlueLM Vision přes NVDA-CN

Tato služba je k dispozici zdarma díky partnerství mezi společností VIVO (vivo.com.cn) a čínskou komunitou NVDA (NVDACN). Poskytuje kvalitní multimodální rozpoznávání a je to doporučený model pro všechny uživatele, zejména pro začátečníky.

K používání tohoto modelu potřebujete pouze bezplatný účet NVDA-CN.

1.  Vytvoření účtu: Přejděte na registrační stránku NVDA-CN: [https://nvdacn.com/admin/register.php](https://nvdacn.com/admin/register.php).
    * **Poznámka**: Stránka je zatím pouze v čínštině. K vyplnění formuláře doporučujeme použít vestavěnou funkci překladu ve vašem prohlížeči.
    * Budete požádáni o uživatelské jméno, heslo a platnou e-mailovou adresu. Heslo si bezpečně uložte, protože automatické obnovení hesla zatím není k dispozici.
2.  Ověření e-mailu: Ve své schránce vyhledejte ověřovací e-mail a kliknutím na odkaz v něm aktivujte účet.
3.  Konfigurace doplňku:
    * Otevřete dialogové okno nastavení NVDA a přejděte do kategorie „Popis obsahu pomocí AI“.
    * Vyberte tlačítko „Spravovat modely“.
    * V seznamu poskytovatelů zvolte „vivo BlueLM Vision (NVDA-CN)“.
    * Do příslušných polí zadejte své uživatelské jméno a heslo k NVDA-CN.
    * Kliknutím na OK přihlašovací údaje uložte.

Nyní můžete model VIVO používat. S jakýmikoli problémy s účtem se můžete obrátit na tým NVDA-CN na adrese `support@nvdacn.com`.


### Jak nastavit Ollama

Toto je v současné době preferovaná možnost pro lokální provoz.

Přestože integrace Ollama byla testována důkladněji než llama.cpp, stále je méně stabilní než volání API a v některých konfiguracích se chová podivně, a to až po pády na počítačích, které nesplňují požadované parametry.
Když tuto možnost zkoušíte poprvé, uložte si pro jistotu všechny dokumenty a vše důležité, než budete pokračovat.

Nejprve se ujistěte, že dokážete se zvoleným modelem s podporou obrazu komunikovat přes příkazový řádek. Postup je následující:

1. Stáhněte si instalační soubor Ollama pro Windows ze stránky [Ollama downloads](https://ollama.com/download).
2. Spusťte tento instalační soubor. Postará se o stažení všech závislostí, které váš počítač bude potřebovat.
3. Najděte model, který chcete použít. Seznam najdete na ollama.com -> models -> vision, nebo [přímo zde](https://ollama.com/search?c=vision).
4. Stáhněte a spusťte tento model tak, že otevřete příkazový řádek a napíšete `ollama run [model_name]`, přičemž „[model_name]“ samozřejmě nahradíte modelem zvoleným v kroku 3. Například `ollama run llama3.2-vision`.
5. Pokud vše proběhlo úspěšně, ocitnete se v interaktivním prostředí, kde můžete psát dotazy a dostávat odpovědi od modelu, něco jako lokální (a omezený) ChatGPT. Vyzkoušejte ho tak, že se na něco zeptáte, a pak napište „/bye“ pro ukončení tohoto rozhraní.
6. Zpět v okně konzole napište `ollama list`. V prvním sloupci uvidíte název jako „llama3.2-vision:latest“.
7. Přejděte do nastavení Popisu obsahu pomocí AI -> Spravovat modely -> Ollama. Do políčka název modelu zadejte tuto hodnotu a klikněte na OK -> OK. Hotovo! V podnabídce modelů přepněte na Ollama a po chvíli by vše mělo fungovat.

### Jak nastavit llama.cpp

Tento poskytovatel je v současné době poněkud chybový a vaše zkušenosti se mohou lišit. O zprovoznění tohoto modelu by se měli pokoušet opravdu jen pokročilí uživatelé se zájmem o provozování lokálních self-hosted modelů a s hardwarem, který k tomu potřebují.

1. Stáhněte si llama.cpp. V době vytvoření tohoto dokumentu tento [pull request](https://github.com/ggerganov/llama.cpp/pull/5882) odstraňuje podporu pro multimodální schopnosti, takže budete chtít použít [poslední verzi s touto podporou](https://github.com/ggerganov/llama.cpp/releases/tag/b2356).
Pokud používáte grafickou kartu Nvidia s podporou CUDA, stáhněte si tyto předpřipravené binární soubory:
[llama-b2356-bin-win-cublas-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/llama-b2356-bin-win-cublas-cu12.2.0-x64.zip) a [cudart-llama-bin-win-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/cudart-llama-bin-win-cu12.2.0-x64.zip)
Popis kroků pro práci s jinou grafickou kartou je nad rámec tohoto dokumentu, ale najdete jej v readme souboru pro llama.cpp.
2. Oba tyto soubory rozbalte do stejné složky.
3. Z Huggingface si stáhněte kvantizované soubory modelů, které chcete použít. Pro LLaVA 1.6 Vicuna 7B: [llava-v1.6-vicuna-7b.Q4_K_M.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/llava-v1.6-vicuna-7b.Q4_K_M.gguf) a [mmproj-model-f16.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/mmproj-model-f16.gguf)
4. Tyto soubory vložte do složky s ostatními spustitelnými soubory llama.cpp.
5. Z příkazového řádku spusťte server llama.cpp a předejte mu soubory .gguf pro model a multimodální projektor (podle následujícího příkladu):
```
server.exe -m llava-v1.6-vicuna-7b.Q4_K_M.gguf --mmproj mmproj-model-f16.gguf
```
6. V dialogovém okně nastavení NVDA přejděte do kategorie Popis obsahu pomocí AI, poté zvolte „Spravovat modely (alt+m)“, jako poskytovatele vyberte „llama.cpp“, klávesou tab přejděte do políčka Adresa URL a zadejte koncový bod zobrazený v konzoli (výchozí hodnota je „http://localhost:8080“).
7. Případně můžete některé z těchto kroků vynechat a spustit llama.cpp na vzdáleném serveru s vyšším výkonem, než má váš lokální počítač, a zadat místo toho jeho koncový bod.

### Jak nastavit LiteLLM Proxy

LiteLLM Proxy poskytuje jednotné rozhraní pro přístup k více modelům AI přes jediný koncový bod, což zjednodušuje správu modelů a umožňuje snadné přepínání mezi poskytovateli.

1. Nastavte proxy server LiteLLM podle [dokumentace LiteLLM proxy](https://docs.litellm.ai/docs/proxy/quick_start). Proxy můžete provozovat lokálně nebo použít vzdálený server.
2. Při lokálním provozu nejrychleji začnete takto:
```
pip install 'litellm[proxy]'
litellm --model gpt-4o
```
Tím se na adrese `http://localhost:4000` spustí proxy server, který přeposílá požadavky na model GPT-4o od OpenAI.
3. Pro produkční nasazení vytvořte soubor `config.yaml` s konfigurací více modelů a ověřování. Podrobnosti najdete v [průvodci konfigurací LiteLLM](https://docs.litellm.ai/docs/proxy/configs).
4. V dialogovém okně nastavení NVDA přejděte do kategorie Popis obsahu pomocí AI, poté zvolte „Spravovat modely (alt+m)“ a jako poskytovatele vyberte „LiteLLM Proxy“.
5. Do políčka Adresa URL zadejte adresu svého proxy serveru (např. „http://localhost:4000“ pro lokální provoz nebo adresu vašeho vzdáleného serveru).
6. Pokud proxy vyžaduje ověření, zadejte klíč do políčka API klíč. Pokud ne, nechte políčko prázdné.
7. Kliknutím na tlačítko „Vypsat modely“ načtěte dostupné modely z proxy a poté v rozbalovacím seznamu vyberte model, který chcete použít.
8. Podle potřeby upravte další nastavení, jako je pokyn, maximální počet tokenů a časový limit, a poté klikněte na OK.

Poznámka: Dostupné modely a jejich schopnosti závisí na konfiguraci vaší LiteLLM proxy. Pro popisy obrázků se ujistěte, že je proxy nakonfigurována s modely, které podporují práci s obrazem.

### Jak nastavit Seer

Seer spouští model PaliGemma2 přímo na vašem počítači, bez klíče API a bez připojení ke cloudu. Mějte na paměti, že jde o model, který umí pouze vytvářet popisky; pokyny ani doplňující otázky nejsou podporovány.

1. Nainstalujte [démona Seer](https://github.com/recursia-lab/Seer). K dispozici je instalátor spouštěný jediným příkazem pro Windows (.bat) a Linux/macOS (.sh).
2. V dialogovém okně nastavení NVDA přejděte do kategorie Popis obsahu pomocí AI, zvolte „Spravovat modely (alt+m)“ a vyberte „Seer (vyžaduje instalaci)“.
3. Výchozí adresa URL je `http://127.0.0.1:11435`. Ponechte ji beze změny, pokud jste nezměnili port démona.
4. Klikněte na OK. Než požádáte o popis, démon musí být spuštěný.

### Jak nastavit Datalab Chandra 2

Datalab Chandra 2 je špičkový model pro zpracování dokumentů a OCR, specializovaný na složitá rozvržení, tabulky, formuláře, ručně psaný text, grafy a matematické vzorce. Lze ho používat přes spravované cloudové API společnosti Datalab, kontejner provozovaný na vlastní infrastruktuře nebo vlastní instanci vLLM.

#### Možnost A: Cloudové API společnosti Datalab (doporučeno)
1. Zaregistrujte si účet na [datalab.to](https://www.datalab.to). Nové účty dostanou zkušební kredity zdarma.
2. Přejděte na [stránku s klíči API](https://www.datalab.to/app/keys) a vygenerujte klíč API.
3. V dialogovém okně nastavení NVDA přejděte do kategorie Popis obsahu pomocí AI, zvolte „Spravovat modely (alt+m)“ a vyberte „Datalab Chandra 2“.
4. Do políčka „API klíč“ zadejte svůj klíč API.
5. Adresa URL je ve výchozím nastavení `https://www.datalab.to/api/v1/convert`. Režim zpracování (`fast`, `balanced` nebo `accurate`) můžete upravit podle svých potřeb.
6. Klikněte na OK. Model bude nyní k dispozici v nabídce Popisu obsahu pomocí AI.

#### Možnost B: Vlastní provoz s vLLM
1. Spusťte lokální server vLLM s modelem Chandra 2 (např. pomocí `chandra_vllm` nebo `vllm serve datalab-to/chandra-ocr-2`). Ve výchozím nastavení server běží na adrese `http://localhost:8000/v1`.
2. V nastavení NVDA -> Popis obsahu pomocí AI -> Spravovat modely -> „Datalab Chandra 2“ zadejte do políčka „Adresa URL“ svůj lokální koncový bod (např. `http://localhost:8000/v1`).
3. Pokud se název modelu liší od výchozího (`datalab-to/chandra-ocr-2`), nastavte ho, políčko API klíč nechte prázdné (nebo zadejte bearer token, pokud je zapnuté ověřování) a klikněte na OK.

## Použití

Ve výchozím nastavení je přiřazeno šest klávesových zkratek:

* NVDA+shift+i: Zobrazí se nabídka s dotazem, zda chcete popsat aktuální objekt pod fokusem, aktuální prohlížený objekt, snímek z fyzické kamery, celou obrazovku, nebo ovládat počítač pomocí AI.
* NVDA+shift+u: Popíše obsah aktuálně prohlíženého objektu pomocí AI.
* NVDA+shift+y: Popíše obrázek (nebo cestu k souboru s obrázkem) ve schránce pomocí AI.
* NVDA+shift+j: Popíše umístění tváře v záběru vybrané kamery. Pokud máte připojeno více kamer, přejděte do nabídky doplňku (NVDA+shift+i) a vyberte tu, kterou chcete použít, pomocí položky „vybrat kameru“ v podnabídce detekce tváře.
* NVDA+alt+c: Otevře dialog konverzace s AI, kde můžete klást doplňující otázky.
* NVDA+control+shift+p: Pozastaví nebo obnoví probíhající relaci ovládání počítače.

Sedm klávesových zkratek ve výchozím stavu přiřazeno není:

* Popsat obsah objektu pod fokusem pomocí AI.
* Pořídit snímek obrazovky a poté jej popsat pomocí AI.
* Pořídit snímek pomocí vybrané kamery a poté jej popsat pomocí AI.
* Zrušit probíhající relaci ovládání počítače.
* Pořídit snímek aktuálního objektu pod fokusem a zkopírovat ho do schránky.
* Pořídit snímek aktuálního prohlíženého objektu a zkopírovat ho do schránky.
* Pořídit snímek celé obrazovky a zkopírovat ho do schránky.

Tyto tři příkazy pro kopírování najdete také v podnabídce „Kopírovat obrázek do schránky“ v nabídce NVDA+shift+i. Neodesílají nic žádné službě AI. Použijte je, když chcete snímek vložit do Be My AI nebo jiné aplikace, kterou tento doplněk nepodporuje. Zkopírovaný obrázek nahradí předchozí obsah schránky.

Neváhejte si je kdykoli přizpůsobit v dialogu Klávesové příkazy.

### Doplňující otázky k popisu

Někdy odpověď, kterou od AI dostanete, nestačí. Obrázek může mít nízkou kvalitu, může být neúplný nebo obsahovat nežádoucí detaily. Možná se chcete zaměřit jen na určitou část nebo pořídit ostřejší snímek, aniž byste ztratili kontext.
Po obdržení popisu můžete stisknout NVDA+alt+c nebo v kontextové nabídce Popisu obsahu pomocí AI (NVDA+shift+i) vybrat „Doplňující dotaz k předchozímu popisu“. Ve výchozím nastavení je fokus v políčku pro zprávu.
Chcete-li přidat další obrázek, nechte okno konverzace otevřené a používejte doplněk jako obvykle. Když pořídíte snímek (ať už z kamery, ovládacího prvku, snímek obrazovky atd.), budete dotázáni, zda ho chcete přiložit k aktuální relaci, nebo zahájit novou.

### Ovládání počítače

Ovládání počítače umožňuje doplňku Popis obsahu pomocí AI ovládat aktivní aplikaci myší a klávesnicí poté, co popíšete úkol. To může pomoci s úkoly, které je obtížné nebo nemožné ručně přístupně dokončit.

Protože tím dáváte modelu AI kontrolu nad svým počítačem, používejte tuto funkci opatrně. Doplněk si před spuštěním vyžádá souhlas, průběžně hlásí prováděné akce a před potenciálně rizikovými akcemi se zeptá. Za to, co provede, odpovídáte vy, proto relaci sledujte a nepoužívejte ji pro citlivou práci nebo práci, kterou je obtížné vrátit zpět.

Ovládání počítače můžete kdykoli pozastavit nebo obnovit klávesovou zkratkou `NVDA+Control+Shift+P`. Během pozastavení doplněk nepokračuje další akcí, dokud ho neobnovíte.

Doplněk stav ovládání signalizuje tóny. Vysoké pípnutí znamená, že model přebírá nebo znovu přebírá kontrolu. Nízké pípnutí znamená, že ovládání bylo pozastaveno, buď protože jste ho pozastavili vy, nebo protože model potřebuje vaši odpověď. Krátké nízké chybové pípnutí znamená, že relace skončila kvůli chybě API.

Během probíhající relace ovládání model před odesláním vstupu oznámí, co se chystá udělat. Dokud toto oznámení nedomluví, nic se nestane, pokud oznámení nepřerušíte klávesou `Control` a nenecháte akci proběhnout dříve.

Pokud si model není jistý, jak akci dokončit, potřebuje více informací nebo vám jinak předá slovo, relace se pozastaví a do popředí se přenese dialog Ovládání počítače. Napište do něj doplňující zprávu a pokračujte v konverzaci, nebo dialog zavřete a relaci ukončete.

Tato funkce funguje pouze s modely, které poskytují nástroj pro ovládání počítače: GPT-5.4, GPT-5.4 mini, GPT-5.5, GPT-5.5 pro, GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna, Claude 4.5 Sonnet, Claude 4.5 Opus, Claude 4.6 Sonnet, Claude 4.6 Opus, Claude 4.7 Opus, Claude 4.8 Opus, Claude 5 Sonnet, Claude 5 Opus, Claude 5 Fable, Claude 5.1 Fable, Claude 5.2 Fable, Claude 5.5 Haiku, Claude 5.5 Sonnet a Claude 5.5 Opus. Ostatní modely umí popisovat obrázky, ale neposkytují strukturované akce myši a klávesnice potřebné k ovládání počítače.

Jak používat ovládání počítače:

1. Nastavte a vyberte některý z podporovaných modelů.
2. Otevřete aplikaci nebo okno, se kterým má model pracovat.
3. Stiskněte `NVDA+shift+i` a zvolte „Ovládat počítač...“.
4. Napište úkol, který chcete provést, a stiskněte Odeslat.
5. Projděte si žádost o souhlas. Pokud relaci povolíte, sledujte prováděné akce a rizikové akce schvalte nebo zrušte.

Poznámka: Tuto funkci považujte za betaverzi. Aktivně pracujeme na tom, aby byla implementace spolehlivější.

## Závislosti

Některé knihovny, které tento doplněk potřebuje, jsou příliš velké na to, aby byly součástí balíčku doplňku. Místo toho se vás NVDA při prvním spuštění s nainstalovaným doplňkem zeptá, zda je chcete stáhnout. Vyberte Ano, počkejte na dokončení stahování a NVDA se restartuje.

Stahuje se soubor zip o velikosti přibližně 35 až 70 MB v závislosti na vaší verzi NVDA. Pochází ze stránky [libs-release](https://github.com/cartertemm/AI-content-describer/releases/tag/libs-release) tohoto repozitáře. Pokud GitHub není dostupný, doplněk nabídne stažení ze zrcadla, které poskytuje čínská komunita NVDA.

Soubor zip obsahuje:

* [NumPy](https://numpy.org/): výpočty s poli, vyžaduje ho OpenCV.
* [OpenCV](https://opencv.org/) (`cv2`): vyhledává vaši tvář v obraze z webové kamery pro funkci detekce tváře.
* [Pillow](https://python-pillow.org/) (`PIL`): pořizuje snímky obrazovky a převádí je na obrázky, které modely AI dokážou přečíst.
* [Markdown](https://python-markdown.github.io/): zobrazuje popisy s formátováním, například s nadpisy, seznamy a tabulkami.
* [pygrabber](https://github.com/andreaschiavinato/python_grabber): vypisuje webové kamery připojené k vašemu počítači.
* Několik modulů ze standardní knihovny Pythonu, které NVDA neobsahuje (`html`, `xml`, `pathlib`, `secrets` a `_markupbase`). Potřebují je výše uvedené knihovny.

Soubory se ukládají do složky s názvem `aic-py-`, za kterým následuje verze Pythonu v NVDA, například `aic-py-3.13`. Tato složka se nachází ve vaší složce s uživatelskou konfigurací NVDA, obvykle `%APPDATA%\nvda`. Každá verze Pythonu má vlastní složku, takže doplněk knihovny stáhne znovu, když nové vydání NVDA změní verzi Pythonu. Odinstalováním doplňku se smaže složka pro aktuální verzi Pythonu v NVDA.

Pokud stahování nefunguje, můžete knihovny nainstalovat sami. Stáhněte si `aic-py-3.13.zip` (nebo soubor pro verzi Pythonu ve vašem NVDA) ze stránky libs-release, rozbalte ho do složky s uživatelskou konfigurací NVDA a restartujte NVDA.

## Sestavení doplňku

K vytvoření balíčku doplňku ze zdrojových kódů budete potřebovat:

* distribuci jazyka Python (doporučujeme verzi 3.7 nebo novější). Instalační programy pro systém Windows naleznete na [webových stránkách Pythonu](https://www.python.org). Upozorňujeme, že v současné době příprava zdrojového kódu NVDA a obsažených modulů třetích stran vyžaduje 32bitovou verzi Pythonu 3.7.
* Scons - [Webové stránky](https://www.scons.org/) - verze 4.3.0 nebo novější. Můžete jej nainstalovat prostřednictvím PIP. `pip install scons`
* Markdown 3.3.0 nebo novější. `pip install markdown`

Poté otevřete vybraný terminál:

```
git clone https://github.com/cartertemm/AI-content-describer.git
cd AI-content-describer
scons
```

Po dokončení příkazu `scons` bude do kořenového adresáře tohoto repozitáře umístěn soubor *.nvda-addon připravený k testování a vydání.

Pokud přidáte další řetězce, které je třeba přeložit, je důležité znovu sestavit soubor .pot:

```
scons pot
```

## Jak doplněk přeložit

Na počítači se systémem Windows:

* stáhněte si [poedit](https://poedit.net/). Pomocí tohoto programu přeložíte jednotlivé řetězce z angličtiny.
* stáhněte si soubor .pot se všemi řetězci [zde](https://raw.githubusercontent.com/cartertemm/AI-content-describer/main/AIContentDescriber.pot)
* Otevřete právě stažený soubor v programu poedit. V zobrazeném okně klikněte na tlačítko „Vytvořit nový překlad“ a vyberte cílový jazyk.
* Projděte a převeďte obsah zdrojového textu do cílového jazyka a poté jej vložte do pole pro překlad. Chcete-li získat další nápovědu, neváhejte kliknout pravým tlačítkem myši na položku seznamu -> výskyty kódu, poté přejděte o řádek výše a přečtěte si komentář začínající slovy „# Translators: “. Tyto komentáře jsou navíc zpřístupněny na jednom místě v souboru .pot.
* Po dokončení klikněte na Soubor -> Uložit nebo stiskněte klávesovou zkratku ctrl+s a poté vyberte místo, kam se nový soubor .mo a .po uloží. Tyto soubory mi pošlete e-mailem nebo přiložte v pull requestu.
* Přeložte obsah souboru readme.md (tento soubor). Přiložte ho také!

## Spolupracovníci

Veškeré vaší spolupráce si velice vážím a uvedu ji zde.
Na doplňku se podíleli:

* [Cary Rowen](https://github.com/cary-rowen): zprovoznil doplněk pro čínské uživatele pomocí zrcadlení závislostí, přidal podporu poskytovatele Vivo Blue
* [Mazen](https://github.com/mzanm): implementace Markdownu, další příspěvky do kódu
* [Kostenkov-2021](https://github.com/Kostenkov-2021): ruský překlad
* [Nidza07](https://github.com/nidza07): srbský překlad
* [Heorhii Halas](nvda.translation.uk@gmail.com) a [George-br](https://github.com/George-br): ukrajinský překlad
* [Umut Korkmaz](umutkork@gmail.com): turecký překlad
* [Platinum_Hikari](urbain_onces.0r@icloud.com): francouzský překlad
* [Lukas](https://4sensegaming.cz): český překlad
* [Michaela](https://technologiebezzraku.sk): slovenský překlad
* [loginerror](https://github.com/theloginerror): polský překlad

Narazili jste na problém? Popište ho v [issue trackeru](https://github.com/cartertemm/AI-content-describer/issues)

Máte návrh na novou funkci? Vytvořte pro ni také ticket a můžeme se domluvit na její implementaci. Pull requesty bez přiřazených issues budou přezkoumány, ale pravděpodobně zaberou všem více času, zejména pokud se rozhodnu, že nová oprava nebo funkce musí fungovat jinak, než jak jste původně navrhovali.

Překlady uvítám s otevřenou náručí. Čím více lidí bude mít k této skvělé technologii přístup, tím lépe!

Pokud nemáte Github nebo ho raději nepoužíváte, můžete mi [poslat e-mail](mailto:carter@ctemm.me) - carter (zavináč) ctemm (tečka) me.

Děkuji za vaši podporu!
