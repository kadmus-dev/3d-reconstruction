import argparse
import torch
import cv2
import os
import numpy as np
import sys
import glob
import pathlib as pt

# a very filthy hack :)
sys.path.append('./lhpe/')

import demo
from modules.pose import Pose, track_poses
from modules.load_state import load_state
from modules.keypoints import extract_keypoints, group_keypoints
from models.with_mobilenet import PoseEstimationWithMobileNet

sys.path.append('./pifuhd/')
from apps.recon import reconWrapper


def get_rect(net, images, height_size):
    net = net.eval()

    stride = 8
    upsample_ratio = 4
    num_keypoints = Pose.num_kpts
    previous_poses = []
    delay = 33
    for image in images:
        rect_path = image.replace('.%s' % (image.split('.')[-1]), '_rect.txt')
        img = cv2.imread(image, cv2.IMREAD_COLOR)
        orig_img = img.copy()
        orig_img = img.copy()
        heatmaps, pafs, scale, pad = demo.infer_fast(
            net, img, height_size, stride, upsample_ratio, cpu=False)

        total_keypoints_num = 0
        all_keypoints_by_type = []
        for kpt_idx in range(num_keypoints):  # 19th for bg
            total_keypoints_num += extract_keypoints(
                heatmaps[:, :, kpt_idx], all_keypoints_by_type, total_keypoints_num)

        pose_entries, all_keypoints = group_keypoints(
            all_keypoints_by_type, pafs)
        for kpt_id in range(all_keypoints.shape[0]):
            all_keypoints[kpt_id, 0] = (
                all_keypoints[kpt_id, 0] * stride / upsample_ratio - pad[1]) / scale
            all_keypoints[kpt_id, 1] = (
                all_keypoints[kpt_id, 1] * stride / upsample_ratio - pad[0]) / scale
        current_poses = []

        rects = []
        for n in range(len(pose_entries)):
            if len(pose_entries[n]) == 0:
                continue
            pose_keypoints = np.ones((num_keypoints, 2), dtype=np.int32) * -1
            valid_keypoints = []
            for kpt_id in range(num_keypoints):
                if pose_entries[n][kpt_id] != -1.0:  # keypoint was found
                    pose_keypoints[kpt_id, 0] = int(
                        all_keypoints[int(pose_entries[n][kpt_id]), 0])
                    pose_keypoints[kpt_id, 1] = int(
                        all_keypoints[int(pose_entries[n][kpt_id]), 1])
                    valid_keypoints.append(
                        [pose_keypoints[kpt_id, 0], pose_keypoints[kpt_id, 1]])
            valid_keypoints = np.array(valid_keypoints)

            if pose_entries[n][10] != -1.0 or pose_entries[n][13] != -1.0:
                pmin = valid_keypoints.min(0)
                pmax = valid_keypoints.max(0)

                center = (0.5 * (pmax[:2] + pmin[:2])).astype(int)
                radius = int(0.65 * max(pmax[0]-pmin[0], pmax[1]-pmin[1]))
            elif pose_entries[n][10] == -1.0 and pose_entries[n][13] == -1.0 and pose_entries[n][8] != -1.0 and pose_entries[n][11] != -1.0:
                # if leg is missing, use pelvis to get cropping
                center = (
                    0.5 * (pose_keypoints[8] + pose_keypoints[11])).astype(int)
                radius = int(
                    1.45*np.sqrt(((center[None, :] - valid_keypoints)**2).sum(1)).max(0))
                center[1] += int(0.05*radius)
            else:
                center = np.array([img.shape[1]//2, img.shape[0]//2])
                radius = max(img.shape[1]//2, img.shape[0]//2)

            x1 = center[0] - radius
            y1 = center[1] - radius

            rects.append([x1, y1, 2*radius, 2*radius])

        np.savetxt(rect_path, np.array(rects), fmt='%d')


def main(args):
    img_ext = ['png', 'jpg', 'jpeg']
    image_dir = args.input_path
    # for file in next(pt.Path(image_dir).iterdir()):
    #    print(file)
    # file_name = sum([glob.glob(image_dir + '*.' + e) for e in img_ext], [])
    # print(f"{img_ext}\t{image_dir}\t{file_name}")
    image_path = str(next(pt.Path(image_dir).iterdir())) #file_name[0]

    print('getting rect')
    net = PoseEstimationWithMobileNet()
    checkpoint = torch.load(
        './lhpe/checkpoint_iter_370000.pth', map_location='cuda')
    load_state(net, checkpoint)

    get_rect(net.cuda(), [image_path], 512)
    print('got rect')

    # after i wrote this line there is nothing holy for me. i can finally kill god.
    print('running pifuhd')
    cmd = ['--dataroot', args.input_path, '--results_path', args.output_path, \
           '--loadSize', '1024', '--resolution', '256', '--load_netMR_checkpoint_path', \
           './pifuhd/checkpoints/pifuhd.pt', \
           '--start_id', '-1', '--end_id', '-1']
    reconWrapper(cmd, True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_path', type=str, default='./pifuhd/sample_images/')
    parser.add_argument('-o', '--output_path', type=str, default='./results')
    args = parser.parse_args()

    main(args)