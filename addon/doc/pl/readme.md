# Opis treści za pomocą AI dla NVDA

Ten dodatek umożliwia uzyskanie szczegółowych opisów obrazów, elementów interfejsu użytkownika oraz innych treści, które są wizualnie niedostępne.

Wykorzystując możliwości zaawansowanych modeli AI oraz algorytmy komputerowego rozpoznawania obrazów, dążymy do dostarczania opisów treści najwyższej jakości, zwiększając ogólną niezależność użytkownika. Aby uzyskać więcej informacji na temat używanych modeli, zapoznaj się z odpowiednią sekcją tego dokumentu.

## Funkcje

* Opisuj aktualnie sfokusowany obiekt, obiekt nawigatora, cały ekran lub wykonaj zdjęcie za pomocą wbudowanej kamery.
* Opisuj obrazy skopiowane do schowka, niezależnie od tego, czy to zdjęcia z e-maila, czy ścieżki w Eksploratorze Windows.
* Określaj, czy twarz użytkownika znajduje się na środku kadru, wykorzystując algorytmy rozpoznawania twarzy (funkcja nie wymaga płatnego dostępu do API).
* Obsługuje wielu dostawców, w tym GPT-4 (OpenAI), Gemini (Google), Claude 3 (Anthropic) i llama.cpp.
* Obsługuje różne formaty, takie jak PNG (.png), JPEG (.jpeg, .jpg), WEBP (.webp) i nieruchome GIFy (.gif).
* Opcjonalne buforowanie odpowiedzi w celu oszczędzania limitów API.
* Zaawansowane funkcje, takie jak dostosowywanie zapytań (promptów) i liczby tokenów, aby dostosować informacje do potrzeb użytkownika.
* Renderowanie Markdown do łatwego przeglądania ustrukturyzowanych informacji (dodaj np. „odpowiedz w Markdown” na końcu zapytania).


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
* Upewnić się, że twarz jest dobrze widoczna na kamerze, a tło wygląda profesjonalnie przed nagraniem wideo lub uczestnictwem w spotkaniach online.


## Modele

