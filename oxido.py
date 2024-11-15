import openai
import requests
import sys

# Ustaw swój klucz API OpenAI

openai.api_key = ""

def generate_other_htmls(prompt):
    #Funkcja do zbierania odpowiedzi z API OpenAI z podanego promptu
    try:
        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Błąd podczas przetwarzania zapytania: {e}")
        return None

        

def fetch_article_from_url(url):
    #Funkcja do pobierania artykułu z podanego URL.
    try:
        response = requests.get(url)
        response.raise_for_status()  # Sprawdź, czy żądanie się powiodło
        return response.text
    except Exception as e:
        print(f"Błąd podczas pobierania artykułu: {e}")
        return None

def generate_html_from_article(article_text, prompt):
    #Funkcja do przesyłania artykułu i promptu do API OpenAI i generowania kodu HTML.
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates HTML content."},
                {"role": "user", "content": f"{prompt}\n\n{article_text}"}
            ],
            max_tokens=2000,  # dopasuj limit tokenów według potrzeb
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Błąd podczas przetwarzania zapytania: {e}")
        return None

def save_html_to_file(html_content, file_path):
    """Funkcja do zapisu wygenerowanego kodu HTML do pliku."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

def generate_and_save_html(prompt, article_text, output_file, isFirst):
    # Przetwórz artykuł w API OpenAI
    if isFirst:
        html_content = generate_html_from_article(article_text, prompt)
    else:
        html_content = generate_other_htmls(prompt)

    if html_content:
        # Zapisz wygenerowany kod HTML do pliku
        save_html_to_file(html_content, output_file)
        print(f"Wygenerowany kod HTML zapisano w pliku {output_file}")
    else:
        print("Wystąpił problem podczas generowania kodu HTML.")

def main():
    # URL do artykułu tekstowego
    article_url = "https://cdn.oxido.pl/hr/Zadanie%20dla%20JJunior%20AI%20Developera%20-%20tresc%20artykulu.txt"

    # Prompt, który zostanie wysłany do OpenAI wraz z treścią artykułu
    prompt_artykul = """
    Przekształć poniższy artykuł na stronę HTML, używając odpowiednich tagów HTML takich jak <h1>, <h2>, <p>, <img>, <figcaption> itp.
    Gdzie to odpowiednie, wstaw obrazy za pomocą tagu <img> z atrybutem src="image_placeholder.jpg" oraz atrybutem alt, opisującym szczegółowo zawartość obrazka.
    Do każdego obrazka dodaj podpis za pomocą tagu <figcaption>. Wygenerowany kod powinien być jedynie zawartością, którą można umieścić między tagami <body> i </body>.
    Nie dodawaj tagów <html>, <head> ani <body>. Pamiętaj, aby nie używać CSS ani JavaScript.
    """

    # Pobierz artykuł z URL
    article_text = fetch_article_from_url(article_url)

    if article_text:
        generate_and_save_html(prompt_artykul, article_text, "artykul.html", True)
    else:
        print("Nie udało się pobrać artykułu z podanego URL.")
        sys.exit()

#---------------------------------------------------------------------------------------------------------------------
    with open("artykul.html", "r", encoding="utf-8") as file:
        file1_content = file.read()

    prompt_szablon = f"""
    Na podstawie tego pliku:
    {file1_content}
    wygeneruj inny szablon strony w HTML, który doda tylko style do wszystkich tagów zawartych w tym pliku. Uzupełnij te style. Sekcja <body> powinna być pusta. 
    Output only the HTML code.
    """
    generate_and_save_html(prompt_szablon, article_text, "szablon.html", False)


#---------------------------------------------------------------------------------------------------------------------
    # Załaduj drugi plik HTML (szablon ze stylami, pusty <body>)
    with open("szablon.html", "r", encoding="utf-8") as file:
        file2_content = file.read()

    prompt_podglad = f"""
    Mam dwa pliki HTML:
    1. Pierwszy plik zawiera kompletną sekcję <body>:
    {file1_content}

    2. Drugi plik to szablon ze stylami i pustą sekcją <body>:
    {file2_content}

    Połącz te pliki, wstawiając zawartość <body> z pierwszego pliku do sekcji <body> drugiego pliku. Zachowaj strukturę i style drugiego pliku.
    Zwróć kompletny scalony kod HTML.
    Odpowiedź powinna zawierać tylko kod html.
    """

    generate_and_save_html(prompt_podglad, article_text, "podglad.html", False)

    
if __name__ == "__main__":
    main()
