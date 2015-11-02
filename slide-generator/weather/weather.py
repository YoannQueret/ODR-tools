#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Generate weather map slide
Use this script at your risk.

Depandencies : 
        aptitude install python-imaging
"""
import datetime
import urllib
import json
import time
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import cStringIO

logo_file='/home/yoann/dev/ODR-tools/slide-generator/weather/wrp.png'
output_directory='/tmp/'

# Number of day to generate
day_count=3

day_array = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
month_array= ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

# -----------------------------

today = datetime.date.today()

# Download all original map and store data into data
i=1
data = []
day = today
while i <= day_count:
	d = { 'date': day.strftime('%Y-%m-%d'), 'maps': []}
	
	url = 'http://www.meteo-paris.com/site/images/cartes/%s.jpeg' % ( day.strftime('%Y-%m-%d') )
	print url
	d['maps'].append({'name': 'weather', 'data': Image.open(cStringIO.StringIO(urllib.urlopen(url).read()))})
	
	url = 'http://www.meteo-paris.com/site/images/cartes/temp_%s.jpg' % ( day.strftime('%Y-%m-%d') )
	print url
	d['maps'].append({'name': 'temp', 'data': Image.open(cStringIO.StringIO(urllib.urlopen(url).read()))})
	
	data.append(d)
	
	day = day+datetime.timedelta(days=1)
	i=i+1


# generate slide from original map
for entry in data:
	print entry['date']
	for map in entry['maps']:
		# Resize original map
		basewidth = 240
		wpercent = (basewidth / float(map['data'].size[0]))
		hsize = int((float(map['data'].size[1]) * float(wpercent)))
		map['data'] = map['data'].resize((basewidth, hsize), PIL.Image.ANTIALIAS)
		
		# Create a blank image
		im = Image.new("RGB", (320, 240), "white")
		
		# Insert 80x240 logo at left
		logo = Image.open(logo_file)
		im.paste(logo, (0, 0))
		
                # Insert map into blank 320x240 slide
                im.paste(map['data'], (80, 0))
                
                
                
                # Draw line on map left border 
                draw = ImageDraw.Draw(im)
		draw.line((80, 0, 80, im.size[0]), fill=128)
		
		# Write date at bottom left
		#draw.text((10, 220),entry['date'],(0,0,0))
		
		# Write Date
		dt = datetime.datetime.strptime(entry['date'], '%Y-%m-%d')
		
		font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 14)
		w, h = draw.textsize(day_array[int(dt.strftime('%w'))], font=font)
		draw.text(((320-240-w)/2, 160),day_array[int(dt.strftime('%w'))],(0,0,0), font=font)
		
		font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)
		w, h = draw.textsize(dt.strftime('%d'), font=font)
		draw.text(((320-240-w)/2, 180),dt.strftime('%d'),(0,0,255), font=font)
		
		font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 14)
		w, h = draw.textsize(month_array[int(dt.strftime('%-m'))-1], font=font)
		draw.text(((320-240-w)/2, 200),month_array[int(dt.strftime('%-m'))-1],(0,0,0), font=font)
		
		
		# Insert Fanny (Special Joke !)
		#fanny = Image.open('/home/yoann/dev/ODR-tools/slide-generator/weather/fanny.png')
		#im.paste(fanny, (50, 165), fanny)
                
		# Insert meteo-paris.com
		#font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 10)
		#draw.text((220, 230), 'meteo-paris.com',(0,0,0), font=font)
                
		del draw
		
		im.save("/tmp/%s-%s.jpg" % (entry['date'], map['name']), optimize=True,quality=90)
		
