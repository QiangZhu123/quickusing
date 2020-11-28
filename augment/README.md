!git clone https://github.com/DeepVoltaire/AutoAugment

from AutoAugment.autoaugment import ImageNetPolicy
image = Image.open(path)
policy = ImageNetPolicy()

transformed = policy(image)
