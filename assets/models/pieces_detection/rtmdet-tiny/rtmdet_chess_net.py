# Inherit and overwrite part of the config based on this config
_base_ = 'mmdet::rtmdet/rtmdet_tiny_8xb32-300e_coco.py'

data_root = 'dataset/chess_net/' # dataset root

train_batch_size = 4
train_num_workers = 1

max_epochs = 200
stage2_num_epochs = 1
base_lr = 0.0005

metainfo = {
    'classes': ('pieces', 'bishop', 'black-bishop', 'black-king', 'black-knight',
                'black-pawn', 'black-queen', 'black-rook', 'white-bishop', 'white-king',
                'white-knight', 'white-pawn', 'white-queen', 'white-rook', 'chess-board')
}

num_classes = len(metainfo['classes'])

train_dataloader = dict(
    batch_size=train_batch_size,
    num_workers=train_num_workers,
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        data_prefix=dict(img='train/'),
        ann_file='train.json'))

val_dataloader = dict(
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        data_prefix=dict(img='val/'),
        ann_file='val.json'))

test_dataloader = val_dataloader

val_evaluator = dict(ann_file=data_root + 'val.json')
test_evaluator = val_evaluator

model = dict(bbox_head=dict(num_classes=num_classes))

# learning rate
param_scheduler = [
    dict(
        type='LinearLR',
        start_factor=1.0e-5,
        by_epoch=False,
        begin=0,
        end=10),
    dict(
        # use cosine lr from 10 to 20 epoch
        type='CosineAnnealingLR',
        eta_min=base_lr * 0.05,
        begin=max_epochs // 2,
        end=max_epochs,
        T_max=max_epochs // 2,
        by_epoch=True,
        convert_to_iter_based=True),
]

train_pipeline_stage2 = [
    dict(type='LoadImageFromFile', backend_args=None),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(
        type='RandomResize',
        scale=(640, 640),
        ratio_range=(0.1, 2.0),
        keep_ratio=True),
    dict(type='RandomCrop', crop_size=(640, 640)),
    dict(type='YOLOXHSVRandomAug'),
    #dict(type='RandomFlip', prob=0.5),
    dict(type='Pad', size=(640, 640), pad_val=dict(img=(114, 114, 114))),
    dict(type='PackDetInputs')
]

# optimizer
optim_wrapper = dict(
    _delete_=True,
    type='OptimWrapper',
    optimizer=dict(type='AdamW', lr=base_lr, weight_decay=0.05),
    paramwise_cfg=dict(
        norm_decay_mult=0, bias_decay_mult=0, bypass_duplicate=True))

default_hooks = dict(
    checkpoint=dict(
        interval=5,
        max_keep_ckpts=2,  # only keep latest 2 checkpoints
        save_best='coco/bbox_mAP'
    ),
    logger=dict(type='LoggerHook', interval=5))

custom_hooks = [
    dict(
        type='PipelineSwitchHook',
        switch_epoch=max_epochs - stage2_num_epochs,
        switch_pipeline=train_pipeline_stage2)
]

# load COCO pre-trained weight
#load_from = './assets/models/pieces_detection/rtmdet-tiny/rtmdet_tiny_8xb32-300e_coco_20220902_112414-78e30dcc.pth'
load_from = './work_dirs/simple_config/best_coco_bbox_mAP_epoch_19.pth'

train_cfg = dict(type='EpochBasedTrainLoop', max_epochs=max_epochs, val_interval=1)
visualizer = dict(vis_backends=[dict(type='LocalVisBackend'),dict(type='TensorboardVisBackend')])