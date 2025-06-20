import requests
import json

def emotion_detector(text_to_analyse):
    """
    Sends a request to the Watson NLP Emotion Detection API and returns detected emotions.

    Parameters:
        text_to_analyse (str): The input text to analyze emotions from.

    Returns:
        dict: Emotion scores and the dominant emotion, or error message in case of failure.
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    payload = {
        "raw_document": {
            "text": text_to_analyse
        }
    }
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad HTTP status codes

        data = response.json()

        emotions = data['emotionPredictions'][0]['emotion']
        dominant_emotion = max(emotions, key=emotions.get)

        return {
            'anger': emotions.get('anger', 0.0), 'disgust': emotions.get('disgust', 0.0),
            'fear': emotions.get('fear', 0.0), joy': emotions.get('joy', 0.0),
            'sadness': emotions.get('sadness', 0.0),
            'dominant_emotion': dominant_emotion
        }

    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error: {str(req_err)}"}

    except (KeyError, IndexError, ValueError) as parse_err:
        return {"error": f"Response parsing error: {str(parse_err)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
