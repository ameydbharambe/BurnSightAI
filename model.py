from xml.parsers.expat import model

import torch
import torch.nn as nn
from torchvision import transforms, models
from torchvision.models import ResNet50_Weights
from PIL import Image

class BurnClassifier:
    def __init__(self, model_path="BurnClassifierFinal.pth", num_labels=3):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.load_model(model_path, num_labels)
        
        #Order of class names must match order of file labels in dataset folder
        self.class_names = [
            "First degree burn",
            "Third degree burn",
            "Second degree burn",
        ]

        #Standard image normalization for ResNet50 model
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    #Swap classification head with 3-class custom head
    def load_model(self, model_path, num_labels):
        model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
        model.fc = nn.Sequential(
               nn.Linear(2048, 128),
               nn.ReLU(inplace=True),
               nn.Linear(128, num_labels))
        model.to(self.device)
        model.load_state_dict(torch.load(model_path, map_location=self.device))
        model.eval()
        return model
    
    def predict(self, image_path):
        image = Image.open(image_path).convert('RGB')
        image = self.transform(image)
        image = image.unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(image)
            probabilities = torch.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)

        return self.class_names[predicted.item()],  confidence.item()

