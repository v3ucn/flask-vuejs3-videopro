import cv2
import numpy as np


# 图片相似度比对

def img_compare_img(target,black_list=[r"C:\Users\zcxey\Downloads\crab_1.png"]):


    for x in black_list:


        # 读取目标图像

        img = cv2.imread(target)


        # 读取违规物品图像

        template = cv2.imread(x)


        # 获取违规物品尺寸

        h,w = template.shape[:2]

        # 进行匹配操作

        res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)

        # 设置阈值

        threshold = 0.8

        # 寻找大于阈值的具体违规位置

        loc = np.where( res >= threshold )

        # 动态标注

        for pt in zip(*loc[::-1]):

            cv2.rectangle(img,pt,(pt[0] + w, pt[1] + h), (0, 0, 255),2)

        # 展示识别结果

        # 进行缩放操作

        cv2.namedWindow("test",0)

        cv2.resizeWindow("test",900,600)

        cv2.imshow("test",img)

        cv2.waitKey(0)





if __name__ == '__main__':
    
    img_compare_img(r"C:\Users\zcxey\Downloads\all.png")





# 视频转图片

def video_to_img(video_src):

    video = cv2.VideoCapture(video_src)

    index = 1


    while(1):

        # 获取视频信息

        ret,frame = video.read()

        # 定义抽帧数

        FPS = video.get(5)
        
        # 按照帧数进行快进展示

        # if index == 150:


        #     cv2.imshow("result",frame)

        #     cv2.waitKey(0)


        #     break

        # 判断视频帧数是否完结

        if ret:

            # 帧率公式

            frameRate = int(FPS) * 10

            if(index % frameRate == 0):

                print(f"开始截取该视频的第{index}帧")

                # 写入操作

                cv2.imwrite(f"./img/{index}.png",frame)

            index += 1

        else:

            print("所有帧数都已经读取完毕")

            break

        





