import requests
from bs4 import BeautifulSoup
import logging
import time
from mercadoLibre.helpers import generate_affiliation_link, add_emojis, parse_cookies
from db_mongo import save_product
from consts import CHANNEL_ID, USER_AGENT, COOKIE


class MercadoLibre:
    def __init__(self, bot, product_queue):
        self.base_url = "https://api.mercadolibre.com/sites/MLM/search"
        self.bot = bot
        self.product_queue = product_queue

    def fetch_products(self, category):
        '''
        Fetches products for a given category and puts them in the product queue 
        Mercado libre e-commerce Category API allows max of 50 items per page, thats why we need to paginate if desired
        if less, we fetch all items in one go.
        '''
        offset = 0
        total_get = category['get']
        pages = (total_get // 50) + (1 if total_get % 50 != 0 else 0)
        limit = min(total_get, 50)  # Fetch up to 50 items per page, but not more than total_get

        for i in range(pages):
            if i == pages - 1:  # Last page
                limit = total_get - offset  # Fetch only the remaining items
            
            url = (
                f"https://api.mercadolibre.com/sites/MLM/search?category={category['id']}"
                f"&attributes=price,original_price,permalink,thumbnail&status=active&product_identifier=GTIN"
                f"&limit={limit}&offset={offset}"
            )
            try:
                res = requests.get(url)
                res.raise_for_status()  # Raise HTTPError for bad responses
                data = res.json()
                products = data.get('results', [])

                new_products = []
                for product in products:
                    # if no "discount" then skip. 
                    if self.is_discounted(product) == False:
                        continue
                                            
                    # Optional, filter based on needs, for example, only products with more than 50% discount
                    if self.discount_threshold(product) == False:
                        continue
                 
                    new_products.append(product)
                
                # logging purposes 
                logging.info(f"{category['id']} {category['name']}: Con descuento: {len(new_products)}")

                # Put the new products in the queue
                for product in new_products:
                    self.product_queue.put(product)

                offset += limit  # Increment offset for the next page

            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed for category {category['id']}: {e}")
                break

    def is_discounted(self, product):
        original_price = product.get('original_price')
        price = product.get('price')
        if not original_price or price >= original_price:
            return False
        return True

    def discount_threshold(self, product):
        price = product.get('price')
        original_price = product.get('original_price')
        discount_percentage = round(100 - (price * 100 / original_price))
        if (
            (price < 500 and discount_percentage >= 50) or
            (500 <= price < 2000 and discount_percentage >= 40) or
            (2000 <= price < 10000 and discount_percentage >= 50) or
            (price >= 10000 and discount_percentage >= 20)
        ): 
            return True
        return False
    


    def is_coupon(self, url):
        headers = {"User-Agent": USER_AGENT,
                   "cookie_string": COOKIE}
        response = requests.get(url, headers=headers, cookies=parse_cookies(COOKIE))
        soup = BeautifulSoup(response.text, 'html.parser')
        label = soup.find('label', id='coupon-awareness-row-label')
        if label:
            return label.get_text(strip=True)
        return None
    def publish_product(self):  
        '''
        Publishes a product in the channel
        Creates custom message with emojis and product information ,
        Waits 30 seconds before publishing the next product. You can adjust this time if needed, but dont saturate the channel
    '''   
        while True:
            product = self.product_queue.get()
            discount = round(100 - (product['price'] * 100 / product['original_price']))


            product['price'] = round(product['price'])
            product['original_price'] = round(product['original_price'])

            affiliate_link = generate_affiliation_link(product['permalink'], logger=logging)
            has_coupon = self.is_coupon(product['permalink']) 

            if(has_coupon): 
                logging.info(f"Coupon found: {product['id']} {has_coupon}")
            else: 
                logging.info(f"No coupon found for {product["permalink"]}")


            if(affiliate_link == None): 
                logging.error(f"Error generating affiliation link: for product {product['id']}")
                return

            header = add_emojis(product['title'], product['category_id'], discount)
            mensaje = (
                f"{header}\n\n"
                f"ENLACE: {affiliate_link}\n\n"
                f"De ${product['original_price']} a <b>${product['price']}</b> &#128293;{' Cupón ✅: {has_cupon}' if has_coupon else ''}\n\n"
                f"👉 <b>{discount}% {' (🚚 Gratis)' if product['shipping']['free_shipping'] else ''}\n\n</b>"
            )
            imagen_url = product['thumbnail'].replace('.jpg', 'C.jpg').replace('.png', 'C.png').replace('.jpeg', 'C.jpeg')
            logging.info(f"Publishing product: {product['id']} - {product['permalink']} - original: {product['original_price']} - ahora: {product['price']} \n")

            try: 
                self.bot.send_photo(CHANNEL_ID, imagen_url, caption=mensaje, parse_mode='HTML')
                save_product(product['id'])
                self.product_queue.task_done()
                time.sleep(30)
            except Exception as e:
                logging.error(f"Error publishing product: {e}")
                self.product_queue.task_done()


