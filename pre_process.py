# encoding:utf-8
import os
import shutil
import random
# from logging import getLogger
from argparse import ArgumentParser


# logger = getLogger()


def mkdir_if_not_exist(path):
    if not os.path.exists(os.path.join(path)):
        os.makedirs(os.path.join(path))


# 写数据 flag:'a+':追加 |'w+'
def write_data(file_name, data, flag):
    with open(file_name, flag) as f:
        f.write(data)


def image_to_text(file):
    return file.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt').replace('.bmp', '.txt')


def is_image(file_path):
    if '.jpg' in file_path or '.jpeg' in file_path or '.png' in file_path or '.bmp' in file_path:
        return True
    else:
        return False


def assert_label(file_path):
    if '.txt' in file_path:
        with open(file_path, 'r') as file:
            label_list_str = file.readlines()

        for label in label_list_str:
            temp_list = label.rstrip().split(' ')
            if float(temp_list[1]) < 0 or float(temp_list[1]) > 1:
                return False
            if float(temp_list[2]) < 0 or float(temp_list[2]) > 1:
                return False
            if float(temp_list[3]) < 0 or float(temp_list[3]) > 1:
                return False
            if float(temp_list[4]) < 0 or float(temp_list[4]) > 1:
                return False
        return True
    return False


# ============================================================================================================
# 分为train和test文件
def data_pre_process_1(root_path, output_path, count):
    mkdir_if_not_exist(output_path)

    mkdir_if_not_exist(output_path)
    mkdir_if_not_exist(os.path.join(output_path, 'train'))
    mkdir_if_not_exist(os.path.join(output_path, 'test'))

    for root, dirs, files in os.walk(root_path):
        random.shuffle(files)

        i = 0
        for file in files:
            if is_image(file):
                dir_path = root.split('/')[-1]
                mkdir_if_not_exist(os.path.join(output_path, 'train', dir_path))
                mkdir_if_not_exist(os.path.join(output_path, 'test', dir_path))

                file_path = os.path.join(root, file)
                # print(file_path)
                if i < count:
                    test_path = os.path.join(output_path, 'test', dir_path)
                    shutil.copy(file_path, test_path)
                    # shutil.copy(file_path, os.path.join(output_path, 'test', dir_path, file))

                    label_file = file_path.replace(file_path.split('.')[-1], 'txt')
                    if os.path.exists(label_file):
                        shutil.copy(label_file, test_path)

                else:
                    train_path = os.path.join(output_path, 'train', dir_path)
                    shutil.copy(file_path, train_path)
                    # shutil.copy(file_path, os.path.join(output_path, 'train', dir_path, file))

                    label_file = file_path.replace(file_path.split('.')[-1], 'txt')
                    if os.path.exists(label_file):
                        shutil.copy(label_file, train_path)
                i += 1
    return


def update_image_path(root_path, label_file):
    write_data(os.path.join(root_path, label_file), "", "w+")

    total_dir = list()
    for root, dirs, files in os.walk(root_path):
        for dir in dirs:
            total_dir.append(dir)

    for dir in total_dir:
        print(dir)
        for root, dirs, files in os.walk(os.path.join(root_path, dir)):
            for file in files:
                if is_image(file):
                    if assert_label(os.path.join(root, image_to_text(file))):
                        write_data(os.path.join(root_path, label_file), dir + os.sep + file + '\n', "a+")
                    else:
                        print("[update_image_path] txt error: ", os.path.join(root, image_to_text(file)))


# 每个类别里提取n张图片放到一个文件夹里
def data_pre_process_2(root_path, output_path, start_count, end_count):
    mkdir_if_not_exist(output_path)

    mkdir_if_not_exist(output_path)

    for root, dirs, files in os.walk(root_path):
        # random.shuffle(files)

        dir = root.split("/")[-1]

        i = 0
        for file in files:
            if is_image(file):
                file_path = os.path.join(root, file)
                file_dir = os.path.dirname(file_path)
                mkdir_if_not_exist(file_dir)

                # print('data_pre_process_3', file_path)
                output_path_1 = os.path.join(output_path, dir)
                mkdir_if_not_exist(output_path_1)

                if start_count <= i < end_count:
                    shutil.copy(file_path, os.path.join(output_path_1, file))
                    label_file = file_path.replace(file_path.split('.')[-1], 'txt')
                    if os.path.exists(label_file):
                        print(label_file)
                        shutil.copy(label_file, output_path_1)

                i += 1
    return


# 每个类别里提取n张图片放到一个文件夹里
def data_pre_process_4(root_path, output_path, count):
    mkdir_if_not_exist(output_path)

    mkdir_if_not_exist(output_path)
    mkdir_if_not_exist(os.path.join(output_path))

    for root, dirs, files in os.walk(root_path):
        random.shuffle(files)

        for i, file in enumerate(files):
            file_path = os.path.join(root, file)
            print(file_path)
            if i < count:
                shutil.move(file_path, os.path.join(output_path, file))
    return


def parse_argvs():
    parser = ArgumentParser(description='pre process')
    parser.add_argument("--func", dest="func", type=int, default=0)
    parser.add_argument("--root_path", dest="root_path", type=str, default="../Data/AI比赛/特定物品识别/images/")
    parser.add_argument("--output_path", dest="output_path", type=str, default="../Data/AI比赛/特定物品识别/images_100/")
    parser.add_argument("--count", dest="count", type=int, default=20)
    parser.add_argument("--start_count", dest="start_count", type=int, default=0)
    parser.add_argument("--end_count", dest="end_count", type=int, default=100)
    args = parser.parse_args()
    print(args)
    # logger.warning(args)
    return args


if __name__ == '__main__':
    args = parse_argvs()

    # data_pre_process('../../Data/car_classifier', '../../Data/car_classifier_new')
    # data_pre_process_1('../../Data/car_classifier_new/', '../../Data/car_classifier_min_50/', 50)

    if args.func == 1:
        # 分为train和test文件
        data_pre_process_1(args.root_path, args.output_path, args.count)
        update_image_path(os.path.join(args.output_path, 'train'), 'image_path.txt')
        update_image_path(os.path.join(args.output_path, 'test'), 'image_path.txt')
    elif args.func == 2:
        # 每个类别里提取n张图片放到一个文件夹里
        data_pre_process_2(args.root_path, args.output_path, args.start_count, args.end_count)
    elif args.func == 3:
        # 生成image_path.txt
        update_image_path(args.root_path, 'image_path.txt')
    else:
        print('do nothing ... --func=1 or 2')
    # data_pre_process_4('../../Data/head_tail_classifier/train/head/', '../../Data/head_tail_classifier/test/head/', 700)
    # data_pre_process_4('../../Data/head_tail_classifier/train/tail/', '../../Data/head_tail_classifier/test/tail/', 700)

    # 拆分车牌头的图片
    # data_pre_process('../../Data/car_head_classifier/head', '../../Data/head_classifier')
    # data_pre_process_1('../../Data/car_classifier/head_classifier/', '../../Data/car_classifier/head_classifier_min_1/', 1)
    # data_pre_process_1('../../Data/car_classifier/head_classifier/', '../../Data/car_classifier/head_classifier_min_20/', 20)
    # data_pre_process_1('../../Data/car_classifier/head_classifier/', '../../Data/car_classifier/head_classifier_min_40/', 40)
    # data_pre_process_2('../../Data/car_classifier/clean_car/car_data_1/', '../../Data/car_classifier/classifier_train_best/', 100)

    # data_pre_process('../../Data/car_head_classifier/tail', '../../Data/tail_classifier')

