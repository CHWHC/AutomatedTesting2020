import os

import cv2

import detect_compo.ip_region_proposal as ip


def resize_height_by_longest_edge(img_path, resize_length=800):
    org = cv2.imread(img_path)
    height, width = org.shape[:2]
    if height > width:
        return resize_length
    else:
        return int(resize_length * (height / width))

def run_all(path):
    key_params = {'min-grad': 10, 'ffl-block': 5, 'min-ele-area': 50, 'merge-contained-ele': True,
                  'max-word-inline-gap': 4, 'max-line-gap': 4}
    for filename in os.listdir(path):
        print('process image: ' + filename)
        resized_height = resize_height_by_longest_edge(os.path.join(path, filename))
        ip.compo_detection(os.path.join(path, filename), 'data/output', key_params, resize_by_height=resized_height,
                           show=False)



def run_single(file_path):
    key_params = {'min-grad': 10, 'ffl-block': 5, 'min-ele-area': 50, 'merge-contained-ele': True,
                  'max-word-inline-gap': 4, 'max-line-gap': 4}
    resized_height = resize_height_by_longest_edge(file_path)
    ip.compo_detection(file_path, 'data/output', key_params, resize_by_height=resized_height,
                       show=True)


if __name__ == '__main__':
    '''
ele:min-grad: 梯度阈值生成二值映射      
        ele:ffl-block: fill-flood 阈值
        ele:min-ele-area: 所选元素的最小面积
        ele:merge-contained-ele: 如果为真，则合并其他元素中包含的元素
        text:max-word-inline-gap: 距离小于空格的单词被计算为一行
        text:max-line-gap:距离小于间隔的行被计算为一个段落
        Tips:
        1. Larger *min-grad* 生成细粒度的二进制映射，同时容易将元素过度分割成小块
        2. Smaller *min-ele-area* 留下微小的元素，容易产生噪噪点
        3. If not *merge-contained-ele*, 别的元素会被识别出来，但容易产生噪点
        4. The *max-word-inline-gap* and *max-line-gap* 是否应该取决于输入图像的大小和分辨率
        mobile: {'min-grad':4, 'ffl-block':5, 'min-ele-area':50, 'max-word-inline-gap':6, 'max-line-gap':1}
        web   : {'min-grad':3, 'ffl-block':5, 'min-ele-area':25, 'max-word-inline-gap':4, 'max-line-gap':4}
    '''
    run_single('data/ATMobile2020-1/2.jpg')

    run_all('data/ATMobile2020-1')
