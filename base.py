from PIL import Image
import pytesseract
import anthropic

# Path to Tesseract executable (change it according to your installation)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Function to process uploaded image and get recommendations
def process_lab_test_image(image_path):
    # Use pytesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(image_path)

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

# Example usage
if __name__ == "__main__":
    # Assuming the uploaded image is named 'main.png'
    uploaded_image_path = 'main.png'
    recommendations = process_lab_test_image(uploaded_image_path)
    print("Recommendations based on lab test results:")
    print(recommendations)