# coding=utf-8
import cv2
import os
import ast
import time
import shutil
import subprocess
import traceback
# from logging import getLogger
from argparse import ArgumentParser


# logger = getLogger()
# ['EVENT_FLAG_ALTKEY', 'EVENT_FLAG_CTRLKEY', 'EVENT_FLAG_LBUTTON', 'EVENT_FLAG_MBUTTON', 'EVENT_FLAG_RBUTTON',
# 'EVENT_FLAG_SHIFTKEY', 'EVENT_LBUTTONDBLCLK', 'EVENT_LBUTTONDOWN', 'EVENT_LBUTTONUP', 'EVENT_MBUTTONDBLCLK',
# 'EVENT_MBUTTONDOWN', 'EVENT_MBUTTONUP', 'EVENT_MOUSEHWHEEL', 'EVENT_MOUSEMOVE', 'EVENT_MOUSEWHEEL',
# 'EVENT_RBUTTONDBLCLK', 'EVENT_RBUTTONDOWN', 'EVENT_RBUTTONUP']

# events = [i for i in dir(cv2) if 'EVENT' in i]
# img = np.zeros((512, 512, 3), np.uint8)


# mouse callback function
# def mouse_click_events(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDBLCLK:
#         cv2.circle(img, (x, y), 100, (255, 0, 0), -1)
def exe_cmd(cmd):
    s = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    s.wait()
    print(s)


def mkdir_if_not_exist(path):
    if not os.path.exists(os.path.join(path)):
        os.makedirs(os.path.join(path))


