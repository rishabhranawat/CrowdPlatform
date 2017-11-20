import requests
import bs4
import time


url = "https://metacademy.org/roadmaps/cjrd/coursera_ml_supplement"

def get_links_from_links(links):
    all_links = set()
    for each_url in links:
        try:
            response = requests.get(each_url)
            if(response.status_code != 200): continue
            each_page_soup = bs4.BeautifulSoup(response.content, "html.parser")
            for l in set(each_page_soup.find_all("a")):
                    if("http" not in l.get("href")):        
                        all_links.add(each_url+l.get("href"))
                    else:
                        all_links.add(l.get("href"))
            time.sleep(4)
        except Exception as e:
            print(e)
            continue
    return all_links

links = set([url])
l2 = get_links_from_links(links)
l3 = get_links_from_links(l2)
l4 = get_links_from_links(l3)

print(len(l4))
f = open("../meta_ml_seeds.txt", "w")
for u in l4:
    try:
        f.write(str(u)+"\n")
    except:
        print(u)
f.close()

