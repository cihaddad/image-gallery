import pymysql
import cgi
import cgitb

db= pymysql.connect(host='localhost',
                     user='gallery',
                     passwd='eecs118',
                     db='gallery')


def list_galleries():
    with db:
        cur = db.cursor()
        sql = "SELECT * FROM `gallery`"
        cur.execute(sql)
        gallery_result = cur.fetchall()
        #for row in gallery_result:
            #print(row)
        return gallery_result
    
def gallery_info(gallery_id):
    with db:
        cur = db.cursor()
        sql = "SELECT * FROM `gallery` WHERE `gallery_id` = %s"
        cur.execute(sql, (gallery_id,))
        gallery_result = cur.fetchone()
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
    
def find_type(typeof):
    with db:
        cur = db.cursor()
        sql = "SELECT `image`.`image_id`, `image`.`title`, `image`.`link`, `image`.`gallery_id`, `image`.`artist_id`,\
        `image`.`detail_id` FROM `image` INNER JOIN `detail` ON `detail`.`image_id` = `image`.`image_id` WHERE `detail`.`type` = %s"
        cur.execute(sql, typeof)
        image_result = cur.fetchall()
        return image_result

def find_artist(name):
    with db:
        cur = db.cursor()
        sql = "SELECT `image`.`image_id`, `image`.`title`, `image`.`link`, `image`.`gallery_id`, `image`.`artist_id`, `image`.`detail_id` \
        FROM `image` INNER JOIN `artist` ON `artist`.`artist_id` = `image`.`artist_id` WHERE `artist`.`name` = %s"
        cur.execute(sql, name)
        image_result = cur.fetchall()
        return image_result

def find_range(year1, year2):
        with db:
            cur = db.cursor()
            sql = "SELECT `image`.`image_id`, `image`.`title`, `image`.`link`, `image`.`gallery_id`, `image`.`artist_id`, `image`.`detail_id`\
            FROM `image` INNER JOIN `detail` ON `detail`.`image_id` = `image`.`image_id` WHERE `detail`.`year` >= %s AND `detail`.`year` <= %s"
            cur.execute(sql, (year1,year2))
            image_result = cur.fetchall()
            return image_result

def find_location(location):
    with db:
        cur = db.cursor()
        sql = "SELECT `image`.`image_id`, `image`.`title`, `image`.`link`, `image`.`gallery_id`, `image`.`artist_id`, `image`.`detail_id`\
               FROM `image` INNER JOIN `detail` ON `detail`.`image_id` = `image`.`image_id` WHERE `detail`.`location` = %s"
        cur.execute(sql, location)
        image_result = cur.fetchall()
        return image_result

def find_artist_country(country):
    with db:
        cur = db.cursor()
        sql = "SELECT * FROM `artist` WHERE `country` = %s"
        cur.execute(sql, country)
        artist_result = cur.fetchall()
        return artist_result

def find_artist_year(birth_year):
    with db:
        cur = db.cursor()
        sql = "SELECT * FROM `artist` WHERE `birth_year` = %s"
        cur.execute(sql, birth_year)
        artist_result = cur.fetchall()
        return artist_result


FORM = cgi.FieldStorage()
search_type = FORM.getvalue("search_type")
search_value = FORM.getvalue("search_value")
image_search = False
artist_search = False
images = []
artists = []
if search_type == "type":
    images = find_type(search_value)
    image_search = True
elif search_type == "range":
    print("range search")
    year1 = FORM.getvalue("year1")
    year2 = FORM.getvalue("year2")
    image_search = True
    images = find_range(year1, year2)
elif search_type == "location":
    print("location search")
    image_search = True
    images = find_location(search_value)
elif search_type == "artist name":
    image_search = True
    images = find_artist(search_value)
elif search_type == "artist birth year":
    print("artist search")
    artist_search = True
    artists = find_artist_year(search_value)
    print(artists)
elif search_type == "country":
    print("artist search")
    artist_search = True
    artists = find_artist_country(search_value)
    print(artists)
else:
    print("NOT A VALID SEARCH TYPE?")
    

print("Content-Type: text/html") #HTML is following
print()
print("<TITLE>Mini Project#3</TITLE>")
print("""<script> 
         var detailPerImage = {};
         var artistInfo = {};
         var imageInfo = {};
         </script>""")
