import pymysql
import cgi
import cgitb

db= pymysql.connect(host='localhost',
                     user='gallery',
                     passwd='eecs118',
                     db='gallery')

cgitb.enable()

def list_galleries():
    with db:
        cur = db.cursor()
        sql = "SELECT * FROM `gallery`"
        cur.execute(sql)
        gallery_result = cur.fetchall()
        #for row in gallery_result:
            #print(row)
        return gallery_result

def list_images(gallery_id):
    with db:
        cur = db.cursor()
        sql = "SELECT COUNT(*) FROM `image` WHERE `gallery_id` = %s"
        cur.execute(sql, gallery_id)
        count_result = cur.fetchall()
        sql = "SELECT * FROM `image` WHERE `gallery_id` = %s"
        cur.execute(sql, gallery_id)
        image_result = cur.fetchall()
        #for row in image_result:
            #print(row)
        return image_result

def list_detail(image_id):
    with db:
        cur = db.cursor()
        sql = "SELECT * FROM `detail` WHERE `image_id` = %s"
        cur.execute(sql, image_id)
        detail_result = cur.fetchone()
        #for row in detail_result:
            #print(row)
        return detail_result

def list_artist(artist_id):
    with db:
        cur = db.cursor()
        sql = "SELECT * FROM `artist` WHERE `artist_id` = %s"
        cur.execute(sql, artist_id)
        artist_result = cur.fetchone()
        return artist_result

def create_gallery(name, description):
    with db:
        cur = db.cursor()
        sql = "INSERT IGNORE INTO `gallery` (name, description) VALUES (%s, %s)"
        cur.execute(sql, (str(name), str(description)))
        db.commit()

def create_artist(name, birth_year, country, description):
    with db:
        cur = db.cursor()
        sql = "INSERT IGNORE INTO `artist` (name, birth_year, country, description) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (str(name), birth_year, str(country), str(description)))
        db.commit()

def add_image_to_gallery(title, link, gallery_id, artist_id, year, type_, width, height, location, description):
    with db:
        cur = db.cursor()
        sql = "SELECT MAX(image_id) FROM `image`"
        cur.execute(sql)
        results = cur.fetchone()
        image_id = results[0]+1
        sql = "SELECT MAX(detail_id) FROM `detail`"
        cur.execute(sql)
        results = cur.fetchone()
        detail_id = results[0]+1
        sql = "INSERT INTO `image` (title, link, gallery_id, artist_id, detail_id) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql, (title, link, gallery_id, artist_id, detail_id))
        sql = "INSERT INTO `detail` (image_id, year, type, width, height, location, description) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (image_id, year, type_, width, height, location, description))
        db.commit()

def delete_image(detail_id, image_id):
    with db:
        cur = db.cursor()
        sql = "SELECT MAX(image_id) FROM `image`"
        cur.execute(sql)
        set_value = cur.fetchone()[0]
        sql = "DELETE FROM `image` WHERE `image_id` = %s"
        cur.execute(sql, image_id)
        print(set_value)
        print(int(image_id) == set_value)
        if ( int(image_id) == set_value ):
            print("altering auto-increment")
            sql = "ALTER TABLE `image` AUTO_INCREMENT = %s"
            cur.execute(sql, set_value)
        sql = "SELECT MAX(detail_id) FROM `detail`"
        cur.execute(sql)
        set_value = cur.fetchone()[0]
        sql = "DELETE FROM `detail` WHERE `detail_id` = %s"
        cur.execute(sql, detail_id)
        if (int(detail_id) == set_value):
            print("altering auto-increment")
            sql = "ALTER TABLE `detail` AUTO_INCREMENT = %s"
            cur.execute(sql, set_value)
        db.commit()

def update_detail(detail_id, image_id, year, typeof, width, height, location, description, title, link):
    with db:
        cur = db.cursor()
        sql = "UPDATE `detail` SET `year`=%s, `type`=%s, `width`=%s, `height`=%s, `location`=%s, `description`=%s \
        WHERE `detail_id`=%s"
        cur.execute(sql, (year, typeof, width, height, location, description, detail_id))
        sql = "UPDATE `image` SET `title`=%s, `link`=%s WHERE `image_id`=%s"
        cur.execute(sql, (title, link, image_id))
        db.commit()
        
def update_artist(artist_id, name, birth_year, country, description):
    with db:
        cur = db.cursor()
        sql = "UPDATE `artist` SET `name`=%s, `birth_year`=%s, `country`=%s, `description`=%s \
        WHERE `artist_id`=%s"
        cur.execute(sql, (name, birth_year, country, description, artist_id))
        db.commit()

def update_gallery(gallery_id, name, description):
    with db:
        cur = db.cursor()
        sql = "UPDATE `gallery` SET `name`=%s, `description`=%s \
        WHERE `gallery_id`=%s"
        cur.execute(sql, (name, description, gallery_id))
        db.commit()

