环境搭建
==========
```
!pip install -U torch==1.5.1+cu101 torchvision==0.6.1+cu101 -f https://download.pytorch.org/whl/torch_stable.html

# install mmcv-full thus we could use CUDA operators
!pip install mmcv-full

# Install mmdetection
!rm -rf mmdetection
!git clone https://github.com/open-mmlab/mmdetection.git
%cd mmdetection

!pip install -e .

# install Pillow 7.0.0 back in order to avoid bug in colab
!pip install Pillow==7.0.0
```


下载预训练模型参数
================
```
!mkdir checkpoints
!wget -c https://open-mmlab.s3.ap-northeast-2.amazonaws.com/mmdetection/v2.0/手动点击model获得路径.pth \
      -O checkpoints/模型名称.pth

```

直接调用模型
```
from mmdet.apis import inference_detector, init_detector, show_result_pyplot
#对于模型，只需要所有的参数文件config,再用init_detector初始化即可，同时要给定下载好的checkpoints，

config = 'configs/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco.py' #所有的模型参数，需要选对 
# Setup a checkpoint file to load
checkpoint = 'checkpoints/模型名称.pth'
#1 initialize the detector
model = init_detector(config, checkpoint, device='cuda:0')

#2 Use the detector to do inference
img = 'demo/demo.jpg'
result = inference_detector(model, img)


#3 Let's plot the result
show_result_pyplot(model, img, result, score_thr=0.3)
```
