import csv
import requests
from bs4 import BeautifulSoup, Tag

def scrape_quotes():
    # retrieve quotes from Paul Graham's website
    url = 'http://www.paulgraham.com/quo.html'
    page = requests.get(url).content
    
    # parse html
    soup = BeautifulSoup(page, 'html.parser')
    quote_elems = soup.find_all('font')
    
    # extract all quotes
    quotes = []
    for q in quote_elems:
        if not q.text: 
            continue
        quote, author = extract_quote_with_author(q)
        quote = quote.strip()
        
        # ignore leading dash in author (not always a normal dash character)
        author = author[1:].strip()
        
        # strip any enclosing quotation marks (not present in poems)
        if (quote.startswith('"') and quote.endswith('"')) or (quote.startswith('\'') and quote.endswith('\'')):
            quote = quote[1:-1].strip()
        quotes.append({'quote': quote, 'author': author})
    return quotes
    
def extract_quote_with_author(elem):
    # author is separated by <br><br>; to be safe we 
    # split by the last occurrence only.
    quote = ''
    author = ''
    br = 0
    author_split_index = -1
    for e in elem:
        if isinstance(e, Tag):
            if e.name == 'br':
                br += 1
                if br == 2:
                    author_split_index = len(quote)
            else:
                br = 0
                # retain italics tags (but strip enclosed tags like <img>)
                if e.name == 'i':
                    quote += "<i>" + e.text + "</i>"
                else:
                    quote += e.text
        else:
            br = 0
            quote += e
    if author_split_index > 0:
        author = quote[author_split_index:]
        quote = quote[:author_split_index]
    return quote, author
    
def save_quotes(quotes, fname):
    fieldnames = ['quote', 'author']
    with open(fname, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for q in quotes:
            writer.writerow(q)
    
if __name__ == "__main__":
    quotes = scrape_quotes()
    for q in quotes:
        print(q['author'])
    save_quotes(quotes, 'paul_graham_website_quotes.csv')
