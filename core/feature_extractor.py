import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

class FeatureExtractor:
    def __init__(self):
        self.model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def extract(self, img_path):
        try:
            img = Image.open(img_path).convert("RGB")
            img = self.transform(img).unsqueeze(0)
            with torch.no_grad():
                return self.model(img).numpy()[0]
        except Exception as e:
            print(f"Failed to process image: {img_path} | {str(e)}")
            return None