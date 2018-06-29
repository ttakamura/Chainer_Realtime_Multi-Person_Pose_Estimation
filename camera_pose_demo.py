import sys
import cv2
import numpy as np
import argparse
import chainer
from pose_detector import PoseDetector, draw_person_pose
from entity import params

sys.path.append('puppet_api_client')

import swagger_client


def request_api(puppet_id, pose):
    api_instance = swagger_client.PuppetApi()
    api_response = api_instance.draw(puppet_id, pose, _preload_content=False)
    img = np.frombuffer(api_response.data, dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


def convert_to_moepose(pose_array):
    bone = {}
    for k, i in params['moecs_joint_indices'].items():
        if i < pose_array.shape[0]:
            x = pose_array[i, 0]
            y = pose_array[i, 1]
            v = pose_array[i, 2]
            bone[k] = {'x': x, 'y': y, 'v': v}
        else:
            bone[k] = {'x': 0, 'y': 0, 'v': 0}

    bone['neck']['y'] -= 20

    # Spine
    spine_x = (bone['L_waist']['x'] + bone['R_waist']['x'])/2
    spine_y = (bone['L_waist']['y'] + (bone['L_waist']['y'] + bone['neck']['y'])/2)/2
    bone['spine'] = {'x': spine_x, 'y': spine_y, 'v': 2}

    return {'bone': bone}


def fetch_transformed_img(puppet_id, pose_array):
    pose = convert_to_moepose(pose_array)
    print('Sending API request...')
    img = request_api(puppet_id, pose)
    print('done')
    return img


def resize_and_pad_image(img, size, padding_color=(255, 255, 255)):
    h, w = img.shape[:2]
    sh, sw = size

    # interpolation method
    if h > sh or w > sw:
        interp = cv2.INTER_AREA
    else:
        interp = cv2.INTER_CUBIC

    aspect = float(w)/h
    saspect = float(sw)/sh

    if (saspect > aspect) or ((saspect == 1) and (aspect <= 1)):  # new horizontal image
        new_h = sh
        new_w = np.round(new_h * aspect).astype(int)
        pad_horz = float(sw - new_w) / 2
        pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
        pad_top, pad_bot = 0, 0

    elif (saspect < aspect) or ((saspect == 1) and (aspect >= 1)):  # new vertical image
        new_w = sw
        new_h = np.round(float(new_w) / aspect).astype(int)
        pad_vert = float(sh - new_h) / 2
        pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        pad_left, pad_right = 0, 0

    # scale and pad
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
    scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padding_color)
    return scaled_img


chainer.using_config('enable_backprop', False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pose detector')
    parser.add_argument('--gpu', '-g', type=int, default=-1, help='GPU ID (negative value indicates CPU)')
    args = parser.parse_args()

    # load model
    pose_detector = PoseDetector("posenet", "models/coco_posenet.npz", device=args.gpu)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        # get video frame
        ret, img = cap.read()
        img = resize_and_pad_image(img, (512, 512))
        print(img.shape)

        if not ret:
            print("Failed to capture image")
            break

        person_pose_array, _ = pose_detector(img)

        if len(person_pose_array) > 0:
            puppet_id = "b2c08639-83f4-478a-9ad8-f240053cfae6"
            res_img = fetch_transformed_img(puppet_id, person_pose_array[0])
            res_img = cv2.addWeighted(res_img, 0.7, draw_person_pose(res_img, person_pose_array), 0.3, 0)

            debug_img = cv2.addWeighted(img, 0.6, draw_person_pose(img, person_pose_array), 0.4, 0)
            res_img = np.concatenate((debug_img, res_img), axis=1)

            cv2.imshow("result", res_img)
            cv2.waitKey(1)
