"""
The evaluation entry point for CelebA-Spoof Challenge.

It will be the entrypoint for the evaluation docker once built.
Basically It downloads a list of videos and run the detector on each video.
Then the runtime output will be reported to the evaluation system.

The participants are expected to implement a deepfake detector class. The sample detector illustrates the interface.
Do not modify other part of the evaluation toolkit otherwise the evaluation will fail.

Author: Yuanjun Xiong, Zhengkui Guo, Yuanhan Zhang
Contact: zhangyuanhan@sensetime.com

CelebA-Spoof Challenge
"""
import time
import sys
import logging

import numpy as np
from eval_kit.client import upload_eval_output, get_image, get_job_name


logging.basicConfig(level=logging.INFO)

sys.path.append('model')
########################################################################################################
# Please change this line to include your own detector extending the eval_kit.detector.DeeperForensicsDetector base class.
from tsn_predict import TSNPredictor as DeeperForensicsDetector
########################################################################################################


def evaluate_runtime(detector_class, image_iter, job_name):
    """
    Please DO NOT modify this part of code or the eval_kit
    Modification of the evaluation toolkit could result in cancellation of your award.

    In this function we create the detector instance. And evaluate the wall time for performing DeeperForensicsDetector.
    """

    # initialize the detector
    logging.info("Initializing detector.")
    try:
        detector = detector_class()
    except:
        # send errors to the eval frontend
        raise
    logging.info("Detector initialized.")


    # run the images one-by-one and get runtime
    output_probs = {}
    output_times = {}
    eval_cnt = 0

    logging.info("Starting runtime evaluation")
    for image_id, image in image_iter:
        time_before = time.time()
        try:
            prob = detector.predict(image)
            assert isinstance(prob, float)
            output_probs[image_id] = prob
        except:
            # send errors to the eval frontend
            logging.error("Image id failed: {}".format(image_id))
            raise
        elapsed = time.time() - time_before
        output_times[image_id] = elapsed
        logging.info("video {} run time: {}".format(image_id, elapsed))

        eval_cnt += 1

        if eval_cnt % 100 == 0:
            logging.info("Finished {} image".format(eval_cnt))

    logging.info("all images finished, uploading evaluation outputs for evaluation.")
    # send evaluation output to the server
    upload_eval_output(output_probs, output_times, job_name)


if __name__ == '__main__':
    job_name = get_job_name()
    celebA_spoof_image_iter = get_image()
    evaluate_runtime(DeeperForensicsDetector, celebA_spoof_image_iter, job_name)


