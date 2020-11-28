TENSORFLOW版本
=================
速度大概0.05s，较慢

```
autoaugment.distort_image_with_autoaugment(pic,'v0')
autoaugment.distort_image_with_randaugment(pic,N,M)
```




PYTORCH版本
=============
```
!git clone https://github.com/DeepVoltaire/AutoAugment

from AutoAugment.autoaugment import ImageNetPolicy
image = Image.open(path)
policy = ImageNetPolicy()

transformed = policy(image)


from autoaugment import ImageNetPolicy
data = ImageFolder(rootdir, transform=transforms.Compose(
                        [transforms.RandomResizedCrop(224), 
                         transforms.RandomHorizontalFlip(), ImageNetPolicy(), 
                         transforms.ToTensor(), transforms.Normalize(...)]))
loader = DataLoader(data, ...)
```
速度大概0.02s，比tensorflow的快点
