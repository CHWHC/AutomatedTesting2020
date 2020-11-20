import copy
import json
import os
import numpy as np
import re

from component import component

error_num = 0
total_num = 0
right_num = 0
uncertain_num = 0
zero = 0
uncertain_num_collect = {}
zero_collect = {}
error_collect = {}
final_collect = {}


def read_data():
    files = os.listdir('./ATMobile2020-1')
    json_files = {}
    for file in files:
        if not file.endswith('.json'):
            continue
        data = json.load(open(os.path.join('ATMobile2020-1', file), 'r', encoding='utf-8'))
        json_files[file.replace('.json', '')] = data
    return json_files


def dfs(root: component, data):
    if 'children' not in data:
        return
    # print(f'data pointer: {data["pointer"]}')
    global uncertain_num
    global error_num

    for child in data['children']:

        if child is None:
            continue
        #        print(f'class: {child["class"]}')
        #        print(f'pointer: {child["pointer"]}')
        t = r'[a-zA-Z0-9]*\.[a-zA-Z0-9]*'
        if ((re.match(t, child["class"]) == None) == True):
            uncertain_num += 1
            uncertain_num_collect[child["pointer"]] = child["class"]
            # print(uncertain_num_collect)
            # print("miao")
        assert child['class'] is not None
        assert 'bounds' in child
        assert 'class' in child
        root_dis(child)
        node = component(child['bounds'], child['class'], child['pointer'], root)
        root.children.append(node)
        dfs(node, child)
    de_children = []
    for c in root.children:
        if c not in de_children:
            de_children.append(c)
    root.children = de_children


def de_data(data):  # 解析数据
    root = data['activity']['root']
    root_dis(root)
    root_node = component(root['bounds'], root['class'], root['pointer'], None)
    dfs(root_node, root)
    # json.dump(component, open('tmp.json', 'w', encoding='utf-8'))
    return root_node


def root_dis(root):
    global error_num  # 冗余
    global total_num
    global right_num
    global uncertain_num  # class不存在
    global zero  # bounds is zero
    array_zero = np.array([0, 0, 0, 0])
    # 以下是判断是否是[0,0,0,0]
    if ('parent' in root):
        total_num += 1
        array_a = np.array(root['bounds'])
        if ((array_a == array_zero).all() == False):
            right_num += 1
        else:
            zero += 1
            zero_collect[root['pointer']] = root["class"]
            # print(zero_collect)
    else:  # 不是root
        total_num += 1
        array_a = np.array(root['bounds'])
        if ((array_a == array_zero).all() == False):
            right_num += 1
        else:
            zero += 1
            zero_collect[root['pointer']] = root["class"]
            # print(root['bounds'])
            # print(zero_collect)

        # 看是不是为负 为负删除
        left_abscissa = root['bounds'][0]
        left_ordinate = root['bounds'][1]
        right_abscissa = root['bounds'][2]
        right_ordinate = root['bounds'][3]
        if left_abscissa < 0 or right_ordinate < 0 or left_ordinate < 0 or right_abscissa < 0:
            error_num += 1
            error_collect[root['pointer']] = root["class"]
        elif (right_abscissa < left_abscissa or right_ordinate < left_ordinate):
            error_num += 1
            error_collect[root['pointer']] = root["class"]


def judgeme(root):
    global uncertain_num_collect
    global error_collect
    global zero_collect
    global uncertain_num
    global error_num
    global final_collect
    if root.pointer in uncertain_num_collect or root.pointer in error_collect or root.pointer in zero_collect:
        # print(root.pointer)
        print(uncertain_num_collect)
        print(error_collect)
        print(zero_collect)

    else:
        final_collect[root.component_class] = root.bounds
    for child in root.children:
        if child is None:
            continue
        judgeme(child)
def clean():
    global uncertain_num_collect
    global error_collect
    global zero_collect
    global uncertain_num
    global error_num
    global final_collect
    global zero
    final_collect.clear()
    uncertain_num_collect.clear()
    zero_collect.clear()
    error_collect.clear()
    zero = 0
    uncertain_num = 0
    error_num=0








datas = read_data()
root_nodes = []
num = 0
f = open("result.json", 'w', encoding='utf-8')
final_collects = {}
for id in datas:
    print(id)
    #f.write(str(id) + ".json")
    root_nodes.append(de_data(datas[id]))
    judgeme(root_nodes[num])
    print(final_collect)
    final_collects[id] = copy.deepcopy(final_collect)
    clean()
json.dump(final_collects, f, ensure_ascii=False)

# for root_node in root_nodes:
'''
 global uncertain_num
    global error_num
    left1=[]
    left2=[]
    right1=[]
    right2=[]
    for child in data['children']:
        co=child['bounds']
        if(len(left1)==0):
            left1.append(co[0])
            left2.append(co[1])
            right1.append(co[2])
            right2.append(co[3])
        else:
            for i in range(0,len(left1)):
                if not (left1[i] > co[0] and left2[i] > co[1] and right1[i] < co[2] and right2[i] < co[3]):
                    if (left1[i]<=co[0] and right1[i]>=co[0]) or (left1[i]<=co[2] and right1[i]>=co[2]):
                        if(left2[i]<=co[1] and left2[i]>=co[1]) or (left2[i]<=co[3] and left2[i]<=co[3]):#相交
                            error_num+=1
                            error_collect[child["pointer"]]=child["class"]
                            print(error_collect)
                        else:
                            left1.append(co[0])
                            left2.append(co[1])
                            right1.append(co[2])
                            right2.append(co[3])
                    else:
                        left1.append(co[0])
                        left2.append(co[1])
                        right1.append(co[2])
                        right2.append(co[3])
                else:#包着的
                    error_num += 1
                error_collect[child["pointer"]] = child["class"]
                print(error_collect)'''
