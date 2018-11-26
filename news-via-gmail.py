import smtplib
import nvg-auth
import requests


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


# gather headlines from newsapi,org with apikey
url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=d4af94b7f71642cd8d60f97b59ab9317')
response = requests.get(url)    
data = response.json()
# save source name, title, and url to each article into 'message' var
message = [a['source']['name'] + ' : ' + a['title'] + '\n' + a['url'] + '\n' for a in data['articles']]

# send email
subject = "news test"
msg = ''.join(message)
send_email(subject, msg)
