import smtplib
import auth
import requests
import json


# function to send email
def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(auth.EMAIL_ADDRESS, auth.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(auth.EMAIL_ADDRESS, auth.EMAIL_ADDRESS, message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")


# gather news
url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=d4af94b7f71642cd8d60f97b59ab9317')
response = requests.get(url)
# print(response.json())
data = response.json()
message=[]

#  write to file
with open('data', 'w') as outfile:
        for a in data['articles']:
            outfile.write(a['source']['name'] + ' : ' + a['title'] + '\n')
            outfile.write("'" + a['url'] + "'" + '\n')
            outfile.write('\n')

# read from file
with open('data.json') as json_file:
    data = json.load(json_file)
    for a in data['articles']:
        message.append(a['source']['name'] + ' : ' + a['title'] + '\n')
        message.append(a['url'] + '\n')

# send email
subject = "news test"
msg = ''.join(message)
send_email(subject, msg)
