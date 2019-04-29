# uses https://github.com/bear/python-twitter
# to install run pip3 install python-twitter
# to run py ./main.py
# make sure running in python 3
import twitter
import requests
import sys
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/SignUp')
def SignUp():
    return render_template('SignUp.html')

@app.route('/ForgotPassword')
def ForgotPassword():
    return render_template('ForgotPassword.html')



@app.route('/coinprice')
def coin():
    
    coinList = ["ETH,BTC,ZIL,XRP,BCH,EOS,BNB,USDT,XLM,ADA,TRX"] #Imported 11 top coin prices

    apiKey = "8ec834fcff9fe8918f654e2ab29459505ba655dca7243b4e50d5c70f824d7259" # unique key

    # url = "https://min-api.cryptocompare.com/data/price"
    # url = "https://min-api.cryptocompare.com/data/pricemulti"
    url = "https://min-api.cryptocompare.com/data/pricemultifull" # details imported

    payload = {
        
        # "fsyms": coin,
        "fsyms": coinList, # 11 coins
        "tsyms": "GBP" #currency values are returned in
    }

    headers = {
        "authorization": "Apikey " + apiKey #api formatting
    }

    data = requests.get(url, headers=headers, params=payload).json()

    data = data['RAW']

    coins = []
    for c in data.keys(): #gets the needed values from the json package
        coin = {
            'price' : data[c]['GBP']['PRICE'],
            'supply':data[c]['GBP']['SUPPLY'],
            'mktcap':data[c]['GBP']['MKTCAP'],
            'fromsymbol':data[c]['GBP']['FROMSYMBOL']
        }
        coins.append(coin)
    

    return(render_template('coinprice.html', d=coins))

@app.route('/coinprice', methods = ["POST"])
def coin_form():

    text = request.form['text'] #request input from page
    search = text.upper() 

    apiKey = "8ec834fcff9fe8918f654e2ab29459505ba655dca7243b4e50d5c70f824d7259"

    url = "https://min-api.cryptocompare.com/data/pricemultifull"

    payload = {
        
        "fsyms": search,
        "tsyms": "GBP"
    }

    headers = {
        "authorization": "Apikey " + apiKey
    }

    data = requests.get(url, headers=headers, params=payload).json()

    data = data['RAW']

    coins = []
    for c in data.keys():
        coin = {
            'price' : data[c]['GBP']['PRICE'],
            'supply':data[c]['GBP']['SUPPLY'],
            'mktcap':data[c]['GBP']['MKTCAP'],
            'fromsymbol':data[c]['GBP']['FROMSYMBOL'],
            'highday':data[c]['GBP']['HIGHDAY'],
            'lowday':data[c]['GBP']['LOWDAY'],
            'changeday':data[c]['GBP']['CHANGEDAY']

        }
        coins.append(coin)


    return render_template('coinprice.html',d = coins)


@app.route('/twitter')
def my_form():
    return render_template('twitter.html')


@app.route('/twitter', methods=['POST'])
def twit():

    searched = "Cryptocurrency"

    text = request.form['text'] #request input from page
    searched = text.upper() 

    if searched == "":
        searched = "Cryptocurrency" # provides a base search for cryptocurrency if nothing has been searched

    api = twitter.Api(\
            consumer_key='TWVxfrliliibQxjNWz4tAlDIj',
            consumer_secret='QK2IBqNorysgD3quaBJVCMDdMApOpo5fW5g6Pl4Di97ToRjsGy',
            access_token_key='3011394611-QmeEQ5yaL6OJTOmqemXV3eS0DpE09P0sy64XhnL',
            access_token_secret='tEMygLkKBDwfVepHAg7G9BI7N8VQJM7U9KKefpV40jUq1'
        )# twitter unique codes
    count = "20"
    data = api.GetSearch(
    raw_query=  'q='+str(searched)+'&'
                'count='+str(count)+'&'
                'lang=en&'
                'tweet_mode=extended&'
                #'geocode=51.4027029,-0.3040634,10mi' #kington
    )

    print(data)
    for i in data: #formats the tweets
        print('---------------------------')
        if hasattr(i, 'retweeted_status'):
            print(i.user.name + ': ' +  i.full_text)
        else:
            print(i.user.name + ': ' +  i.retweeted_status.full_text)

    return(render_template('Twitter.html', d=data))

@app.route('/trending')
def trend():

    return render_template('Trending.html')


if __name__ == '__main__':
    app.run(debug=True) 
