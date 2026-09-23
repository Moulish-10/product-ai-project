from PIL import Image

def prepare_image(image : Image.Image) -> Image.Image:

    image = image.convert("RGB")

    return image
