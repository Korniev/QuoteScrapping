import json
from database.models import Author, Quote


def load_authors():
    with open('data_json/authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)

    for author_data in authors_data:
        author, created = Author.objects.get_or_create(
            fullname=author_data['fullname'],
            defaults={
                'born_date': author_data['born_date'],
                'born_location': author_data['born_location'],
                'description': author_data['description']
            }
        )
        if created:
            print(f"Author {author.fullname} created.")


def load_quotes():
    with open('data_json/quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)

    for quote_data in quotes_data:
        author = Author.objects(fullname=quote_data['author']).first()
        if author:
            quote = Quote(
                author=author,
                tags=quote_data['tags'],
                quote=quote_data['quote']
            )
            quote.save()
            print(f"Quote '{quote.quote[:30]}...' saved.")
        else:
            print(f"Author {quote_data['author']} not found.")


if __name__ == "__main__":
    load_authors()
    load_quotes()
