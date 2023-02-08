import requests
import json
from bs4 import BeautifulSoup


def write_to_file(data):
    """
    This function convert result to JSON and write it to file after that.
    :param data:
    :return: None
    """
    # Serializing json
    json_object = json.dumps({'clothes': data}, indent=4)
    # Writing to sample.json
    with open("output.json", "w") as outfile:
        outfile.write(json_object)
        outfile.write('')


def scrape_page(page, info):
    """
    Searching "SCRIPT" tag which contain necessary info and extract it.
    :param page: given page
    :param info: list contains result for every page
    :return: None
    """""
    # make request to the URL
    req = requests.get(page)
    # Parse of the HTML
    soup = BeautifulSoup(req.content, 'html.parser')

    # TODO Think for better way to clear info
    # extract data from request
    script = soup.find_all('script')[4].text.split(' = ')[1]
    script = script.split(';')[0]
    data = json.loads(script)
    necessary_data = data["ecommerce"]["detail"]["products"][0]

    title = soup.find("title").text.split(" - ")[0]
    price = float(necessary_data["salePrice"])
    color = necessary_data['colorId']
    sizes = necessary_data['sizeNoAvailability'].split(',')
    result = {
        "title": title,
        "price": price,
        "color": color,
        "size": sizes,
    }
    info.append(result)


clothes_info = []

# URL1 is main url from given task. Other links are from me, to check for issues.
url1 = "https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99"
url2 = "https://shop.mango.com/gb/women/jackets-and-suit-jackets-jackets-and-suit-jackets/pocket-tweed-jacket_47014035.html?c=05"
url3 = "https://shop.mango.com/gb/women/skirts-long/denim-long-skirt_47073771.html?c=TM"
url4 = "https://shop.mango.com/gb/women/trousers-straight/leather-effect-straight-trousers_47010031.html?c=99"

list_pages = [url1, url2, url3, url4]

# We use List Comprehension to iterate pages and collect date from them
[scrape_page(x, clothes_info) for x in list_pages]

# Now we write this data in JSON file
write_to_file(clothes_info)
