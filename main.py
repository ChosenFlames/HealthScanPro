from flask import Flask, request, render_template
from PIL import Image
import pytesseract
import anthropic
import io

app = Flask(__name__, static_url_path='/static')

# Path to Tesseract executable (change it according to your installation)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Function to process uploaded image and get recommendations
def process_lab_test_image(image):
    # Use pytesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(image)

    # Construct a more detailed prompt
    prompt = f"Lab test results:\n\n{extracted_text}\n\nPlease provide detailed recommendations based on these lab test results, including potential diagnoses, further tests or investigations needed, and treatment options. If any values are outside of normal ranges, please explain the significance and implications. Additionally, provide guidance on lifestyle changes, dietary recommendations, or any other relevant advice for managing or improving the patient's condition."

    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key="YOUR_API_KEY_HERE")

    # Generate recommendations using the Claude API
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )

    # Return the content of the generated message (recommendations)
    return message.content

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read()))
    recommendations = process_lab_test_image(image)
    return recommendations

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)