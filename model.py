import torch
import torch.nn as nn

from PIL import Image

from torchvision import transforms

from transformers import ResNetForImageClassification

class BurnClassifier:
    def __init__(self):
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        #Class names in order of dataset folder labels
        self.class_names = [
            "First degree burn",
            "Third degree burn",
            "Second degree burn",
        ]
        self.outputs = len(self.class_names)
        
        #Apply required transformations to process images for ResNet50 model
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        self.model = self.load_model()
        
    def load_model(self):
        
        model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50")
        model.classifier = nn.Sequential(
        nn.Flatten(1),
        nn.Linear(2048, 128),
        nn.ReLU(inplace=True),
        nn.Linear(128, self.outputs)
        )
        
        state_dict = torch.load("BurnClassifierTransformer.pth", map_location=self.device)
        model.load_state_dict(state_dict)

        model.to(self.device)
        model.eval()

        return model
    
    
    def predict(self, image_path):
        image = Image.open(image_path).convert('RGB')
        image = self.transform(image)
        image = image.unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(pixel_values=image)
            probabilities = torch.softmax(outputs.logits, dim=1)
            confidence, predicted = torch.max(probabilities, 1)

        return self.class_names[predicted.item()],  confidence.item()
