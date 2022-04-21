import os
import json
import hashlib
import pandas as pd
from io import StringIO
from google.auth import jwt
from google.cloud import pubsub_v1
from google.cloud import storage
## Def Parameters
service_account_path = 'serviceaccount.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_path

def write_cs(blob):
    bt = blob.download_as_string()
    s = str(bt, 'utf-8')
    s = StringIO(s)
    df = pd.read_csv(s)
    
    df['Latitude'] = df['Latitude'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
    df['Longitude'] = df['Longitude'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
    
    grouped = df.groupby('Country')
    l_grouped = list(grouped)
    
    client_country = storage.Client()
    bucket_country = client_country.get_bucket('pruebade-bucketbycountrycsv')
    
    for i in range(len(l_grouped)):
        path = 'upload_test/GlobalLandTemperaturesByCity_'+str(i)+'.csv'
        bucket_country.blob(path).upload_from_string(l_grouped[i][1].to_csv(), 'text/csv')

def callback(message):
    message_path_cs = message.data.decode('utf-8')
    message_json = json.loads(message_path_cs)
    cadena = message_json['body']
    message_path_b = cadena[0:cadena.find('/')]
    message_path_f = cadena[cadena.find('/')+1:len(cadena)]
    
    client = storage.Client()
    bucket = client.get_bucket(message_path_b)
    blob = bucket.get_blob(message_path_f)
    write_cs(blob)
    message.ack()

##EJECUCION

##-----------------------------------------------PARAMETROS DE EJECUCION-----------------------------------------------###
project_id = 'pruebade'
subscription_id = "ejecucion-cs"
service_account_info = json.load(open('serviceaccount.json'))

##-----------------------------------------------PARAMETROS DE EJECUCION-----------------------------------------------###

audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"

credentials = jwt.Credentials.from_service_account_info(
service_account_info, audience=audience
)

subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
subscription_path = subscriber.subscription_path(project_id, subscription_id)
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print("Listening for messages on {}..\n".format(subscription_path))
streaming_pull_future.result()

