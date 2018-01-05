# python3
# 缩放iOS图片获得二倍图、三倍图 
# 缩放icon 图片

from PIL import Image, ImageFilter
import glob
import os, sys
import json

# 扩展图片为1、2、3倍图
def scale_image(file_name,file_type):
	ori_img = Image.open(file_name + '.' + file_type)
	ori_img = ori_img.convert("RGBA")

	#一倍图
	new_img = ori_img.resize((int(ori_img.width/2),int(ori_img.height/2)),Image.BILINEAR)
	new_img.save(file_name + '@1x.' + file_type)

	#三倍图
	new_img = ori_img.resize((int(ori_img.width*1.5),int(ori_img.height*1.5)),Image.BILINEAR)
	new_img.save(file_name + '@3x.' + file_type)
        
	#二倍图重命名
	try:
		os.rename(file_name + '.' + file_type,file_name + '@2x.' + file_type)
	except Exception:
		print('发生错误')
	else:
		pass
	finally:
		pass

# 是否是需要扩展的图片
def is_normal_image(file_name):

	ignore_string = ['@1x','@2x','@3x']

# 如果自带@1x,@2x,@3x，则不需要进行扩展
	for name in ignore_string:
		if name in file_name:
			return False

	return True

# 缩放icon图标生成所有的图标
def scale_icon_image(file_path):

    #0为大小 1为倍数 (20,2)指的是40x40
    iPhone_img_dict = [
    (20,2),
    (20,3),
    (29,2),
    (29,3),
    (40,2),
    (40,3),
    (60,2),
    (60,3),
    ]

    iPad_img_dict = [
    (20,1),
    (20,2),
    (29,1),
    (29,2),
    (40,1),
    (40,2),
    (76,1),
    (76,2),
    (83.5,2),
    ]

    json_msg = {"images":[],"info":{"version":1,"author":"xcode"}}

    icon_img = Image.open(file_path)

    #如果有则删掉文件夹中所有文件
    if os.path.exists('AppIcon.appiconset'):
        all_files = glob.glob(r"/AppIcon.appiconset/*")
        for file_name in all_files:
            os.remove('./AppIcon.appiconset/' + file_name)
    else :
        #创建目录
        os.mkdir('AppIcon.appiconset')

    for img_dict in [iPhone_img_dict,iPad_img_dict]:
        for img_info in img_dict :
            idiom = "iphone"
            if img_dict == iPad_img_dict:
                idiom = "ipad"

            #获取图片大小
            img_size = int(img_info[0] * img_info[1])
            
            #设置图片名称
            img_name = 'icon_' + idiom + '_' + str(img_info[0]) + '@' + str(img_info[1]) + 'x.png'

            #设置图片信息
            info = {
            "size":str(img_info[0]) + 'x' + str(img_info[0]),
            "idiom":idiom,
            "filename":img_name,
            "scale":str(img_info[1]) + 'x'
            }
            json_msg["images"].append(info)

            #创建图片
            new_icon = icon_img.resize((img_size,img_size),Image.BILINEAR)
            new_icon.save('AppIcon.appiconset/' + img_name)

    #特殊处理marketing部分
    icon_img.save('AppIcon.appiconset/icon_1024.png')
    itunes_special = {
      "idiom" : "ios-marketing",
      "size" : "1024x1024",
      "scale" : "1x",
      "filename" : "icon_1024.png"
    }
    json_msg["images"].append(itunes_special)

    #转为格式化后的json文本并写入文件
    fp_txt = json.dumps(json_msg, indent=4, sort_keys=False, ensure_ascii=False)
    fp = open('AppIcon.appiconset/Contents.json','w')
    fp.write(fp_txt)
    fp.close()

def show_help_msg():
    print('需要输入两个参数，action 和 path.\n \
action 有两个选择 \n \
1) scale_icon : 此时的 path 需要输入图片的名字，最好大小为1024*1024，png格式的图片,可以将图片进行缩放生成各种需要的 icon 大小\n \
2) scale_image : 此时的 path 需要输入图片文件夹的名字，会将文件夹中所有的 .png 格式图片转为 iOS 的倍数图，图片文件夹中的原始图片为 二倍图 \n \
')

if len(sys.argv) < 3 :
    show_help_msg()
action = sys.argv[1]
path = sys.argv[2]

if action == 'scale_icon':
    scale_icon_image(path)
elif action == 'scale_image':
    png_files = glob.glob(r"*.png")
    for img_file in png_files :
        file_name = img_file[:-4]
        if is_normal_image(file_name):
            scale_image(file_name,'png')
        else :
            print(file_name)
else :
    show_help_msg()