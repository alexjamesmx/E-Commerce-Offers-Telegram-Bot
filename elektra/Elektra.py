from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

class ElektraScraper:
    def __init__(self, bot, product_queue, input_file, products_file="products.txt", galleries_file="galleries.txt"):
        self.input_file = input_file
        self.products_file = products_file
        self.galleries_file = galleries_file
        self.products_urls = []
        self.categories_urls = []

    def read_xlsx(self):
        df = pd.read_excel(self.input_file)
        return df["URL"].tolist()  # Returns a list of URLs from the Excel file

    def web_scrapping_getURls(self, original_urls):
        urls_products_or_categories = []
        for original_url in original_urls:
            try:
                response = requests.get(original_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                scripts = soup.find_all('script')
                for s in scripts:
                    if "window.location.href" in s.text:
                        new_url = s.text.split("window.location.href = ")[1].split(";")[0].replace('"', '')
                        urls_products_or_categories.append((original_url, new_url))
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL {original_url}: {e}")
        return urls_products_or_categories

    def web_scrapping_get_individual_products(self, urls):
        galleries_url = []
        products_url = []
        for original_url, new_url in urls:
            if "/p?" in new_url:
                products_url.append((original_url, new_url))
            else:
                galleries_url.append((original_url, new_url))
        return {
            "products_urls": products_url,
            "galleries_urls": galleries_url
        }

    def web_scrape_single_products(self, urls):
        data = []
        for original_url, product_url in urls:
            try:
                response = requests.get(product_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                sku_id_tag = soup.find('span', {"class": "vtex-product-identifier-0-x-product-identifier__value"})
                if not sku_id_tag:
                    print(f"SKU not found for URL: {product_url}")
                    continue
                sku_id = sku_id_tag.text.strip()
                api_url = f"https://www.elektra.mx/api/catalog_system/pub/products/search?fq=skuId:{sku_id}"
                api_response = requests.get(api_url)
                if api_response.status_code != 200:
                    print(f"Error fetching product data for URL: {product_url}")
                    continue
                product_data = api_response.json()[0]

                if "items" not in product_data or "commertialOffer" not in product_data["items"][0]["sellers"][0]:
                    print(f"No fields exist processing URL {product_url}: Invalid JSON response")
                    continue

                original_price = product_data["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]
                title = product_data["productName"]
                price = product_data["items"][0]["sellers"][0]["commertialOffer"]["Price"]
                discount = int(100 - (price * 100 / original_price))
                data.append({
                    "title": title,
                    "price": price,
                    "original_price": original_price,
                    "discount": discount,
                    "url": product_url,
                    "affiliate_url": original_url
                })
    
            except Exception as e:
                print(f"Error processing URL {product_url}: {e}")
        return data

    def run(self):
        if os.path.exists(self.products_file) and os.path.exists(self.galleries_file):
            with open(self.products_file, "r") as f:
                self.products_urls = [tuple(line.strip().split(", ")) for line in f.readlines()]
            with open(self.galleries_file, "r") as f:
                self.categories_urls = [tuple(line.strip().split(", ")) for line in f.readlines()]
        else:
            print("Reading file...")
            original_urls = self.read_xlsx()

            print("Getting URLs...")
            all_urls = self.web_scrapping_getURls(original_urls)

            print("Getting products or gallery products...")
            dict_urls = self.web_scrapping_get_individual_products(all_urls)
            self.products_urls = dict_urls["products_urls"]
            self.categories_urls = dict_urls["galleries_urls"]

            # Save URLs to files
            with open(self.products_file, "w") as f:
                for original_url, new_url in self.products_urls:
                    f.write(f"{original_url}, {new_url}\n")
        
            with open(self.galleries_file, "w") as f:
                for original_url, new_url in self.categories_urls:
                    f.write(f"{original_url}, {new_url}\n")

        # Now that we have the URLs for products and categories, let's get the data of the products first
        print("Scraping single products...") 
        data = self.web_scrape_single_products(self.products_urls)
        return data
