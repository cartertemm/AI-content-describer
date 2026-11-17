# AI opisivač sadržaja za NVDA

Ovaj dodatak vam omogućava da dobijete detaljne opise za slike, kontrole korisničkog interfejsa i drugi vizuelno nepristupačan sadržaj.

Kroz multimodalne sposobnosti naprednih AI modela i algoritama računarskog vida, naš cilj je da vam dostavimo najbolje opise sadržaja i povećamo vašu samostalnost. Za više informacija o modelima koji se koriste, pogledajte odgovarajući odeljak ovog dokumenta.

## Karakteristike

* Opisivanje fokusiranog objekta, navigacionog objekta, celog ekrana ili fotografisanje ugrađenom kamerom
* Opisivanje bilo koje slike koja je kopirana u privremenu memoriju, bez obzira da li je to slika iz e-maila ili putanja u Windows istraživaču datoteka
* Kopiranje slike fokusiranog objekta, navigacionog objekta ili celog ekrana u privremenu memoriju, kako biste je nalepili u druge aplikacije
* Određivanje da li je lice korisnika u centru kadra korišćenjem algoritama računarskog vida (nije potreban plaćeni API pristup)
* Korišćenje podržanih modela za upravljanje aktivnom aplikacijom radnjama miša i tastature, za zadatke koji mogu biti nepristupačni
* Podrazumevano besplatan, uz mogućnost da dodate sopstveni API ključ za više modela
* Podrška za više provajdera (GPT od kompanije OpenAI i besplatni Pollinations nivo, Gemini od kompanije Google, Mistral Large 4, Claude od kompanije Anthropic, Grok od kompanije xAI, Kimi od kompanije Moonshot AI, vivo BlueLM Vision preko NVDA-CN, Datalab Chandra 2, Ollama, llama.cpp, LiteLLM Proxy i Seer)
* Podrška za širok broj formata uključujući PNG (.png), JPEG (.jpeg i .jpg), WEBP (.webp), i neanimirani GIF (.gif)
* Opciono pamćenje ili keširanje odgovora kako bi se uštedela API potrošnja
* Za napredno korišćenje, prilagodite upit i broj tokena kako biste prilagodili informacije vašim potrebama
* Postavljanje dodatnih pitanja i prilaganje dodatnih slika
* Prikaz Markdown formata za lakši pristup strukturiranim informacijama (samo omogućite podešavanje "Otvori svaki rezultat u dijalogu koji se može pretraživati" i dodajte na primer "odgovori u Markdown formatu" na kraj vaših upita)

## Svrha korišćenja

Ovaj projekat je motivisalo nekoliko različitih primera.

NVDA ima ugrađenu mogućnost da izvrši optičko prepoznavanje znakova (OCR), što je ogroman korak napred. Ako pokušavate da pročitate tekst sa slike ili iz PDF dokumenta, ovo je opcija koju tražite.

Ali, OCR može samo da analizira podatke koji su *možda* tekstualni. Gubi svrhu kada je u pitanju prepoznavanje konteksta, objekata i veze između njih koje ove slike predstavljaju. A Internet je pun takvih slika. Logotipi, portreti, mimovi, ikone, grafikoni, dijagrami, trakasti ili linijski grafikoni... Šta god vam padne na pamet. Ovakav sadržaj je svuda, i obično nije u formatu koji omogućava čitaču ekrana da ga obradi.
Do skoro, u glavnom je neograničena odgovornost bila na autorima sadržaja da pruže alternativne tekstualne opise. Iako je ovo još uvek neophodno, teško je promeniti činjenicu da su opisi visokog kvaliteta izuzetak, a ne pravilo.

Sada, mogućnosti su skoro beskrajne. Možete:

* Shvatiti vizuelni izgled radne površine ili određenog prozora kako biste razumeli pozicije ikonica kada učite druge
* Dobijati detaljne informacije o statusu igrica, virtuelnih mašina, i tako dalje kada zvuk nije dovoljan ili je nedostupan
* Shvatiti šta se prikazuje na grafikonu
* Razumeti slike ekrana ili deljenje ekrana u aplikacijama Zoom ili Microsoft Teams
* Zatražiti od podržanog modela da vam pomogne da koristite nepristupačnu aplikaciju ili da završi zadatak u prozoru u prvom planu
* Uveriti se da se vaše lice jasno vidi na kameri i da vaša pozadina izgleda profesionalno pre nego što snimite video zapise ili učestvujete u onlajn sastancima

## Modeli

