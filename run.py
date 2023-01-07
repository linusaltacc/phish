import streamlit as st
import requests
from test_pretrained_model import phish
import json
st.title('Fake Link Detector')
st.subheader("Team Hello World")
print("*")
inpu = st.text_input('URL', value='http://example.org')
print("Entered ",str(inpu))
import urllib.parse
print(phish(inpu))
predictionProbability , prediction, threshold=phish(inpu)
url = 'https://ipqualityscore.com/api/json/url/1NHw3nJcLriTVGPogr7vqNWMhYYsnVgf/' + urllib.parse.quote(inpu, safe='')
print(url)
st.subheader("ML results")
print(predictionProbability , prediction, threshold)
st.write(prediction)
st.write("Threshold : " ,threshold)
st.write("Prediction Probability : " ,predictionProbability)
import json,urllib.request

# print(url)
resp = urllib.request.urlopen(url).read()
resp = json.loads(resp)

# st.write(resp)
st.subheader("API results")
st.write("IP Address : " ,resp['ip_address'])
if resp['spamming'] or resp['malware'] or resp['phishing'] or resp['suspicious']:
    st.header("The Entered Website is NOT SAFE")
else:
    st.header("The Entered Website is SAFE")

st.write("Spamming : " , resp['spamming'])
st.write("Malware : " , resp['malware'])
st.write("Phishing : " , resp['phishing'])
st.write("Suspicious : " , resp['suspicious'])
st.write("Created on : ", resp['domain_age']['human'])

