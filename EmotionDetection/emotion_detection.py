import requests

def emotion_detector(text_to_analyse):
    """
    Sends a request to the Watson NLP Emotion Detection API and returns detected emotions.

    Parameters:
        text_to_analyse (str): The input text to analyze emotions from.

    Returns:
        dict: Emotion scores and the dominant emotion (values are None for status_code=400).
        str: Error message for other failures.
    """
    
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    payload = {"raw_document": {"text": text_to_analyse}}
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        # Handle 400 status code (blank input)
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        
        # Raise error for non-200/400 status codes
        response.raise_for_status()
        
        # Process successful response (status 200)
        formatted_response = response.json()
        emotions = formatted_response['emotionPredictions'][0]['emotion']
        dominant_emotion = max(emotions, key=emotions.get)
        
        return {
            'anger': emotions.get('anger', 0.0),
            'disgust': emotions.get('disgust', 0.0),
            'fear': emotions.get('fear', 0.0),
            'joy': emotions.get('joy', 0.0),
            'sadness': emotions.get('sadness', 0.0),
            'dominant_emotion': dominant_emotion
        }
    
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"