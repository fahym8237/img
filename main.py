from google import genai
from PIL import Image
import base64
import os
import io


COURSE_NAME = "Certified Information Systems Auditor (CISA)"
OUTPUT_FILE = "CISA_course_image.png"

TARGET_SIZE = (750, 422)


prompt = f"""
Create a premium professional certification course thumbnail.

Course concept:
{COURSE_NAME}

IMPORTANT:
Do NOT display the course title anywhere.

Create a modern 16:9 landscape design representing:

- Cybersecurity
- Information systems auditing
- IT governance
- Risk management
- Compliance
- Data protection
- Digital auditing
- Professional certification
- Exam preparation
- Advanced technology

Visual style:

- Premium
- Professional
- Modern
- Futuristic
- Corporate
- Sophisticated
- Trustworthy
- High visual impact

Use:

- Futuristic digital networks
- Circuit-board patterns
- Cybersecurity elements
- Digital data visualization
- Secure network structures
- Abstract audit/check concepts
- Certification-inspired visual elements
- Sophisticated lighting
- Depth and gradients

LOGO:

Include the official ISACA logo subtly and professionally.

The logo should be clean, recognizable, undistorted,
and naturally integrated into the composition.

TEXT RESTRICTIONS:

- No course title.
- No random text.
- No fake certification text.
- No fake badges.
- No watermark.
- No Udemy logo.
- No Udemy branding.
- No reference to Udemy.

The ONLY textual/logo element permitted is the official ISACA logo.

Create a visually attractive premium certification
exam-preparation thumbnail.
"""


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured.")


client = genai.Client(api_key=api_key)


print("Generating image...")


interaction = client.interactions.create(
    model="gemini-nano-banana-2.1",
    input=prompt,
    response_format={
        "type": "image",
        "mime_type": "image/png",
        "aspect_ratio": "16:9",
        "image_size": "1K"
    }
)


if not interaction.output_image:
    raise RuntimeError("Gemini did not return an image.")


image_data = base64.b64decode(
    interaction.output_image.data
)


image = Image.open(
    io.BytesIO(image_data)
)

print("Generated:", image.size)


image = image.convert("RGB")

image = image.resize(
    TARGET_SIZE,
    Image.Resampling.LANCZOS
)

image.save(
    OUTPUT_FILE,
    "PNG",
    optimize=True
)


print("====================================")
print("IMAGE GENERATED SUCCESSFULLY")
print("====================================")
print(f"File: {OUTPUT_FILE}")
print(f"Size: {image.size}")
print("Format: PNG")