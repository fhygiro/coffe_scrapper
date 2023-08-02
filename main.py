import requests
from bs4 import BeautifulSoup as BS
import json


def main():
    product_link = []
    site_url = "https://www.teanadin.ru"
    url = "https://www.teanadin.ru/shop/kofe-2c/"
    req = requests.get(url)
    src = req.text
    soup = BS(src, "lxml")
    print("Searching for paddings..")
    paddings_count = len(soup.find(class_="paging-navigation").find_all("a")) - 1
    print(f"Paddings are: {paddings_count}")

    print("Searching for links...")

    for i in range(1, paddings_count + 1):
        if i == 1:
            url = "https://www.teanadin.ru/shop/kofe-2c/"
        else:
            url = f"https://www.teanadin.ru/shop/kofe-2c_{i}/"

        req = requests.get(url)
        src = req.text
        soup = BS(src, "lxml")
        list_link = soup.find_all(class_="highslide")

        for link in list_link:
            product_link.append(link.get("href"))

    print(f"Links are: {len(product_link)}")

    data_list = []

    for link in product_link:
        url = site_url + link
        req = requests.get(url)
        src = req.text
        soup = BS(src, "lxml")

        attrs_list = []

        name = soup.find("h1").text
        price = soup.find(class_="sell-btns").find(class_="big-price-digit").text + " руб"
        attrs = soup.find_all("tr", class_="tablerow")

        for attr in attrs:
            i = 1
            key = ""

            for row in attr:
                row_f = {}

                if i == 1:
                    key = row.text.replace(": ")
                    row_f[key] = ""
                elif i == 2:
                    row_f[key] = row.text
                    attrs_list.append(row_f)
                i += 1

        data = {
            "Название": name,
            "Цена": price,
            "Характеристики": attrs_list
        }

        data_list.append(data)

        print(url + " is done")

    with open("coffe_data.json", "w", encoding="utf-8") as json_file:
        json.dump(data_list, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
