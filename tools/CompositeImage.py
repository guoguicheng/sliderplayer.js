# -*- coding:utf-8 -*- 
#########################################################
#ͼƬ����ƴ�ӳɳ�ͼ��������ҳsliderplayer.js����֡����###
#�轫ͼƬ���ڸĽű�ͬ����images�ļ����ڣ�Ĭ�Ϻ�׺Ϊ.jpg##
#########################################################

from PIL import Image
import os
import sys
def createImagesContent(width,height):
	return Image.new ("RGBA", (width, height), (255, 255, 255)) #�½�һ��image����creating images from scratch
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
	#���ص�ͼ
	colCount=4
	baseWidth,baseHeight=580,300
	imageList=loadImagesList(indir,ext)
	
	rowCount=len(imageList)/colCount if len(imageList)%colCount==0 else len(imageList)/colCount+1
	
	base_img = createImagesContent(colCount*baseWidth,rowCount*baseHeight)
	currentIndex=0
	
	for i in range(rowCount):
		for j in range(colCount):
			# ���Բ鿴ͼƬ��size��mode������mode��RGB��RGBA��RGBA��RGB����Alpha͸����
			# print base_img.size, base_img.mode
			left, upper=j*baseWidth, i*baseHeight
			box = (left,upper, left+baseWidth, upper+baseHeight)  # ��ͼ����ҪP��������
			
			#break
			#������ҪP��ȥ��ͼƬ
			
			region = Image.open(ur'%s' %(imageList[currentIndex]))
			#�������ѡ��һ�������������ͼƬ
			#region = tmp_img.crop((0,0,304,546)) #ѡ��һ������
			#����ʹ������ͼƬ
			#region = tmp_img

			#ʹ�� paste(region, box) ������ͼƬճ������һ��ͼƬ��ȥ.
			# ע�⣬region�Ĵ�С�����box�Ĵ�С��ȫƥ�䡣��������ͼƬ��mode���Բ�ͬ���ϲ���ʱ����Զ�ת���������Ҫ����͸���ȣ���ʹ��RGMA mode
			#��ǰ��ͼƬ�������ţ�����Ӧbox�����С
			# region = region.rotate(180) #��ͼƬ������ת
			
			region = region.resize((baseWidth,baseHeight))
			base_img.paste(region, box)
			if currentIndex<len(imageList):
				currentIndex+=1
			else:
				break
	#base_img.show() # �鿴�ϳɵ�ͼƬ
	base_img.save(outfile) #����ͼƬ
if __name__=="__main__":
	ext,inputdir=sys.argv[1],sys.argv[2]
	if(inputdir==""):
		print("������ͼƬ�б��ļ��е�ַ!")
		quit()
	try:
		outfile=sys.argv[3]
	except:
		outfile="./out.jpg"
	compositeImages(ext,inputdir,outfile)
