<a id="readme-top"></a>

<h1 align="center">Offers, Promotions Telegram Bot</h1>

<div align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-v3.8-blue">
  <img alt="Telegram" src="https://img.shields.io/badge/telegram-bot-blue">
  <img alt="MongoDB" src="https://img.shields.io/badge/mongodb-database-blue">
</div>

<div align="center">
I built this bot to aggregate the best offers from various e-commerce sites in one place. Currently, the bot is configured to fetch offers from Mercado Libre, but you can easily modify it to fetch offers from other e-commerce sites. Pull requests are welcome!
<br></br>

The bot is still in development, so it may have some bugs and missing features. I'll be working on improving it and adding more features.
<br></br>

Join the Telegram group for testing and feedback ➡️ [Offers, Promotions Telegram Bot](https://t.me/superdescuentos_mx)

</div>

![Telegram Channel Screenshot](/screenshot.png)

## Prerequisites

- **Python**: `v3.8 or higher` (Tested with `3.11.5`)
- **Telegram Bot**: Create a new bot using [BotFather](https://core.telegram.org/bots#6-botfather) and get the `API Token`.
- **Telegram Channel**: Create a new channel and add the bot as an admin. Get the `channel ID` from the channel settings.
- **IDE**: Optional. Visual Studio Code with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) is recommended.
- **Python Libraries**: Install the required libraries using `pip install -r requirements.txt`.
- **MongoDB**: Install MongoDB locally or use a cloud service like [MongoDB Atlas](https://www.mongodb.com/cloud/atlas). Get the `connection string` from the MongoDB dashboard.

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/alexjamesmx/e-commerce-offers-telegram-bot.git
   ```

2. Change the directory and install the required libraries:

   ```sh
   cd e-commerce-offers-telegram-bot
   pip install -r requirements.txt
   ```

3. Define the `/consts.py` file with your values. Use a secret file, environment variables, or another method to store your secrets.

4. Deploy the bot.
   You can deploy it on any cloud or self-hosted service. If deploying on Heroku, refer to the `/Procfile`. Learn more about Heroku [here](https://devcenter.heroku.com/articles/getting-started-with-python). Otherwise, remove the Procfile as it is not useful for other deployment methods.

5. Run the bot:

   ```sh
   python bot.py
   ```

## Environment Variables

Ensure you read the next section to know how to get the cookie and CSRF token.

```python
# Telegram bot token
API_TOKEN = YOUR_API_TOKEN

# Telegram channel ID
CHANNEL_ID = YOUR_CHANNEL_ID

# Mercado Libre affiliation ID
AFFILIATE_ID = YOUR_AFFILIATE_ID

# MongoDB configuration
DB_CONFIG_MONGO = {
    'uri': YOUR_DB_CONFIG_MONGO['uri'],  # connection string
    'database': YOUR_DB_CONFIG_MONGO['database']  # name of the database
}

# Mercado Libre cookie
COOKIE = YOUR_COOKIE

# CSRF token
X_CSRF_TOKEN = YOUR_X_CSRF_TOKEN

# User agent
USER_AGENT = YOUR_USER_AGENT

```

### Mercado libre API

Mercado libre opens their API to fetch products. These are the endpoints I use:

Getting the categories:
https://api.mercadolibre.com/sites/MLM/categories

Getting the products from a category:
https://api.mercadolibre.com/sites/SITE/search?category=CATEGORY_ID&attributes=id,title,price,currency_id,original_price,permalink

I.E: https://api.mercadolibre.com/sites/MLM/search?category=MLM1747&attributes=id,title,price,currency_id,original_price,permalink

MLM is the site for Mexico, you can change it to the site you want to get offers from.

See documentation here: https://developers.mercadolibre.com.mx/es_ar

Sadly, there is no public endpoint for generating affiliation links, so I had to use the browser developer tool to get the cookie and csrf token. This step is not necessary if you don't want to use affiliation links and benefit from the potential commissions.

### Steps for getting the cookie and csrf token

Go to the Mercado libre product generation link:
https://www.mercadolibre.com.mx/afiliados/linkbuilder

Open the browser developer tool, go to the network tab and filter by Fetch/XHR requests.

Click on the "Generar enlace" button, you'll see a request called "createUrls", click on it and go to the request headers.

You'll see the cookie and csrf token in the request headers.

Copy the cookie and csrf token and paste them in the `/consts.py` file.

For the user agent, you can use the one in the request headers.

### Features

- Get offers from Mercado Libre
- Get offers from a specific category
- Get the coupons if available of the product
- Publish the offers in a Telegram channel
- Save the offers in a MongoDB database
- Get the offers from the database avoiding duplicate offers if re-run the bot
- Parallerism is used to get the offers faster
- More e-commerce sites can be added following similar logic

### Contributing

Feel free to contribute to this project, I'll be happy to review your pull requests. Hope you enjoy it! and star the repo ⭐ if you like it.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. In a nutshell, you can do whatever you want with the code.
