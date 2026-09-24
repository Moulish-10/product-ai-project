from PIL import Image

def prepare_image(image : Image.Image) -> Image.Image:

    if image.mode in ("RGBA", "LA", "P"):
        image = image.convert("RGB")
        background = Image.new("RGB", image.size(255,255,255))
        background.paste(image, mask = image.getchannel("A"))
        image = background
    else:
        image = image.convert("RGB")

    return image