if len(images) > 0:
    print("""
    <style>
    
    body{
      background: #ECE9E6;  /* fallback for old browsers */
      background: -webkit-linear-gradient(to right, #FFFFFF, #ECE9E6);  /* Chrome 10-25, Safari 5.1-6 */
      background: linear-gradient(to right, #FFFFFF, #ECE9E6); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
    }
    
    div.gallery_intro{
      padding: 5px;
      text-align: center;
      background-image: url("https://images.pexels.com/photos/1227511/pexels-photo-1227511.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=750&w=1260");
      background-color: black;
      color: white;
      font-size: 25px;
    }

    div.header_buttons{
      text-align:left;
      margin: 5px;
    }


    div.columnleft{
        float:left;
        width: 50%;
    }

    div.columnright{
        float:right;
        width:50%;

    }

    div.thumbnail {
      margin: 5px;
      border: 1px solid #ccc;
      float: left;
      width: 360px;
      height: 300px;
    }

    div.thumbnail:hover {
      border: 1px solid #777;
    }

    div.thumbnail img {
      width: 100%;
      height: 60%;
    }

    div.thumbnail p{
        padding: 5px;
        width: 350px;
        overflow: scroll;
        white-space: nowrap;
        text-align: left;
    }

    div.detail-panel img{
        width:100%;
        height:auto;
    }

    div.display-detail {
        background-image: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);}

    div.display-icons{
        margin: 5px;
        text-align: center;
    }

    div.display-icons #del_image{
      background-color: red;
      border: none;
      color: white;
      padding: 15px 25px;
      text-align: center;
      font-size: 16px;
      cursor: pointer;
    }

    #artist_display{
        text-align: center;
        

    }

    #artist_button{
      background-color: orange;
      border: none;
      color: white;
      padding: 15px 25px;
      margin: auto;
      font-size: 16px;
      cursor: pointer;

    }

    div.display-icons #edit_image{
      background-color: green;
      border: none;
      color: white;
      padding: 15px 25px;
      text-align: center;
      font-size: 16px;
      cursor: pointer;
    }

    div.display-icons #del_image:hover {
      box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
    }

    div.display-icons #edit_image:hover {
      box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
    }

    #artist_button:hover {
      box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
    }

    input[type=text], select {
      width: 100%;
      padding: 12px 20px;
      margin: 8px 0;
      display: inline-block;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
    }

    input[type=number], select {
      width: 100%;
      padding: 12px 20px;
      margin: 8px 0;
      display: inline-block;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
    }

    input[type=submit] {
      width: 100%;
      background-color: #4CAF50;
      color: white;
      padding: 14px 20px;
      margin: 8px 0;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }

    input[type=submit]:hover {
      background-color: #45a049;
    }

    }
    </style>
    """)

    print("""<div class=\"gallery_intro\ id=\"header_info\"><H1 id=\"header_title\">Search Result(s) for Image(s)</H1>
             <H3 id=\"header_description\">For Search Type: {}</H3><p>Select Image Below to View it!<p>
          </div>""".format(search_type));

    print("<div class=\"columnleft\"><div class=\"image-panel\" id=\"image_display\"></div></div>")
    print("""<div class=\"columnright\">
                 <div class=\"detail-panel\">
                     <img id=\"display_image\" alt=\"place image here\"></img>
                     <div class=\"display-icons\">
                     <button class=\"icon\" type=\"button\" id=\"del_image\">Delete Image</button>
                     <button class=\"icon\" type=\"button\" id=\"edit_image\">Edit Information</button>
                     </div>
                     <div class=\"display-detail\" id=\"display_detail\"></div>
                     <form id=\"detail_update\" target=\"display_gallery.py\" action=\"filehandler.py\" method = \"post\" hidden = \"true\"></form>
                     <form id=\"artist_update\" action=\"filehandler.py\" method = \"post\" hidden = \"true\"></form>
                     <form id=\"gallery_update\" target=\"display_gallery.py\" action=\"filehandler.py\" method = \"post\" hidden =\"true\"></form>
                     <form id=\"delete_image\" target=\"display_gallery.py\" action = \"filehandler.py\" method = \"post\" hidden =\"true\"></form>
                     <div id=\"artist_display\"><button type=\"button\" id=\"artist_button\">View Artist Info</button>
                     <H1 id=\"artist_information\"></H1>
                     </div>
                 </div>
             </div>""")


    print(""" <script>
            function update_detail(detail_id){
                var detail_item = detailPerImage[detail_id];
                var image_item = imageInfo[detail_item[1]];
                console.log(detail_item);
                console.log(image_item[1]);
                var detail_element = document.getElementById("display_detail");
                var form_element = document.getElementById(\"detail_update\");
                var edit_element = document.getElementById("edit_image");
                edit_element.addEventListener("click", function() {
                    detail_element.hidden = true;
                    form_element.hidden = false;
                    form_element.innerHTML=`
                     Detail ID: <input type=\"number\" name=\"upd_detail_id\" value=\"${detail_id}\" hidden=\"true\"required><br>
                     Image ID: <input type=\"number\" name=\"upd_image_id\" value=\"${image_item[0]}\" hidden=\"true\" required><br>
                     Title: <input type = \"text\" name = \"upd_image_title\" value=\"${image_item[1]}\" required><br> 
                     Link: <input type = \"text\" name=\"upd_image_link\" value=\"${image_item[2]}\" required><br>  
                     Enter the detail of image <br>  
                     Year: <input type = \"number\" name = \"upd_detail_year\" value=\"${detail_item[2]}\" required><br> 
                     Type: <input type = \"text\" name = \"upd_detail_type\" value=\"${detail_item[3]}\" required><br> 
                     Width: <input type = \"number\" name = \"upd_detail_width\" value=\"${detail_item[4]}\" required><br> 
                     Height: <input type = \"number\" name = \"upd_detail_height\" value=\"${detail_item[5]}\" required><br> 
                     Location: <input type = \"text\" name = \"upd_detail_location\" value=\"${detail_item[6]}\" required><br> 
                     Description: <input type = \"text\" name = \"upd_detail_description\" value=\"${detail_item[7]}\" required><br>
                     <input type = "hidden" value=${image_item[3]} name=\"gallery_id\"><br>
                     <input type=\"submit\" value=\"Update Detail\">`;
                });
                form_element.onsubmit = function(){ setTimeout(function () { window.location.reload(); }, 1500); };
            }

            function update_artist(artist_id){
                var artist_item = artistInfo[artist_id];
                console.log(artist_item);
                var element = document.getElementById(\"artist_update\");
                element.hidden = false;
                element.innerHTML = `UPDATE ARTIST INFORMATION<br>
                    Name: <input type = \"text\" name = \"upd_artist_name\" value=\"${artist_item[1]}\" required><br>
                    Birth Year: <input type = \"number\" name = \"upd_artist_birthyear\" value=${artist_item[2]} required><br> 
                    Country: <input type = \"text\" name =\"upd_artist_country\" value=\"${artist_item[3]}\" required><br>
                    Description: <input type =\"text\" name=\"upd_artist_description\" value=\"${artist_item[4]}\" required><br>
                    Artist ID: <input type =\"number\" name=\"upd_artist_id\" value = \"${artist_id}\" required>
                    <input type =\"submit\" value=\"Update Artist\">`;
            }

            function update_gallery(gallery_id){
                var form_element = document.getElementById("gallery_upd_form");
                form_element.onsubmit = function() { setTimeout(function() {window.location.reload(); }, 1500); };
                form_element.submit();
            }

            function delete_image(detail_id, image_id){
                var element = document.getElementById("del_image");
                var form_element = document.getElementById("delete_image");
                form_element.innerHTML = `
                    Image ID: <input type = \"number\" name = \"del_image_id\" value=${image_id} required><br>
                    Detail ID: <input type = \"number\" name = \"del_detail_id\" value=${detail_id} required>`;
                console.log(detail_id);
                console.log(image_id);
                element.addEventListener("click", function() {
                    form_element.submit();
                    setTimeout(function () { window.location.reload(); }, 1500);
                });
            }

            function artistInfo(detail_id){
                var detail_item = detailPerImage[detail_id];
                var image_item = imageInfo[detail_item[1]];
                var artist_item = artistInfo[image_item[4]];
                var artist_button = document.getElementById("artist_button");
                var element = document.getElementById("artist_information");
                element.hidden = true;
                artist_button.addEventListener("click", function() {
                        element.hidden = false;
                        element.innerHTML = `Name: ${artist_item[1]}<br>
                            Birth Year: ${artist_item[2]}<br>
                            Country: ${artist_item[3]}<br>
                            Description: ${artist_item[4]}<br>`;   
                });
                
               // element.addEventListener(\"click\", function() {update_artist(artist_item[0]);});
            }

            function addImage() {
                var form_element = document.getElementById("add_image_form");
                form_element.onsubmit = function() { setTimeout(function() {window.location.reload(); }, 1500); };
                form_element.submit();
            }

            function display_image(image_id){
                var element = document.getElementById("display_image");
                element.src = `${imageInfo[image_id][2]}`;
            }

            function show_images(){
                for (var key in imageInfo) {
                    if (imageInfo.hasOwnProperty(key)) {
                        var id = imageInfo[key][5] + \"_\" + key;
                        var elem = document.getElementById(id);
                        if(elem.hidden == true){
                            elem.hidden = false;
                        }
                        else{
                            elem.hidden = true;
                        }
                    }
                }
            }

            function show_detail(detail_id){
                var element = document.getElementById("display_detail");
                document.getElementById("detail_update").hidden = true;
                element.hidden = false;
                var detail_item = detailPerImage[detail_id];
                console.log(detail_item);
                element.innerHTML = `<H1>Year: ${detail_item[2]}<br>Type: ${detail_item[3]}<br>Width: ${detail_item[4]}<br>Height: ${detail_item[5]}<br>Location: ${detail_item[6]}<br>Description: ${detail_item[7]}</H1>`;
                
            }

            function image_to_gallery(){
                for (var key in imageInfo) {
                    if (imageInfo.hasOwnProperty(key)) {
                        console.log(key + " -> " + imageInfo[key]);
                        var element = document.createElement(\"DIV\");
                        element.className = "thumbnail";
                        element.id = imageInfo[key][5] + \"_\" + key;
                        element.hidden=true;
                        document.getElementById(\"image_display\").appendChild(element);
        
                        var img_elem = document.createElement(\"IMG\");
                        var info_elem = document.createElement("p");
                        img_elem.src = imageInfo[key][2];
                        info_elem.innerHTML = `Title: ${imageInfo[key][1]}<br>Link: ${imageInfo[key][2]}`;
                        //element.id = gallery_id + \"_\" + i;
                        img_elem.alt = \"image\";
                        img_elem.width=\"250\";
                        img_elem.height=\"250\";
                        var detail_id = imageInfo[key][5];
                        var image_id = imageInfo[key][0];
                        element.addEventListener(\"click\",
                        function(detail_id_, image_id_) {
                            return function() {
                                display_image(image_id_);
                                show_detail(detail_id_);
                                update_detail(detail_id_);
                                delete_image(detail_id_, image_id_);
                                artistInfo(detail_id_);
                        }; }(detail_id, image_id));
                        element.appendChild(img_elem);
                        element.appendChild(info_elem);
                        //document.getElementById(\"image_display\").appendChild(element);
                    }
                }
            }

            function detail_to_image(){
                var keys = Object.keys(imageInfo);
                console.log(imageInfo);
                for(i = 0; i < keys.length; i++){
                    var item = detailPerImage[keys[i]];
                    var detail_id = item[0];
                    var element = document.createElement("\H1\");
                    element.id = \"detail\" + detail_id;
                    element.innerHTML = "Year: " + item[2] + "<br>Type: " + item[3] + "<br>Width: " + item[4] + "<br>Height: " + item[5] + "<br>Location: " + item[6] + "<br>Description: " + item[7]; 
                    element.hidden = true;
                    element.addEventListener(\"click\", function (_id){ return function() {artistInfo(_id); }; }(detail_id) );
                    document.getElementById(\"detail_display\").appendChild(element);
                }

            }
            </script>""")


    #aggregate all relevant data and place it in script for access within script portion of code
    detail_result = {} #key-value where key is detail_id and value is the tuple found in detail table for given detail_id 
    artist_result = {} #key-value where key is artist id found from image query and value is tuple in artist table for given artist id
    image_result_ = {} #key-value where key is image id and value is tuple found in image table for given image id

    for row in images:
        if len(row) > 0:
            i_id = row[0]
            title = row[1]
            link = row[2]
            g_id = row[3]
            a_id = row[4]
            d_id = row[5]
            image_result_[i_id] = row;
            artist_result[a_id] = list_artist(a_id)
            detailPerImage = list_detail(i_id)
            detail_result[d_id] = detailPerImage


    #for key, value in image_result.items():
    #    for item in value:
    #        print(""" <script>
    #        var arr = new Array({}, \"{}\", \"{}\", {}, {}, {});
    #        imagesPerGallery[{}].push(arr);
    #        </script>""".format(item[0], item[1], item[2], item[3], item[4], item[5], key))


    for key, value in detail_result.items():
        print(""" <script>
              var arr = new Array({}, {}, {}, \"{}\", {}, {}, \"{}\", \"{}\");
              detailPerImage[{}] = arr;
            </script>""".format(value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], key))

    for key, value in artist_result.items():
        print(""" <script>
                  artistInfo[{}] = new Array({}, \"{}\", {}, \"{}\", \"{}\");
                  </script> """.format(key, value[0], value[1], value[2], value[3], value[4]))

    for key, value in image_result_.items():
        print(""" <script> imageInfo[{}] = new Array({}, \"{}\", \"{}\", {}, {}, {}) </script>""".format(key, value[0], value[1], value[2], value[3], value[4], value[5]))

    print("<script> image_to_gallery();  </script>")

    print("<script> show_images(); </script>")

