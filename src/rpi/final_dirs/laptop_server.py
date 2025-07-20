from flask import Flask, request, jsonify
import os
from google.genai import types
from google import genai

client = genai.Client()

app = Flask(__name__)


def process_image_with_gemini(image_file, goal_description):
    """
    Process the received image with Gemini API based on the goal description
    """
    try:
        # Read the image file
        image_bytes = image_file.read()

        print(f"Processing image with Gemini API for goal: {goal_description}")

        # Create comprehensive prompt for motor car navigation
        comprehensive_prompt = f"""
The agent that called you is controlling a motor car with a camera. You are not the motor car or the camera, but you are being called as a function to help the MCP Server decide what to do next. Your goal is: "{goal_description}"

Analyze this image and respond with a short, clear action code (see below), followed by a brief explanation (1-2 sentences) about why you chose that action and any relevant uncertainty or nuance. If you are unsure about the best movement (for example, if moving left might move the target too far, or if the target is only partially visible), mention that in your explanation. The car's hardware interface is not always perfectly accurate—movements may drift or overshoot—so be cautious in your recommendations.

Possible action codes and when to use them:
1. GOAL_ACHIEVED: Use "GOAL_ACHIEVED" if the target object is clearly visible and centered in the camera frame, meaning the car has reached the desired position.
2. MOVE_LEFT: Use "MOVE_LEFT" if the target is visible but positioned to the left side of the frame (left 25% of screen). If you are unsure how much to move left, or if a small move might overshoot, mention this.
3. MOVE_RIGHT: Use "MOVE_RIGHT" if the target is visible but positioned to the right side of the frame (right 25% of screen). Note any uncertainty about how much to move.
4. MOVE_FORWARD: Use "MOVE_FORWARD" if the target is visible but too far away or needs to be approached. If the distance is unclear, mention it.
5. MOVE_BACKWARD: Use "MOVE_BACKWARD" if the target is visible but too close or needs backing up.
6. TURN_RIGHT: Use "TURN_RIGHT" if the target is not visible in the current frame and you recommend rotating right to search.
7. TURN_LEFT: Use "TURN_LEFT" if the target is not visible in the current frame and you recommend rotating left to search.
8. NOT_FOUND: Use "NOT_FOUND" if the target object is completely absent from the current view.

IMPORTANT:
- Respond with the action code (e.g., "MOVE_RIGHT") on the first line, then a short explanation (1-2 sentences) on the next line.
- Be specific about the target's position and any uncertainty about the movement or the car's accuracy.
- If the target is partially visible or ambiguous, explain your reasoning and suggest the most appropriate movement.
- The car's movement is not always precise; mention if a movement might overshoot or if fine adjustment is needed.
- Keep your response concise and focused on helping the car center and approach the target safely.
- Remember, you are assisting the MCP Server by analyzing the image and providing your best recommendation for the next action.

ADDITIONAL INSTRUCTIONS:
- Do NOT use vague or generic action codes like "REORIENT" or "ADJUST POSITION". You must select one of the specific action codes listed above (e.g., "TURN_LEFT", "MOVE_RIGHT", etc.).
- If you think the car should reorient, specify the exact direction (TURN_LEFT or TURN_RIGHT) and explain why that direction is best based on the image.
- If you are uncertain between two actions, pick the most likely one and explain your reasoning, but always use a specific action code from the list.
- Never invent new action codes or use synonyms; only use the codes provided above.
- If the image is ambiguous, state the ambiguity in your explanation, but still choose the most appropriate action code from the list.
- If you would have said something like "reorient" or "adjust", instead say "TURN_LEFT" or "TURN_RIGHT" and justify your choice.
"""

        # Send to Gemini API
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg",
                ),
                comprehensive_prompt,
            ],
        )

        print(f"Gemini response: {response.text}")
        return response.text.strip()

    except Exception as e:
        print(f"Error processing image with Gemini: {e}")
        return f"ERROR: {str(e)}"


@app.route("/receive_image", methods=["POST"])
def receive_image():
    """
    Receive image from Pi and process with Gemini API
    """
    try:
        if "image" not in request.files:
            return (
                jsonify({"status": "error", "message": "No image file received"}),
                400,
            )

        image_file = request.files["image"]
        goal_description = request.form.get("goal", "Find the target object")

        print(f"Received image: {image_file.filename}")
        print(f"Goal description: {goal_description}")

        # Process the image with Gemini
        gemini_response = process_image_with_gemini(image_file, goal_description)

        # Save the image locally for debugging (optional)
        image_file.seek(0)  # Reset file pointer
        image_file.save("received_screenshot.bmp")

        return gemini_response, 200

    except Exception as e:
        print(f"Error processing received image: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Laptop server is running"})


if __name__ == "__main__":
    # print("Starting Laptop Image Processing Server...")
    # print("Available endpoints:")
    print("  POST /receive_image - Receive and process images from Pi")
    print("  GET  /health        - Health check")
    # print("\nServer running on http://0.0.0.0:8000")
    app.run(host="0.0.0.0", port=8000, debug=True)
