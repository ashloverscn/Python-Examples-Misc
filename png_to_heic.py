from PIL import Image
import pillow_heif

# Register the plugin (required for old versions)
pillow_heif.register_heif_opener()

# Open PNG and save using Pillow's save
img = Image.open('./cache/output.png')
img.save('./cache/output.heif', format="HEIF", quality=90)

print("Saved PNG as HEIF via fallback method.")

# Open the PNG image
img = Image.open('./cache/output.png')

# Save as true .heic image
pillow_heif.write_heif(
    img,
    './cache/output.heic',
    quality=90,
    heif_version="HEIC"
)

print("✅ PNG → HEIC saved successfully.")
