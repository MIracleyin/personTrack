# -*- coding: utf-8 -*-
# !@time: 19-4-27 下午9:42
# !@author: superMC @email: 18758266469@163.com
# !@fileName: people2features.py

import os
from fid.inference import detect_face, mobile_face_model, get_faceFeatures
import csv
from fid.mtcnn.detect import create_mtcnn_net, MtcnnDetector
import numpy as np
import cv2


def one_manImg(img_dir, csv_path, model_path="fid/InsightFace_Pytorch/facenet_checkpoints/model_ir_se50.pth"):
    pnet, rnet, onet = create_mtcnn_net(p_model_path="fid/mtcnn/mtcnn_checkpoints/pnet_epoch.pt",
                                        r_model_path="fid/mtcnn/mtcnn_checkpoints/rnet_epoch.pt",
                                        o_model_path="fid/mtcnn/mtcnn_checkpoints/onet_epoch.pt", use_cuda=True)
    mtcnn_detector = MtcnnDetector(pnet=pnet, rnet=rnet, onet=onet, min_face_size=24)
    mobileFace = mobile_face_model(model_path)
    img_paths = os.listdir(img_dir)
    if not os.path.exists(csv_path):
        print('创建数据库')
        with open(csv_path, 'w', encoding='UTF-8') as file_csv:
            writer = csv.writer(file_csv)
            header = ['Features%d' % x for x in range(512)]
            header.insert(0, 'Name')
            writer.writerow(header)

    with open(csv_path, 'r', encoding='UTF-8') as file_csv:
        reader = csv.reader(file_csv)
        names = [row[0] for row in reader][1:]
    with open(csv_path, 'a+', encoding='UTF-8') as file_csv:
        writer = csv.writer(file_csv)
        for img_path in img_paths:
            label = os.path.splitext(img_path)[0]
            if label in names:
                print('%s的数据已存在,跳过' % label)
            else:
                img_path = os.path.join(img_dir, img_path)
                image = cv2.imread(img_path)
                faces, _ = detect_face(mtcnn_detector, image)
                if len(faces) == 1:
                    print('正在输入:', label)
                    # cv2.imshow('demo', faces[0])
                    # cv2.waitKey(0)
                    features = get_faceFeatures(mobileFace, faces[0])[0]
                    content = np.append(label, features)
                    writer.writerow(content)

                else:
                    print('%s图片不符合要求' % img_path)


def no_detect_one_manImg(img_dir, csv_path,
                         model_path="fid/InsightFace_Pytorch/facenet_checkpoints/model_ir_se50.pth"):
    mobileFace = mobile_face_model(model_path)
    img_paths = os.listdir(img_dir)
    img_paths = [x for x in img_paths if x.endswith('.png') or x.endswith('.jpg')]
    if not os.path.exists(csv_path):
        print('创建数据库')
        with open(csv_path, 'w', encoding='UTF-8') as file_csv:
            writer = csv.writer(file_csv)
            header = ['Features%d' % x for x in range(512)]
            header.insert(0, 'Name')
            writer.writerow(header)
    with open(csv_path, 'r', encoding='UTF-8') as file_csv:
        reader = csv.reader(file_csv)
        names = [row[0] for row in reader][1:]

    with open(csv_path, 'a+', encoding='UTF-8') as file_csv:
        writer = csv.writer(file_csv)
        for img_path in img_paths:
            label = os.path.splitext(img_path)[0]
            if label in names:
                print('%s的数据已存在,跳过' % label)
            else:
                print('正在输入:', label)
                img_path = os.path.join(img_dir, img_path)
                face = cv2.imread(img_path)
                features = get_faceFeatures(mobileFace, face)[0]
                content = np.append(label, features)
                writer.writerow(content)


if __name__ == '__main__':
    one_manImg('data/person_with_name', 'data/one_man_img.csv')
    no_detect_one_manImg('data/face_with_name', 'data/one_man_img.csv')
