
#libraries 
import telebot
import time
import logging
import sys 
import os
import json

#parallerism
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import queue

#erro handling 
from requests.exceptions import ConnectionError, ReadTimeout

# helpers
from consts import API_TOKEN

#bots
from mercadoLibre.MercadoLibre import MercadoLibre
from elektra.Elektra import Elektra


bot = telebot.TeleBot(API_TOKEN)
product_queue = queue.Queue()
ml = MercadoLibre(bot, product_queue)
el = Elektra(bot, product_queue, "elektra/input.xlsx") 

def bot_handler():
    # Execute n threads for each category in parallel to fetch products 
    with ThreadPoolExecutor(max_workers=len(categories[0])) as executor:
        futures_ml = [executor.submit(ml.fetch_products, category) for category in categories[0]]
        for future in as_completed(futures_ml):
            try: 
                future.result()
            except Exception as e:
                logging.error(f"Error fetching products: {e}")
 
categories = []

with open("./mercadoLibre/categories.json", "r") as json_data:
    data = json.load(json_data)  
    categories.append(data["categories"])

if __name__ == "__main__":
    # Uncomment for log file generation 
    # if os.path.exists("bot.log"):
    #     os.remove("bot.log")  

    # Start product handler thread
    handler_thread = threading.Thread(target=ml.publish_product, daemon=True)
    handler_thread.start()

    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
      handlers=[
        # Uncomment for log file generation 
        # logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ])
    while True:
        try:
            logging.info("Running new execution...")
            bot_handler()
            logging.info("Waiting for products if available to publish...")
            product_queue.join() 
            logging.info("Done. Sleeping 3 minutes before restart...")
            time.sleep(120) 
        except (ConnectionError, ReadTimeout) as e:
            logging.error(f"Conection Error: {e}")
            sys.stdout.flush()
            os.execv(sys.argv[0], sys.argv)



#check coupon web scrapping works 
# url = "https://www.mercadolibre.com.mx/papel-higienico-kimberly-clark-kleenex-cotonelle-doble-hoja-de40u/p/MLM19544225#polycard_client=storefronts&type=product&tracking_id=bd9055d5-e301-4d58-85bc-eaec27a20250&source=eshops&wid=MLM1487063918&sid=storefronts"
# obtener_cupon_awareness(url)




