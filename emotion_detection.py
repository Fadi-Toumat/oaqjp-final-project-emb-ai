import requests

# New emotion detection function
def emotion_detector(text_to_analyse):  # Define emotion detection function
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'  # Emotion API endpoint
    myobj = { "raw_document": { "text": text_to_analyse } }  # Same JSON structure
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}  # Emotion-specific headers
    response = requests.post(url, json = myobj, headers=header)  # POST request
    return response.text  # Return raw API response