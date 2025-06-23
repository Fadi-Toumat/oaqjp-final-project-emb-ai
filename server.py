"""
Flask application for emotion detection using Watson NLP API.
This module sets up a Flask server to analyze emotions in text input.
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def sent_emotion_detector():
    """
    Analyze emotions in the provided text and return formatted results.

    Retrieves text from 'textToAnalyze' query parameter, processes it through
    the emotion detection service, and returns formatted results. Handles
    invalid input and errors appropriately.

    Returns:
        str: Formatted emotion analysis results or error messages
    """
    # Retrieve the text to detect from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')

    # Pass the text to the emotion_detector function and store the response
    response = emotion_detector(text_to_analyze)

    # Handle error cases
    if isinstance(response, str):  # Network/API errors
        return response

    # Check for blank input (dominant_emotion is None)
    if response.get('dominant_emotion') is None:
        return "Invalid text! Please try again!"

    # Format the response string
    return (
        f"For the given statement, the system response is "
        f"'anger': {response.get('anger')}, "
        f"'disgust': {response.get('disgust')}, "
        f"'fear': {response.get('fear')}, "
        f"'joy': {response.get('joy')} and "
        f"'sadness': {response.get('sadness')}. "
        f"The dominant emotion is {response.get('dominant_emotion')}."
    )


@app.route("/")
def render_index_page():
    """
    Render the main index page of the Emotion Detection application.

    Returns:
        Rendered HTML template for the application's homepage.
    """
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
