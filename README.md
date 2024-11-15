# Oxido zadanie rekrutacyjne
 Jest to prosta aplikacja, która pobiera treść z podanej strony, za pomocą AI generuje wygląd strony internetowej i zapisuje plik html do podanego folderu.
Użyte biblioteki:
openai - pozwala na używanie chatuGPT wewnątrz kodu
requests - pozwala na pobranie zawartości ze strony internetowej (w tym przypadku tylko tekst)
sys - dzięki niej program zakońzy działanie, gdy napotka błąd przy pobeiraniu pliku tekstowego

Działanie programu:
Jest jedna zmienna globalna openai.api_key, która zawiera klucz do api OpenAI (w celu dbania o dane prywatne klucz ten w kdozie jest niedostepny)

1. Metoda main:
1.1 Podaje się link do storny zawierającej treść, która ma być edytowana i wygenerowane do pliku html.
1.2 Podaje się zapytanie do chatuGPT, dzięki któremu będzie mógł wygenerować plik html.
1.3 Pobieranie artykułu ze strony za pomocą metody "fetch_article_from_url"
1.4 Sprawdzanie, czy można pobrać podany artykuł, jeśli nie - wyświetlany jest odpowiedni komunikat w konsoli i program kończy działanie.
W przeciwnym wypadku wywoływana jest metoda "generate_and_save_html" dla pliku artykul.html.
1.5 W następnych krokach podawany jest nowy prompt dla do generowania plików szablon.html oraz podgląd.html

2. Metoda fetch_article_from_url
2.1 Pobieranie danych z podanego linku
2.2 Sprawdzanie, czy żądanie się powiodło
2.3 Zwrócenie tekstu, jeśli się powiodło.
2.4 Wyłapanie wyjątku, napisanie odpowiedniego komunikatu oraz zakończenie programu, jeżeli się nie powiodło. 

3. Metoda generate_html_from_article
3.1 Tworzenie odpowiedzi za pomocą API OpenAI wraz z odpowiednimi atrybutami (model="gpt-3.5-turbo" itd.)
3.2 Zwrócenie odpowiedzi jeżeli wszytsko się powiodło.
3.3 Wyłapanie wyjątku, napisanie odpowiedniego komunikatu oraz zakończenie programu, jeżeli się nie powiodło.

4. Metoda generate_other_htmls
4.1 Motoda podobna do generate_html_from_article, jendnak przyjmuje za argument tylko prompt

5. Metoda save_html_to_file:
5.1 Standardowa procedura zapisu do pliku.

6 Metoda generate_and_save_html:
6.1 Motoda void stworzona, aby kod w funkcji main był schludniejszy.
6.2 Argument isFirst sprawdza, czy jest to generacja pliku artykul.html czy pozostałe 
6.3 Sprawdzanie, czy można pobrać podany artykuł, jeśli nie - wyświetlany jest odpowiedni komunikat w konsoli i program kończy działanie.
W przeciwnym wypadku zaczyna się przetwarzanie artukułu za pomocą API OpenAI w metodzie "generate_html_from_article" lub "generate_other_htmls".
Jeżeli się powiedzie, przetworzony artykuł zostaje zapisany do pliku "artykuł.html" za pomocą metody "save_html_to_file", w konsoli wyświetlany jest komunikat o powodzeniu i program konczy działanie. W przeciwnym wypadku zostaje wyświetlony komunikat o błędzie i program kończy działanie.

 Uruchomienie:
 Aby uruchomić program należy otowrzyć terminal ze ścieżką do foledu, w kórym znajduje się plik oxido.py i użyć komendy
 > python oxido.py
