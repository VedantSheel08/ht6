from flask import Flask, request, jsonify
import os
from google.genai import types
from google import genai

client = genai.Client()

app = Flask(__name__)


def process_image_with_gemini(image_file, goal_description):
    """
    Process the received image with Gemini API based on the goal description.
    """

    prompt = f"""
You are an image analysis function for a motor car with a camera. Your goal: "{goal_description}"

Analyze the image and respond with:
- The best action code (see below) on the first line.
- A brief explanation (1-2 sentences) on the next line, including any uncertainty or nuance.

Action codes (choose one):
1. GOAL_ACHIEVED: Target is clearly visible and centered (car has reached goal).
2. MOVE_LEFT: Target is visible on the left 25% of the frame. Note if unsure how much to move or risk of overshoot.
3. MOVE_RIGHT: Target is visible on the right 25%. Note any uncertainty.
4. MOVE_FORWARD: Target is visible but too far away. Mention if distance is unclear.
5. MOVE_BACKWARD: Target is visible but too close.
6. TURN_RIGHT: Target not visible; recommend rotating right to search.
7. TURN_LEFT: Target not visible; recommend rotating left to search.
8. NOT_FOUND: Target is completely absent from the view.

Instructions:
- Be specific about the target's position and any uncertainty about movement or car accuracy.
- If the target is partially visible or ambiguous, explain your reasoning and suggest the best movement.
- Mention if a movement might overshoot or if fine adjustment is needed.
- Do NOT use vague codes like "REORIENT" or "ADJUST POSITION"—pick from the list above.
- If reorientation is needed, specify TURN_LEFT or TURN_RIGHT and why.

Keep your response concise and focused on helping the car center and approach the target safely.
"""

    try:
        # Always read the image from disk, as in the working example
        with open('received_screenshot.bmp', 'rb') as f:
            image_bytes = f.read()

        print(f"Processing image with Gemini API for goal: {goal_description}")

        # Use the same model and prompt as the working minimal example
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type='image/jpeg',
                ),
                prompt,
            ]
        )

        print(f"Gemini response: {response.text}")
        return response.text.strip()

    except Exception as e:
        print(f"Error processing image with Gemini: {e}")
        return f"ERROR: {str(e)}"

@app.route("/receive_image", methods=["POST"])
def receive_image():
    """
    Receive image from Pi and process with Gemini API.
    This version saves the image to disk and then processes it from disk,
    just like the working minimal example.
    """
    try:
        if "image" not in request.files:
            return (
                jsonify({"status": "error", "message": "No image file received"}),
                400,
            )

        image_file = request.files["image"]
        goal_description = request.form.get("goal", "Find the target object")

        # Save the image to disk as 'received_screenshot.bmp'
        image_file.save("received_screenshot.bmp")

        # Process the image with Gemini (from disk)
        gemini_response = process_image_with_gemini(image_file, goal_description)

        return gemini_response, 200

    except Exception as e:
        print(f"Error processing received image: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Laptop server is running"})

if __name__ == "__main__":
    print("  POST /receive_image - Receive and process images from Pi")
    print("  GET  /health        - Health check")
    app.run(host="0.0.0.0", port=8000, debug=True)
