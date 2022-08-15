import requests


botToken = '5140137870:AAEvAV7xaUOyjLR4uMFcIMnUtZG5VhOaMvQ'
chatID = 1101456056
chatID = 1127134309
baseUrl = f'https://api.telegram.org/bot{botToken}'

def sendMessage(message):
    url= f'{baseUrl}/sendMessage?chat_id={chatID}&text={message}'
    response = requests.get(url)
    return response.json()

response = sendMessage('Hola!')
print(response)