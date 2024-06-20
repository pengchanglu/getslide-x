import json 
import os 
import argparse
from tqdm import tqdm
import glob
import cv2 
import numpy as np
 
def convert_label_json(json_dir,save_dir,classes):
    files=os.listdir(json_dir)
    #删选出json文件
    jsonFiles=[]
    for file in files:
        if os.path.splitext(file)[1]==".json":
            jsonFiles.append(file)
    #获取类型        
    classes=classes.split(',')
    
    #获取json对应中对应元素
    for json_path in tqdm(jsonFiles):
        path=os.path.join(json_dir,json_path)
        with open(path,'r') as loadFile:
            print(loadFile)
            json_dict=json.load(loadFile)
        h,w=json_dict['imageHeight'],json_dict['imageWidth']
        txt_path=os.path.join(save_dir,json_path.replace('json','txt'))
        txt_file=open(txt_path,'w')
        
        for shape_dict in json_dict['shapes']:
            label=shape_dict['label'] 
            label_index=classes.index(label)
            points=shape_dict['points']
            points_nor_list=[]
            for point in points:
                points_nor_list.append(point[0]/w)
                points_nor_list.append(point[1]/h)
            points_nor_list=list(map(lambda x:str(x),points_nor_list))
            points_nor_str=' '.join(points_nor_list)
            label_str=str(label_index)+' '+points_nor_str+'\n'
            txt_file.writelines(label_str)
            
            
if __name__=="__main__":
    parser=argparse.ArgumentParser(description="json convert to txt params")
    #设json文件所在地址
    parser.add_argument('-json',type=str,default='E:/python/yolov8/img',help='json path')
    #设置txt文件保存地址
    parser.add_argument('-save',type=str,default='E:/python/yolov8/img',help='save path')
    #设置label类型,用“,”分隔
    parser.add_argument('-classes',type=str,default='car-labe',help='classes')
    args=parser.parse_args()
    print(args.json,args.save,args.classes)
    convert_label_json(args.json,args.save,args.classes)
