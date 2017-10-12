import sys
from urllib import urlopen
import json
import requests
import sqlite3 as sql
import pafy 
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


key = 'AIzaSyCj5NpamOFqud9eTl8cTInvaPSc_8oycuk'
download_flag = ''




def download_image(image_url, image_id, image_type):
	path = 'static/images/'+ image_type +'---'+ image_id +'.jpg'
	with open(path, 'wb') as handle:
			response = requests.get(image_url, stream=True)

			if not response.ok:
				print response

			for block in response.iter_content(1024):
				if not block:
					break

				handle.write(block)
	return path		

def download_video(video_id):
	url = "https://www.youtube.com/watch?v="+video_id	
	video = pafy.new(url)
	streams = video.streams
	med_quality = streams[3]
	med_quality.download()	
	print '-------------------downloading----------------------'	

def get_video_info(video_id, reference, download_flag):
	video_link = 'https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet%2CcontentDetails%2Cstatistics&id='+video_id+'&key='+key	
	print 'get video info...'
	if (download_flag) :
		download_video(video_id)
	res = json.loads(urlopen(video_link).read())
	video_url = 'https://www.youtube.com/watch?v='+str(res['items'][0]['id'])
	video_title = str(res['items'][0]['snippet']['title'])
	video_duration = str(res['items'][0]['contentDetails']['duration']).split('M')
	video_duration =  video_duration[0].split('T')[1] +' : '+ video_duration[1].split('S')[0]
	video_views = str(res['items'][0]['statistics']['viewCount'])
	video_thumbnail_url = str(res['items'][0]['snippet']['thumbnails']['default']['url'])
	video_full_sized_image_url = 'https://img.youtube.com/vi/'+str(res['items'][0]['id'])+'/0.jpg'
	video_thumbnail_path = download_image(video_thumbnail_url, video_id, 'thumbnail')
	video_full_sized_image_path = download_image(video_thumbnail_url, video_id, 'full_sized')
	print video_full_sized_image_path
	with sql.connect("database.db") as con:
		cur = con.cursor()
		cur.execute("INSERT INTO videos (video_id,video_url,video_title,video_duration,video_views,video_thumbnail_url,video_full_sized_image_url,video_thumbnail_path,video_full_sized_image_path,reference) VALUES (?,?,?,?,?,?,?,?,?,?)",(video_id,video_url,video_title,video_duration,video_views,video_thumbnail_url,video_full_sized_image_url,video_thumbnail_path,video_full_sized_image_path,reference) )
		con.commit()
		print 'inserted-------------------------------------successfully'
	con.close()
	



def get_channel_info(channel_link, download_flag):
	channel_name = channel_link.split('user/')[-1].split('/')[0]
	print channel_name
	link2 = 'https://www.googleapis.com/youtube/v3/channels?key='+key+'&forUsername='+channel_name+'&part=id'
	res = json.loads(urlopen(link2).read())
	channel_id = res['items'][0]['id']
	rows = certain_list_db(channel_id)
	if (len(rows)):
		print '--------------Found--------------'
	else :
		link3 = 'https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId='+channel_id+'&maxResults=50&key='+key
		print link3
		res = json.loads(urlopen(link3).read())
		videos = res['items']
		for video in videos:
			video_id = video['id']['videoId']
			get_video_info(video_id, channel_id, download_flag)
	rows = certain_list_db(channel_id)	
	return rows		




def get_playlist_info(playlist_link, download_flag):
	playlist_id = playlist_link.split('list=')[1]
	rows = certain_list_db(playlist_id)
	if (len(rows)):
		print '--------------Found--------------'
	else :
		link = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId='+playlist_id+'&key='+key
		res = json.loads(urlopen(link).read())
		videos = res['items']
		for video in videos:
			video_id = video['snippet']['resourceId']['videoId']
			get_video_info(video_id, playlist_id, download_flag)
	rows = certain_list_db(playlist_id)	
	return rows			



def list_db():
	con = sql.connect("database.db")
	con.row_factory = sql.Row   
	cur = con.cursor()
	cur.execute("select * from videos")
	rows = cur.fetchall()
	print rows 


