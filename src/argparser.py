from configargparse import ArgumentParser
import argparse

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_parser():
    parser = ArgumentParser(description='Road Segmentation CILlitbang',
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add('-c', '--config', is_config_file=True, help='config file path')

    parser.add('--arg-log', type=str2bool, default=True,
               help='save arguments to config file')

    parser.add('--epochs', type=int, default=50,
               help='number of training epochs')
    parser.add('--steps', type=int, default=100,
               help='number of steps per epoch')
    parser.add('--val-steps', type=int, default=22,
               help='number of validation steps after each epoch')
    parser.add('--batch-size', type=int, default=4,
               help='batch size for training')
    parser.add('--seed', type=int, default=0,
               help='random seed for training (necessary for reproducibility)')

    parser.add('--predict-best', type=str2bool, default=True,
               help='predict with best model weights')
    parser.add('--train-model', type=str2bool, default=True,
               help='perform training on the model')

    parser.add('--comb-pred', type=str2bool, default=True,
               help='combine different rotated and flipped predictions into one')
    parser.add('--gather-mode', type=str, default='avg',
               help='take average of combined results or discrete voting with voting threshold')
    parser.add('--scale-mode', type=str, default='resize',
               help='resize test images or predict sub-images in sliding window way')

    parser.add('--train-path', type=str, default='../data/training/',
               help='path containing training images & groundtruth')
    parser.add('--val-path', type=str, default='../data/validation/',
               help='path containing validation images & groundtruth')
    parser.add('--test-path', type=str, default='../data/test/',
               help='path containing test images to predict')
    parser.add('--model-path', type=str, default='../tmp/model.h5',
               help='path where the current best model weights will be stored')

    parser.add('--sub-log', type=str2bool, default=True,
               help='save entire submission in out directory')
    parser.add('--sub-name', type=str, default='dilated 2 submission',
               help='descriptive name of submission for folder in out directory')
    parser.add('--sub-thresh', type=float, default=0.5,
               help='foreground submission threshold for mask to submission csv conversion')

    parser.add('--rotation-range', type=int, default=360,
               help='rotation range to use for augmentation dictionary')
    parser.add('--width-shift-range', type=float, default=0.05,
               help='range for width shift in augmentation dictionary')
    parser.add('--height-shift-range', type=float, default=0.05,
               help='range for height shift in augmentation dictionary')
    parser.add('--shear-range', type=float, default=0.05,
               help='shear range for augmentation dictionary')
    parser.add('--zoom-range', type=list, default=[0.95, 1.05],
               help='zoom range for augmentation dictionary')
    parser.add('--brightness-range', type=list, default=[1.0, 1.2],
               help='brightness range for augmentation dictionary')
    parser.add('--horizontal-flip', type=str2bool, default=True,
               help='lets ImageDataGenerator flip images horizontally')
    parser.add('--vertical-flip', type=str2bool, default=True,
               help='lets ImageDataGenerator flip images vertically')
    parser.add('--fill-mode', type=str, default='reflect',
               help='fill mode when shifting images')

    parser.add('--model', choices=['unet', 'unet_dilated1', 'unet_dilated2', 'unet_dilated3'], default='unet_dilated2',
               help='which model to use for training')
    parser.add('--adam-lr', type=float, default=1e-4,
               help='learning rate of adam to use during training')

    parser.add('--line-smoothing-mode', type=str, default='both', choices=['beforeHough', 'afterHough', 'both', 'None'],
               help='Apply line smoothin before(beforeHough, after (afterHough) or both(both) or not at all (None)')
    parser.add('--apply-hough', type=str2bool, default=True,
               help='Should Hough Transform postprocessing be applied')
    parser.add('--hough-discretize-mode', type=str, default='graphcut', choices=['discretize', 'graphcut'],
               help='Which discretization function should be applied during Hough transform')
    parser.add('--discretize-mode', type=str, default='graphcut', choices=['discretize', 'graphcut'],
               help='Which discretization function should be applied for the final submission')
    parser.add('--region-removal', type=bool, default=True,
               help='Should small regions be removed')

    return parser


def write_config_file(args, path='config.conf'):
    with open(path, 'w') as f:
        for k in sorted(args.__dict__):
            print(k.replace('_', '-'), '=', args.__dict__[k], file=f)

