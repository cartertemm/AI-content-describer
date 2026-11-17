# Opis treści za pomocą AI dla NVDA

Ten dodatek umożliwia uzyskanie szczegółowych opisów obrazów, elementów interfejsu użytkownika oraz innych treści, które są wizualnie niedostępne.

Wykorzystując możliwości multimodalne zaawansowanych modeli AI oraz algorytmy komputerowego rozpoznawania obrazów, dążymy do dostarczania opisów treści najwyższej jakości, zwiększając ogólną niezależność użytkownika. Aby uzyskać więcej informacji na temat używanych modeli, zapoznaj się z odpowiednią sekcją tego dokumentu.

## Funkcje

* Opisuj aktualnie sfokusowany obiekt, obiekt nawigatora, cały ekran lub wykonaj zdjęcie za pomocą wbudowanej kamery.
* Opisuj obrazy skopiowane do schowka, niezależnie od tego, czy to zdjęcia z e-maila, czy ścieżki w Eksploratorze Windows.
* Kopiuj obraz sfokusowanego obiektu, obiektu nawigatora lub całego ekranu do schowka, aby wkleić go w innych aplikacjach.
* Określaj, czy twarz użytkownika znajduje się na środku kadru, wykorzystując algorytmy komputerowego rozpoznawania obrazów (funkcja nie wymaga płatnego dostępu do API).
* Używaj obsługiwanych modeli do sterowania aktywną aplikacją za pomocą myszy i klawiatury przy zadaniach, które mogą być niedostępne.
* Domyślnie bezpłatny; opcjonalnie możesz dodać własny klucz API, aby uzyskać dostęp do większej liczby modeli.
* Obsługuje wielu dostawców (GPT od OpenAI i bezpłatny dostęp przez Pollinations, Gemini od Google, Mistral Large 4, Claude od Anthropic, Grok od xAI, Kimi od Moonshot AI, vivo BlueLM Vision przez NVDA-CN, Datalab Chandra 2, Ollama, llama.cpp, LiteLLM Proxy i Seer).
* Obsługuje różne formaty, takie jak PNG (.png), JPEG (.jpeg, .jpg), WEBP (.webp) i nieruchome GIFy (.gif).
* Opcjonalne buforowanie odpowiedzi w celu oszczędzania limitów API.
* Zaawansowane funkcje, takie jak dostosowywanie zapytań (promptów) i liczby tokenów, aby dostosować informacje do potrzeb użytkownika.
* Zadawaj pytania uzupełniające i dołączaj dodatkowe obrazy.
* Renderowanie Markdown do łatwego przeglądania ustrukturyzowanych informacji (wystarczy włączyć ustawienie otwierania wyników w przeglądalnym oknie dialogowym i dodać np. „odpowiedz w Markdown” na końcu zapytania).

## Przykłady użycia

Projekt ten miał kilka głównych celów.

NVDA natywnie obsługuje rozpoznawanie tekstu (OCR), co jest przełomowe. Jeśli chcesz wyodrębnić tekst z obrazu lub pliku PDF, to doskonałe rozwiązanie.

Jednak OCR analizuje tylko dane, które *mogą być* tekstem. Nie uwzględnia kontekstu, obiektów ani relacji przedstawionych na obrazach. A internet jest pełen takich treści: logo, portrety, memy, ikony, wykresy, diagramy, grafy słupkowe/liniowe… Są wszędzie i często nie są w formacie, który może być interpretowany przez czytniki ekranu.
Do niedawna istniała silna zależność od autorów treści, którzy dostarczali alternatywne opisy tekstowe. Choć nadal jest to konieczne, wysoka jakość tych opisów zdarza się rzadziej niż byśmy chcieli.

Teraz możliwości są niemal nieograniczone. Możesz:

* Wizualizować pulpit lub konkretne okno, aby zrozumieć rozmieszczenie ikon podczas szkolenia innych.
* Uzyskać szczegółowe informacje o statusie gier, maszyn wirtualnych itp., gdy dźwięk jest niewystarczający lub niedostępny.
* Dowiedzieć się, co przedstawia wykres.
* Rozszyfrować zrzuty ekranu lub udostępnianie ekranu w Zoomie lub Microsoft Teams.
* Poprosić obsługiwany model o pomoc w obsłudze niedostępnej aplikacji lub wykonaniu zadania w oknie na pierwszym planie.
* Upewnić się, że twarz jest dobrze widoczna na kamerze, a tło wygląda profesjonalnie przed nagraniem wideo lub uczestnictwem w spotkaniach online.

## Modele

