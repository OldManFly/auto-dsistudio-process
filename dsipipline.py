#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 15:34:15 2021

@author: liangalbert
"""

import os
import glob
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from itertools import combinations
from PIL import ImageTk, Image

DSI_path = '/Applications/dsi_studio.app/Contents/MacOS/dsi_studio'

# =============================================================================
# DSI function
# =============================================================================
def src(source, output):
	return os.system(DSI_path+ ' --action=src --source='+source+ ' --output=' + output)

def rec(source):
	return os.system(DSI_path+ ' --action=rec --source='+source+ ' --method=1 --motion_correction=1')

def fiber_tracking(source,atlas_path,roi1,roi2,output):
	tracking_parameter =' --fa_threshold=0.0001 --dt_threshold=0 --turning_angle=48 --step_size=0.2 --smoothing=0.3 --min_length=0.2 --max_length=10 --tracking_method=0 --initial_dir=0 --interpolation=0 --voxelwise=0 --default_otsu=0.5 --tip_iteration=10 --fiber_count=5000  --seed_count=70000000 --thread_count=4'
	return os.system(DSI_path+ ' --action=trk --source='+source+' --t1t2=' + atlas_path + tracking_parameter + '  --roi='+roi1+' --roi2='+roi2+' --output='+output+' --export=stat,tdi,tdi2')

def roi_based(source,atlas_path,roi,output):
	return os.system(DSI_path+ ' --action=ana --source='+source+ '  --region='+roi+' --t1t2=' + atlas_path +' --output='+output)


# =============================================================================
# GUI function
# =============================================================================
def button_file():
	global file_select
	file_select = filedialog.askdirectory()
	file_show.set(file_select)
	
def button_atlas():
	global atlas_select
	atlas_select = filedialog.askopenfilename()
	atlas_show.set(atlas_select)
def button_roi():
	global roi_select
	roi_select = filedialog.askdirectory()
	roi_show.set(roi_select)
def button_process():
	result = file_select+'/result'
# =============================================================================
# 	Create ROI list
# =============================================================================
	roi = glob.glob(roi_select+'/*.nii')
	strg = "+"
	all_roi = strg.join(roi)
# =============================================================================
# 	DSI process
# =============================================================================
#	labelText.set(mode.get())   ##teat
	labelText_ROI.set('ROI based')
	labelText_track.set('Track based')
	if os.path.isdir(result)==False:
		os.mkdir(result)
		os.mkdir(result+'/src')
		os.mkdir(result+'/ROI_index')
		os.mkdir(result+'/Tracking_index')
		
	subject_list = glob.glob(file_select+'/*/*/*/2dseq')
	for i in subject_list:
#		src(i,result+'/src/'+i.split("/")[5]+'.src.gz')
		print('src now')
	src_file = glob.glob(result+'/src/*.src.gz')
	for k in src_file:
#		rec(k)
		print('rec now')
	fib_file = glob.glob(result+'/src/*.fib.gz')
# =============================================================================
# 	ROI based
# =============================================================================
	if mode.get() ==labelText_ROI.get():
		for j in fib_file:
#			roi_based(j,atlas_select,all_roi,result+'/DTI_index/'+j.split('/')[7].split('.')[0]+'.txt')
			print('ROI now')
	
# =============================================================================
# 	Track based
# =============================================================================
	elif mode.get() == labelText_track.get():
		for track in fib_file:
			 for com_roi in combinations(roi,2):
#				  fiber_tracking(track,atlas_select,com_roi[0],result+'/Tracking_index/'+com_roi[1],com_roi[0].split('/')[-1]+'_'+com_roi[1].split('/')[-1]+'_track.trk')
				  print('tracking now')
		
		
		
		
	
# =============================================================================
# main GUI
# =============================================================================
if __name__ == '__main__':
	window = tk.Tk()
	window.title('DSI studio multiple subject interface')
	window.geometry('500x400')
# =============================================================================
# 	BUTTON
# =============================================================================
	file_path = tk.Button(window, text='File path', command=lambda:button_file())
	file_path.grid(column=0,row=1)
	
	file_show = tk.StringVar()  ##接button 的值
	file_box = tk.Label(window, textvariable=file_show, bg='white', fg='black', font=('Arial', 12), width=30, height=2)
	file_box.grid(column=0,row=5)
	
	roi_path = tk.Button(window, text='ROI path', command=lambda:button_roi())
	roi_path.grid(column=0,row=10)
	
	roi_show = tk.StringVar()  ##接button 的值
	roi_box = tk.Label(window, textvariable=roi_show, bg='white', fg='black', font=('Arial', 12), width=30, height=2)
	roi_box.grid(column=0,row=15)
	
	atlas_path = tk.Button(window, text='atlas path', command=lambda:button_atlas())
	atlas_path.grid(column=0,row=20)
	
	atlas_show = tk.StringVar()  ##接button 的值
	atlas_box = tk.Label(window, textvariable=atlas_show, bg='white', fg='black', font=('Arial', 12), width=30, height=2)
	atlas_box.grid(column=0,row=25)
	
	processing = tk.Button(window, text='Excution', command=lambda:button_process())
	processing.grid(column=0,row=45)
	
	
	
# =============================================================================
# 	選擇分析方法
# =============================================================================
	
	labelTop = tk.Label(window,text = "Choose analysis method")
	labelTop.grid(column=0, row=30)
	
	mode = ttk.Combobox(window,values=['ROI based', 'Track based'],state='readonly')
	mode.grid(column=0,row=35)
	mode.bind('<<button_process>>',button_process)
	
#	
#	labelText = tk.StringVar()
#	mylabel = tk.Label(window, textvariable=labelText, height=5, font=('Arial', 16))
#	mylabel.grid(column=3,row=35)
	
	labelText_ROI = tk.StringVar()	
	labelText_track = tk.StringVar()
	
# =============================================================================
# 	進度條
# =============================================================================
#	progress=ttk.Progressbar(window,length=100,mode='determinate')
#	progress.grid(column=3,row=20)

# =============================================================================
# 圖片	
# =============================================================================
	
	img = Image.open('./graph/dsi_studio.jpg')
	img = img.resize( (img.width//2, img.height//2) )
	imgTK = ImageTk.PhotoImage(img)
	imgLabel = tk.Label(window,image=imgTK)
	imgLabel.grid(column=4,row=10)
	
	
	img2 = Image.open('./graph/NTK.png')
	img2 = img2.resize( (img2.width//30, img2.height//30) )
	imgTK2 = ImageTk.PhotoImage(img2)
	imgLabel2 = tk.Label(window,image=imgTK2)
	imgLabel2.grid(column=4,row=20)
	window.mainloop()
	