* [Pollinations](https://pollinations.ai/): Tim koji stoji iza Pollinations.AI velikodušno sponzoriše besplatan GPT4 pristup za ovaj projekat, tako da korisnici ne moraju da unose sopstveni API ključ. Imajte na umu da je primećeno da ova usluga ume da ima greške, i toplo preporučujemo da koristite sopstvene ključeve kako biste u potpunosti iskoristili ovaj projekat.
* [OpenAI GPT modeli](https://platform.openai.com/docs/models): Zahtevaju OpenAI API ključ. Obuhvataju porodicu GPT-5.4 (5.4 i 5.4 mini), porodicu GPT-5.5 (5.5 i 5.5 pro), porodicu GPT-6 (6 Astra i 6 Luna) i porodicu GPT-6.1 (6.1 Sol i 6.1 Terra). Porodice GPT-5.4, GPT-5.5, GPT-6 i GPT-6.1 podržavaju upravljanje računarom.
* [Google Gemini](https://deepmind.google/models/gemini/), uključujući modele 2.5 Flash, 2.5 Flash-Lite, 2.5 Pro, 3.1 Flash-Lite, 3.1 Pro Preview, 3.5 Flash, 3.5 Flash-Lite, 3.6 Flash, 3.7 Flash, 3.8 Flash, 4 Hydrogen, 4 Argon i 4 Carbon.
* [Anthropic Claude](https://docs.anthropic.com/claude/docs/vision), uključujući Claude 4.5 (Sonnet, Opus), 4.6 (Sonnet, Opus), 4.7 Opus, 4.8 Opus, 5 (Sonnet, Opus, Fable), 5.1 Fable, 5.2 Fable i 5.5 (Haiku, Sonnet, Opus). Svi oni podržavaju upravljanje računarom.
* [Mistral Large 4](https://docs.mistral.ai/models/mistral-large-4-0)
* [xAI Grok](https://docs.x.ai/developers/models), uključujući Grok 4.20 (bez rezonovanja), 4.3, 4.5, 4.6 i 4.7.
* [Kimi](https://platform.kimi.ai/docs/guide/use-kimi-vision-model), multimodalni modeli kompanije Moonshot AI, uključujući Kimi K3 i Kimi K2.6.
* vivo BlueLM Vision: multimodalni model kompanije vivo, dostupan preko besplatnog NVDA-CN naloga. Pogledajte odeljak za podešavanje ispod.
* [Datalab Chandra 2](https://github.com/datalab-to/chandra): Najsavremeniji model za vid i OCR kompanije Datalab, specijalizovan za složene rasporede dokumenata, tabele, obrasce, rukopis, grafikone i matematiku. Podržava Datalab API u oblaku (na adresi [datalab.to](https://www.datalab.to)) ili sopstvenu instalaciju preko vLLM-a (korišćenjem `chandra_vllm` ili `/v1` krajnjih tačaka kompatibilnih sa OpenAI).
* [Ollama (nestabilno)](https://ollama.com/)
* [llama.cpp (izuzetno nestabilno i sporo u zavisnosti od vašeg hardvera, testirano sa modelima llava-v1.5/1.6, BakLLaVA, Obsidian i MobileVLM 1.7B/3B)](https://github.com/ggerganov/llama.cpp)
* [LiteLLM Proxy](https://docs.litellm.ai/docs/proxy/quick_start): Pristup većem broju AI modela preko jedinstvenog proxy servera. Zahteva URL adresu LiteLLM proxy servera, i opciono API ključ, u zavisnosti od podešavanja vašeg proxy servera. U dijalogu za podešavanje modela prikazuje se kao "LiteLLM Proxy". Podržava dinamički izbor modela i dodatna pitanja. Kompatibilan je sa svim formatima (PNG, JPEG, WEBP, GIF).
* [Seer](https://github.com/recursia-lab/Seer): Lokalno pokreće PaliGemma2 preko Seer servisa. Nisu potrebni API ključ ni internet veza. Napomena: ovaj model služi samo za kratke opise slika. Upiti i dodatna pitanja nisu podržani.

Pratite uputstva ispod kako biste podesili svaki od ovih modela.

## Početak

Preuzmite najnoviju verziju dodatka sa [ovog linka](https://github.com/cartertemm/AI-content-describer/releases/latest/). Kliknite na datoteku na računaru na kojem je NVDA instaliran, i nastavite sa instalacijom prateći uputstva.

Kada se NVDA prvi put pokrene sa ovim dodatkom, pitaće vas da preuzmete neke dodatne biblioteke. Pogledajte odeljak `Zavisnosti` ovog dokumenta za detalje.

Od verzije 2025.06.05, korišćenje modela GPT4 je besplatno zahvaljujući velikodušnosti zajednice koja stoji iza PollinationsAI.

Ako imate sredstva i želite da isprobate dodatne modele, uvek možete da koristite sopstveni API ključ i smanjite broj zahteva prema njihovim serverima. Ako ne, slobodno pređite na odeljak `Korišćenje` ovog dokumenta.

Pratite uputstva ispod da biste dobili API ključ od podržanog provajdera.

### Koji model da koristim?

Ranije smo davali preporuke za najjeftinije i najkvalitetnije opcije, ali se situacija toliko brzo menja da nije moguće održavati ih ažurnim.

Ukratko, većina najnovijih modela je dostigla nivo na kom su tačni za većinu svakodnevnih primena, pa izaberite provajdera koji vam je poznat.

Većina ljudi želi ravnotežu između tačnosti i cene. [LLM arena rang lista](https://lmarena.ai/leaderboard) (posebno kategorija vision) meri tačnost, dok [LLM kalkulator cena](https://www.llm-prices.com/) prikazuje cene.

Ako želite da koristite upravljanje računarom, izaberite jedan od podržanih OpenAI ili Anthropic modela navedenih iznad. Besplatan Pollinations pristup je koristan za opise slika, ali ne podržava upravljanje računarom.

### Dobijanje API ključa od kompanije OpenAI:

1. Posetite [OpenAI stranicu za API ključeve](https://platform.openai.com/account/api-keys)
2. Ako još nemate nalog, napravite ga. Ako imate, prijavite se.
3. Na stranici API keys, kliknite na opciju za pravljenje novog tajnog ključa. Kopirajte ga u vašu privremenu memoriju.
4. Uplatite bar 1 dolar na vaš nalog
5. U dijalogu NVDA podešavanja, krećite se dole do kategorije AI opisivač sadržaja, a zatim izaberite "upravljaj modelima (alt+m)", izaberite bilo koji OpenAI model (na primer "GPT-6.1 Sol") kao provajdera, tabom se krećite do polja za API ključ i nalepite ključ koji ste upravo napravili.

U trenutku pisanja ovog uputstva, OpenAI daje kredite novim nalozima za programere koji se mogu koristiti tri meseca, nakon ovog perioda oni se gube. Nakon ovog perioda, moraćete da kupite kredite. Obično korišćenje nikada ne bi trebalo da košta više od 5.00 dolara mesečno. Kako biste imali uvid, originalna verzija ovog dodatka je razvijena za nešto manje od jednog dolara. Uvek je moguće prijaviti se na vaš OpenAI nalog i kliknuti na "usage" da proverite vašu potrošnju.

### Dobijanje API ključa od kompanije Google

1. Prvo morate da napravite Google workspace projekat na stranici [Google cloud console](https://console.cloud.google.com/projectcreate). Uverite se da ste prijavljeni na vaš Google nalog.
2. Napravite ime dužine između četiri i trideset znakova, kao što je "Gemini" ili "NVDA dodatak"
3. Posetite [Google AI studio stranicu za API ključeve](https://makersuite.google.com/app/apikey)
4. Kliknite na "create API key"
5. U dijalogu NVDA podešavanja, krećite se dole do kategorije AI opisivač sadržaja, a zatim izaberite "upravljaj modelima (alt+m)", izaberite "Google Gemini" kao provajdera, tabom se krećite do polja za API ključ i nalepite ključ koji ste upravo napravili.

### Dobijanje API ključa od kompanije Anthropic

1. Prijavite se na [Anthropic konzolu](https://console.anthropic.com/login).
2. Kliknite na vaš profil -> API keys.
3. Kliknite na Create Key.
4. Unesite ime za ključ, kao što je "AIContentDescriber", a zatim kliknite na "Create Key" i kopirajte vrednost koja se pojavi. Ovo ćete nalepiti u polje za API ključ u kategoriji AI opisivač sadržaja u dijalogu NVDA podešavanja -> upravljaj modelima -> bilo koji Claude model (na primer "Claude 5 Sonnet").
5. Ako to već niste učinili, kupite bar 5 dolara kredita na [Anthropic stranici sa planovima](https://console.anthropic.com/settings/plans).

### Dobijanje API ključa od kompanije Mistral

1. Prijavite se ili napravite MistralAI nalog na [MistralAI stranici za prijavu](https://auth.mistral.ai/ui/login).
2. Ako pravite nalog ili se prijavljujete prvi put, dodajte radni prostor kada se to od vas zatraži, tako što ćete uneti ime i prihvatiti uslove korišćenja.
3. Kada se prijavite, izaberite "API keys" iz menija.
4. Kliknite na "create a new key" i kopirajte ga u privremenu memoriju. Ovu vrednost ćete nalepiti u polje za API ključ u kategoriji AI opisivač sadržaja u dijalogu NVDA podešavanja -> upravljaj modelima -> Mistral Large 4.
5. Uplatite sredstva na nalog, ako je potrebno.

### Dobijanje API ključa od kompanije Kimi (Moonshot AI)

1. Prijavite se ili napravite nalog na [Kimi platformi za programere](https://platform.kimi.ai/).
2. Kada se prijavite, otvorite odeljak za API ključeve u konzoli i napravite novi ključ.
3. Kopirajte ključ u privremenu memoriju. Ovu vrednost ćete nalepiti u polje za API ključ u kategoriji AI opisivač sadržaja u dijalogu NVDA podešavanja -> upravljaj modelima -> Kimi K3 (ili drugi Kimi model).
4. Uplatite sredstva na nalog, ako je potrebno.


### Aktiviranje modela VIVO BlueLM Vision preko NVDA-CN

Ova usluga je dostupna besplatno zahvaljujući partnerstvu između kompanije VIVO (vivo.com.cn) i kineske NVDA zajednice (NVDACN). Pruža visokokvalitetno multimodalno prepoznavanje i preporučeni je model za sve korisnike, posebno za one koji tek počinju.

Da biste koristili ovaj model, potreban vam je samo besplatan NVDA-CN nalog.

1.  Napravite nalog: Posetite NVDA-CN stranicu za registraciju: [https://nvdacn.com/admin/register.php](https://nvdacn.com/admin/register.php).
    * **Napomena**: Stranica je trenutno na kineskom jeziku. Preporučujemo da koristite ugrađenu funkciju za prevođenje u vašem pretraživaču kako biste popunili obrazac.
    * Biće vam zatraženi korisničko ime, lozinka i važeća e-mail adresa. Obavezno sačuvajte lozinku na bezbednom mestu, jer automatski oporavak lozinke još uvek nije dostupan.
2.  Potvrdite vašu e-mail adresu: Proverite vaše prijemno sanduče, pronađite e-mail za potvrdu i kliknite na link u njemu kako biste aktivirali nalog.
3.  Podesite dodatak:
    * Otvorite dijalog NVDA podešavanja i idite do kategorije "AI opisivač sadržaja".
    * Izaberite dugme "Upravljaj modelima".
    * Sa liste provajdera izaberite "vivo BlueLM Vision (NVDA-CN)".
    * Unesite vaše NVDA-CN korisničko ime i lozinku u odgovarajuća polja.
    * Kliknite na U redu da sačuvate vaše podatke za prijavu.

Sada možete da koristite VIVO model. Za sva pitanja u vezi sa nalogom, možete da kontaktirate NVDA-CN tim na adresi `support@nvdacn.com`.


### Podešavanje modela Ollama

Ovo je trenutno preporučena opcija za lokalno podešavanje.

Iako je Ollama integracija testirana temeljnije od llama.cpp, i dalje je manje stabilna od korišćenja API-ja i poznato je da se u nekim konfiguracijama čudno ponaša, uključujući i rušenja na računarima koji ne ispunjavaju potrebne zahteve.
U najmanju ruku, kada ovo prvi put isprobavate, sačuvajte sve dokumente i sve što vam je važno pre nego što nastavite, za slučaj da vam se ovo desi.

Prvo se uverite da možete da koristite vaš izabrani model koji podržava slike preko komandne linije. Koraci su sledeći:

1. Preuzmite Ollama instalaciju za Windows sa stranice [Ollama downloads](https://ollama.com/download).
2. Pokrenite ovu instalaciju. Ona će preuzeti sve zavisnosti koje su potrebne vašem računaru.
3. Pronađite model koji želite da koristite. Listu možete pronaći na ollama.com -> models -> vision, ili [direktno ovde](https://ollama.com/search?c=vision).
4. Preuzmite i pokrenite ovaj model tako što ćete otvoriti komandnu liniju i upisati `ollama run [model_name]`, naravno zamenjujući "[model_name]" modelom koji ste izabrali u koraku 3. Na primer, `ollama run llama3.2-vision`.
5. Ako se proces uspešno završio, naći ćete se u interaktivnom okruženju u kom možete da upisujete upite i dobijate odgovore od modela, nešto kao lokalni (i ograničeni) ChatGPT. Isprobajte ga tako što ćete nešto pitati (bilo šta) da vidite da li radi, a zatim upišite "/bye" da izađete iz ovog interfejsa.
6. U prozoru konzole upišite `ollama list`. Prva kolona će prikazati ime kao što je "llama3.2-vision:latest".
7. Idite u podešavanja AI opisivača sadržaja -> upravljaj modelima -> Ollama. U polje za ime modela unesite ovu vrednost i kliknite na U redu -> U redu. To je sve! Izaberite Ollama u podmeniju modela i trebalo bi da proradi posle nekog vremena.

### Podešavanje llama.cpp

Ovaj provajder trenutno ima dosta grešaka, i rezultati se mogu razlikovati. Trebalo bi da ga isprobavaju samo napredni korisnici koje zanima pokretanje lokalnih modela, i koji imaju hardver za to.

1. Preuzmite llama.cpp. U trenutku pisanja ovog uputstva, ovaj [pull request](https://github.com/ggerganov/llama.cpp/pull/5882) uklanja multimodalne mogućnosti, pa ćete želeti da koristite [poslednju verziju sa ovom podrškom](https://github.com/ggerganov/llama.cpp/releases/tag/b2356).
Ako koristite Nvidia grafičku karticu sa CUDA podrškom, preuzmite ove unapred napravljene binarne datoteke:
[llama-b2356-bin-win-cublas-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/llama-b2356-bin-win-cublas-cu12.2.0-x64.zip) i [cudart-llama-bin-win-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/cudart-llama-bin-win-cu12.2.0-x64.zip)
Koraci za rad sa drugom grafičkom karticom nisu obuhvaćeni ovim uputstvom, ali se mogu pronaći u llama.cpp readme datoteci.
2. Raspakujte obe datoteke u isti folder.
3. Pronađite kvantizovane formate modela koje želite da koristite na sajtu Huggingface. Za LLaVA 1.6 Vicuna 7B: [llava-v1.6-vicuna-7b.Q4_K_M.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/llava-v1.6-vicuna-7b.Q4_K_M.gguf) i [mmproj-model-f16.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/mmproj-model-f16.gguf)
4. Stavite ove datoteke u folder sa ostalim llama.cpp binarnim datotekama.
5. Iz komandne linije pokrenite binarnu datoteku llava.cpp servera, prosleđujući .gguf datoteke za model i multimodalni projektor (na sledeći način):
```
server.exe -m llava-v1.6-vicuna-7b.Q4_K_M.gguf --mmproj mmproj-model-f16.gguf
```
6. U dijalogu NVDA podešavanja, krećite se dole do kategorije AI opisivač sadržaja, a zatim izaberite "upravljaj modelima (alt+m)", izaberite "llama.cpp" kao provajdera, tabom se krećite do polja za osnovnu URL adresu i unesite krajnju tačku prikazanu u konzoli (podrazumevano "http://localhost:8080").
7. Druga mogućnost je da preskočite neke od ovih koraka i pokrenete llama.cpp na udaljenom serveru sa jačim hardverom od vašeg računara, a zatim unesete tu krajnju tačku.

### Podešavanje LiteLLM Proxy

LiteLLM Proxy pruža jedinstven interfejs za pristup većem broju AI modela preko jedne krajnje tačke, što pojednostavljuje upravljanje modelima i omogućava lako prebacivanje između provajdera.

1. Podesite LiteLLM proxy server prateći [LiteLLM proxy dokumentaciju](https://docs.litellm.ai/docs/proxy/quick_start). Proxy možete pokrenuti lokalno ili koristiti udaljeni server.
2. Ako ga pokrećete lokalno, najbrži način da počnete je:
```
pip install 'litellm[proxy]'
litellm --model gpt-4o
```
Ovo će pokrenuti proxy server na adresi `http://localhost:4000` koji prosleđuje zahteve modelu GPT-4o kompanije OpenAI.
3. Za produkcionu upotrebu, napravite `config.yaml` datoteku da biste podesili više modela i autentifikaciju. Pogledajte [LiteLLM vodič za podešavanje](https://docs.litellm.ai/docs/proxy/configs) za detalje.
4. U dijalogu NVDA podešavanja, krećite se dole do kategorije AI opisivač sadržaja, a zatim izaberite "upravljaj modelima (alt+m)" i izaberite "LiteLLM Proxy" kao provajdera.
5. Unesite URL adresu vašeg proxy servera u polje za osnovnu URL adresu (na primer "http://localhost:4000" za lokalni server ili URL adresu vašeg udaljenog servera).
6. Ako vaš proxy zahteva autentifikaciju, unesite API ključ u polje za API ključ. Ako ne, ostavite ga praznim.
7. Kliknite na dugme "Prikaži modele" da preuzmete dostupne modele sa vašeg proxy servera, a zatim izaberite model koji želite da koristite iz padajuće liste.
8. Prilagodite ostala podešavanja kao što su upit, maksimalan broj tokena i vremensko ograničenje po potrebi, a zatim kliknite na U redu.

Napomena: Dostupni modeli i njihove mogućnosti zavise od podešavanja vašeg LiteLLM proxy servera. Uverite se da je vaš proxy podešen sa modelima koji podržavaju slike kako bi opisivanje slika radilo.

### Podešavanje modela Seer

Seer pokreće PaliGemma2 na vašem računaru bez API ključa i bez veze sa oblakom. Imajte na umu da ovaj model služi samo za kratke opise slika; upiti i dodatna pitanja nisu podržani.

1. Instalirajte [Seer servis](https://github.com/recursia-lab/Seer). Dostupna je instalacija jednom komandom za Windows (.bat) i Linux/macOS (.sh).
2. U dijalogu NVDA podešavanja idite do kategorije AI opisivač sadržaja, izaberite "upravljaj modelima (alt+m)" i izaberite "Seer (requires installation)".
3. Osnovna URL adresa je podrazumevano `http://127.0.0.1:11435`. Ostavite je takvu osim ako niste promenili port servisa.
4. Kliknite na U redu. Servis mora biti pokrenut pre nego što zatražite opis.

### Podešavanje modela Datalab Chandra 2

Datalab Chandra 2 je najsavremeniji model za obradu dokumenata i OCR, specijalizovan za složene rasporede, tabele, obrasce, rukopis, grafikone i matematičke formule. Može se koristiti preko Datalab API-ja u oblaku, lokalnog kontejnera ili sopstvene vLLM instance.

#### Opcija A: Korišćenje Datalab API-ja u oblaku (preporučeno)
1. Napravite nalog na adresi [datalab.to](https://www.datalab.to). Novi nalozi dobijaju besplatne probne kredite.
2. Posetite [stranicu za API ključeve](https://www.datalab.to/app/keys) i napravite API ključ.
3. U dijalogu NVDA podešavanja idite do kategorije AI opisivač sadržaja, izaberite "upravljaj modelima (alt+m)" i izaberite "Datalab Chandra 2".
4. Unesite vaš API ključ u polje "API ključ".
5. Osnovna URL adresa je podrazumevano podešena na `https://www.datalab.to/api/v1/convert`. Možete da prilagodite režim obrade (`fast`, `balanced` ili `accurate`) u zavisnosti od vaših potreba.
6. Kliknite na U redu. Model će sada biti dostupan u meniju AI opisivača sadržaja.

#### Opcija B: Sopstvena instalacija sa vLLM
1. Pokrenite vaš lokalni vLLM server sa modelom Chandra 2 (na primer, korišćenjem `chandra_vllm` ili `vllm serve datalab-to/chandra-ocr-2`). Server podrazumevano radi na adresi `http://localhost:8000/v1`.
2. U NVDA podešavanjima -> AI opisivač sadržaja -> Upravljaj modelima -> "Datalab Chandra 2", unesite vašu lokalnu krajnju tačku u polje "Osnovna URL adresa" (na primer, `http://localhost:8000/v1`).
3. Podesite ime modela ako se razlikuje od podrazumevanog (`datalab-to/chandra-ocr-2`), ostavite API ključ praznim (ili unesite bearer token ako je autentifikacija omogućena) i kliknite na U redu.

## Korišćenje

Podrazumevano je dodeljeno šest prečica:

* NVDA+šift+i: Prikaži meni koji pita da li opisati trenutni fokus, navigacioni objekat, fizičku kameru ili ceo ekran, ili upravljati računarom veštačkom inteligencijom.
* NVDA+šift+u: Opiši sadržaj trenutnog navigacionog objekta korišćenjem veštačke inteligencije.
* NVDA+šift+y: Opiši sliku (ili putanju do datoteke sa slikom) u privremenoj memoriji korišćenjem veštačke inteligencije.
* NVDA+šift+j: Opiši položaj vašeg lica u kadru izabrane kamere. Ako imate više povezanih kamera, idite u meni AI opisivača sadržaja (NVDA+šift+i) i izaberite kameru koju želite da koristite stavkom "izaberi kameru" u podmeniju za prepoznavanje lica.
* NVDA+alt+c: Otvori dijalog razgovora sa veštačkom inteligencijom za postavljanje dodatnih pitanja.
* NVDA+control+šift+p: Pauziraj ili nastavi aktivnu sesiju upravljanja računarom.

Sedam prečica je nedodeljeno:

* Opiši sadržaj trenutno fokusirane stavke korišćenjem veštačke inteligencije.
* Slikaj ekran, a zatim ga opiši korišćenjem veštačke inteligencije.
* Fotografiši izabranom kamerom, a zatim opiši sliku korišćenjem veštačke inteligencije.
* Otkaži aktivnu sesiju upravljanja računarom.
* Slikaj trenutni fokusirani objekat i kopiraj sliku u privremenu memoriju.
* Slikaj trenutni navigacioni objekat i kopiraj sliku u privremenu memoriju.
* Slikaj ceo ekran i kopiraj sliku u privremenu memoriju.

Tri komande za kopiranje se nalaze i u podmeniju "Kopiraj sliku u privremenu memoriju" u NVDA+šift+i meniju. One ništa ne šalju AI usluzi. Koristite ih da nalepite snimak u Be My AI ili neku drugu aplikaciju koju ovaj dodatak ne podržava. Kopirana slika zamenjuje prethodni sadržaj privremene memorije.

Ne ustručavajte se da ove prečice prilagodite u bilo kom trenutku iz dijaloga ulaznih komandi.

### Dodatna pitanja o opisu

Ponekad odgovor koji dobijete od veštačke inteligencije nije dovoljan. Možda je slika lošeg kvaliteta, nepotpuna ili sadrži neželjene detalje. Možda želite da se usredsredite samo na određeni deo ili da napravite jasniju fotografiju bez gubljenja konteksta.
Nakon što dobijete opis, možete pritisnuti NVDA+alt+c, ili izabrati "Dodatna pitanja o prethodnom opisu" iz kontekstnog menija AI opisivača sadržaja (NVDA+šift+i). Fokus je podrazumevano postavljen na polje za poruku.
Da biste dodali još jednu sliku, samo ostavite prozor razgovora otvoren i koristite dodatak kao i obično. Kada se napravi slika (bilo da je sa kamere, sistemske kontrole, slike ekrana itd.), bićete upitani da li želite da je priložite trenutnoj sesiji ili da započnete novu.

### Upravljanje računarom

Upravljanje računarom omogućava AI opisivaču sadržaja da upravlja aktivnom aplikacijom pomoću miša i tastature nakon što opišete zadatak. Ovo može da pomogne kod zadataka koje je teško ili nemoguće ručno obaviti zbog nepristupačnosti.

Pošto ovo daje AI modelu kontrolu nad vašim računarom, koristite ga pažljivo. Dodatak traži vašu saglasnost pre početka, obaveštava vas o radnjama dok se izvršavaju i pita vas pre potencijalno rizičnih radnji. Vi ste odgovorni za ono što radi, pa pratite sesiju i izbegavajte da ga koristite za osetljive poslove ili one koje je teško poništiti.

Upravljanje računarom možete pauzirati ili nastaviti u bilo kom trenutku prečicom `NVDA+Control+Shift+P`. Dok je pauziran, dodatak neće izvršiti sledeću radnju dok ga ne nastavite.

Dodatak koristi zvučne signale da označi stanje upravljanja. Visok zvučni signal znači da model preuzima ili nastavlja upravljanje. Nizak zvučni signal znači da je upravljanje pauzirano, bilo zato što ste ga vi pauzirali ili zato što modelu treba vaš unos. Kratak nizak zvučni signal greške znači da je sesija zaustavljena zbog API greške.

Dok je sesija upravljanja aktivna, model će najaviti šta namerava da uradi pre nego što pošalje unos. Ništa se ne dešava dok se ta najava ne završi, osim ako ne pritisnete `Control` da prekinete najavu i omogućite da se radnja izvrši ranije.

Ako model nije siguran kako da izvrši radnju, treba mu više informacija ili vam iz nekog drugog razloga vraća reč, sesija se pauzira i dijalog za upravljanje računarom prelazi u prvi plan. Upišite dodatnu poruku u njega da nastavite razgovor, ili zatvorite dijalog da zaustavite sesiju.

Ova funkcija radi samo sa modelima koji pružaju alat za upravljanje računarom: GPT-5.4, GPT-5.4 mini, GPT-5.5, GPT-5.5 pro, GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna, Claude 4.5 Sonnet, Claude 4.5 Opus, Claude 4.6 Sonnet, Claude 4.6 Opus, Claude 4.7 Opus, Claude 4.8 Opus, Claude 5 Sonnet, Claude 5 Opus, Claude 5 Fable, Claude 5.1 Fable, Claude 5.2 Fable, Claude 5.5 Haiku, Claude 5.5 Sonnet i Claude 5.5 Opus. Ostali modeli mogu da opisuju slike, ali ne pružaju strukturirane radnje miša i tastature potrebne za upravljanje računarom.

Da biste koristili upravljanje računarom:

1. Podesite i izaberite jedan od podržanih modela.
2. Otvorite aplikaciju ili prozor sa kojim želite da model radi.
3. Pritisnite `NVDA+shift+i`, a zatim izaberite "Upravljaj računarom...".
4. Upišite zadatak koji želite da se izvrši i pritisnite Pošalji.
5. Pregledajte zahtev za saglasnost. Ako dozvolite sesiju, pratite radnje i odobrite ili otkažite sve zahteve za rizične radnje.

Napomena: Ovu funkciju treba smatrati beta verzijom, i aktivno radimo na tome da implementacija bude pouzdanija.

## Zavisnosti

Neke biblioteke koje su potrebne ovom dodatku su prevelike da bi bile uključene u paket dodatka. Umesto toga, kada se NVDA prvi put pokrene sa instaliranim dodatkom, bićete upitani da li želite da ih preuzmete. Izaberite da, sačekajte da se preuzimanje završi, i NVDA će se ponovo pokrenuti.

Preuzima se zip datoteka veličine oko 35 do 70 MB, u zavisnosti od vaše verzije NVDA. Preuzima se sa stranice [libs-release](https://github.com/cartertemm/AI-content-describer/releases/tag/libs-release) ovog repozitorijuma. Ako GitHub nije dostupan, dodatak nudi da pokuša sa alternativnim serverom koji obezbeđuje kineska NVDA zajednica.

Zip datoteka sadrži:

* [NumPy](https://numpy.org/): računanje sa nizovima, potrebno za OpenCV.
* [OpenCV](https://opencv.org/) (`cv2`): pronalazi vaše lice na slikama sa veb kamere za funkciju prepoznavanja lica.
* [Pillow](https://python-pillow.org/) (`PIL`): pravi slike ekrana i pretvara ih u slike koje AI modeli mogu da pročitaju.
* [Markdown](https://python-markdown.github.io/): prikazuje opise sa formatiranjem, kao što su naslovi, liste i tabele.
* [pygrabber](https://github.com/andreaschiavinato/python_grabber): prikazuje listu veb kamera na vašem računaru.
* Nekoliko modula iz standardne Python biblioteke koje NVDA ne sadrži (`html`, `xml`, `pathlib`, `secrets` i `_markupbase`). Potrebni su gore navedenim bibliotekama.

Datoteke se smeštaju u folder čije ime počinje sa `aic-py-` iza čega sledi verzija Pythona koju koristi NVDA, na primer `aic-py-3.13`. Ovaj folder se nalazi u folderu vaše NVDA korisničke konfiguracije, obično `%APPDATA%\nvda`. Svaka verzija Pythona ima svoj folder, što znači da dodatak ponovo preuzima biblioteke kada novo izdanje NVDA promeni verziju Pythona. Uklanjanjem dodatka briše se folder za trenutnu verziju Pythona koju koristi NVDA.

Ako preuzimanje ne radi, biblioteke možete instalirati i sami. Preuzmite `aic-py-3.13.zip` (ili datoteku za verziju Pythona koju koristi vaš NVDA) sa stranice libs-release, raspakujte je u folder vaše NVDA korisničke konfiguracije i ponovo pokrenite NVDA.

## Pakovanje dodatka

Da biste napravili paket dodatka iz izvornog koda, trebaće vam:

* Python distribucija (3.7 ili novija se preporučuje). Proverite [Python websajt](https://www.python.org) za Windows instalacije. Molimo imajte na umu da priprema NVDA izvornog koda i drugih neophodnih modula zahteva 32-bitnu verziju Pythona 3.7.
* Scons - [websajt](https://www.scons.org/) - verzija 4.3.0 ili novija. Možete da ga instalirate uz PIP. `pip install scons`
* Markdown 3.3.0 ili noviji. `pip install markdown`

Zatim otvorite Terminal po vašem izboru:

```
git clone https://github.com/cartertemm/AI-content-describer.git
cd AI-content-describer
scons
```

Nakon što se završi `scons` komanda, *.nvda-addon datoteka će biti u glavnom folderu ovog repozitorijuma i biće spremna za testiranje i objavljivanje.

Ako dodate dodatne stringove koji zahtevaju prevod, važno je ponovo spakovati .pot datoteku ovako:

```
scons pot
```

## Kako prevoditi?

Na Windows računaru:

* Preuzmite [poedit](https://poedit.net/). Ovo je program kojeg ćete koristiti da svaku poruku prevedete sa Engleskog.
* Preuzmite .pot datoteku sa svim stringovima [ovde](https://raw.githubusercontent.com/cartertemm/AI-content-describer/main/AIContentDescriber.pot)
* Otvorite datoteku koju ste upravo preuzeli u programu poedit. Kliknite "Napravi novi prevod" u prozoru koji se pojavi, a zatim odaberite odredišni jezik.
* Prođite kroz izvorne tekstove i prevedite ih na odredišni jezik, tako što ćete ih upisati u polje za prevod. Za dodatnu pomoć, desnim klikom na stavku -> pojavljivanja u kodu možete u redu iznad pročitati komentare koji počinju sa "# Translators: ". Ovi komentari su vam dodatno dostupni na jednom mestu u .pot datoteci.
* Kada završite, kliknite na Datoteka -> Sačuvaj ili pritisnite ctrl+s a zatim izaberite lokaciju za nove .mo i .po datoteke kako bi bile sačuvane. Ovo su datoteke koje treba da mi pošaljete e-mailom ili da ih priložite uz vaš pull request.
* Prevedite sadržaj datoteke readme.md (ova datoteka). Takođe priložite taj prevod!

## Saradnici

Svima se od srca zahvaljujemo i biće spomenuti.
Sledeće osobe su radile na ovom dodatku.

* [Cary Rowen](https://github.com/cary-rowen): omogućio rad dodatka za kineske korisnike preko alternativnih servera za zavisnosti, dodao podršku za Vivo Blue provajdera
* [Mazen](https://github.com/mzanm): implementacija Markdown formata, drugi doprinosi kodu
* [Kostenkov-2021](https://github.com/Kostenkov-2021): ruski prevod
* [Nidza07](https://github.com/nidza07): srpski prevod
* [Heorhii Halas](nvda.translation.uk@gmail.com) i [George-br](https://github.com/George-br): ukrajinski prevod
* [Umut Korkmaz](umutkork@gmail.com): turski prevod
* [Platinum_Hikari](urbain_onces.0r@icloud.com): francuski prevod
* [Lukas](https://4sensegaming.cz): češki prevod
* [Michaela](https://technologiebezzraku.sk): slovački prevod
* [loginerror](https://github.com/theloginerror): poljski prevod

Imate problem? Pošaljite ga na Engleskom u [issue tracker](https://github.com/cartertemm/AI-content-describer/issues)

Imate predlog za novu funkciju? Prijavite to na isti način, a zatim možemo da pričamo o implementaciji. Takođe ću pregledati pull requests bez prethodno napravljenih tiketa, ali je moguće da će utrošiti više vremena za sve, posebno ako odlučim da nova ispravka ili funkcija mora da radi drugačije od onoga što je predloženo.

Prevodi su dobrodošli. Što više ljudi može da pristupi ovoj moćnoj tehnologiji, to bolje!

Ako nemate Github, ili ne želite da ga koristite, možete da mi [napišete e-mail](mailto:carter@ctemm.me) - carter (et) ctemm (tačka) me.

Hvala na podršci!
