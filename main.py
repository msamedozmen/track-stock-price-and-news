import requests
import datetime as dt
import html
from twilio.rest import Client
import smtplib

time_now = dt.datetime.now()
day=time_now.day
month = time_now.month
year =time_now.year
last_three_days = day -3
from_time =f"{year}-0{month}-0{last_three_days}"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
# print(from_time)
stock_api_key="stock api"

stocks_url="https://www.alphavantage.co/query"
stock_param = {
    "function":"TIME_SERIES_DAILY_ADJUSTED",
    "symbol":STOCK,
    "apikey":stock_api_key
    
}
#STEP1 GET STOCK VALUES
stock_response = requests.get(url=stocks_url,params=stock_param)
# print(stock_response)
# print(stock_response.json())
stock_name =stock_response.json()["Meta Data"]["2. Symbol"]
stock_data =stock_response.json()["Time Series (Daily)"]

days = list(stock_data)[1:3]
close =[]
for day in days:
    close_value=(stock_data[day]["4. close"])
    close.append(close_value)

close_dif =float(close[0])-float(close[1])
# print(close_dif)
close_diff_perc =float(float(close[0])/float(close[1]))*100-100
# print(round(close_diff_perc,3),"%")

#STEP2 NEWS

news_api_key ="NEWS API KEY"
news_url="https://newsapi.org/v2/everything"

news_parameters = {
    "q": "tesla",
    "from":from_time,
    "sortBy":"publishedAt",
    "apiKey": news_api_key
}


news_response = requests.get(url=news_url,params=news_parameters)
news_data = news_response.json()["articles"]
# print(news_data)
heads =[]
briefs=[]
for i in range(3):
    headline = news_data[i]["title"]
    headline=html.escape(headline)
    heads.append(headline)
    brief = news_data[i]["description"]
    brief=html.escape(brief)
    briefs.append(brief)
    
# print(briefs)
print(heads)

nl = '\n'
b="🔺"
#STEP 3 SEND MESSAGES
account_sid = "ACCOUNT ID"
auth_token = "TOKEN"
client = Client(account_sid, auth_token)
message = client.messages.create(
  body=f"{STOCK}: 🔺{close_diff_perc} {nl}Headline: {heads[0]} {nl} Brief: {briefs[0]} {nl}Headline: {heads[1]} {nl} Brief: {briefs[1]} {nl}Headline: {heads[2]} {nl} Brief: {briefs[2]} ",
  from_="+NUM",
  to="+YOUR PHON NUMBER"
)
print(message.sid)
a =f"Subject:Today's Tesle Stock Value{nl}{nl}{STOCK}: {close_diff_perc}{nl}Headline: {heads[0]}{nl}Brief: {briefs[0]}{nl}Headline: {heads[1]}{nl}Brief: {briefs[1]}{nl}Headline: {heads[2]}{nl}Brief: {briefs[2]}"
# a.encode("utf-8")
print(f"Subject:Today's Tesle Stock Value{nl}{nl}{STOCK}: '🔺'{close_diff_perc}{nl}Headline: {heads[0]}{nl} Brief: {briefs[0]} {nl}Headline: {heads[1]} {nl} Brief: {briefs[1]} {nl}Headline: {heads[2]} {nl} Brief: {briefs[2]} ")
my_email = "MAIL"
my_pass ="PASSWORD"
connection = smtplib.SMTP("smtp.gmail.com")
connection.starttls()
connection.login(user=my_email,password=my_pass)
connection.sendmail(from_addr=my_email,to_addrs="MAIL",msg=a.encode("utf-8"))
connection.close()
print(f"{heads[0]}")



