from torch.utils.data import random_split
import torch
from dataset import SpectogramDS
from data_formatting import get_data_df
from model import Net
from math import sqrt

def get_data():
    ds = SpectogramDS(get_data_df())

    num_items = len(ds)
    train_len = round(num_items * 0.70)
    validate_len = num_items - train_len
    train_ds, val_ds = random_split(ds, [train_len, validate_len])

    train_data = torch.utils.data.DataLoader(train_ds, batch_size=16, shuffle=True)
    val_data = torch.utils.data.DataLoader(val_ds, batch_size=16, shuffle=False)

    return train_data, val_data


def train(model, train_data, epochs=10, lr = 0.001):
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(),lr=lr)
    scheduler = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr=sqrt(lr),
                                                    steps_per_epoch=int(len(train_data)),
                                                    epochs=epochs,
                                                    anneal_strategy='linear')

    # Repeat for each epoch
    for epoch in range(epochs):
        running_loss = 0.0
        correct_prediction = 0
        total_prediction = 0

        for i, data in enumerate(train_data):
            inputs, labels = data


            # Zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            scheduler.step()

            # Keep stats for Loss and Accuracy
            running_loss += loss.item()

            _, prediction = torch.max(outputs,1)
            correct_prediction += (prediction == labels).sum().item()
            total_prediction += prediction.shape[0]

            minibatch = 5
            if i % minibatch == 0:   
               print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / minibatch))
        
        # Print stats at the end of the epoch
        num_batches = len(train_data)
        avg_loss = running_loss / num_batches
        acc = correct_prediction/total_prediction
        print(f'Epoch: {epoch}, Loss: {avg_loss:.2f}, Accuracy: {acc:.2f}')


def test(model, val_data):
    correct = 0
    total = 0
    model.eval()
    # since we're not training, we don't need to calculate the gradients for our outputs
    with torch.no_grad():
        for data in val_data:
            images, labels = data
            # calculate outputs by running images through the network
            outputs = model(images)
            # the class with the highest energy is what we choose as prediction
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f'Accuracy of the network on test images: {100 * correct // total} %')
    return 100 * correct // total


if __name__ == "__main__":
    train_data, val_data = get_data()
    # model = Net()

    # train(model, train_data, 20)
    # path = "../../models/full2.pth"
    # torch.save(model.state_dict(), path)
    # test(model, val_data)