import os
import numpy as np
import json
from open_cv import normalize_and_clamp_red , speed
from prediction import prediction
import cv2

def json_to_npy(path):
    """
    將 data.txt 
    的內容讀取並儲存為 data.npy
    每行會解析為 Python 物件 (dict、list)
    """
    print("執行 abc.py : " + str(path))
    
    txt_path = os.path.join(path, "data.json")    #全部來源data
    is_hand_path = os.path.join(path , "is_hand.json")  #只有手的data
    new_path = create_folder(path , "output")   #目標資料夾
    
    #count_detect(txt_path ,path , 2)
    #area_detect(txt_path , 0.3)
    open_cv_process(is_hand_path , txt_path)
    #prediction(path , None)
    print("執行 abc.py  結束" )

def open_cv_process(is_hand_path, txt_path):
    """
    用於統一管理執行與opencv相關的判斷
    """
    print("執行 open_cv_process ...........................................")
    with open(txt_path ,  "r") as f:
        for line in f:
            data = json.loads(line.strip())
            name , box1 , box2 , box3 = find_box(data)
            
            if name is None:
                continue
            
            img3 = os.path.join("C:\\Users\\user\\Desktop\\all_img" , name)  #速度表圖
            
            #speed(img3 , box3)
            #skin_detect(img1 , box1)
            if box3 is not None:
                normalize_and_clamp_red(img3 , box3)
    print("執行 open_cv_process .結束..........................................")


def count_detect(data_json, path , limit = 3):
    """
    計數邏輯，若遇到出現手的照片超過一定次數，則發出警告
    
    data_json : 全部讀取到的json檔案路徑
    path : 只有手的json檔案路徑
    """
    data_play_phone = []
    
    output_file = os.path.join(path, "count_detect.txt")
    count = 0
    ready_to_skip = False
    with open(output_file, "a", encoding="utf-8") as f:  # 追加寫入
        #=====================================================================
        """for in json
                計數是否歸零 = true
                for in line["locstion"]
                    if c == 1:
                        計數是否歸零 = false
                if 計數是否歸零:
                    count = 0
        """
        for line in data_json:
            print(".........................................." + line)
            line = line.strip()
            data_list = json.loads(line)
            for item in data_list["location"]:
                ready_to_skip = True
                if item["class"] == 1:
                    ready_to_skip = False
                    count += 1
                    if count >= limit:
                        alarm(data_list["name"])
                        data_play_phone.append(data_list["name"])
                    print(str(data_list["name"]) + "    " + str(count))
                    break
        #=====================================================================
            if ready_to_skip:
                count = 0
            
    print("結束執行 count_detect...........................................")
    return data_play_phone

def area(x1, y1, x2, y2):
    """計算正方形面積"""
    if x2 <= x1 or y2 <= y1:
        return 0
    return (x2 - x1) * (y2 - y1)

def cover_area(a, b):
    """計算兩個 box 的交集面積"""
    inter_x1 = max(a["x1"], b["x1"])
    inter_y1 = max(a["y1"], b["y1"])
    inter_x2 = min(a["x2"], b["x2"])
    inter_y2 = min(a["y2"], b["y2"])

    if (inter_x2 <= inter_x1) or (inter_y2 <= inter_y1):
        return 0
    
    return (inter_x2 - inter_x1) * (inter_y2 - inter_y1)

def distance(box1, box2):
    """計算兩個 box 的中心點距離"""
    center1_x = (box1["x1"] + box1["x2"]) / 2
    center1_y = (box1["y1"] + box1["y2"]) / 2
    center2_x = (box2["x1"] + box2["x2"]) / 2
    center2_y = (box2["y1"] + box2["y2"]) / 2

    return ((center1_x - center2_x) ** 2 + (center1_y - center2_y) ** 2) ** 0.5

def area_detect(path, limit_area_in_hand = 0.3 , limit_dis = 50):
    
    """偵測兩者面積的重疊率 和 距離
    path : 只有手的json檔案路徑
    """
    data_play_phone_cover = []
    data_play_phone_dis = []
    with open(path, "r") as f:
        for line in f:
            data = json.loads(line.strip())

            name , box1 , box2 = find_box(data)
            # 計算面積
            area1 = area(box1["x1"], box1["y1"], box1["x2"], box1["y2"])
            area2 = area(box2["x1"], box2["y1"], box2["x2"], box2["y2"])

            in_area = cover_area(box1, box2)
            dis = distance(box1 , box2)
            # 若面積不為負數，則計算覆蓋率
            if area1 > 0:
                cover1 = in_area / area1

            # 最後輸出
            if (cover1 >= limit_area_in_hand):
                alarm(name + f" | 覆蓋率 : {cover1:.3f}")
                data_play_phone_cover.append(name)
            if (dis >= limit_dis):
                alarm(name + f" | 距離 : {dis:.3f}")
                data_play_phone_dis.append(name)
                
                """
                print(name + f"交集面積 = {in_area}")
                print(f"  覆蓋率: class1 = {cover1:.3f}, class2 = {cover2:.3f}")
                print("--------------------------------------------------")
                """
                
    return data_play_phone_cover , data_play_phone_dis

def find_box(data ):
    """
    找到手和手機的box
    回傳參數
    圖片名 , 手機(location) , 手(location)
    """
    name = data["name"]
    boxes = data["location"]

    box1 = None
    box2 = None
    box3 = None

    # 取得 class 1 與 class 2 的 box
    for b in boxes:
        if b["class"] == 1:  #手機
            box1 = b
        elif b["class"] == 0:  #手
            box2 = b
        elif b["class"] == 2:  #速度表
            box3 = b

    # 若找不到任一 class 就跳過/同一個畫面中 手 和 手機 沒有同時出現則不回傳 速度表
    if box1 is None or box2 is None:
        return None,None,None,None
    
    #print(str(name) + "  box1:" + str(box1) + "  box2:" + str(box2) + "  box3:" + str(box3))
    return name , box1 , box2 , box3
    

def alarm(message):
    """警告"""
    print("發出警告 : " + message)


def create_folder(path , name):
    """
    建立資料夾
    """
    new_path = os.path.join(path, name)
    if not os.path.exists(new_path):
        os.makedirs(new_path, exist_ok=True)
    return new_path

if __name__ == "__main__":
    path = os.getcwd() 
    json_to_npy(path)