def get_files(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            L.append(os.path.join(root, file))      # os.path.join 获取完整路径
    return L


def get_img_files(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jepg"):
                L.append(os.path.join(root, file))      # os.path.join 获取完整路径
    return L


# 写数据 flag:'a+':追加 |'w+'
def write_data(file_name, data, flag):
    with open(file_name, flag) as f:
        f.write(data)


# 读数据 flag:'r'
def read_data(file_name, flag):
    with open(file_name, flag) as f:
        return f.read()


class SignLabel:
    def __init__(self, sign_type):
        self.car_points = []
        self.draw_image = None
        if sign_type == "things":
            self.class_list = ['厨师帽', '安全帽', '厨师服', '口罩', '电风扇', '电视机', '电冰箱', '洗衣机', '空调', '微波炉',
                               '炒锅', '砧板', '桌子', '椅子', '沙发']
        elif sign_type == "flag":
            self.class_list = ['五星红旗', '中国共产党党旗', '八一军旗', '美国国旗', '英国国旗',
                               '法国国旗', '日本国旗', '朝鲜国旗', '韩国国旗', '俄罗斯国旗',
                               '西班牙国旗', '奥运会会旗', '联合国旗帜', '欧盟旗帜', '菲律宾共和国国旗',
                               '印度国旗', '巴西国旗', '越南国旗', '老挝国旗', '柬埔寨国旗',
                               '缅甸国旗', '泰国国旗', '马来西亚国旗', '新加坡国旗', '阿富汗国旗',
                               '伊拉克国旗', '伊朗国旗', '叙利亚国旗', '约旦国旗', '黎巴嫩国旗',
                               '以色列国旗', '巴勒斯坦国旗', '沙特阿拉伯国旗', '瑞典国旗', '澳大利亚国旗',
                               '加拿大国旗', '白俄罗斯国旗', '北约旗帜', '东南亚国家联盟旗帜', '世贸组织会旗']
        return

    def mouse_click_events(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.draw_image, (x, y), 3, (0, 0, 255), -1)
            print('click: [%d, %d]' % (x, y))
            self.car_points.append((x, y))

            if len(self.car_points) % 2 == 0:
                cv2.rectangle(self.draw_image, self.car_points[len(self.car_points)-2], self.car_points[len(self.car_points)-1],
                              (0, 0, 255), 2)
                self.show_classes()

    # ============================================================================================================
    # def show_image(self, image_file):
    #     label_file = image_file.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt')
    #     print(image_file)
    #     print(label_file)
    #
    #     image = cv2.imread(image_file)
    #     h, w, c = image.shape
    #     print('(h, w, c): (%d, %d, %d)' % (h, w, c))
    #
    #     with open(label_file, 'r') as file:
    #         label_list = file.readlines()
    #
    #     for label in label_list:
    #         temp_list = label.rstrip().split(' ')
    #         x1 = float(temp_list[1]) * w - (float(temp_list[3]) * w / 2)
    #         y1 = float(temp_list[2]) * h - (float(temp_list[4]) * h / 2)
    #
    #         x2 = float(temp_list[1]) * w + (float(temp_list[3]) * w / 2)
    #         y2 = float(temp_list[2]) * h + (float(temp_list[4]) * h / 2)
    #
    #         if int(temp_list[0]) == 0:
    #             cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    #         elif int(temp_list[0]) == 1:
    #             cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
    #
    #     cv2.imshow('show_image', image)
    #     cv2.waitKey(0)
    #
    # def show_images(self, root_path):
    #     for root, dirs, files in os.walk(root_path):
    #         for file in files:
    #             if '.txt' not in file:
    #                 self.show_image(os.path.join(root, file))

    # ============================================================================================================
    def draw_rectangle(self, image, label_list, times=1):
        print('本张图所有标记信息：')
        for index, label in enumerate(label_list):
            print('index: %d 详细信息: %s' % (index + 1, label))
            a = 765 / len(self.class_list) * int(label["class"])
            if a <= 255:
                color = (a, 0, 0)
            elif a <= 510:
                color = (255, a - 255, 0)
            else:
                color = (255, 255, a - 510)
            cv2.rectangle(image, (int(label["points"][0]*times), int(label["points"][1]*times)),
                          (int(label["points"][2]*times), int(label["points"][3]*times)), color, 2)
        self.show_action()
        return image

    def write_label(self, label_file, label_list, w, h):
        write_data(label_file, "", "w+")        # 清空原来的数据

        for label in label_list:
            save_str = label["class"] + " "
            save_str += str((float(label["points"][0]) + float(label["points"][2])) / 2 / w) + " "
            save_str += str((float(label["points"][1]) + float(label["points"][3])) / 2 / h) + " "
            save_str += str((float(label["points"][2]) - float(label["points"][0])) / w) + " "
            save_str += str((float(label["points"][3]) - float(label["points"][1])) / h) + "\n"
            write_data(label_file, save_str, 'a+')

    def show_classes(self):
        output_str = ""
        for i, class_name in enumerate(self.class_list):
            if (i + 1) % 10 == 0:
                output_str += str(i) + ":" + class_name + '\n'
            else:
                output_str += str(i) + ":" + class_name + '\t'
        print('=================================================================')
        print('[Enter] 输入数字标记类别，按空格确认类别：（详细类别如下所示）（本次重新标记请按 r）：')
        print(output_str)

    def show_action(self):
        print('=================================================================')
        print('[Enter] 输入文件执行对应操作： s: 保存图片  q: 下一张图片  d: 删除图片')
        print('[Enter] 如果要删除该图片中的某个标记框，用： shift + 数字（如 shift + 1表示删除第0个框）')

    def sign_image(self, image_file, label_file):
        times = 1

        print(image_file)
        print(label_file)

        cv2.namedWindow('sign_image')
        cv2.setMouseCallback('sign_image', self.mouse_click_events)    # 鼠标事件绑定

        base_image = cv2.imread(image_file)
        h, w, c = base_image.shape
        image = base_image.copy()

        print('(h, w, c): (%d, %d, %d)' % (h, w, c))

        if os.path.exists(label_file):
            with open(label_file, 'r') as file:
                label_list_str = file.readlines()
        else:
            label_list_str = list()

        print(label_list_str)
        label_list = list()
        for label in label_list_str:
            temp_list = label.rstrip().split(' ')
            x1 = float(temp_list[1]) * w - (float(temp_list[3]) * w / 2)
            y1 = float(temp_list[2]) * h - (float(temp_list[4]) * h / 2)

            x2 = float(temp_list[1]) * w + (float(temp_list[3]) * w / 2)
            y2 = float(temp_list[2]) * h + (float(temp_list[4]) * h / 2)

            label_list.append(dict())
            label_list[-1]["class"] = temp_list[0]
            label_list[-1]["points"] = (int(x1), int(y1), int(x2), int(y2))

        self.draw_image = self.draw_rectangle(image.copy(), label_list, times)

        class_num = 0

        while True:
            try:
                cv2.imshow('sign_image', self.draw_image)

                # 保存车牌标记框
                k = cv2.waitKey(1) & 0xFF
                if k == ord('0') or k == ord('1') or k == ord('2') or k == ord('3') or k == ord('4') or \
                   k == ord('5') or k == ord('6') or k == ord('7') or k == ord('8') or k == ord('9'):
                    class_num = class_num * 10 + (k - 48)
                    if class_num < len(self.class_list):
                        print('标记类别: %d, %s ?' % (class_num, self.class_list[class_num]))
                    else:
                        print('标记数值 %d 大于最大类别ID，请重新标记' % class_num)
                        class_num = 0

                if k == ord(' '):
                    print('=================================================================')
                    if len(self.car_points) == 2:
                        print('[append] 本次标记信息 %d: %s ...' % (class_num, self.class_list[class_num]))
                        label_list.append(dict())
                        label_list[-1]["class"] = str(class_num)
                        label_list[-1]["points"] = (int(self.car_points[0][0]/times), int(self.car_points[0][1]/times),
                                                    int(self.car_points[1][0]/times), int(self.car_points[1][1]/times))
                        self.car_points = []
                        self.draw_image = self.draw_rectangle(image.copy(), label_list, times)
                        class_num = 0
                    else:
                        print('[append] fail: %s' % self.car_points)
                # if k == ord('1'):
                #     print('=================================================================')
                #     print('[append] class 0: car plate ...')
                #     if len(self.car_points) == 2:
                #         label_list.append(dict())
                #         label_list[-1]["class"] = '0'
                #         label_list[-1]["points"] = (self.car_points[0][0], self.car_points[0][1],
                #                                     self.car_points[1][0], self.car_points[1][1])
                #         self.car_points = []
                #         self.draw_image = self.draw_rectangle(image.copy(), label_list)
                #         self.show_action()
                #     else:
                #         print('[append] fail: %s' % self.car_points)
                # # 保存车辆标记框
                # if k == ord('2'):
                #     print('=================================================================')
                #     print('[append] class 1: car ...')
                #     if len(self.car_points) == 2:
                #         label_list.append(dict())
                #         label_list[-1]["class"] = '1'
                #         label_list[-1]["points"] = (self.car_points[0][0], self.car_points[0][1],
                #                                     self.car_points[1][0], self.car_points[1][1])
                #         self.car_points = []
                #         self.draw_image = self.draw_rectangle(image.copy(), label_list, times)
                #         self.show_action()
                #     else:
                #         print('[append] fail: %s' % self.car_points)

                if k == ord('c'):
                    print('=================================================================')
                    print('改变图片尺寸 ...')
                    if times == 2:
                        times = 0.5
                    elif times == 1:
                        times = 2
                    else:
                        times = 1
                    image = cv2.resize(base_image, (int(base_image.shape[1]*times), int(base_image.shape[0]*times)))
                    print(times, image.shape)

                    self.car_points = []
                    self.draw_image = self.draw_rectangle(image.copy(), label_list, times)
                    cv2.imshow('sign_image', self.draw_image)

                # 重新加载图片
                if k == ord('r'):
                    print('=================================================================')
                    print('resign ...')
                    self.car_points = []
                    self.draw_image = self.draw_rectangle(image.copy(), label_list, times)

                # 保存，显示下一张
                if k == ord('s'):
                    print('=================================================================')
                    print('[save] ... \n')
                    self.write_label(label_file, label_list, w, h)
                    self.car_points = []
                    break
                # 退出，不保存，显示下一张
                if k == ord('q'):
                    print('=================================================================')
                    print('[next] ... \n')
                    self.car_points = []
                    break
                if k == ord('d'):
                    print('=================================================================')
                    print('[delete] image and label ... \n')
                    self.car_points = []
                    if os.path.exists(image_file):
                        os.remove(image_file)
                    if os.path.exists(label_file):
                        os.remove(label_file)
                    break

                # 删除标记框
                if k == ord('!'):
                    print('=================================================================')
                    object = label_list.pop(0)
                    print('[delete] ...index: 1; label: %s' % object)
                    self.draw_image = self.draw_rectangle(image.copy(), label_list, times)
                if k == ord('@'):
                    print('=================================================================')
                    object = label_list.pop(1)
                    print('[delete] ...index: 2; label: %s' % object)
                    self.draw_image = self.draw_rectangle(image.copy(), label_list, times)
                if k == ord('#'):
                    print('=================================================================')
                    object = label_list.pop(2)
                    print('[delete] ...index: 3; label: %s' % object)
                    self.draw_image = self.draw_rectangle(image.copy(), label_list, times)
                if k == ord('$'):
                    print('=================================================================')
                    object = label_list.pop(3)
                    print('[delete] ...index: 4; label: %s' % object)
                    self.draw_image = self.draw_rectangle(image.copy(), label_list, times)
                if k == ord('%'):
                    print('=================================================================')
                    object = label_list.pop(4)
                    print('[delete] ...index: 5; label: %s' % object)
                    self.draw_image = self.draw_rectangle(image.copy(), label_list, times)
                if k == ord('^'):
                    print('=================================================================')
                    object = label_list.pop(5)
                    print('[delete] ...index: 6; label: %s' % object)
                    self.draw_image = self.draw_rectangle(image.copy(), label_list, times)
                if k == ord('&'):
                    print('=================================================================')
                    object = label_list.pop(6)
                    print('[delete] ...index: 7; label: %s' % object)
                    self.draw_image = self.draw_rectangle(image.copy(), label_list, times)

            except Exception:
                msg = traceback.format_exc()
                print(msg)

        return

    def sign_images(self, root_path, process_all=True):
        print('process_all: %s' % process_all)

        for root, dirs, files in os.walk(root_path):
            for file in files:
                if '.txt' not in file:
                    process_flag = True

                    # 只处理未处理过的
                    label_name = file.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt')
                    if os.path.exists(os.path.join(root, label_name)) \
                            and process_all is False:
                        process_flag = False

                    if process_flag is True:
                        self.sign_image(os.path.join(root, file), os.path.join(root, label_name))


def parse_argvs():
    parser = ArgumentParser(description='sign label')
    parser.add_argument("--sign_type", dest="sign_type", type=str, default="things",
                        choices=["things", "flag", "ocr", "face"])
    parser.add_argument("--root_path", dest="root_path", type=str, default="../Data/AI比赛/特定物品识别/images_100/")
    parser.add_argument("--process_all", dest="process_all", type=ast.literal_eval, default=False, choices=[True, False])
    args = parser.parse_args()
    print(args)
    # logger.warning(args)
    return args


if __name__ == '__main__':
    args = parse_argvs()
    # show_image("../Data/yolo/yolo_data_new/car_detect_train/daozha_1/480466_闽DF3N37.jpg")
    # show_images(root_path="../Data/yolo/yolo_data_new_1/car_detect_train/")

    sign_label = SignLabel(args.sign_type)
    sign_label.sign_images(root_path=args.root_path, process_all=args.process_all)