* [Pollinations](https://pollinations.ai/): Zespół Pollinations.AI hojnie sponsoruje bezpłatny dostęp do GPT4 dla tego projektu, więc użytkownicy nie muszą podawać własnego klucza API. Zauważono jednak, że usługa bywa zawodna, dlatego zdecydowanie zalecamy korzystanie z własnych kluczy, aby w pełni wykorzystać możliwości tego projektu.
* [Modele GPT od OpenAI](https://platform.openai.com/docs/models): Wymagają klucza API OpenAI. Obejmują rodzinę GPT-5.4 (5.4 i 5.4 mini), rodzinę GPT-5.5 (5.5 i 5.5 pro), rodzinę GPT-6 (6 Astra i 6 Luna) oraz rodzinę GPT-6.1 (6.1 Sol i 6.1 Terra). Sterowanie komputerem obsługują rodziny GPT-5.4, GPT-5.5, GPT-6 i GPT-6.1.
* [Google Gemini](https://deepmind.google/models/gemini/), w tym modele 2.5 Flash, 2.5 Flash-Lite, 2.5 Pro, 3.1 Flash-Lite, 3.1 Pro Preview, 3.5 Flash, 3.5 Flash-Lite, 3.6 Flash, 3.7 Flash, 3.8 Flash, 4 Hydrogen, 4 Argon i 4 Carbon.
* [Anthropic Claude](https://docs.anthropic.com/claude/docs/vision), w tym Claude 4.5 (Sonnet, Opus), 4.6 (Sonnet, Opus), 4.7 Opus, 4.8 Opus, 5 (Sonnet, Opus, Fable), 5.1 Fable, 5.2 Fable i 5.5 (Haiku, Sonnet, Opus). Wszystkie obsługują sterowanie komputerem.
* [Mistral Large 4](https://docs.mistral.ai/models/mistral-large-4-0)
* [xAI Grok](https://docs.x.ai/developers/models), w tym Grok 4.20 (bez rozumowania), 4.3, 4.5, 4.6 i 4.7.
* [Kimi](https://platform.kimi.ai/docs/guide/use-kimi-vision-model), modele multimodalne od Moonshot AI, w tym Kimi K3 i Kimi K2.6.
* vivo BlueLM Vision: model multimodalny od vivo, dostępny przez bezpłatne konto NVDA-CN. Zobacz sekcję konfiguracji poniżej.
* [Datalab Chandra 2](https://github.com/datalab-to/chandra): Nowoczesny model wizyjny i OCR od Datalab, specjalizujący się w złożonych układach dokumentów, tabelach, formularzach, piśmie odręcznym, wykresach i wzorach matematycznych. Obsługuje zarządzane API w chmurze Datalab (na stronie [datalab.to](https://www.datalab.to)) lub własne wdrożenia przez vLLM (za pomocą `chandra_vllm` lub punktów końcowych `/v1` zgodnych z OpenAI).
* [Ollama (niestabilny)](https://ollama.com/)
* [llama.cpp (bardzo niestabilny i wolny, w zależności od sprzętu, przetestowany z modelami llava-v1.5/1.6, BakLLaVA, Obsidian i MobileVLM 1.7B/3B)](https://github.com/ggerganov/llama.cpp)
* [LiteLLM Proxy](https://docs.litellm.ai/docs/proxy/quick_start): Dostęp do wielu modeli AI przez jeden serwer proxy. Wymaga adresu URL serwera proxy LiteLLM oraz, w zależności od konfiguracji proxy, opcjonalnie klucza API. W oknie konfiguracji modeli występuje jako „LiteLLM Proxy”. Obsługuje dynamiczny wybór modelu i pytania uzupełniające. Zgodny ze wszystkimi formatami (PNG, JPEG, WEBP, GIF).
* [Seer](https://github.com/recursia-lab/Seer): Uruchamia PaliGemma2 lokalnie przez usługę Seer. Nie wymaga klucza API ani połączenia z internetem. Uwaga: ten model tylko generuje podpisy obrazów. Zapytania i pytania uzupełniające nie są obsługiwane.

Szczegółowe instrukcje konfiguracyjne znajdują się poniżej.

## Pierwsze kroki

Pobierz najnowszą wersję dodatku z [tego linku](https://github.com/cartertemm/AI-content-describer/releases/latest/). Kliknij na plik na komputerze z zainstalowanym NVDA i przeprowadź instalację zgodnie z wyświetlanymi instrukcjami.

Przy pierwszym uruchomieniu NVDA z dodatkiem pojawi się prośba o pobranie dodatkowych bibliotek. Szczegóły znajdziesz w sekcji `Zależności` tego dokumentu.

Od wersji 2025.06.05 korzystanie z GPT4 jest bezpłatne dzięki hojności społeczności skupionej wokół PollinationsAI.

Jeśli masz środki i chcesz wypróbować inne modele, zawsze możesz użyć własnego klucza API i zmniejszyć liczbę zapytań do ich serwerów. Jeśli nie, możesz przejść od razu do sekcji `Jak korzystać z tego dodatku`.

Wykonaj poniższe kroki, aby uzyskać klucz API od obsługiwanego dostawcy.

### Którego modelu użyć?

Wcześniej podawaliśmy zalecenia dotyczące najtańszych i najlepszych jakościowo opcji, ale rynek zmienia się tak szybko, że nie da się ich aktualizować na bieżąco.

W skrócie: większość najnowszych modeli osiągnęła poziom, na którym są dokładne w większości codziennych zastosowań, więc wybierz dostawcę, którego znasz.

Większość osób szuka równowagi między dokładnością a kosztem. [Ranking LLM arena](https://lmarena.ai/leaderboard) (szczególnie kategoria vision) mierzy poprawność, a [kalkulator cen LLM](https://www.llm-prices.com/) przedstawia ceny.

Jeśli chcesz korzystać ze sterowania komputerem, wybierz jeden z obsługiwanych modeli OpenAI lub Anthropic wymienionych powyżej. Bezpłatny dostęp przez Pollinations przydaje się do opisywania obrazów, ale nie obsługuje sterowania komputerem.

### Jak uzyskać klucz API od OpenAI

1. Przejdź na stronę [OpenAI API key](https://platform.openai.com/account/api-keys).
2. Jeśli nie masz konta, utwórz je. Jeśli masz, zaloguj się.
3. Na stronie kluczy API kliknij, aby utworzyć nowy klucz. Skopiuj go do schowka.
4. Zasil konto kwotą co najmniej 1 USD.
5. W oknie ustawień NVDA przejdź do kategorii „Opis treści za pomocą AI”, wybierz „Zarządzaj modelami (alt+m)”, wybierz jako dostawcę dowolny model OpenAI (na przykład „GPT-6.1 Sol”), przejdź do pola klucza API i wklej tam wygenerowany klucz.

W momencie pisania tego tekstu Open-AI udostępnia nowym kontom deweloperskim darmowy limit, z którego można korzystać przez trzy miesiące, po czym wygasa. Po tym okresie będziesz musiał zakupić nowy limit. Typowe wykorzystanie nie powinno nigdy przekraczać 5 dolarów (USD) miesięcznie. Jako punkt odniesienia, oryginalna wersja tego dodatku została opracowana za nieco mniej niż dolara. Zawsze możesz zalogować się na swoje konto OpenAI i kliknąć „usage”, aby sprawdzić swój limit.

### Jak uzyskać klucz API od Google

1. Najpierw utwórz projekt w Google Workspace, przechodząc na stronę [Google Cloud Console](https://console.cloud.google.com/projectcreate). Upewnij się, że jesteś zalogowany do swojego konta Google.
2. Stwórz nazwę projektu o długości od 4 do 30 znaków, np. „Gemini” lub „NVDA addon”.
3. Przejdź na stronę kluczy API Google AI Studio: [API keys](https://makersuite.google.com/app/apikey).
4. Kliknij „utwórz klucz API”.
5. W ustawieniach NVDA przejdź do kategorii „Opis treści za pomocą AI”, wybierz „zarządzaj modelami (alt+m)”, ustaw jako dostawcę „Google Gemini”, przejdź do pola klucza API i wklej tam wygenerowany klucz.

### Jak uzyskać klucz API od Anthropic

1. Zaloguj się do [Anthropic Console](https://console.anthropic.com/login).
2. Kliknij w swój profil -> API keys.
3. Kliknij „Utwórz klucz”.
4. Wprowadź nazwę klucza, np. „AIContentDescriber”, a następnie kliknij „Utwórz klucz” i skopiuj wyświetloną wartość. Wklej ten klucz w polu klucza API w kategorii „Opis treści za pomocą AI” w ustawieniach NVDA -> Zarządzaj modelami -> dowolny model Claude (na przykład „Claude 5 Sonnet”).
5. Jeśli jeszcze tego nie zrobiłeś, doładuj konto kwotą co najmniej 5 USD na stronie [Anthropic Plans](https://console.anthropic.com/settings/plans).

### Jak uzyskać klucz API od Mistral

1. Zaloguj się lub utwórz konto MistralAI na [stronie logowania MistralAI](https://auth.mistral.ai/ui/login).
2. Jeśli tworzysz konto lub logujesz się po raz pierwszy, dodaj obszar roboczy zgodnie z instrukcjami, podając nazwę i akceptując warunki korzystania.
3. Po zalogowaniu wybierz z menu „API keys”.
4. Kliknij „create a new key” i skopiuj klucz do schowka. Wklej go w polu klucza API w kategorii „Opis treści za pomocą AI” w ustawieniach NVDA -> Zarządzaj modelami -> Mistral Large 4.
5. W razie potrzeby zasil konto.

### Jak uzyskać klucz API od Kimi (Moonshot AI)

1. Zaloguj się lub utwórz konto na [platformie deweloperskiej Kimi](https://platform.kimi.ai/).
2. Po zalogowaniu otwórz w konsoli sekcję kluczy API i utwórz nowy klucz.
3. Skopiuj klucz do schowka. Wklej go w polu klucza API w kategorii „Opis treści za pomocą AI” w ustawieniach NVDA -> Zarządzaj modelami -> Kimi K3 (lub inny model Kimi).
4. W razie potrzeby zasil konto.


### Aktywacja modelu VIVO BlueLM Vision przez NVDA-CN

Ta usługa jest dostępna bezpłatnie dzięki współpracy firmy VIVO (vivo.com.cn) z chińską społecznością NVDA (NVDACN). Zapewnia wysokiej jakości rozpoznawanie multimodalne i jest zalecanym modelem dla wszystkich użytkowników, zwłaszcza początkujących.

Aby korzystać z tego modelu, potrzebujesz tylko bezpłatnego konta NVDA-CN.

1.  Utwórz konto: Przejdź na stronę rejestracji NVDA-CN: [https://nvdacn.com/admin/register.php](https://nvdacn.com/admin/register.php).
    * **Uwaga**: Strona jest obecnie w języku chińskim. Zalecamy skorzystanie z wbudowanej funkcji tłumaczenia w przeglądarce, aby wypełnić formularz.
    * Zostaniesz poproszony o podanie nazwy użytkownika, hasła i prawidłowego adresu e-mail. Przechowuj hasło w bezpiecznym miejscu, ponieważ automatyczne odzyskiwanie hasła nie zostało jeszcze wdrożone.
2.  Zweryfikuj adres e-mail: Sprawdź skrzynkę odbiorczą, znajdź wiadomość weryfikacyjną i kliknij zawarty w niej link, aby aktywować konto.
3.  Skonfiguruj dodatek:
    * Otwórz okno ustawień NVDA i przejdź do kategorii „Opis treści za pomocą AI”.
    * Wybierz przycisk „Zarządzaj modelami”.
    * Z listy dostawców wybierz „vivo BlueLM Vision (NVDA-CN)”.
    * Wpisz nazwę użytkownika i hasło NVDA-CN w odpowiednich polach.
    * Kliknij OK, aby zapisać dane logowania.

Model VIVO jest teraz gotowy do użycia. W sprawach związanych z kontem możesz skontaktować się z zespołem NVDA-CN pod adresem `support@nvdacn.com`.


### Jak skonfigurować Ollama

Obecnie jest to zalecana opcja do lokalnej konfiguracji.

Choć integracja z Ollama została przetestowana dokładniej niż llama.cpp, nadal jest mniej stabilna niż korzystanie z API i w niektórych konfiguracjach zachowuje się nietypowo, łącznie z awariami na komputerach, które nie spełniają wymagań sprzętowych.
Przy pierwszej próbie zapisz przynajmniej wszystkie dokumenty i inne ważne dane, zanim przejdziesz dalej, na wypadek gdyby to Ciebie spotkało.

Zacznij od upewnienia się, że możesz korzystać z wybranego modelu obsługującego obrazy w wierszu poleceń. Kroki są następujące:

1. Pobierz instalator Ollama dla Windows ze strony [Ollama downloads](https://ollama.com/download).
2. Uruchom instalator. Pobierze on wszystkie zależności potrzebne na Twoim komputerze.
3. Znajdź model, którego chcesz używać. Listę znajdziesz na ollama.com -> models -> vision lub [bezpośrednio tutaj](https://ollama.com/search?c=vision).
4. Pobierz i uruchom ten model, otwierając wiersz poleceń i wpisując `ollama run [model_name]`, oczywiście zastępując „[model_name]” nazwą modelu wybranego w kroku 3. Na przykład `ollama run llama3.2-vision`.
5. Jeśli proces zakończył się powodzeniem, zobaczysz interaktywną powłokę, w której możesz wpisywać zapytania i otrzymywać odpowiedzi od modelu, coś w rodzaju lokalnego (i ograniczonego) ChatGPT. Przetestuj ją, zadając dowolne pytanie, a następnie wpisz „/bye”, aby ją zamknąć.
6. W oknie konsoli wpisz `ollama list`. W pierwszej kolumnie zobaczysz nazwę, na przykład „llama3.2-vision:latest”.
7. Przejdź do ustawień Opis treści za pomocą AI -> Zarządzaj modelami -> Ollama. W polu nazwy modelu wpisz tę wartość i kliknij OK -> OK. Gotowe! Przełącz się na Ollama w podmenu modeli, a po chwili wszystko powinno działać.

### Jak skonfigurować llama.cpp

Ten dostawca jest obecnie dość niestabilny i wyniki mogą się różnić. Jest głównie przeznaczony dla zaawansowanych użytkowników zainteresowanych lokalnym uruchamianiem modeli na odpowiednio silnym komputerze.

1. Pobierz llama.cpp. W moment pisania tego dokumentu, [ten pull request](https://github.com/ggerganov/llama.cpp/pull/5882) usuwa możliwości multimodalne, więc użyj [ostatniej wersji z tą funkcjonalnością](https://github.com/ggerganov/llama.cpp/releases/tag/b2356).
Jeśli korzystasz z karty graficznej Nvidia z obsługą CUDA, pobierz te wstępnie zbudowane pliki binarne:
[llama-b2356-bin-win-cublas-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/llama-b2356-bin-win-cublas-cu12.2.0-x64.zip) oraz [cudart-llama-bin-win-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/cudart-llama-bin-win-cu12.2.0-x64.zip).
Kroki dla innych kart graficznych wykraczają poza zakres tego dokumentu, ale są opisane w dokumentacji llama.cpp.
2. Wypakuj oba pliki do tego samego folderu.
3. Pobierz z HuggingFace zquantowane modele, które chcesz używać. Dla LLaVA 1.6 Vicuna 7B: [llava-v1.6-vicuna-7b.Q4_K_M.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/llava-v1.6-vicuna-7b.Q4_K_M.gguf) oraz [mmproj-model-f16.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/mmproj-model-f16.gguf).
4. Umieść te pliki w folderze z resztą plików binarnych llama.cpp.
5. W terminalu uruchom serwer llava.cpp, przekazując pliki .gguf dla modelu i projektora multimodalnego w następujący sposób:
```
server.exe -m llava-v1.6-vicuna-7b.Q4_K_M.gguf --mmproj mmproj-model-f16.gguf
```
6. W ustawieniach NVDA przejdź do kategorii „Opis treści za pomocą AI”, wybierz „Zarządzaj modelami (alt+m)”, ustaw jako dostawcę „llama.cpp”, przejdź do pola bazowego adresu URL i wprowadź adres widoczny w konsoli (domyślnie „http://localhost:8080”).
7. Alternatywnie możesz pominąć niektóre kroki, uruchamiając llama.cpp na zdalnym serwerze o wyższej specyfikacji niż lokalny komputer, a następnie wprowadzić tamten adres URL.

### Jak skonfigurować LiteLLM Proxy

LiteLLM Proxy zapewnia jednolity interfejs dostępu do wielu modeli AI przez jeden punkt końcowy, co upraszcza zarządzanie modelami i ułatwia przełączanie się między dostawcami.

1. Skonfiguruj serwer proxy LiteLLM zgodnie z [dokumentacją LiteLLM proxy](https://docs.litellm.ai/docs/proxy/quick_start). Proxy możesz uruchomić lokalnie lub na zdalnym serwerze.
2. Przy uruchomieniu lokalnym najszybciej zaczniesz w ten sposób:
```
pip install 'litellm[proxy]'
litellm --model gpt-4o
```
To polecenie uruchomi serwer proxy pod adresem `http://localhost:4000`, który przekazuje zapytania do GPT-4o od OpenAI.
3. Do zastosowań produkcyjnych utwórz plik `config.yaml`, aby skonfigurować wiele modeli i uwierzytelnianie. Szczegóły znajdziesz w [przewodniku konfiguracji LiteLLM](https://docs.litellm.ai/docs/proxy/configs).
4. W oknie ustawień NVDA przejdź do kategorii „Opis treści za pomocą AI”, wybierz „Zarządzaj modelami (alt+m)” i ustaw jako dostawcę „LiteLLM Proxy”.
5. Wpisz adres URL serwera proxy w polu bazowego adresu URL (np. „http://localhost:4000” dla serwera lokalnego lub adres URL serwera zdalnego).
6. Jeśli proxy wymaga uwierzytelniania, wpisz klucz API w polu klucza API. W przeciwnym razie pozostaw je puste.
7. Kliknij przycisk „Lista modeli”, aby pobrać dostępne modele z proxy, a następnie wybierz z listy rozwijanej model, którego chcesz używać.
8. W razie potrzeby dostosuj inne ustawienia, takie jak zapytanie, maksymalna liczba tokenów i limit czasu, a następnie kliknij OK.

Uwaga: Dostępne modele i ich możliwości zależą od konfiguracji proxy LiteLLM. Upewnij się, że proxy ma skonfigurowane modele obsługujące obrazy, aby opisywanie obrazów działało.

### Jak skonfigurować Seer

Seer uruchamia PaliGemma2 na Twoim komputerze bez klucza API i bez połączenia z chmurą. Pamiętaj, że ten model tylko generuje podpisy obrazów; zapytania i pytania uzupełniające nie są obsługiwane.

1. Zainstaluj [usługę Seer](https://github.com/recursia-lab/Seer). Dostępny jest instalator uruchamiany jednym poleceniem dla Windows (.bat) oraz Linux/macOS (.sh).
2. W oknie ustawień NVDA przejdź do kategorii „Opis treści za pomocą AI”, wybierz „Zarządzaj modelami (alt+m)” i wybierz „Seer (requires installation)”.
3. Domyślny bazowy adres URL to `http://127.0.0.1:11435`. Pozostaw go bez zmian, chyba że zmieniłeś port usługi.
4. Kliknij OK. Usługa musi być uruchomiona, zanim spróbujesz uzyskać opis.

### Jak skonfigurować Datalab Chandra 2

Datalab Chandra 2 to nowoczesny model do analizy dokumentów i OCR, specjalizujący się w złożonych układach, tabelach, formularzach, piśmie odręcznym, wykresach i wzorach matematycznych. Można z niego korzystać przez zarządzane API w chmurze Datalab, kontener lokalny lub własną instancję vLLM.

#### Opcja A: API w chmurze Datalab (zalecane)
1. Załóż konto na stronie [datalab.to](https://www.datalab.to). Nowe konta otrzymują bezpłatne kredyty próbne.
2. Wejdź na [stronę kluczy API](https://www.datalab.to/app/keys) i wygeneruj klucz API.
3. W oknie ustawień NVDA przejdź do kategorii „Opis treści za pomocą AI”, wybierz „Zarządzaj modelami (alt+m)” i wybierz „Datalab Chandra 2”.
4. Wpisz klucz API w polu „Klucz API”.
5. Domyślny bazowy adres URL to `https://www.datalab.to/api/v1/convert`. Możesz dostosować tryb przetwarzania (`fast`, `balanced` lub `accurate`) do swoich potrzeb.
6. Kliknij OK. Model będzie teraz dostępny w menu Opis treści za pomocą AI.

#### Opcja B: Własny serwer z vLLM
1. Uruchom lokalny serwer vLLM z Chandra 2 (np. za pomocą `chandra_vllm` lub `vllm serve datalab-to/chandra-ocr-2`). Domyślnie serwer działa pod adresem `http://localhost:8000/v1`.
2. W ustawieniach NVDA -> Opis treści za pomocą AI -> Zarządzaj modelami -> „Datalab Chandra 2” wpisz lokalny punkt końcowy w polu „Bazowy adres URL” (np. `http://localhost:8000/v1`).
3. Ustaw nazwę modelu, jeśli różni się od domyślnej (`datalab-to/chandra-ocr-2`), pozostaw pole klucza API puste (lub podaj token bearer, jeśli uwierzytelnianie jest włączone) i kliknij OK.

## Jak korzystać z tego dodatku

Domyślnie przypisano sześć skrótów klawiszowych:

* NVDA+shift+i: Otwiera menu z opcjami opisania aktualnie sfokusowanego elementu, obiektu nawigatora, kamery fizycznej, całego ekranu lub sterowania komputerem za pomocą AI.
* NVDA+shift+u: Opisuje zawartość bieżącego obiektu nawigatora za pomocą AI.
* NVDA+shift+y: Opisuje obraz (lub ścieżkę do obrazu) w schowku za pomocą AI.
* NVDA+shift+j: Opisuje pozycję twarzy w kadrze wybranej kamery. Jeśli podłączonych jest wiele kamer, przejdź do menu „Opis treści za pomocą AI” (NVDA+shift+i) i wybierz kamerę za pomocą elementu „Wybierz kamerę” w podmenu wykrywania twarzy.
* NVDA+alt+c: Otwiera okno rozmowy z AI, w którym można zadawać pytania uzupełniające.
* NVDA+control+shift+p: Wstrzymuje lub wznawia aktywną sesję sterowania komputerem.

Siedem skrótów klawiszowych jest domyślnie nieprzypisanych:

* Opisanie zawartości aktualnie sfokusowanego elementu za pomocą AI.
* Wykonanie zrzutu ekranu i opisanie go za pomocą AI.
* Zrobienie zdjęcia za pomocą wybranej kamery i opisanie go za pomocą AI.
* Anulowanie aktywnej sesji sterowania komputerem.
* Wykonanie zrzutu bieżącego obiektu z fokusem i skopiowanie go do schowka.
* Wykonanie zrzutu bieżącego obiektu nawigatora i skopiowanie go do schowka.
* Wykonanie zrzutu całego ekranu i skopiowanie go do schowka.

Trzy polecenia kopiowania są też dostępne w podmenu „Kopiuj obraz do schowka” menu NVDA+shift+i. Nie wysyłają one niczego do usługi AI. Użyj ich, aby wkleić zrzut do Be My AI lub innej aplikacji, której ten dodatek nie obsługuje. Skopiowany obraz zastępuje poprzednią zawartość schowka.

Możesz dostosować te skróty klawiszowe w dowolnym momencie w ustawieniach zdarzeń wejściowych.

### Kontynuowanie rozmowy o opisie

Czasami odpowiedź otrzymana od AI jest niewystarczająca. Być może obraz jest niskiej jakości, niekompletny lub zawiera niepotrzebne szczegóły. Może chcesz skupić się tylko na określonym fragmencie albo zrobić wyraźniejsze zdjęcie bez utraty kontekstu.
Po otrzymaniu opisu możesz nacisnąć NVDA+alt+c lub wybrać „Kontynuuj rozmowę o poprzednim opisie” z menu kontekstowego Opis treści za pomocą AI (NVDA+shift+i). Domyślnie fokus jest ustawiony na polu wiadomości.
Aby dodać kolejny obraz, pozostaw okno rozmowy otwarte i korzystaj z dodatku jak zwykle. Po wykonaniu zdjęcia (z kamery, kontrolki systemowej, zrzutu ekranu itp.) zostaniesz zapytany, czy chcesz dołączyć je do bieżącej sesji, czy rozpocząć nową.

### Sterowanie komputerem

Funkcja sterowania komputerem pozwala dodatkowi Opis treści za pomocą AI sterować aktywną aplikacją za pomocą myszy i klawiatury po opisaniu przez Ciebie zadania. Może to pomóc w zadaniach, które trudno lub nie da się wykonać ręcznie z powodu braku dostępności.

Ponieważ ta funkcja daje modelowi AI kontrolę nad Twoim komputerem, korzystaj z niej ostrożnie. Dodatek prosi o zgodę przed rozpoczęciem, informuje o wykonywanych działaniach na bieżąco i pyta przed potencjalnie ryzykownymi działaniami. Odpowiadasz za to, co robi, więc obserwuj sesję i nie używaj jej do poufnych lub trudnych do cofnięcia zadań.

W dowolnym momencie możesz wstrzymać lub wznowić sterowanie komputerem skrótem `NVDA+Control+Shift+P`. W czasie wstrzymania dodatek nie wykona kolejnego działania, dopóki go nie wznowisz.

Dodatek sygnalizuje stan sterowania dźwiękami. Wysoki sygnał oznacza, że model przejmuje lub wznawia sterowanie. Niski sygnał oznacza, że sterowanie zostało wstrzymane, przez Ciebie albo dlatego, że model potrzebuje Twojej odpowiedzi. Krótki niski sygnał błędu oznacza, że sesja została zatrzymana z powodu błędu API.

W trakcie aktywnej sesji model zapowiada, co zamierza zrobić, zanim wyśle polecenia. Nic się nie dzieje, dopóki zapowiedź się nie skończy, chyba że naciśniesz `Control`, aby przerwać mowę i pozwolić na wcześniejsze wykonanie działania.

Jeśli model nie wie, jak wykonać działanie, potrzebuje więcej informacji lub z innego powodu oddaje Ci głos, sesja zostaje wstrzymana, a okno sterowania komputerem pojawia się na pierwszym planie. Wpisz w nim kolejną wiadomość, aby kontynuować rozmowę, lub zamknij okno, aby zakończyć sesję.

Ta funkcja działa tylko z modelami udostępniającymi narzędzie do sterowania komputerem: GPT-5.4, GPT-5.4 mini, GPT-5.5, GPT-5.5 pro, GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna, Claude 4.5 Sonnet, Claude 4.5 Opus, Claude 4.6 Sonnet, Claude 4.6 Opus, Claude 4.7 Opus, Claude 4.8 Opus, Claude 5 Sonnet, Claude 5 Opus, Claude 5 Fable, Claude 5.1 Fable, Claude 5.2 Fable, Claude 5.5 Haiku, Claude 5.5 Sonnet i Claude 5.5 Opus. Inne modele potrafią opisywać obrazy, ale nie zwracają ustrukturyzowanych działań myszy i klawiatury potrzebnych do sterowania komputerem.

Aby skorzystać ze sterowania komputerem:

1. Skonfiguruj i wybierz jeden z obsługiwanych modeli.
2. Otwórz aplikację lub okno, na którym model ma pracować.
3. Naciśnij `NVDA+shift+i`, a następnie wybierz „Steruj komputerem...”.
4. Wpisz zadanie, które ma zostać wykonane, i naciśnij Wyślij.
5. Przejrzyj prośbę o zgodę. Jeśli zezwolisz na sesję, obserwuj działania i zatwierdzaj lub anuluj prośby dotyczące ryzykownych działań.

Uwaga: Należy traktować tę funkcję jako wersję beta. Aktywnie pracujemy nad zwiększeniem bezpieczeństwa jej implementacji.

## Zależności

Niektóre biblioteki potrzebne temu dodatkowi są zbyt duże, aby dołączyć je do paczki dodatku. Zamiast tego przy pierwszym uruchomieniu NVDA z zainstalowanym dodatkiem pojawi się pytanie, czy je pobrać. Wybierz „Tak”, poczekaj na zakończenie pobierania, a NVDA uruchomi się ponownie.

Pobierany jest plik zip o rozmiarze od około 35 do 70 MB, w zależności od wersji NVDA. Pochodzi on ze strony [libs-release](https://github.com/cartertemm/AI-content-describer/releases/tag/libs-release) tego repozytorium. Jeśli GitHub jest niedostępny, dodatek zaproponuje użycie serwera lustrzanego udostępnianego przez chińską społeczność NVDA.

Plik zip zawiera:

* [NumPy](https://numpy.org/): obliczenia na tablicach, wymagane przez OpenCV.
* [OpenCV](https://opencv.org/) (`cv2`): wyszukuje twarz na obrazach z kamery internetowej na potrzeby funkcji wykrywania twarzy.
* [Pillow](https://python-pillow.org/) (`PIL`): wykonuje zrzuty ekranu i konwertuje je na obrazy, które mogą odczytać modele AI.
* [Markdown](https://python-markdown.github.io/): wyświetla opisy z formatowaniem, takim jak nagłówki, listy i tabele.
* [pygrabber](https://github.com/andreaschiavinato/python_grabber): wyświetla listę kamer internetowych podłączonych do komputera.
* Kilka modułów biblioteki standardowej Pythona, których NVDA nie zawiera (`html`, `xml`, `pathlib`, `secrets` i `_markupbase`). Potrzebują ich powyższe biblioteki.

Pliki trafiają do folderu o nazwie `aic-py-`, po której następuje wersja Pythona używana przez NVDA, na przykład `aic-py-3.13`. Folder ten znajduje się w folderze konfiguracji użytkownika NVDA, zwykle `%APPDATA%\nvda`. Każda wersja Pythona ma własny folder, więc dodatek ponownie pobiera biblioteki, gdy nowe wydanie NVDA zmienia wersję Pythona. Odinstalowanie dodatku usuwa folder dla bieżącej wersji Pythona używanej przez NVDA.

Jeśli pobieranie nie działa, możesz zainstalować biblioteki samodzielnie. Pobierz `aic-py-3.13.zip` (lub plik dla wersji Pythona używanej przez Twoje NVDA) ze strony libs-release, wypakuj go do folderu konfiguracji użytkownika NVDA i uruchom NVDA ponownie.

## Kompilowanie dodatku

Aby utworzyć paczkę dodatku ze źródła, potrzebujesz:

* Dystrybucji Python (zalecana wersja 3.7 lub nowsza). Zobacz [stronę Python](https://www.python.org) w celu pobrania instalatorów dla systemu Windows. Uwaga: przygotowanie kodu źródłowego NVDA i uwzględnionych modułów wymaga 32-bitowej wersji Python 3.7.
* Scons - [strona](https://www.scons.org/) - wersja 4.3.0 lub nowsza. Możesz zainstalować go za pomocą PIP: `pip install scons`.
* Markdown 3.3.0 lub nowsza: `pip install markdown`.

Następnie w terminalu wpisz:

```
git clone https://github.com/cartertemm/AI-content-describer.git
cd AI-content-describer
scons
```

Po zakończeniu działania polecenia `scons`, plik *.nvda-addon zostanie umieszczony w głównym folderze tego repozytorium, gotowy do testowania i do wydania.

Jeśli dodasz nowe ciągi wymagające tłumaczenia, ważne jest, aby ponownie wygenerować plik .pot, wpisując:

```
scons pot
```

## Jak zlokalizować dodatek?

Na komputerze z systemem Windows:

* Pobierz [poedit](https://poedit.net/). To jest program, którego będziesz używać do tłumaczenia z języka angielskiego.
* Pobierz plik .pot zawierający wszystkie ciągi tekstowe [tutaj](https://raw.githubusercontent.com/cartertemm/AI-content-describer/main/AIContentDescriber.pot)
* Otwórz plik, który właśnie pobrałeś, w programie poedit. Kliknij "Utwórz nowe tłumaczenie" w oknie, które się pojawi, a następnie wybierz język docelowy.
* Przejdź przez tekst źródłowy i umieść jego przetłumaczoną zawartość po stronie języka docelowego. Jeśli potrzebujesz dodatkowej pomocy, kliknij prawym przyciskiem myszy na danym elemencie -> "code occurrences", a następnie przejdź o linię wyżej, aby przeczytać komentarz zaczynający się od "# Translators: ". Te komentarze są również dostępne w jednym miejscu w pliku .pot.
* Po zakończeniu kliknij File -> Save lub naciśnij ctrl+s, a następnie wybierz miejsce, w którym ma zostać zapisany nowy plik .mo i .po. To są pliki, które należy wysłać do mnie mailowo lub załączyć w pull request.
* Przetłumacz zawartość pliku readme.md (ten plik). Dołącz go również!

## Wkład społeczności

Wszystkie są bardzo cenione i będą uwzględnione.
Następujące osoby pracowały nad dodatkiem.

* [Cary Rowen](https://github.com/cary-rowen): umożliwił korzystanie z dodatku chińskim użytkownikom dzięki serwerom lustrzanym zależności, dodał obsługę dostawcy Vivo Blue
* [Mazen](https://github.com/mzanm): implementacja markdown, różna pomoc przy kodowaniu
* [Kostenkov-2021](https://github.com/Kostenkov-2021): tłumaczenie na język rosyjski
* [Nidza07](https://github.com/nidza07): tłumaczenie na język serbski
* [Heorhii Halas](nvda.translation.uk@gmail.com) i [George-br](https://github.com/George-br): tłumaczenie na język ukraiński
* [Umut Korkmaz](umutkork@gmail.com): tłumaczenie na język turecki
* [Platinum_Hikari](urbain_onces.0r@icloud.com): tłumaczenie na język francuski
* [Lukas](https://4sensegaming.cz): tłumaczenie na język czeski
* [Michaela](https://technologiebezzraku.sk): tłumaczenie na język słowacki
* [loginerror](https://github.com/theloginerror): tłumaczenie na język polski

Masz problem? Zgłoś go [tutaj](https://github.com/cartertemm/AI-content-describer/issues)

Masz sugestię dotyczącą nowej funkcji? Utwórz zgłoszenie, i zobaczymy, co da się zrobić. Pull requesty bez powiązanych zgłoszeń będą przeglądane, ale mogą zająć więcej czasu, szczególnie jeśli zdecyduję, że nowa poprawka lub funkcjonalność musi działać inaczej, niż zaproponowano.

Tłumaczenia są mile widziane. Im więcej osób będzie miało dostęp do tej potężnej technologii, tym lepiej!

Jeśli nie masz Githuba lub wolisz go nie używać, możesz [wysłać mi email](mailto:carter@ctemm.me) - carter (at) ctemm (dot) me.

Dziękuję za wsparcie!
