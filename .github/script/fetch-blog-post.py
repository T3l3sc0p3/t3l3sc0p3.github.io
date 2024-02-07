import os, sys, requests
from bs4 import BeautifulSoup

def fetch(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f'Failed to fetch data from {url}. Status code: {response.status_code}')
        return None

def parse(feed_xml):
    entries = []
    for entry in BeautifulSoup(feed_xml, 'lxml').find_all('entry'):
        entries.append({'title': entry.find('title').text, 'url': entry.find('id').text, 'published': entry.find('published').text})
    return entries

def update(path, entries):
    with open(path, 'r') as file:
        content = file.read()
    tag = '<!-- Fetch-Blog-Post:Start -->'
    start = content.find(tag) + len(tag)
    end = content.find('<!-- Fetch-Blog-Post:End -->')
    if start != -1 and end != -1:
        new_content = content[:start]
        for entry in entries:
            new_content += f'\n- [{entry["title"]}]({entry["url"]})'
        new_content += f'\n{content[end:]}'
        with open(path, 'w') as file:
            file.write(new_content)

def main(urls):
    entries = []
    for url in urls:
        feed_xml = fetch(url)
        if feed_xml:
            entries.extend(parse(feed_xml))
    update("README.md", sorted(entries, key=lambda x: x['published'], reverse=True)[:10])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f'Usage: python {os.path.basename(sys.argv[0])} <xml-url-1> <xml-url-2> ... <xml-url-n>')
        sys.exit(1)
    main(sys.argv[1:])
