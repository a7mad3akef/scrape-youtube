import sqlite3

conn = sqlite3.connect('database.db')
print "Opened database successfully";

conn.execute('CREATE TABLE videos (video_id TEXT, video_url TEXT, video_title TEXT, video_duration TEXT, video_views TEXT, video_thumbnail_url TEXT, video_full_sized_image_url TEXT, video_thumbnail_path TEXT, video_full_sized_image_path TEXT, reference TEXT)')
print "Table created successfully";
conn.close()