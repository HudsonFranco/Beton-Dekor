import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configuration
cloudinary.config(
    cloud_name="dztlh19q1",
    api_key="536528844238579",
    api_secret="9kZvTKky6eerqz0hKejA0W4VoJg",
    secure=True
)

# Upload an image from your project (example: static/images/revestimento3D.jpeg)
upload_result = cloudinary.uploader.upload("static/images/revestimento3D.jpeg",
                                           public_id="revestimento3D",
                                           folder="produtos")
print("Upload URL:", upload_result["secure_url"])

# Optimize delivery by resizing and applying auto-format and auto-quality
optimize_url, _ = cloudinary_url("produtos/revestimento3D", fetch_format="auto", quality="auto")
print("Optimized URL:", optimize_url)

# Transform the image: auto-crop to square aspect_ratio
auto_crop_url, _ = cloudinary_url("produtos/revestimento3D", width=500, height=500, crop="auto", gravity="auto")
print("Auto-crop URL:", auto_crop_url)