def find_type(typeof):
    with db:
        cur = db.cursor()
        sql = "SELECT * FROM `detail` INNER JOIN `image` ON `detail.image_id` = `image.image_id` WHERE type = %s"
        cur.execute(sql, typeof)
        image_result = cur.fetchall()

def find_artist(name):
    with db:
        cur = db.cursor()
        sql = "SELECT * FROM `image` INNER JOIN `artist` ON `artist.artist_id` = `image.artist_id` WHERE name = %s"
        cur.execute(sql, name)
        image_result = cur.fetchall()
        for row in image_result:
            print(image_result)

def find_location(location):
    with db:
        cur = db.cursor()
        sql = "SELECT * FROM `detail` INNER JOIN `image` ON `detail.image_id` = `image.image_id` WHERE location = %s"
        cur.execute(sql, location)
        image_result = cur.fetchall()
        for row in image_result:
            print(row)

def find_artist_country(country):
    with db:
        cur = db.cursor()
        sql = "SELECT `name` FROM `artist` WHERE `country` = %s"
        cur.execute(sql, country)
        artist_result = cur.fetchall()
        for row in image_result:
            print(row);

def find_artist_year(birth_year):
    with db:
        cur = db.cursor()
        sql = "SELECT `name` FROM `artist` WHERE `birth_year` = %s"
        cur.execute(sql, birth_year)
        artist_result = cur.fetchall()
        for row in artist_result:
            print(row)


FORM = cgi.FieldStorage()

if "gallery_title" in FORM and "gallery_description" in FORM:
    name = FORM.getvalue("gallery_title")
    description = FORM.getvalue("gallery_description")
    create_gallery(name, description)

if "artist_name" in FORM and "artist_birth_year" in FORM and "artist_country" in FORM and "artist_description" in FORM:
    name = FORM.getvalue("artist_name")
    birth_year = FORM.getvalue("artist_birth_year")
    country = FORM.getvalue("artist_country")
    description = FORM.getvalue("artist_description")
    create_artist(name, birth_year, country, description)

if ("image_title" in FORM and "image_link" in FORM and "image_artist_id" in FORM and "image_year" in FORM and "image_type" in FORM and "image_width" in FORM
and "image_height" in FORM and "image_location" in FORM and "image_description" in FORM):
    add_image_to_gallery(FORM.getvalue("image_title"), FORM.getvalue("image_link"), FORM.getvalue("image_gallery_id"), FORM.getvalue("image_artist_id"),
    FORM.getvalue("image_year"), FORM.getvalue("image_type"), FORM.getvalue("image_width"), FORM.getvalue("image_height"), FORM.getvalue("image_location"),
    FORM.getvalue("image_description"))
    
    
if "del_image_id" in FORM and "del_detail_id" in FORM:
    image_id = FORM.getvalue("del_image_id")
    detail_id = FORM.getvalue("del_detail_id")
    delete_image(detail_id, image_id)

if "upd_gallery_title" in FORM and "upd_gallery_description" in FORM and "upd_gallery_id" in FORM:
    update_gallery(FORM.getvalue("upd_gallery_id"), FORM.getvalue("upd_gallery_title"), FORM.getvalue("upd_gallery_description"))
    
if ("upd_detail_id" in FORM and "upd_image_id" in FORM and "upd_detail_year" in FORM and "upd_detail_type" in FORM and "upd_detail_width" in FORM and "upd_detail_height" in FORM and
"upd_detail_location" in FORM and "upd_detail_description" in FORM and "upd_image_title" in FORM and "upd_image_link" in FORM):
    update_detail(FORM.getvalue("upd_detail_id"), FORM.getvalue("upd_image_id"), FORM.getvalue("upd_detail_year"), FORM.getvalue("upd_detail_type"), FORM.getvalue("upd_detail_width"),
    FORM.getvalue("upd_detail_height"), FORM.getvalue("upd_detail_location"), FORM.getvalue("upd_detail_description"), FORM.getvalue("upd_image_title"), FORM.getvalue("upd_image_link"))                   
        
if ("upd_artist_id" in FORM and "upd_artist_name" in FORM and "upd_artist_birthyear" in FORM and "upd_artist_country" in FORM and "upd_artist_description" in FORM):
    update_artist(FORM.getvalue("upd_artist_id"), FORM.getvalue("upd_artist_name"), FORM.getvalue("upd_artist_birthyear"), FORM.getvalue("upd_artist_country"), FORM.getvalue("upd_artist_description"))


print("Content-Type: text/html") #HTML is following
print()
print("<TITLE>Mini Project#3</TITLE>")
print("<H1>Close this window to view updates to gallery</H1>")
