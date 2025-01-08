import torch.nn.functional as F
from torch.nn import init
import torch.nn as nn
import torch

class Net (nn.Module):

    def __init__(self):
        super().__init__()
        conv_layers = []

        for in_channel, out_channel in [(3, 8), (8, 16), (16, 32), (32, 64)]:
            conv = nn.Conv2d(in_channel, out_channel, kernel_size=(5, 5), stride=(2, 2), padding=(2, 2))
            relu = nn.ReLU()
            bn = nn.BatchNorm2d(out_channel)
            init.kaiming_normal_(conv.weight, a=0.1)
            conv.bias.data.zero_()
            conv_layers += [conv, relu, bn]

        # Linear Classifier
        self.ap = nn.AdaptiveAvgPool2d(output_size=1)
        self.lin = nn.Linear(in_features=64, out_features=17)

        # Wrap the Convolutional Blocks
        self.conv = nn.Sequential(*conv_layers)
 

    def forward(self, x):
        # Run the convolutional blocks
        x = self.conv(x)

        # Adaptive pool and flatten for input to linear layer
        x = self.ap(x)
        x = x.view(x.shape[0], -1)
        
        # Linear layer
        x = self.lin(x)

        # Final output
        return x
