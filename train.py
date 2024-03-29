import argparse

import torch
import numpy as np
from torch import nn
from torch import optim
import torch.nn.functional as F
from torchvision import datasets, transforms, models

from util_functions import load_data
from functions import build_classifier, validation, train_model, test_model, save_model, load_checkpoint

parser = argparse.ArgumentParser(description='Train neural network.')


parser.add_argument('data_directory', action = 'store',
                    help = 'Enter path to training data.',default="../ImageClassifier/flowers/train")

parser.add_argument('--arch', action='store',
                    dest = 'pretrained_model', choices=['vgg11', 'vgg13', 'vgg16', 'vgg19', 'densenet121', 'densenet161'], default = 'vgg13',
                    help= 'Enter pretrained model to use; this classifier can currently work with\
                           VGG and Densenet architectures. The default is VGG-13.')

parser.add_argument('--save_dir', action = 'store',
                    dest = 'save_directory', default = 'checkpoint.pth',
                    help = 'Enter location to save checkpoint in.')

parser.add_argument('--learning_rate', action = 'store',
                    dest = 'lr', type=float, default = 0.01,
                    help = 'Enter learning rate for training the model, default is 0.01.')

parser.add_argument('--dropout', action = 'store',
                    dest='drpt', type=float, default = 0.05,
                    help = 'Enter dropout for training the model, default is 0.05.')

parser.add_argument('--hidden_units', action = 'store',
                    dest = 'units', type=int, default = 512,
                    help = 'Enter number of hidden units in classifier, default is 512.')

parser.add_argument('--epochs', action = 'store',
                    dest = 'num_epochs', type = int, default = 20,
                    help = 'Enter number of epochs to use during training, default is 20')

parser.add_argument('--gpu', action = "store_true", default = False,
                    help = 'Turn GPU mode on or off, default is off.')

results = parser.parse_args()

data_dir = results.data_directory
save_dir = results.save_directory
learning_rate = results.lr
dropout = results.drpt
hidden_units = results.units
epochs = results.num_epochs
gpu_mode = results.gpu

# Load and preprocess data 
trainloader, testloader, validloader, train_data, test_data, valid_data = load_data(data_dir)

# Load pretrained model
pre_tr_model = results.pretrained_model
model = getattr(models,pre_tr_model)(pretrained=True)

# Build and attach new classifier
if arch == "vgg11" or arch == "vgg13" or arch == "vgg16" or arch == "vgg19":
    input_units = model.classifier[0].in_features
elif arch == "densenet121" or arch == "densenet161":
    input_units = model.classifier.in_features

build_classifier(model, input_units, hidden_units, dropout)

# Recommended to use NLLLoss when using Softmax
criterion = nn.NLLLoss()
# Using Adam optimizer which makes use of momentum to avoid local minima
optimizer = optim.Adam(model.classifier.parameters(), learning_rate)

# Train model
model, optimizer = train_model(model, epochs,trainloader, validloader, criterion, optimizer, gpu_mode)

# Test model
test_model(model, testloader, gpu_mode)
# Save model
save_model(model, train_data, optimizer, save_dir, epochs)