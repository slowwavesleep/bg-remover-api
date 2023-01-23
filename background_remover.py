from pathlib import Path
import io
import requests

import torch
from PIL import Image, UnidentifiedImageError
from torchvision import transforms
import numpy as np
from tqdm.auto import tqdm


class BgRemover:

    def __init__(
            self,
            model,
            preprocessor,
            device,
    ):
        self.model = model
        self.preprocessor = preprocessor
        self.device = device

    def mask_background(self, img) -> np.ndarray:
        input_tensor = self.preprocessor(img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            output = self.model(input_tensor)
        mask = output["out"][0].argmax(0).detach().cpu().numpy().astype(np.uint8)
        bin_mask = np.expand_dims(mask, 2)
        bin_mask = np.concatenate([bin_mask, bin_mask, bin_mask], axis=-1)
        masked = np.where(bin_mask == 0, 0, np.array(img))
        return masked

    def remove_background(self, img, save_path) -> None:
        masked = self.mask_background(img)
        Image.fromarray(masked).save(save_path)


def read_images(path_pattern: str):
    path = Path()
    paths = path.glob(path_pattern)
    images = []
    keys = []
    for path in paths:
        try:
            images.append(Image.open(path))
            keys.append(path)
        # skip broken images
        except UnidentifiedImageError:
            print(f"Skipping image at {path}")
    return keys, images


def img_from_url(url):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    return img


def default_init() -> BgRemover:
    device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")

    preprocessor = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    model = torch.hub.load("pytorch/vision:v0.6.0", "deeplabv3_resnet101", pretrained=True).to(device).eval()

    bg_remover = BgRemover(model, preprocessor, device)

    return bg_remover


def process_dir(in_dir: str, out_dir: str, remover: BgRemover) -> None:
    keys, images = read_images(in_dir + "/**/*.jpg")  # "./sample/**/*.jpg"
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    for k, img in tqdm(zip(keys, images), total=len(images)):
        new_path = out_dir / k.parts[1] / k.parts[2]
        new_path.parent.mkdir(exist_ok=True)
        remover.remove_background(img, new_path)






