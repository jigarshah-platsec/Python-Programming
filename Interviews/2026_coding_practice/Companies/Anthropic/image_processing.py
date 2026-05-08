import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# Create dummy images for the example
def create_dummy_images():
    if not os.path.exists('thumbnails'):
        os.makedirs('thumbnails')
    for i in range(5):
        img = Image.new('RGB', (1000, 1000), color=(73, 109, 137))
        img.save(f'image_{i}.jpg')
    print("Dummy images created.")

# Task function: Resize an image
def resize_image(image_path):
    size = (128, 128)
    with Image.open(image_path) as img:
        img.thumbnail(size)
        # Save to a new folder
        filename = os.path.basename(image_path)
        img.save(f'thumbnails/{filename}')
        return f"{filename} resized"

if __name__ == '__main__':
    create_dummy_images()
    image_files = [f'image_{i}.jpg' for i in range(5)]

    # Use ThreadPoolExecutor to run tasks in parallel
    print("\nStarting resizing...")
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Map the function to the image files
        results = executor.map(resize_image, image_files)
    
    # Print results as they complete
    for result in results:
        print(result)
    print("All images processed.")
