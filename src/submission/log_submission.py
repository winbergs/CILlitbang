import argparser
import shutil
import os

from submission.mask_to_submission import masks_to_submission

'''
This file contains our logging mechanism. With the function provided we copy and save all data into
the log directory. This is used for experiments. With this we have all data and can replicate what
we did.
'''


def log_submission(submission_identifier, args):
    # Initializing submission path where submission will be logged
    submission_path = os.path.join('..', 'out', submission_identifier)
    if not os.path.exists(submission_path):
        os.makedirs(submission_path)
    print('Logging submission: ' + submission_path)

    # Copying model weights
    shutil.copy2(args.model_path, os.path.join(submission_path, args.model + '.h5'))

    # Copying results directories
    shutil.copytree(os.path.join(args.test_path, 'results', 'discrete'), os.path.join(submission_path, 'discrete'))
    shutil.copytree(os.path.join(args.test_path, 'results', 'continuous'), os.path.join(submission_path, 'continuous'))
    shutil.copytree(os.path.join(args.test_path, 'results', 'discrete_post'), os.path.join(submission_path, 'discrete_post'))
    shutil.copytree(os.path.join(args.test_path, 'results', 'continuous_post'), os.path.join(submission_path, 'continuous_post'))

    # Copying tensorboard log files
    if args.train_model:
        shutil.copytree(os.path.join('..', 'logs', 'fit', submission_identifier), os.path.join(submission_path, 'tensorboard'))

    # Saving argument config file
    argparser.write_config_file(args, path=os.path.join(submission_path, 'config.cfg'))

    # Masking result to kaggle submission format and saving file it as csv file
    result_path = os.path.join(submission_path, 'discrete')
    submission_filename = os.path.join(submission_path, 'submission.csv')
    image_filenames = []
    for file in os.listdir(result_path):
        image_filename = os.path.join(result_path, file)
        image_filenames.append(image_filename)
    masks_to_submission(submission_filename, *image_filenames, foreground_threshold=args.sub_thresh)

    # Masking postprocessed result to kaggle submission format and saving file it as csv file
    result_path = os.path.join(submission_path, 'discrete_post')
    submission_filename = os.path.join(submission_path, 'submission_post.csv')
    image_filenames = []
    for file in os.listdir(result_path):
        image_filename = os.path.join(result_path, file)
        image_filenames.append(image_filename)
    masks_to_submission(submission_filename, *image_filenames, foreground_threshold=args.sub_thresh)
