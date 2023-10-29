import cv2
from PIL import Image
import imagehash as iHash
import numpy as np
from numpy.linalg import norm
import csv
import msvcrt
import os

TITLE='以圖搜圖小程式？　Ｖ０．４．０　'
MENU=[
    '０）Ｅ　Ｘ　Ｉ　Ｔ',
    '１）執行－以圖搜圖',
    '２）建立－資料索引',
]
ORDER=[1,2,0]
GRAPH_LENGTH=20
HASH_SIZE=8

def imgRetrieval():
    while 1:
        Title('以圖搜圖')
        TitlePrint('！請輸入圖片路徑或０以回到主選單！',edge='　')
        TitlePrint(edge='＝',cont='＝')
        print()
        path=Full2Half(input("請輸入："))
        print()
        TitlePrint(edge='＝',cont='＝')
        Reflash()
        if path.isdigit() and path == '0':
            InfoPrint(f'回到主選單～\n')
            break
        else:            
            HashList=Img2Hash(path)
            if HashList: 
                InfoPrint(f'正在搜尋圖片\n','處理中')
                ans=CountDiff(HashList)
                if(ans[1]>0.8):
                    InfoPrint(f'\n最相似的圖片為 "{ans[0]}" 。\n'
                            +f'相似度為 "{ans[1]*100}%" 。\n','完成')
                else:
                    InfoPrint(f'找不到相似圖片。\n\n','失敗')
                    _yn=input('請問是否需要建立索引？（Ｙ／Ｎ）：')
                    if _yn=="Y":
                        pass
                    if _yn=="N":
                        pass
                    else:
                        InfoPrint(f'請輸入有效的數字!!!\n',type='警告')
                Wait4Key()
            else: 
                next

def indexCreate():
    while 1:
        Title('建立資料索引')
        TitlePrint('！請輸入圖片路徑或０以回到主選單！',edge='　')
        TitlePrint(edge='＝',cont='＝')
        print()
        path=Full2Half(input("請輸入："))
        print()
        TitlePrint(edge='＝',cont='＝')
        Reflash()
        if path.isdigit() and path == '0':
            InfoPrint(f'回到主選單～\n')
            break
        else:
            HashList=Img2Hash(path)
            if HashList: 
                WriteCSV(HashList)
            else: 
                next

def CountDiff(HashList):
    data=ReadCSV()
    ans=["",0]
    for x in data:
        temp=CosSimilarity(HashList[0],x[1])
        if ans[1]<temp:ans=[x[0],CosSimilarity(HashList[0],x[1])]
    return ans

def CosSimilarity(vector_a,vector_b):
    # 定義兩個向量
    v_a = np.array(vector_a.hash)
    v_a=v_a.flatten().astype('int')
    v_b = np.array(iHash.hex_to_hash(vector_b).hash)
    v_b=v_b.flatten().astype('int')
    
    # 計算餘弦相似度
    cosine_similarity = np.dot(v_a,v_b) / (norm(v_a)*norm(v_b))

    #InfoPrint(cosine_similarity,"相似度")
    return cosine_similarity

def ReadCSV(path='./db/index.csv'):
    data=[]
    with open(path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
        f.close()
    return data

def WriteCSV(HashList,path='./db/index.csv'):
    with open(path, "a") as f:
        InfoPrint(f'正在建立索引表\n','處理中')
        while 1:
            name=input('請命名：')
            name+=GetExt(_TempPath)
            if not FileExist(f'./db/img/{name}',0):break
            InfoPrint(f'檔案 "{name}" 已存在！',"錯誤")
        f.write(f"{name}")
        for x in HashList:
            f.write(f",{x}")
        f.write("\n")
        f.close()
        InfoPrint(f'正在移動檔案\n','處理中')
        os.rename(_TempPath, f'./db/img/{name}')
    Reflash()
    InfoPrint(f'已成功為 "{name}" 建立新的索引\n','恭喜')
    return True

def FileExist(path,err=True):
    if os.path.isfile(path):
        return True
    if err:InfoPrint("檔案不存在！","錯誤")
    return False

def GetExt(path):
    return os.path.splitext(path)[1]

def Img2Hash(path):
    if not FileExist(path):return False
    global _TempPath
    _TempPath=path
    InfoPrint(f'正在建立哈希值\n','處理中')

    img=cv2.imread(path)
    img=Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    HashList=[
        iHash.average_hash(img,HASH_SIZE),
        iHash.phash(img,HASH_SIZE),
        iHash.dhash(img,HASH_SIZE),
        iHash.whash(img,HASH_SIZE),
        #iHash.colorhash(img),#colorhash先暫時不用
        iHash.crop_resistant_hash(img),#colorhash儲存但暫不計算
    ]
    for x in HashList:
        print(x)
    return HashList

def InfoPrint(text='',type='通知'):
    print(f'{type}：{text}')

def TitlePrint(text='',edge='＊',cont='　',size=GRAPH_LENGTH):
    print(edge+cont*(size-len(text)//2)+text+cont*(size-len(text)//2)+edge)

def Title(text='',edge='＊',cont='　',size=GRAPH_LENGTH):
    TitlePrint(cont='＊')
    TitlePrint()
    TitlePrint(text,edge=edge,cont=cont,size=size)
    TitlePrint()
    TitlePrint(cont='＊')

def Full2Half(str):
    n = []
    s = str
    for char in s:
        num = ord(char)
        if num == 0x3000:
            num = 32
        elif 0xFF01 <= num <= 0xFF5E:
            num -= 0xfee0
        num = chr(num)
        n.append(num)
    return ''.join(n)

def Wait4Key():
    print('！　請　按　任　意　鍵　繼　續　！')
    msvcrt.getch()
    Reflash()

def Reflash():
    os.system('cls')

def main():
    while(1):
        Title(TITLE)
        TitlePrint('！請輸入數字以決定需要的功能！',edge='　')
        TitlePrint(edge='＝',cont='＝')
        for i in ORDER:
            TitlePrint(MENU[i],edge='　')
        TitlePrint(edge='＝',cont='＝')
        print()
        select=Full2Half(input("請選擇："))
        print()
        if select.isdigit() and int(select) in ORDER:
            if select=='1':
                Reflash()
                InfoPrint(f'你選擇了 {MENU[int(select)]}\n')
                imgRetrieval()
            elif select=='2':
                Reflash()
                InfoPrint(f'你選擇了 {MENU[int(select)]}\n')
                indexCreate()
            else:
                Reflash()
                InfoPrint(f'歡迎您的下次使用～\n',type='謝謝')
                break
        else:
            Reflash()
            InfoPrint(f'請輸入有效的數字!!!\n',type='警告')       
    Wait4Key() 
    exit()

if __name__ =='__main__':
    main()