from my_secret_variables import * 
#telegram bot token 
API_TOKEN = MY_API_TOKEN
#telegram channel id 
CHANNEL_ID = MY_CHANNEL_ID 



#MERCADO LIBRE 
#mercado libre affliation id, being the name of your affiliation tag
AFFILIATE_ID = MY_AFFILIATE_ID 

#mongo db configuration or use whatever database you want 
DB_CONFIG_MONGO = {
    'uri': MY_DB_CONFIG_MONGO['uri'],  # connection string
    'database': MY_DB_CONFIG_MONGO['database'] #name of the database 
}

# Mercado libre coockie, get  it using the browser developer tool > network > request headers > cookie 
# You'll see the cookie header when generating a affiliation link, the request is "createUrls" 
COOKIE = MY_COOKIE
X_CSRF_TOKEN = MY_X_CSRF_TOKEN

USER_AGENT = MY_USER_AGENT

#ELEKTRA 