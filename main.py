from google import genai
from PIL import Image
import base64
import os
import io


# ============================================================
# CONFIGURATION
# ============================================================

COURSE_NAME = "Certified Information Systems Auditor (CISA)"
OUTPUT_FILE = "CISA_course_image.png"

TARGET_WIDTH = 750
TARGET_HEIGHT = 422


# ============================================================
# PROMPT
# ============================================================

prompt = f"""
Create a premium professional certification course thumbnail.

Course concept:
{COURSE_NAME}

IMPORTANT:
The course title itself MUST NOT appear anywhere in the image.

Create a visually impressive 16:9 landscape composition representing:

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

- Modern
- Premium
- Professional
- Corporate
- Futuristic
- Sophisticated
- Trustworthy
- High visual impact

Use visual elements such as:

- Futuristic cybersecurity interfaces
- Digital network structures
- Circuit-board patterns
- Secure data streams
- Abstract audit/check concepts
- Digital dashboards
- Security shields
- Data visualization
- Subtle certification/exam symbolism
- Sophisticated lighting
- Depth and layered composition

LOGO REQUIREMENT:

Include the official ISACA logo subtly and professionally.

The logo should be:
- Clean
- Accurate
- Undistorted
- Clearly recognizable
- Integrated naturally into the composition
- Small enough not to dominate the design

TEXT RESTRICTIONS:

- Do NOT display the course title.
- Do NOT add random text.
- Do NOT add fake certification text.
- Do NOT add fake badges.
- Do NOT add watermarks.
- Do NOT include Udemy branding.
- Do NOT include the Udemy logo.
- Do NOT reference Udemy.

The ONLY textual/logo element permitted is the official ISACA logo.

Create a visually attractive premium certification
exam-preparation thumbnail.

Aspect ratio: 16:9.
"""


# ============================================================
# API KEY
# ============================================================

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=api_key)


# ============================================================
# GENERATE IMAGE
# ============================================================

print("Generating image...")

interaction = client.interactions.create(
    model="gemini-nano-banana-2.1",
    input=prompt,
    response_format={
        "type": "image",

        # IMPORTANT:
        # Gemini Interactions API currently accepts JPEG here.
        "mime_type": "image/jpeg",

        "aspect_ratio": "16:9",
        "image_size": "1K"
    }
)


# ============================================================
# GET GENERATED IMAGE
# ============================================================

if not interaction.output_image:
    raise RuntimeError(
        "Gemini did not return an image."
    )


image_data = base64.b64decode(
    interaction.output_image.data
)


# ============================================================
# LOAD IMAGE
# ============================================================

image = Image.open(
    io.BytesIO(image_data)
)

print(f"Gemini generated image: {image.size}")


# ============================================================
# CONVERT + RESIZE
# ============================================================

image = image.convert("RGB")

image = image.resize(
    (TARGET_WIDTH, TARGET_HEIGHT),
    Image.Resampling.LANCZOS
)


# ============================================================
# SAVE FINAL PNG
# ============================================================

image.save(
    OUTPUT_FILE,
    format="PNG",
    optimize=True
)


# ============================================================
# VERIFY
# ============================================================

check = Image.open(OUTPUT_FILE)

print()
print("========================================")
print("IMAGE GENERATED SUCCESSFULLY")
print("========================================")
print(f"File   : {OUTPUT_FILE}")
print(f"Size   : {check.width} x {check.height}")
print(f"Format : {check.format}")
print("========================================")


if check.size != (750, 422):
    raise RuntimeError(
        f"Wrong final size: {check.size}"
    )
