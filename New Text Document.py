from bs4 import BeautifulSoup
import requests

root = 'https://www.reddit.com/r/VinylDeals/new/?f=flair_name%3A%22US%22'
result = requests.get(root)
content = result.text
soup = BeautifulSoup(content, 'lxml')
box = soup.find_all('h3', class_='_eYtD2XCVieq6emjKBH3m')
times = soup.find_all('span', class_='_2VF2J19pUIMSLJFky-7PEI')
comment_url = soup.find_all('div', class_='_3-miAEojrCvx_4FQ8x3P-s')

links = []        
for i in comment_url:
    for link in i.find_all('a', href=True, class_='_1UoeAeSRhOKSNdY_h3iS1O _1Hw7tY9pMr-T1F4P1C-xNU _3U_7i38RDPV5eBv7m4M-9J _2qww3J5KKzsD7e5DO0BvvU'):
        links.append(link['href'])


def extract_link(i):
    result = requests.get(f'https://www.reddit.com{links[i]}', headers={'User-Agent': 'Mozilla/5.0'}).text
    soup = BeautifulSoup(result, 'lxml')
    box = soup.find("a", href=True, class_='_3t5uN8xUmg0TOwRCOGQEcU')
    if box != None:
        return box['href']
    return '---- Link failed!!! ----'


with open('VinylDeals.txt', 'w', encoding='utf-8') as file:
    for i in range(len(box)):
        title = box[i].get_text()
        price = title.rsplit("$", 1)[1].split(" ", 1)[0]
        time = times[i].get_text()
        link = str(extract_link(i))
        print(f"Title: {title}\nPrice: ${price}\nTime: {time}\nLink: {link}\n\n")
        file.write(f"Title: {title}\nPrice: ${price}\nTime: {time}\nLink: {link}\n\n")