def certain_list_db(reference):
	data = []
	con = sql.connect("database.db")
	con.row_factory = sql.Row   
	cur = con.cursor()
	cur.execute("select * from videos where reference = '"+reference+"'")
	rows = cur.fetchall() 
	for row in rows:
		data.append([x for x in row])
	return data

@app.route('/')
def index():
	
   	return render_template("index.html")

@app.route('/process', methods=['POST'])
def process():
	link = request.form['link']
	download_flag = request.form['download_flag']
	playlist_flag = 'list='
	channel_flag = 'user/'
	error= ''
	rows=[]
	if playlist_flag in link: 
		rows = get_playlist_info(link, download_flag)
	elif channel_flag in link:
		rows = get_channel_info(link, download_flag)
	else:
		error = 'Please enter a valid url'	
	return jsonify({'name' : 'Done', 'error':error, 'rows':rows})   	


if __name__ == '__main__':
   app.run('0.0.0.0','9999')   


## this code for playlist scrapping and get some info
# import bs4 as bs
# from urllib import urlopen
# import re
# import pafy
# link2 = 'https://www.youtube.com/watch?v=ztiHRiFXtoc&list=PLvFsG9gYFxY_2tiOKgs7b2lSjMwR89ECb'
# link = 'https://www.youtube.com/playlist?list=PLvFsG9gYFxY_2tiOKgs7b2lSjMwR89ECb'
# link = link.split('list=')[-1].split('&')[0]
# link = 'https://www.youtube.com/playlist?list='+link
# print link
# sauce = urlopen(link).read()
# soup = bs.BeautifulSoup(sauce, 'lxml')
# links = soup.find_all('a', class_='pl-video-title-link')
# for link in links:
# 	url = 'https://www.youtube.com'+link['href'].split("&")[0]
# 	video = pafy.new(url)
# 	print('Title : ' + video.title)
# 	print('Duration : ' + video.duration)
# 	print('Views : ' + str(video.viewcount))
# 	print('Pics : ' + video.thumb, video.bigthumb, video.bigthumbhd)

## this code for channel scrapping and get some info
# import bs4 as bs
# from urllib import urlopen
# import re
# import pafy
# link = 'https://www.youtube.com/user/AsapSCIENCE/videos'
# sauce = urlopen(link).read()
# soup = bs.BeautifulSoup(sauce, 'lxml')
# links = soup.find_all('a', href = re.compile('^/watch'))
# for link in links:
# 	url = 'https://www.youtube.com'+link['href'].split("&")[0]
# 	video = pafy.new(url)
# 	print('Title : ' + video.title)
# 	print('Duration : ' + video.duration)
# 	print('Views : ' + str(video.viewcount))
# 	print('Pics : ' + video.thumb, video.bigthumb, video.bigthumbhd)


## this code to make it run on the shell but the shell doesn't see the rest of the link after this sign(&)
# if sys.argv[1] == '-p':
# 	playlist_link = sys.argv[2]
# 	print playlist_link
# 	# get_playlist_info(playlist_link)
# elif sys.argv[1] == '-c':
# 	channel_link = sys.argv[2]
# 	get_channel_info(channel_link)
# else:
# 	print 'enter good param'


## this code to give the url of the video content but i couldn't pass YouTube permissions for download it
# res = urllib.urlopen('https://www.youtube.com/get_video_info?video_id=Tif2a8vXeAA')
# data = res.read()
# info = urlparse.parse_qs(data)
# title = info['title'][0]
# fname = title + '.mp4'
# stream_map = info['url_encoded_fmt_stream_map'][0]
# vs_info = stream_map.split(',')
# medium_mp4 = vs_info[2]
# v_info = urlparse.parse_qs(medium_mp4)
# v_quality =  v_info['quality'][0]
# v_type =  v_info['type'][0]
# v_url = v_info['url'][0]
# res = urllib.urlopen(v_url)
# print res.headers
# for video in vs_info:
# 	item = urlparse.parse_qs(video)
# 	print item['quality'][0]
# 	print item['type'][0]
# 	print item['url'][0]
