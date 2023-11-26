# This script computes optical flow between two frames and saves it as an image.
#
# Adapted from the following example that runs on a video:
#   https://github.com/spmallick/learnopencv/blob/master/Optical-Flow-Estimation-using-Deep-Learning-RAFT/inference.py

import os
import sys
import datetime

sys.path.append("RAFT/core")

from argparse import ArgumentParser
from collections import OrderedDict

import cv2
import numpy as np
import torch

from raft import RAFT
from utils import flow_viz


def frame_preprocess(frame, device):
    frame = torch.from_numpy(frame).permute(2, 0, 1).float()
    frame = frame.unsqueeze(0)
    frame = frame.to(device)
    return frame


def vizualize_flow(img, flo, counter):
    # permute the channels and change device is necessary
    img = img[0].permute(1, 2, 0).cpu().numpy()
    flo = flo[0].detach().permute(1, 2, 0).cpu().numpy()

    # map flow to rgb image
    flo = flow_viz.flow_to_image(flo)
    flo = cv2.cvtColor(flo, cv2.COLOR_RGB2BGR)

    # concatenate and save
    img_flo = np.concatenate([img, flo], axis=0)
    if not os.path.exists("/data"):
        os.makedirs("/data")
    filename = f"/data/output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    return cv2.imwrite(filename, img_flo)


def get_cpu_model(model):
    new_model = OrderedDict()
    # get all layer's names from model
    for name in model:
        # create new name and update new model
        new_name = name[7:]
        new_model[new_name] = model[name]
    return new_model


def inference(args):
    # get the RAFT model
    model = RAFT(args)

    # load pretrained weights
    pretrained_weights = torch.load(args.model, map_location=torch.device("cpu"))

    if torch.cuda.is_available():
        device = "cuda"
        # parallel between available GPUs
        model = torch.nn.DataParallel(model)
        # load the pretrained weights into model
        model.load_state_dict(pretrained_weights)
        model.to(device)
    else:
        device = "cpu"
        # change key names for CPU runtime
        pretrained_weights = get_cpu_model(pretrained_weights)
        # load the pretrained weights into model
        model.load_state_dict(pretrained_weights)

    # change model's mode to evaluation
    model.eval()

    # load and resize the frames
    frame_1 = cv2.imread("/data/frame_1.png")
    frame_2 = cv2.imread("/data/frame_2.png")

    if not frame_1:
        print("Error loading from /data/...")
        print("Loading from from /default_data/...")
        frame_1 = cv2.imread("/default_data/frame_1.png")
        frame_2 = cv2.imread("/default_data/frame_2.png")

    # resize for raft
    frame_1 = cv2.resize(frame_1, (640, 360))
    frame_2 = cv2.resize(frame_2, (640, 360))

    # frame preprocessing
    frame_1 = frame_preprocess(frame_1, device)
    frame_2 = frame_preprocess(frame_2, device)

    # perform inference
    flow_low, flow_up = model(frame_1, frame_2, iters=args.iters, test_mode=True)
    vizualize_flow(frame_1, flow_up, counter=0)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--model", help="restore checkpoint")
    parser.add_argument("--iters", type=int, default=12)
    parser.add_argument("--video", type=str, default="./videos/car.mp4")
    parser.add_argument("--save", action="store_true", help="save demo frames")
    parser.add_argument("--small", action="store_true", help="use small model")
    parser.add_argument(
        "--mixed_precision", action="store_true", help="use mixed precision"
    )

    args = parser.parse_args(["--model=models/raft-sintel.pth"])
    inference(args)
