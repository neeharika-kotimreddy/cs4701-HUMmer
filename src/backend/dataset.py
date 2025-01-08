from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image


class SpectogramDS(Dataset):

    def __init__(self, df):
        self.df = df

    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, index):
        img_path = self.df.loc[index, "path"]
        song_name = self.df.loc[index, "song"]
        img = Image.open(img_path)
        transform = transforms.Compose( [
            transforms.ToTensor(),
            ])
        img = transform(img)
        return img, song_name