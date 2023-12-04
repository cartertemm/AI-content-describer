# AI opisivač sadržaja za NVDA

Ovaj dodatak vam omogućava da dobijete detaljne opise za slike i drugi vizuelni nepristupačan sadržaj.

Kroz multimodalne sposobnosti GPT-4 velikog jezičkog modela (eng. large language model), naš cilj je da vam dostavimo najbolje opise sadržaja. Za više informacija o osnovi modela, posetite [GPT-4V](https://openai.com/research/gpt-4v-system-card).

## Karakteristike

* Opisivanje fokusiranog objekta, navigacionog objekta ili celog ekrana
* Opisivanje bilo koje slike koja je kopirana u privremenu memoriju, bez obzira da li je to slika iz e-maila ili putanja u Windows istraživaču datoteka
* Podrška za širok broj formata uključujući PNG (.png), JPEG (.jpeg i .jpg), WEBP (.webp), i neanimirani GIF (.gif)
* Opciono pamćenje ili keširanje odgovora kako bi se uštedela API potrošnja
* Za napredno korišćenje, prilagodite upit i broj tokena kako biste prilagodili informacije vašim potrebama

## Svrha korišćenja

Ovaj projekat je motivisalo nekoliko različitih primera.

NVDA ima ugrađenu mogućnost da izvrši optičko prepoznavanje znakova (OCR), što je ogroman korak napred. Ako pokušavate da pročitate tekst sa slike ili iz PDF dokumenta, ovo je opcija koju tražite.

Ali, OCR može samo da analizira podatke koji su *možda* tekstualni. Gubi svrhu kada je u pitanju prepoznavanje konteksta, objekata i veze između njih koje ove slike predstavljaju. A Internet je pun takvih slika. Logotipi, portreti, mimovi, ikone, grafikoni, dijagrami, trakasti ili linijski grafikoni... Šta god vam padne na pamet. Ovakav sadržaj je svuda, i obično nije u formatu koji omogućava čitaču ekrana da ga obradi.
Do skoro, u glavnom je neograničena odgovornost bila na autorima sadržaja da pruže alternativne tekstualne opise. Iako je ovo još uvek neophodno, teško je promeniti činjenicu da su opisi visokog kvaliteta izuzetak, a ne pravilo.

Sada, mogućnosti su skoro beskrajne. Možete:

* Shvatiti vizuelni izgled radne površine ili određenog prozora kako biste razumeli pozicije ikonica kada učite druge
* Dobijati detaljne informacije o statusu igrica, virtuelnih mašina, i tako dalje kada zvuk nije dovoljan ili je nedostupan
* Shvatiti šta se prikazuje na grafikonu
* Pročitati slike ekrana
* Uveriti se da se vaše lice jasno vidi na kameri pre nego što snimite video zapise ili učestvujete u onlajn sastancima

## Početak

Preuzmite najnoviju verziju dodatka sa [ovog linka](https://github.com/cartertemm/AI-content-describer/releases/latest/). Kliknite na datoteku na računaru na kojem je NVDA instaliran, a zatim pratite uputstva ispod da biste dobili API ključ za OpenAI:

1. Posetite https://platform.openai.com/account/api-keys
2. Ako još nemate nalog, napravite ga. Ako imate, prijavite se.
3. Na stranici API keys, kliknite na opciju za pravljenje novog tajnog ključa. Kopirajte ga u vašu privremenu memoriju.
4. Uplatite bar 1 dolar na vaš nalog
5. U dijalogu NVDA podešavanja, krećite se dole do kategorije AI opisivač sadržaja, a zatim se tabom krećite do polja za API ključ i nalepite ključ koji ste upravo napravili.

U trenutku pisanja ovog uputstva, OpenAI daje kredite novim nalozima za programere koji se mogu koristiti tri meseca, nakon ovog perioda oni se gube.

Nakon ovog perioda, moraćete da kupite kredite. Obično korišćenje nikada ne bi trebalo da košta više od 5.00 dolara mesečno. Kako biste imali uvid, originalna verzija ovog dodatka je razvijena za nešto manje od jednog dolara. Uvek je moguće prijaviti se na vaš OpenAI nalog i kliknuti na "usage" da proverite vašu potrošnju.

## Korišćenje

Podrazumevano su dodeljene tri prečice:

* NVDA+šift+i: Prikaži meni koji pita da li opisati trenutni fokus, navigacioni objekat ili ceo ekran veštačkom inteligencijom.
* NVDA+šift+u: Opiši sadržaj trenutnog navigacionog objekta korišćenjem veštačke inteligencije.
* NVDA+šift+y: Opiši sliku (ili putanju do datoteke sa slikom) u privremenoj memoriji korišćenjem veštačke inteligencije.

Dve prečice su nedodeljene:

* Opiši sadržaj trenutno fokusirane stavke korišćenjem veštačke inteligencije.
* Slikaj ekran, a zatim ga opiši korišćenjem veštačke inteligencije.

Ne ustručavajte se da ove prečice prilagodite u bilo kom trenutku iz dijaloga ulaznih komandi.

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

Nakon što se završi `scons` komanda, *.nvda-addon datoteka će biti u glavnom folderu i biće spremna za testiranje i objavljivanje.

Ako dodate dodatne stringove koji zahtevaju prevod, važno je ponovo spakovati .pot datoteku ovako:

```
scons pot
```

## Kako prevoditi?

Na Windows računaru:

* Preuzmite [poedit](https://poedit.net/). Ovo je program kojeg ćete koristiti da svaku poruku prevedete sa Engleskog.
* Preuzmite .pot datoteku sa svim stringovima [ovde](https://raw.githubusercontent.com/cartertemm/AI-content-describer/main/AIContentDescriber.pot)
* Otvorite datoteku koju ste upravo preuzeli u programu poedit. Kliknite  "Napravi novi prevod" u prozoru koji se pojavi, a zatim odaberite odredišni jezik.
* Prođite kroz izvorne tekstove i prevedite ih  na odredišni jezik, tako što ćete ih upisati u polje za prevod. Za dodatnu pomoć, desnim klikom na stavku -> pojavljivanja u kodu možete u redu iznad pročitati komentare koji počinju sa "# Translators: ". Ovi komentari su vam dodatno dostupni na jednom mestu u .pot datoteci.
* Kada završite, kliknite na Datoteka -> Sačuvaj ili pritisnite ctrl+s a zatim izaberite lokaciju za nove .mo i .po datoteke kako bi bile sačuvane. Ovo su datoteke koje treba da mi pošaljete e-mailom ili da ih priložite uz vaš pull request.
* Prevedite sadržaj datoteke readme.md (ova datoteka). Takođe priložite taj prevod!

## Saradnici

Svima se od srca zahvaljujemo i biće spomenuti.

Imate problem? Pošaljite ga na Engleskom u [issue tracker](https://github.com/cartertemm/AI-content-describer/issues)

Imate predlog za novu funkciju? Prijavite to na isti način, a zatim možemo da pričamo o implementaciji. Takođe ću pregledati pull requests bez prethodno napravljenih tiketa, ali je moguće da će utrošiti više vremena za sve, posebno ako odlučim da nova ispravka ili funkcija mora da radi drugačije od onoga što je predloženo.

Prevodi su dobrodošli.

Ako nemate Github, ili ne želite da ga koristite, možete da mi [napišete e-mail](mailto:cartertemm@gmail.com) - cartertemm (et) gmail (tačka) com.

rHvala na podršci!
