import openai
import requests

# Ustaw swój klucz API OpenAI

openai.api_key = ""


def fetch_article_from_url(url):
    """Funkcja do pobierania artykułu z podanego URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Sprawdź, czy żądanie się powiodło
        return response.text
    except Exception as e:
        print(f"Błąd podczas pobierania artykułu: {e}")
        return None

def generate_html_from_article(article_text, prompt):
    """Funkcja do przesyłania artykułu i promptu do API OpenAI i generowania kodu HTML."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Możesz użyć też modelu 'gpt-4', jeśli jest dostępny
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

def main():
    # URL do artykułu tekstowego
    article_url = "https://cdn.oxido.pl/hr/Zadanie%20dla%20JJunior%20AI%20Developera%20-%20tresc%20artykulu.txt"

    # Prompt, który zostanie wysłany do OpenAI wraz z treścią artykułu
    prompt = """
    Przekształć poniższy artykuł na stronę HTML, używając odpowiednich tagów HTML takich jak <h1>, <h2>, <p>, <img>, <figcaption> itp.
    Gdzie to odpowiednie, wstaw obrazy za pomocą tagu <img> z atrybutem src="image_placeholder.jpg" oraz atrybutem alt, opisującym szczegółowo zawartość obrazka.
    Do każdego obrazka dodaj podpis za pomocą tagu <figcaption>. Wygenerowany kod powinien być jedynie zawartością, którą można umieścić między tagami <body> i </body>.
    Nie dodawaj tagów <html>, <head> ani <body>. Pamiętaj, aby nie używać CSS ani JavaScript.
    """

    # Pobierz artykuł z URL
    article_text = fetch_article_from_url(article_url)

    if article_text:
        # Przetwórz artykuł w API OpenAI
        html_content = generate_html_from_article(article_text, prompt)

        if html_content:
            # Zapisz wygenerowany kod HTML do pliku
            output_file = "artykul.html"
            save_html_to_file(html_content, output_file)
            print(f"Wygenerowany kod HTML zapisano w pliku {output_file}")
        else:
            print("Wystąpił problem podczas generowania kodu HTML.")
    else:
        print("Nie udało się pobrać artykułu z podanego URL.")

    prompt = """
    Na podstawie poprzedniego wygenerowanego pliku html wygeneruj inny szablon strony w HTML, który doda tylko style do odpowiednich tagów. Sekcja <body> powinna być pusta.
    """
    html_content = generate_html_from_article(article_text, prompt)
    if html_content:
        output_file = "szablon.html"
        save_html_to_file(html_content, output_file)
        print(f"Wygenerowany kod HTML zapisano w pliku {output_file}")
    else:
        print("Wystąpił problem podczas generowania kodu HTML.")


    with open("artykul.html", "r", encoding="utf-8") as file:
        file1_content = file.read()

    # Załaduj drugi plik HTML (szablon ze stylami, pusty <body>)
    with open("szablon.html", "r", encoding="utf-8") as file:
        file2_content = file.read()

    prompt = f"""
    Jesteś pomocnym asystentem znającym HTML. 
    Mam dwa pliki HTML:
    1. Pierwszy plik zawiera kompletną sekcję <body>:
    {file1_content}

    2. Drugi plik to szablon ze stylami i pustą sekcją <body>:
    {file2_content}

    Połącz te pliki, wstawiając zawartość <body> z pierwszego pliku do sekcji <body> drugiego pliku. Zachowaj strukturę i style drugiego pliku.
    Zwróć kompletny scalony kod HTML.
    """
    
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
        ]
    )

    # Pobierz wynik z odpowiedzi
    merged_html = response['choices'][0]['message']['content']

    with open("podglad.html", "w", encoding="utf-8") as merged_file:
        merged_file.write(merged_html)

    
if __name__ == "__main__":
    main()
