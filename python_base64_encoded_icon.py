import base64
from PIL import Image
from io import BytesIO

# Base64-encoded icon data
base64_icon = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAAEklEQVR42mJ4AAIAAAoAAv/lG9cAAAAASUVORK5CYII="

# Decode base64 data
icon_data = base64.b64decode(base64_icon)

# Load image from decoded data
image = Image.open(BytesIO(icon_data))

# Show the image
image.show()