if len(artists) > 0:
    print("""
    <style>
    body{

        background: #ECE9E6;  /* fallback for old browsers */
        background: -webkit-linear-gradient(to right, #FFFFFF, #ECE9E6);  /* Chrome 10-25, Safari 5.1-6 */
        background: linear-gradient(to right, #FFFFFF, #ECE9E6); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
    }
    #artist_view div{
        margin: 20px;
        border: 2px solid black;
        border-radius: 5px;
        background: #ED4264;  /* fallback for old browsers */
        background: -webkit-linear-gradient(to right, #FFEDBC, #ED4264);  /* Chrome 10-25, Safari 5.1-6 */
        background: linear-gradient(to right, #FFEDBC, #ED4264); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

    }

    #artist_info{
        text-align: center;
    }
    
    input[type=text], select {
      width: 50%;
      padding: 12px 20px;
      margin: 8px 0;
      display: inline-block;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
    }

    input[type=number], select {
      width: 50%;
      padding: 12px 20px;
      margin: 8px 0;
      display: inline-block;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
    }

    input[type=submit] {
      width: 50%;
      background-color: #4CAF50;
      color: white;
      padding: 14px 20px;
      margin: 8px 0;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }

    input[type=submit]:hover {
      background-color: #45a049;
    }

        
    </style>
    """)
    print("""<script> artistInfo = {}

                function edit_artist(artist_id){
                    var form_element = document.getElementById("edit_artist_form");
                    artist_item = artistInfo[artist_id];
                    form_element.hidden = false;
                    form_element.innerHTML = `UPDATE ARTIST INFORMATION<br>
                        Name: <input type = \"text\" name = \"upd_artist_name\" value=\"${artist_item[1]}\" required><br>
                        Birth Year: <input type = \"number\" name = \"upd_artist_birthyear\" value=${artist_item[2]} required><br> 
                        Country: <input type = \"text\" name =\"upd_artist_country\" value=\"${artist_item[3]}\" required><br>
                        Description: <input type =\"text\" name=\"upd_artist_description\" value=\"${artist_item[4]}\" required><br>
                        Artist ID: <input type =\"number\" name=\"upd_artist_id\" value = \"${artist_id}\" required>
                        <input type =\"submit\" value=\"Update Artist\">`;
                    form_element.onsubmit = function(){ setTimeout(function () { window.location.reload(); }, 1500); };
                }
    
    
                function display_artists(){
                    for (var key in artistInfo) {
                        if (artistInfo.hasOwnProperty(key)) {
                            var artist_view = document.getElementById("artist_view");
                            var element = document.createElement("DIV");
                            element.addEventListener("click", function(artist_id){
                                return function(){
                                edit_artist(artist_id);
                                };
                            }(artistInfo[key][0]));
                            element.id = key;
                            var info = document.createElement("H1");
                            info.innerHTML = `Artist ID: ${artistInfo[key][0]}<br>Name: ${artistInfo[key][1]}<br>Birth Year: ${artistInfo[key][2]}<br>Country: ${artistInfo[key][3]}<br>
                            Description: ${artistInfo[key][4]}`;
                            element.append(info);
                            artist_view.append(element);
                        }
                    }
                }
            </script>""")
    print("""
             <div id="header"><H1>Search Results for Artist(s)<br>Type: {}</H1><p>Select Artist Box to modify contents!</p></div>
             <div id="artist_view"> </div>
             <div id="artist_info"><form action="filehandler.py" target="display_search.py" hidden="true" id="edit_artist_form"></form></div>
        """.format(search_type))
    
    for row in artists:
        if len(row) > 0:
            artist_id = row[0]
            name = row[1]
            birth_year = row[2]
            country = row[3]
            description = row[4]
            print(""" <script>
                     artistInfo[{}] = new Array({}, \"{}\", {}, \"{}\", \"{}\");
                     </script> """.format(artist_id, artist_id, name, birth_year, country, description))
    print("<script> display_artists(); </script>")

if(len(artists) == 0 and artist_search):
    print("<H1>No Artist(s) Found with Search Query</H1>")

if(len(images) == 0 and image_search):
    print("<H1>No Image(s) Found with Search Query</H1>")
    
db.close()