* [GPT4 vision](https://platform.openai.com/docs/guides/vision)
* [Google Gemini pro vision](https://blog.google/technology/ai/google-gemini-ai/)
* [Claude 3 (Haiku, Sonett, Opus)](https://docs.anthropic.com/claude/docs/vision)
* [llama.cpp (niestabilny i wolny, w zależności od sprzętu, przetestowany z modelami llava-v1.5/1.6, BakLLaVA, Obsidian i MobileVLM 1.7B/3B)](https://github.com/ggerganov/llama.cpp)

Szczegółowe instrukcje konfiguracyjne znajdują się poniżej.

## Pierwsze kroki

Pobierz najnowszą wersję dodatku z [tego linku](https://github.com/cartertemm/AI-content-describer/releases/latest/). Kliknij na plik na komputerze z zainstalowanym NVDA, a następnie wykonaj poniższe kroki, aby uzyskać klucz API od obsługiwanego dostawcy.
Jeśli nie wiesz, którego dostawcę wybrać, autor dodatku i testerzy zalecają Gemini jako bardziej ekonomiczne rozwiązanie, podczas gdy OpenAI oferuje większą dokładność. Claude 3 Haiku to najtańsza i najszybsza opcja, ale jej jakość może być słabsza.
Oczywiście, wyniki te w dużym stopniu zależą od danego zadania, dlatego zalecamy eksperymentowanie z różnymi modelami i zapytaniami, aby znaleźć rozwiązanie sprawdzające się najlepiej.  

### Jak uzyskać klucz API od OpenAI

1. Przejdź na stronę [OpenAI API key](https://platform.openai.com/account/api-keys).
2. Jeśli nie masz konta, utwórz je. Jeśli masz, zaloguj się.
3. Na stronie kluczy API kliknij, aby utworzyć nowy klucz. Skopiuj go do schowka.
4. Zasil konto kwotą co najmniej 1 USD.
5. W oknie ustawień NVDA przejdź do kategorii „Opis treści za pomocą AI”, wybierz „Zarządzaj modelami (alt+m)”, wybierz jako dostawcę „GPT-4 Vision”, przejdź do pola klucza API i wklej tam wygenerowany klucz.

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
4. Wprowadź nazwę klucza, np. „AIContentDescriber”, a następnie kliknij „Utwórz klucz” i skopiuj wyświetloną wartość. Wklej ten klucz w polu klucza API w kategorii „Opis treści za pomocą AI” w ustawieniach NVDA -> Zarządzaj modelami -> Claude 3.
5. Jeśli jeszcze tego nie zrobiłeś, doładuj konto kwotą co najmniej 5 USD na stronie [Anthropic Plans](https://console.anthropic.com/settings/plans).


### Jak skonfigurować llama.cpp

Ten dostawca jest obecnie dość niestabilny i jest głównie przeznaczony dla zaawansowanych użytkowników zainteresowanych lokalnym uruchamianiem modeli na odpowiednio silnym komputerze.

1. Pobierz llama.cpp. W moment pisania tego dokumentu, [ten pull request](https://github.com/ggerganov/llama.cpp/pull/5882) usuwa możliwości multimodalne, więc użyj [ostatniej wersji z tą funkcjonalnością](https://github.com/ggerganov/llama.cpp/releases/tag/b2356).
Jeśli korzystasz z karty graficznej Nvidia z obsługą CUDA, pobierz te wstępnie zbudowane pliki binarne:  
[llama-b2356-bin-win-cublas-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/llama-b2356-bin-win-cublas-cu12.2.0-x64.zip) oraz [cudart-llama-bin-win-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/cudart-llama-bin-win-cu12.2.0-x64.zip).  
Kroki dla innych kart graficznych są opisane w dokumentacji llama.cpp.

2. Wypakuj oba pliki do tego samego folderu.

3. Pobierz z HuggingFace zquantowane modele, które chcesz używać. Dla LLaVA 1.6 Vicuna 7B: [llava-v1.6-vicuna-7b.Q4_K_M.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/llava-v1.6-vicuna-7b.Q4_K_M.gguf) oraz [mmproj-model-f16.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/mmproj-model-f16.gguf).

4. Umieść te pliki w folderze z resztą plików binarnych llama.cpp.

5. W terminalu uruchom serwer llava.cpp, przekazując pliki .gguf dla modelu i projektora multimodalnego w następujący sposób: 
```
server.exe -m llava-v1.6-vicuna-7b.Q4_K_M.gguf --mmproj mmproj-model-f16.gguf
```

6. W ustawieniach NVDA przejdź do kategorii „Opis treści za pomocą AI”, wybierz „Zarządzaj modelami (alt+m)”, ustaw jako dostawcę „llama.cpp”, przejdź do pola URL bazowego i wprowadź adres widoczny w konsoli (domyślnie „http://localhost:8080”).

7. Alternatywnie możesz pominąć niektóre kroki, uruchamiając llama.cpp na zdalnym serwerze o wyższej specyfikacji niż lokalny komputer, a następnie wprowadzić tamten adres URL.

## Jak korzystać z tego dodatku

Domyślnie przypisano cztery skróty klawiszowe:

* NVDA+shift+i: Otwiera menu z opcjami opisania aktulanie sfokusowanego elementu, obiektu nawigatora, kamery fizycznej lub całego ekranu.
* NVDA+shift+u: Opisuje zawartość bieżącego obiektu nawigatora za pomocą AI.
* NVDA+shift+y: Opisuje obraz (lub ścieżkę do obrazu) w schowku za pomocą AI.
* NVDA+shift+j: Opisuje pozycję twarzy w kadrze wybranej kamery. Jeśli podłączonych jest wiele kamer, przejdź do menu „Opis treści za pomocą AI” (NVDA+shift+i) i wybierz kamerę w podmenu „Wybierz kamerę”.

Trzy skróty klawiszowe są domyślnie nieprzypisane:

* Opisanie zawartości aktulanie sfokusowanego elementu za pomocą AI.
* Wykonanie zrzutu ekranu i opisanie go za pomocą AI.
* Zrobienie zdjęcia za pomocą wybranej kamery i opisanie go za pomocą AI.

Możesz dostosować te skróty klawiszowe w dowolnym momencie w ustawieniach zdarzeń wejściowych.

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
* * Po zakończeniu kliknij Flie -> Save lub naciśnij ctrl+s, a następnie wybierz miejsce, w którym ma zostać zapisany nowy plik .mo i .po. To są pliki, które należy wysłać do mnie mailowo lub załączyć w pull request.
* Przetłumacz zawartość pliku readme.md (ten plik). Dołącz go również!

## Wkład społeczności

Wszystkie są bardzo cenione i będą uwzględnione.
Następujące osoby pracowały nad dodatkiem.

* [Mazen](https://github.com/mzanm): implementacja markdown, różna pomoc przy kodowaniu
* [Kostenkov-2021](https://github.com/Kostenkov-2021): tłumaczenie na język rosyjski
* [Nidza07](https://github.com/nidza07): tłumaczenie na język serbski
* [Heorhii Halas](nvda.translation.uk@gmail.com): tłumaczenie na język ukraiński
* [Umut Korkmaz](umutkork@gmail.com): tłumaczenie na język turecki
* [Platinum_Hikari](urbain_onces.0r@icloud.com): tłumaczenie na język francuski
* [Lukas](https://4sensegaming.cz): tłumaczenie na język czeski
* [Michaela](https://technologiebezzraku.sk): tłumaczenie na język słowacki
* [loginerror](https://github.com/theloginerror): tłumaczenie na język polski

Masz problem? Zgłoś go do [tutaj](https://github.com/cartertemm/AI-content-describer/issues)

Masz sugestię dotyczącą nowej funkcji? Utwórz zgłoszenie, i zobaczymy, co da się zrobić. Pull requesty bez powiązanych zgłoszeń będą przeglądane, ale mogą zająć więcej czasu, szczególnie jeśli zdecyduję, że nowa poprawka lub funkcjonalność musi działać inaczej, niż zaproponowano.

Tłumaczenia są mile widziane. Im więcej osób będzie miało dostęp do tej potężnej technologii, tym lepiej!

Jeśli nie masz Githuba lub wolisz go nie używać, możesz [wysłać mi email](mailto:cartertemm@gmail.com) - cartertemm (at) gmail (dot) com.

Dziękuję za wsparcie!