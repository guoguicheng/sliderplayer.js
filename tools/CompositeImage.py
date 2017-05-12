# -*- coding:utf-8 -*- 
#########################################################
#图片序列拼接成长图，用于网页sliderplayer.js序列帧播放###
#需将图片置于改脚本同级的images文件夹内，默认后缀为.jpg##
#########################################################

from PIL import Image
import os
import sys
def createImagesContent(width,height):
	return Image.new ("RGBA", (width, height), (255, 255, 255)) #新建一个image对象creating images from scratch
def loadImagesList(dir='images',ext='.jpg'):
	allfiles = []
	needExtFilter = (ext != None)
	for root,dirs,files in os.walk(dir):
		for filespath in files:
			filepath = os.path.join(root, filespath)
			extension = os.path.splitext(filepath)[1][1:]
			if needExtFilter and extension in ext:
				allfiles.append(filepath)
			elif not needExtFilter:
				allfiles.append(filepath)
	return allfiles
def compositeImages(ext,indir,outfile):
	#加载底图
	colCount=4
	baseWidth,baseHeight=580,300
	imageList=loadImagesList(indir,ext)
	
	rowCount=len(imageList)/colCount if len(imageList)%colCount==0 else len(imageList)/colCount+1
	
	base_img = createImagesContent(colCount*baseWidth,rowCount*baseHeight)
	currentIndex=0
	
	for i in range(rowCount):
		for j in range(colCount):
			# 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
			# print base_img.size, base_img.mode
			left, upper=j*baseWidth, i*baseHeight
			box = (left,upper, left+baseWidth, upper+baseHeight)  # 底图上需要P掉的区域
			
			#break
			#加载需要P上去的图片
			
			region = Image.open(ur'%s' %(imageList[currentIndex]))
			#这里可以选择一块区域或者整张图片
			#region = tmp_img.crop((0,0,304,546)) #选择一块区域
			#或者使用整张图片
			#region = tmp_img

			#使用 paste(region, box) 方法将图片粘贴到另一种图片上去.
			# 注意，region的大小必须和box的大小完全匹配。但是两张图片的mode可以不同，合并的时候回自动转化。如果需要保留透明度，则使用RGMA mode
			#提前将图片进行缩放，以适应box区域大小
			# region = region.rotate(180) #对图片进行旋转
			
			region = region.resize((baseWidth,baseHeight))
			base_img.paste(region, box)
			if currentIndex<len(imageList):
				currentIndex+=1
			else:
				break
	#base_img.show() # 查看合成的图片
	base_img.save(outfile) #保存图片
if __name__=="__main__":
	ext,inputdir=sys.argv[1],sys.argv[2]
	if(inputdir==""):
		print("请输入图片列表文件夹地址!")
		quit()
	try:
		outfile=sys.argv[3]
	except:
		outfile="./out.jpg"
	compositeImages(ext,inputdir,outfile)
 