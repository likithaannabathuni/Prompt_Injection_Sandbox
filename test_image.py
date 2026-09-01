from image_generator import generate_image


# Test prompt
prompt = """
Create a professional futuristic illustration of an AI security
laboratory. Show a computer screen displaying a prompt injection
attack being detected by an AI security system. Modern technology
style, clean interface, blue and purple lighting.
"""


print("\nGenerating image...")
print("Please wait...\n")


image_data = generate_image(prompt)


if image_data:
    with open("test_generated_image.png", "wb") as f:
        f.write(image_data)

    print("✅ Image generated successfully!")
    print("📁 Saved as: test_generated_image.png")

else:
    print("❌ Image generation failed.")
    print("No image data was returned.")