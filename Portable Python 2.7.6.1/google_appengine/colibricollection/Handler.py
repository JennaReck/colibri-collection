import webapp2
import jinja2
import os
import time
import datetime
import random
import hashlib
import hmac
import urllib
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from google.appengine.api import urlfetch
from google.appengine.ext.ndb.key import Key

jinja_environment = jinja2.Environment(extensions=['jinja2.ext.autoescape'],autoescape=True,
										 loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),
										'templates')))
secret = "Ec3ifP6wGmS"

class Handler(webapp2.RequestHandler):

    def write(self, *a, **na):
        self.response.out.write(*a, **na)
    
    def render_str(self, template, **params):
        t = jinja_environment.get_template(template)
        return t.render(params)
    
    def render(self, template, **na):
        self.write(self.render_str(template, **na))

    def make_pagination(self, p, url_parameters, products, products_per_page):
        html = ""
        if not p:
            p = 1
        try:
            int(p)
        except:
            return False
        p = int(p)
        if len(products)%products_per_page != 0:
            all_pages = (len(products)/products_per_page) + 1
        else:
            all_pages = len(products)/products_per_page
        if all_pages < 1:
            all_pages = 1
        if p > all_pages:
            return False #checks if p is higher than all_pages, redirect to 404
        if not p or p == 1:
            html += "<div id='pagination'><span class='prev-next-unused'>prev</span> <span class='pagination-current'>1</span> "
            if all_pages > 1 and all_pages <= 5:
                for page_num in range(2, all_pages + 1):
                    html += (" <a href='/search" + url_parameters + "&p=" + str(page_num) +
                            "' class='pagination-noncurrent'>" + str(page_num) + "</a>")
                        
                html += " <a href='/search" + url_parameters + "&p=2' class='prev-next-used'>next</a></div>"
            if all_pages == 1:
                html += " <span class='prev-next-unused'>next</span></div>"
            if all_pages > 5:
                for page_num in range(2, 6):
                    html += (" <a href='/search" + url_parameters + "&p=" + str(page_num) +
                            "' class='pagination-noncurrent'>" + str(page_num) + "</a>")
                        
                html += (" <span class='pagination-ellipses'>...</span> <a href='/search" +
                        url_parameters + "&p=2' class='prev-next-used'>next</a></div>")
        else:
            html += ("<div id='pagination'><a href='/search" + url_parameters +
                    "&p=" + str(p - 1) + "' class='prev-next-used'>prev</a>")
            if p <= 4:
                if all_pages <= 5:
                    for page_num in range(1, all_pages + 1):
                        if page_num == p:
                            html += " <span class='pagination-current'>" + str(p) + "</span>"
                        else:
                            html += (" <a href='/search" + url_parameters + "&p=" + str(page_num) +
                                                                                                 "' class='pagination-noncurrent'>" + str(page_num) + "</a>")
                    if p == all_pages:
                        html += " <span class='prev-next-unused'>next</span></div>"
                    else:
                        html += (" <a href='/search" + url_parameters + "&p=" + str(p + 1) +
                                "' class='prev-next-used'>next</a></div>")
                else:
                    for page_num in range(1, 6):
                        if page_num == p:
                            html += " <span class='pagination-current'>" + str(p) + "</span>"
                        else:
                            html += (" <a href='/search" + url_parameters +
                                    "&p=" + str(page_num) + "'>" + str(page_num) + "</a>")
                                        
                    html += (" <span class='pagination-ellipses'>...</span> <a href='/search" +
                             url_parameters + "&p=" + str(p + 1) +
                             "' class='prev-next-used'>next</a></div>")
            else:
                html += (" <a href='/search" + url_parameters + "&p=" + str(p - 2) +
                         "' class='pagination-noncurrent'>" + str(p - 2) + "</a>" +
                         " <a href='/search" + url_parameters + "&p=" +
                         str(p - 1) + "' class='pagination-noncurrent'>" +
                         str(p - 1) + "</a>" + " <span class='pagination-current'>" +
                         str(p) + "</span>")
                    
                if all_pages > p + 2:
                    for nextpage in [p + 1, p + 2]:
                        html += (" <a href='/search" + url_parameters + "&p=" + str(nextpage) +
                                "' class='pagination-noncurrent'>" + str(nextpage) + "</a>")
                    if p + 2 == all_pages:
                        html += (" <a href='/search" + url_parameters + "&p=" + str(p + 1) +
                                "' class='prev-next-used'>next</a></div>")
                    else:
                        html += (" <span class='pagination-ellipses'>...</span> <a href='/search" +
                                 url_parameters + "&p=" + str(p + 1) +
                                 "' class='prev-next-used'>next</a></div>")
                if p + 1 == all_pages:
                    html += (" <a href='/search" + url_parameters + "&p=" + str(p + 1) +
                             "' class='pagination-current'>" + str(p + 1) +
                             "</a> <a href='/search" + url_parameters + "&p=" + str(p + 1) +
                             "' class='prev-next-used'>next</a></div>")
                if p == all_pages:
                    html += " <span class='prev-next-unused'>next</span></div>"
        return html

    def next_content(self, p, content, items_per_page):
        if not p or p == "1" or p == 1:
            return content[:items_per_page]
        try:
            int(p)
        except:
            return False
        p = int(p)
        if items_per_page * (p - 1) + 1 > len(content):
            return False
        else:
            return content[(p - 1) * items_per_page:p * items_per_page]
       

    def make_cookie(self, admin):
            user_cookie = admin.key.id()
            hash_start = str(user_cookie)[:10]
            user_hash = hmac.new(secret, hash_start).hexdigest()
            return user_cookie, user_hash
	
    def make_salt(self):                                
        salt = ""
        for x in range(0,5):
            salt += chr(random.randrange(97,123))
        return salt
                    
    def make_pw_hash(self, name, pw, salt=None):
        if salt == None:
            salt = self.make_salt()
        h = hashlib.sha256(name + pw + salt).hexdigest()
        return '%s,%s' % (h, salt)
                    
    def valid_password(self, username, password, h):
            salt = h.split(",")[1]
            return h == self.make_pw_hash(username, password, salt)

    def cookie_check(self, cookies, admin_check=False):
        if len(cookies) > 5:
            cookie_user_id, cookie_user_hash = cookies.split("|")
            hash_start = str(cookie_user_id)[:10]
            cookie_username = UserDB.get_by_id(int(cookie_user_id))
            if cookie_username == None:
                return False
            else:
                cookie_username = cookie_username.username
                if cookie_user_hash == hmac.new(secret, hash_start).hexdigest():
                    if admin_check == True:
                        if cookie_username == "jreck21":
                            return True
                        else:
                            return False
                    return True
                else:
                    return False
        else:
            return False

    def user_check(self):
        cookies = self.request.cookies.get('username',"0|0")
        return self.cookie_check(cookies), int(cookies.split("|")[0])

    def admin_user_check(self):
        cookies = self.request.cookies.get('username',"0|0")
        return self.cookie_check(cookies, True)

    def locked_out(self):
        lockout = memcache.get("lockout")
        if lockout:
            return True
        else:
            return False

    def update_failed_logins(self):
        failed_logins = memcache.get("failed_logins")
        if not failed_logins:
            #set memcache to expire in 1 hour, set current time in list.
            memcache.set("failed_logins", [1, time.time()], 3600)
        else:
            if failed_logins[0] + 1 >= 5:
                memcache.set("lockout", True, 3600) #set lockout to last 1 hour
            else:
                #set new expiration time based on time set minus
                #difference of time set and current time
                #(updating this makes sure it still expires in an hour)
                memcache.set("failed_logins",
                            [failed_logins[0] + 1,
                            failed_logins[1]],
                            3600 - (time.time() - failed_logins[1]))

    def truncate_and_strip_html(self, text, length):
        html_tags = ["<p>", "</p>", "<h3>", "</h3>"]
        for tag in html_tags:
            text = text.replace(tag, "")
        return text[:length].rsplit(" ", 1)[0] + "..."

    def get_hum_cache(self, cache_type, clear=False):
        if clear == True:
            memcache.delete(cache_type + "_pt1")
            memcache.delete(cache_type + "_pt2")
            memcache.delete(cache_type + "_pt3")
        part1 = memcache.get(cache_type + "_pt1")
        part2 = memcache.get(cache_type + "_pt2")
        part3 = memcache.get(cache_type + "_pt3")
        if part1 and part2 and part3:
            return part1 + part2 + part3
        hum_list = []
        if cache_type == "full_hum_list":
            id_order = range(1,343)
            #hum_list = SpeciesDB.query().order(SpeciesDB.common_name).fetch()
        if cache_type == "full_family_hum_list":
            id_order = [56, 335, 68, 60, 164, 236, 282, 202, 34, 268, 275, 252, 158, 134, 315, 191, 170, 176, 173, 133, 82, 197, 212, 230, 276, 97, 279, 320, 64, 178, 283, 339, 251, 203, 267, 13, 102, 272, 215, 336, 257, 30, 293, 306, 180, 6, 175, 40, 2, 17, 186, 321, 316, 77, 317, 167, 11, 47, 76, 265, 119, 248, 210, 162, 218, 81, 274, 85, 241, 295, 302, 138, 146, 141, 65, 285, 36, 10, 168, 35, 142, 294, 153, 135, 266, 27, 232, 340, 73, 163, 166, 108, 324, 342, 67, 292, 78, 3, 184, 12, 224, 183, 15, 8, 91, 66, 331, 179, 171, 297, 237, 157, 313, 245, 235, 194, 246, 104, 174, 129, 240, 319, 227, 59, 199, 238, 45, 337, 58, 41, 149, 114, 125, 75, 92, 118, 214, 46, 80, 260, 94, 86, 195, 160, 233, 126, 53, 123, 61, 122, 50, 130, 226, 70, 332, 18, 83, 308, 62, 270, 63, 338, 137, 43, 54, 96, 298, 136, 23, 172, 225, 341, 189, 262, 42, 147, 327, 89, 281, 100, 88, 32, 39, 289, 127, 250, 84, 124, 26, 90, 121, 185, 152, 221, 79, 280, 38, 278, 22, 330, 19, 325, 209, 299, 69, 155, 161, 165, 5, 182, 286, 201, 111, 231, 128, 223, 131, 244, 208, 103, 144, 304, 105, 33, 291, 211, 51, 177, 277, 29, 220, 117, 322, 49, 44, 242, 256, 305, 193, 4, 222, 334, 159, 48, 318, 143, 154, 115, 249, 258, 247, 151, 31, 288, 200, 72, 273, 333, 188, 323, 259, 106, 239, 95, 28, 113, 287, 204, 269, 16, 296, 253, 307, 110, 205, 196, 20, 87, 290, 309, 264, 263, 261, 219, 52, 192, 14, 312, 98, 7, 326, 25, 148, 9, 37, 140, 314, 71, 109, 116, 254, 206, 99, 57, 328, 284, 150, 132, 21, 216, 198, 229, 311, 120, 74, 310, 55, 234, 1, 255, 169, 139, 213, 301, 156, 187, 303, 145, 112, 300, 101, 190, 181, 207, 271, 93, 107, 228, 24, 329, 217, 243]
            #hum_list = SpeciesDB.query().order(SpeciesDB.subfamily).order(SpeciesDB.binomial_name).fetch()
        if cache_type == "full_s_to_l_hum_list":
            id_order = [16, 129, 264, 261, 269, 28, 104, 120, 174, 239, 246, 255, 287, 296, 340, 46, 74, 36, 73, 89, 95, 99, 102, 113, 206, 224, 259, 79, 84, 149, 219, 240, 310, 323, 327, 12, 319, 22, 27, 77, 86, 91, 106, 114, 234, 305, 3, 195, 1, 15, 26, 34, 41, 49, 72, 75, 80, 100, 127, 141, 166, 172, 184, 213, 216, 217, 230, 232, 260, 263, 272, 282, 320, 322, 342, 191, 242, 298, 9, 92, 125, 209, 233, 247, 249, 258, 271, 299, 311, 189, 204, 17, 21, 23, 32, 40, 47, 54, 55, 60, 69, 81, 82, 85, 88, 96, 108, 117, 118, 126, 136, 150, 158, 160, 161, 162, 167, 173, 182, 183, 190, 210, 218, 225, 243, 288, 290, 295, 321, 324, 163, 192, 279, 302, 303, 76, 101, 139, 145, 238, 278, 94, 2, 6, 8, 11, 13, 38, 39, 42, 43, 44, 65, 87, 109, 110, 111, 121, 128, 138, 165, 175, 186, 196, 201, 205, 214, 241, 248, 265, 267, 274, 286, 289, 291, 300, 307, 316, 318, 330, 53, 112, 5, 37, 137, 146, 159, 187, 222, 314, 333, 334, 341, 155, 169, 262, 328, 35, 58, 61, 63, 64, 67, 78, 90, 119, 131, 142, 143, 154, 168, 177, 193, 200, 208, 221, 223, 227, 231, 236, 237, 244, 266, 284, 294, 309, 317, 325, 336, 337, 203, 276, 4, 10, 71, 97, 115, 152, 153, 211, 273, 277, 56, 140, 292, 329, 19, 30, 33, 45, 50, 51, 52, 57, 62, 98, 105, 124, 134, 144, 147, 164, 170, 171, 181, 185, 197, 202, 207, 215, 220, 245, 253, 254, 257, 301, 304, 312, 331, 338, 339, 48, 18, 194, 198, 29, 20, 25, 59, 66, 70, 122, 123, 135, 148, 179, 235, 250, 270, 275, 283, 313, 315, 332, 335, 285, 83, 130, 252, 308, 7, 68, 157, 178, 199, 226, 268, 297, 326, 103, 176, 188, 251, 151, 14, 133, 212, 280, 156, 180, 306, 256, 132, 229, 31, 93, 107, 116, 293, 281, 24, 228]
            #hum_list = SpeciesDB.query().order(SpeciesDB.male_length).order(SpeciesDB.common_name).fetch()
        if cache_type == "full_l_to_s_hum_list":
            id_order = [228, 24, 281, 107, 116, 293, 93, 31, 132, 229, 256, 306, 180, 156, 14, 133, 212, 280, 151, 176, 188, 251, 103, 7, 68, 157, 178, 199, 226, 268, 297, 326, 83, 130, 252, 308, 285, 20, 25, 59, 66, 70, 122, 123, 135, 148, 179, 235, 250, 270, 275, 283, 313, 315, 332, 335, 29, 18, 194, 198, 48, 19, 30, 33, 45, 50, 51, 52, 57, 62, 98, 105, 124, 134, 144, 147, 164, 170, 171, 181, 185, 197, 202, 207, 215, 220, 245, 253, 254, 257, 301, 304, 312, 331, 338, 339, 56, 140, 292, 329, 4, 10, 71, 97, 115, 152, 153, 211, 273, 277, 203, 276, 35, 58, 61, 63, 64, 67, 78, 90, 119, 131, 142, 143, 154, 168, 177, 193, 200, 208, 221, 223, 227, 231, 236, 237, 244, 266, 284, 294, 309, 317, 325, 336, 337, 155, 169, 262, 328, 5, 37, 137, 146, 159, 187, 222, 314, 333, 334, 341, 53, 112, 2, 6, 8, 11, 13, 38, 39, 42, 43, 44, 65, 87, 109, 110, 111, 121, 128, 138, 165, 175, 186, 196, 201, 205, 214, 241, 248, 265, 267, 274, 286, 289, 291, 300, 307, 316, 318, 330, 94, 76, 101, 139, 145, 238, 278, 163, 192, 279, 302, 303, 17, 21, 23, 32, 40, 47, 54, 55, 60, 69, 81, 82, 85, 88, 96, 108, 117, 118, 126, 136, 150, 158, 160, 161, 162, 167, 173, 182, 183, 190, 210, 218, 225, 243, 288, 290, 295, 321, 324, 189, 204, 9, 92, 125, 209, 233, 247, 249, 258, 271, 299, 311, 191, 242, 298, 1, 15, 26, 34, 41, 49, 72, 75, 80, 100, 127, 141, 166, 172, 184, 213, 216, 217, 230, 232, 260, 263, 272, 282, 320, 322, 342, 3, 195, 22, 27, 77, 86, 91, 106, 114, 234, 305, 12, 319, 79, 84, 149, 219, 240, 310, 323, 327, 36, 73, 89, 95, 99, 102, 113, 206, 224, 259, 46, 74, 28, 104, 120, 174, 239, 246, 255, 287, 296, 340, 261, 269, 264, 129, 16]
            #hum_list = SpeciesDB.query().order(-SpeciesDB.male_length).order(SpeciesDB.common_name).fetch()
        if cache_type == "full_date_hum_list":
            id_order = [127, 80, 196, 231, 170, 84, 38, 282, 259, 205, 66, 284, 247, 64, 209, 299, 87, 24, 206, 288, 190, 246, 180, 293, 332, 320, 215, 148, 218, 307, 97, 143, 276, 56, 76, 104, 82, 263, 92, 71, 138, 156, 204, 291, 86, 21, 37, 245, 273, 340, 186, 69, 90, 110, 244, 256, 269, 111, 101, 146, 174, 330, 120, 323, 14, 22, 60, 89, 159, 162, 184, 200, 222, 318, 199, 243, 310, 285, 187, 58, 114, 306, 2, 99, 109, 175, 195, 208, 342, 15, 47, 96, 302, 34, 173, 77, 103, 191, 264, 294, 36, 226, 261, 279, 40, 223, 26, 125, 130, 164, 172, 45, 68, 158, 161, 194, 217, 249, 255, 283, 289, 292, 327, 329, 334, 339, 16, 144, 122, 201, 237, 336, 12, 13, 25, 33, 42, 57, 74, 78, 79, 147, 181, 188, 197, 224, 250, 268, 326, 335, 6, 27, 31, 32, 44, 49, 62, 70, 98, 105, 107, 124, 128, 131, 136, 145, 154, 155, 227, 238, 253, 254, 265, 270, 274, 301, 308, 309, 315, 316, 341, 65, 314, 317, 18, 28, 72, 141, 149, 150, 167, 176, 202, 211, 220, 257, 258, 260, 278, 303, 304, 305, 311, 81, 100, 298, 319, 182, 83, 88, 123, 129, 140, 193, 235, 272, 286, 20, 59, 63, 73, 91, 102, 132, 189, 212, 216, 239, 240, 281, 5, 7, 30, 39, 50, 115, 118, 121, 163, 219, 312, 94, 133, 61, 95, 134, 241, 52, 67, 75, 126, 142, 151, 192, 252, 271, 275, 290, 313, 337, 169, 17, 179, 297, 1, 8, 11, 48, 160, 198, 248, 321, 4, 54, 55, 137, 139, 183, 185, 207, 116, 106, 277, 108, 166, 331, 23, 171, 165, 213, 251, 262, 266, 295, 322, 324, 333, 19, 35, 113, 338, 51, 117, 229, 135, 177, 214, 41, 29, 43, 85, 112, 119, 210, 225, 234, 236, 242, 280, 300, 3, 53, 153, 157, 287, 10, 178, 203, 221, 328, 9, 46, 93, 152, 168, 228, 230, 232, 233, 267, 296, 325]
            #hum_list = SpeciesDB.query().order(-SpeciesDB.discovery_date).order(SpeciesDB.common_name).fetch()
        if cache_type == "full_rarity_hum_list":
            id_order = [26, 37, 79, 84, 127, 169, 247, 259, 289, 21, 38, 77, 104, 120, 156, 162, 164, 186, 188, 205, 215, 231, 245, 256, 293, 307, 18, 36, 71, 95, 99, 174, 190, 208, 330, 16, 32, 88, 106, 161, 163, 166, 170, 181, 189, 194, 206, 209, 251, 282, 312, 331, 341, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 19, 20, 22, 23, 24, 25, 27, 28, 29, 30, 31, 33, 34, 35, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 72, 73, 74, 75, 76, 78, 80, 81, 82, 83, 85, 86, 87, 89, 90, 91, 92, 93, 94, 96, 97, 98, 100, 101, 102, 103, 105, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 121, 122, 123, 124, 125, 126, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 157, 158, 159, 160, 165, 167, 168, 171, 173, 175, 176, 177, 178, 179, 180, 182, 183, 184, 185, 187, 191, 192, 193, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 207, 210, 211, 212, 213, 214, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 246, 248, 249, 250, 252, 253, 254, 255, 257, 258, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 283, 284, 285, 286, 287, 288, 290, 291, 292, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 308, 309, 310, 311, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 332, 333, 334, 335, 336, 337, 338, 339, 340, 342, 172]
            #hum_list = SpeciesDB.query().order(SpeciesDB.rarity_rank).order(SpeciesDB.common_name).fetch()
        for num in id_order:
            hum_list.append(SpeciesDB.get_by_id(num))
        memcache.set(cache_type + "_pt1", hum_list[:100])
        memcache.set(cache_type + "_pt2", hum_list[100:200])
        memcache.set(cache_type + "_pt3", hum_list[200:])
        return hum_list

    def get_midnight_seconds(self):
	h, m, s = time.strftime("%H:%M:%S").split(":")
	s_dif = 60-int(s)
	m_dif = 59-int(m)
	h_dif = 23-int(h)
	return s_dif + (m_dif * 60) + (h_dif * 60 * 60)

    def get_featured_hum(self):
        f_hum = memcache.get("featured_hum")
        if f_hum:
            return f_hum
        hum_list = self.get_hum_cache("full_hum_list")
        f_hum = hum_list[random.randrange(1,343)]
        expire_time = self.get_midnight_seconds()
        memcache.set("featured_hum", f_hum, expire_time)
        return f_hum

    def get_locations_cache(self, clear=False):
        if clear == True:
            memcache.delete("hum_locations_list")
        hum_locations_list = memcache.get("hum_locations_list")
        if hum_locations_list:
            return hum_locations_list
        locations_list = []
        hum_list = self.get_hum_cache("full_hum_list")
        for hum in hum_list:
            for location in hum.locations:
                if location not in locations_list:
                    locations_list.append(location)
        memcache.set("hum_locations_list", locations_list.sort())
        return locations_list

    def get_locations_html_cache(self, clear=False):
        if clear == True:
            memcache.delete("hum_locations_html")
        hum_locations_html = memcache.get("hum_locations_html")
        if hum_locations_html:
            return hum_locations_html
        hum_locations_html = ""
        hum_locations_list = self.get_locations_cache()
        for location in hum_locations_list:
            s_location = location.replace(" ", "-")
            s_location = s_location.replace(",", "+")
            hum_locations_html += '<option value="' + s_location + '">' + location + '</option>'
        memcache.set("hum_locations_html", hum_locations_html)
        return hum_locations_html

    def get_hum_dropdown_html(self, clear=False):
        if clear == True:
            memcache.delete("hum_dropdown_html")
        hum_dropdown_html = memcache.get("hum_dropdown_html")
        if hum_dropdown_html:
            return hum_dropdown_html
        hum_dropdown_html = ""
        hum_list = self.get_hum_cache("full_hum_list")
        for hum in hum_list:
            hum_dropdown_html += '<option value="' + hum.link + '">' + hum.common_name + '</option>'
        memcache.set("hum_dropdown_html", hum_dropdown_html)
        return hum_dropdown_html

    def make_fav_checkmark_html(self, hum, user_data, favorites_page=False):
        html_output = "<div class='sort-icon-container'>"
        if favorites_page:
            html_output += ("<a href='javascript:toggleMainFavorites(" +
                            str(hum.key.id()) +
                            ")' class='main-links favorites-undo-link hidden'>Undo remove from favorites?</a>")
            
        html_output += "<a href='javascript:toggle"
        if favorites_page:
            html_output += "Main"
        else:
            html_output += "Sort"
        html_output += ("Favorites(" + 
                        str(hum.key.id()) + 
                        ")'")
        if favorites_page:
            html_output += " class='favorites-icons'"
            
        html_output += ("><div id='favid" + 
                        str(hum.key.id()) + 
                        "' class='sort-icon ")
        if hum.key.id() in user_data.favorites_list:
            html_output += "sort-fav' title='Remove from favorites?'"
        else:
            html_output += "sort-not-fav' title='Add to favorites?'"
        html_output += "'></div></a><a href='/checklist'"
        if favorites_page:
            html_output += " class='favorites-icons'"
        html_output += "title='View checklist page'><img src='"
        if hum.key.id() in user_data.check_list:
            html_output += "/images/sort-checkmark.png'"
        else:
            html_output += "/images/sort-not-checkmark.png'"
        html_output += " alt='checkmark' /></a></div></div>"
        return html_output

    def make_name_only_hum_container(self, hum_list, user_data, favorites_page=False):
        html_output = ""
        odd = False
        for hum in hum_list:
            html_output += "<div class='sort-hum-container"
            if odd == True:
                html_output += " sort-odd"
            odd = not odd ### sets odd to opposite boolean value
            html_output += ("'><a href='" + hum.link +
                            "'><img src='" + 
                            hum.thumbnail.link + 
                            "' class='sort-hum-thumbnail thumb' alt='" + 
                            hum.common_name +
                            "' /></a><span class='sort-hum-name'><a href='" +
                            hum.link + "'>" +
                            hum.common_name + 
                            " (" + hum.binomial_name + 
                            ")</a></span>" +
                            self.make_fav_checkmark_html(hum, user_data, favorites_page=favorites_page))
        return html_output
            
    def make_alphabetical_html(self, user_data):
        html_output = memcache.get("alphabetical_sort")
        if html_output:
            return html_output
        hum_list = self.get_hum_cache("full_hum_list")
        html_output = ""
        if hum_list:
            hum = hum_list.pop(0)
        else:
            return html_output
        odd = False
        for current_letter in range(65, 91):
            if hum.common_name[0] == chr(current_letter):
                html_output += "<div class='main-headers'>" + chr(current_letter) + "</div>"
                while hum.common_name[0] == chr(current_letter):
                    html_output += "<div class='sort-hum-container"
                    if odd == True:
                        html_output += " sort-odd"
                    odd = not odd ### sets odd to opposite boolean value
                    html_output += ("'><a href='" + hum.link +
                                    "'><img src='" + 
                                    hum.thumbnail.link + 
                                    "' class='sort-hum-thumbnail thumb' alt='" + 
                                    hum.common_name +
                                    "' /></a><span class='sort-hum-name'><a href='" +
                                    hum.link + "'>" +
                                    hum.common_name +
                                    " (" + hum.binomial_name + 
                                    ")</a></span>" +
                                    self.make_fav_checkmark_html(hum, user_data))
                    if hum_list:
                        hum = hum_list.pop(0)
                    else:
                        break
        memcache.set("alphabetical_sort", html_output)
        return html_output
        
    def make_subfamily_html(self, user_data):
        html_output = memcache.get("subfamily_sort")
        if html_output:
            return html_output
        hum_list = self.get_hum_cache("full_family_hum_list")
        html_output = ""
        p_text = "<p>Hermits (from the subfamily Phaethornithinae) are tropical and subtropical hummingbirds comprising about 30-40 species. Their feathers are typically more muted or dull as opposed to their more iridescent counterparts. Most hermit species have a green, brown, rufous, or grey coloration. The males and females often share very similar plumage, with differences limited to bill shape, tail shape, and/or strength of coloration. Hummingbirds of this subfamily also typically have long, slightly decurved bills, but there is large variation from species to species.</p>"
        t_text = "<p>Typical hummingbirds (from the subfamily Trochilinae) are most commonly known for their iridescent plumage in metallic reds, oranges, greens, and blues. The Trochilinae subfamily is comprised of about 300 different species, displaying an incredible range of colors, sizes, and bill types. The males and females often exhibit broad differences in color, iridescence, and size. The majority of species live in tropical and subtropical climates, but several species also breed in temperate climates.</p>"
        html_output = "<div class='main-headers'>Subfamily Phaethornithinae</div>" + p_text
        previous_genus = ""
        odd = False
        new_subfamily = False
        for hum in hum_list:
            if hum.subfamily == "2nd" and new_subfamily == False:
                html_output += "<div class='main-headers'>Subfamily Trochilinae</div>" + t_text
                new_subfamily = True
            current_genus = hum.binomial_name.split(" ")[0]
            if current_genus != previous_genus:
                html_output += "<div class='main-subheaders'>Genus " + current_genus + "</div>"
                odd = False
            previous_genus = current_genus
            html_output += "<div class='sort-hum-container"
            if odd == True:
                html_output += " sort-odd"
            odd = not odd ### sets odd to opposite boolean value
            html_output += ("'><a href='" + 
                            hum.link + 
                            "'><img src='" + 
                            hum.thumbnail.link + 
                            "' class='sort-hum-thumbnail thumb' alt='" + 
                            hum.common_name + 
                            "' /></a><span class='sort-hum-name'><a href='" +
                            hum.link +
                            "'>" + hum.binomial_name +
                            " (" + hum.common_name +
                            ")</a></span>" +
                            self.make_fav_checkmark_html(hum, user_data))
        memcache.set("subfamily_sort", html_output)
        return html_output
                    
    def make_other_sort_html(self, sort_type, user_data):
        html_output = memcache.get(sort_type + "_sort")
        if html_output:
            return html_output
        if sort_type == "smallest-to-largest":
            hum_list = self.get_hum_cache("full_s_to_l_hum_list")
            html_output = "<div class='main-headers'>Smallest to Largest</div>"
        if sort_type == "largest-to-smallest":
            hum_list = self.get_hum_cache("full_l_to_s_hum_list")
            html_output = "<div class='main-headers'>Largest to Smallest</div>"
        if sort_type == "date-discovered":
            hum_list = self.get_hum_cache("full_date_hum_list")
            html_output = "<div class='main-headers'>Date Discovered</div>"
        if sort_type == "rarity":
            html_output = memcache.get("rarity_sort")
            hum_list = self.get_hum_cache("full_rarity_hum_list")
            html_output = "<div class='main-headers'>Rarity</div>"
        odd = False
        for hum in hum_list:
            html_output += "<div class='sort-hum-container"
            if odd == True:
                html_output += " sort-odd"
            odd = not odd ### sets odd to opposite boolean value
            html_output += ("'><a href='" +
                            hum.link +
                            "'><img src='" + 
                            hum.thumbnail.link + 
                            "' class='sort-hum-thumbnail thumb' alt='" + 
                            hum.common_name + 
                            "' /></a><table class='sort-hum-name'><tr><td><a href='" +
                            hum.link + "'>" +
                            hum.common_name + " (" + hum.binomial_name + 
                            ")</a></td></tr><tr><td>")
            if sort_type == "smallest-to-largest" or sort_type == "largest-to-smallest":
                html_output += "Male Length: " + str(hum.male_length) + " inches"
            if sort_type == "date-discovered":
                html_output += "Date discovered: " + str(hum.discovery_date)
            if sort_type == "rarity":
                html_output += "Conservation status: " + ["EX (extinct)","EW (extinct in the wild)","CR (critically endangered)","EN (endangered)","VU (vulnerable)","NT (near threatened)","LC (least concerned)", "DD (data deficient)"][hum.rarity_rank-1]
            html_output += ("</td></tr></table>" + 			
                            self.make_fav_checkmark_html(hum, user_data))
        memcache.set(sort_type + "_sort", html_output)
        return html_output
            
    def make_find_by_html(self, user_data, location="", colors=""):
        if location:
            hum_list = memcache.get(location+"1")
            hum_list2 = memcache.get(location+"2")
            hum_list3 = memcache.get(location+"3")
            if not hum_list:
                hum_list = SpeciesDB.query(SpeciesDB.locations.IN([location])).order(SpeciesDB.common_name).fetch()
                if len(hum_list) < 100:
                    memcache.set(location+"1", hum_list)
                elif len(hum_list) < 200:
                    memcache.set(location+"1", hum_list[:100])
                    memcache.set(location+"2", hum_list[100:])
                else:
                    memcache.set(location+"1", hum_list[:100])
                    memcache.set(location+"2", hum_list[100:200])
                    memcache.set(location+"2", hum_list[200:])
            else:
                if hum_list2:
                    hum_list += hum_list2
                if hum_list3:
                    hum_list += hum_list3
            html_output = "<div class='main-headers'>" + str(len(hum_list)) + " hummingbirds found in " + location + "</div>"
        elif colors:
            color_key = ""
            for color in colors:
                color_key += color
            hum_list = memcache.get(color_key+"1")
            hum_list2 = memcache.get(color_key+"2")
            hum_list3 = memcache.get(color_key+"3")
            if not hum_list:
                f_hum_list = self.get_hum_cache("full_hum_list")
                hum_list = []
                for hum in f_hum_list:
                    if set(colors).issubset(hum.colors):
                        hum_list.append(hum)
                if len(hum_list) < 100:
                    memcache.set(color_key+"1", hum_list)
                elif len(hum_list) < 200:
                    memcache.set(color_key+"1", hum_list[:100])
                    memcache.set(color_key+"2", hum_list[100:])
                else:
                    memcache.set(color_key+"1", hum_list[:100])
                    memcache.set(color_key+"2", hum_list[100:200])
                    memcache.set(color_key+"2", hum_list[200:])
            else:
                if hum_list2:
                    hum_list += hum_list2
                if hum_list3:
                    hum_list += hum_list3
            html_output = "<div class='main-headers'>" + str(len(hum_list)) + " hummingbirds found by color</div>"
        else:
            hum_list = [] ###set to empty list to avoid possible undefined error later
            html_output = "<div class='main-headers'>Find Hummingbirds by...</div>"
        if not hum_list:
            html_output += "<div class='center'>Please try a different search combination.</div>"
            return html_output
        odd = False
        for hum in hum_list:
            html_output += "<div class='sort-hum-container"
            if odd == True:
                html_output += " sort-odd"
            odd = not odd ### sets odd to opposite boolean value
            html_output += ("'><a href='" +
                            hum.link +
                            "'><img src='" + 
                            hum.thumbnail.link + 
                            "' class='sort-hum-thumbnail thumb' alt='" + 
                            hum.common_name + 
                            "' /></a><table class='sort-hum-name'><tr><td><a href='" +
                            hum.link + "'>" +
                            hum.common_name + " (" + hum.binomial_name + 
                            ")</a></td></tr><tr><td class='find-locations-td'>")
            if location:
                html_output += ("Locations: " + 
                                ", ".join(hum.locations))
            html_output += ("</td></tr></table>" + 
                            self.make_fav_checkmark_html(hum, user_data))
        return html_output

    def make_checklist_html(self, sort_type, user_data):
        html_output = memcache.get("checklist_" + sort_type)
        if html_output:
            return html_output
        html_output = ""
        hum_list = self.get_hum_cache("full_hum_list")
        unchecked_list = []
        checked_list = []
        for hum in hum_list:
            if hum.key.id() in user_data.check_list:
                checked_list.append(hum)
            else:
                unchecked_list.append(hum)
        total_count = str(len(unchecked_list) + len(checked_list))
        if sort_type == "unchecked" or sort_type == "both":
            html_output += ("<div class='main-headers'>Unvisited<div class='main-headers-right-link'>" +
                            str(len(unchecked_list)) + "/" + total_count + "</div></div>")
            unchecked_html_output = self.make_name_only_hum_container(unchecked_list, user_data, False)
            if unchecked_html_output == "":
                html_output += "<p>It looks like you've visited all the hummingbird species.</p>"
            else:
                html_output += unchecked_html_output
        if sort_type == "checked" or sort_type == "both":
            html_output += ("<div class='main-headers'>Visited<div class='main-headers-right-link'>" +
                            str(len(checked_list)) + "/" + total_count + "</div></div>")
            checked_html_output = self.make_name_only_hum_container(checked_list, user_data, False)
            if checked_html_output == "":
                html_output += "<p>It looks like you haven't visited any hummingbird species yet.</p>"
            else:
                html_output += checked_html_output
        memcache.set("checklist_" + sort_type, html_output)
        return html_output

    def make_favorite_html(self, sort_type, user_data):
        f_html = memcache.get("f_html_" + sort_type)
        if f_html:
            return f_html
        hum_list = self.get_hum_cache("full_hum_list")
        f_hum_list = []
        if sort_type == "alphabetical":
            for hum in hum_list:
                if hum.key.id() in user_data.favorites_list:
                    f_hum_list.append(hum)
        elif sort_type == "recent":
            for c_id in user_data.favorites_list:
                for hum in hum_list:
                    if hum.key.id() == c_id:
                        f_hum_list.append(hum)
                        break
        f_html = self.make_name_only_hum_container(f_hum_list, user_data, True)
        memcache.set("f_html_" + sort_type, f_html)
        return f_html

    def get_other_resources(self, resource_type):
		resource = memcache.get("Resource:"+resource_type)
		if resource:
			return resource
		else:
			resource = ResourcesDB.query(ResourcesDB.resource_type==resource_type).fetch()
			memcache.set("Resource:"+resource_type, resource)
			return resource

    def remove_duplicate_results(self, results):
        final_results = []
        for result in results:
            if result not in final_results:
                final_results.append(result)
        return final_results

    def search_hums(self, query):
        query = query.lower()
        results = memcache.get("Q: " + query)
        if results:
            return results
        hum_list = self.get_hum_cache("full_hum_list")
        word_list = query.split()
        c_word_list = []
        for word in word_list:
            if word.find("%") == -1:
                c_word_list.append(word)
        query = " ".join(c_word_list)
        results = []
        for hum in hum_list:
            if query in hum.common_name.lower():
                if query + " " in hum.common_name.lower()[:len(query)+1] or query + "-" in hum.common_name.lower()[:len(query)+1] or " " + query in hum.common_name.lower()[len(query)+1:] or query + "-" in hum.common_name.lower()[len(query)+1:] or " " + query + " " in hum.common_name.lower() or " " + query + "-" in hum.common_name.lower() or "-" + query + " " in hum.common_name.lower() or query == hum.common_name.lower():
                    results.append(hum)
            if query in hum.binomial_name.lower():
                if query + " " in hum.binomial_name.lower()[:len(query)+1] or query + "-" in hum.binomial_name.lower()[:len(query)+1] or " " + query in hum.binomial_name.lower()[len(query)+1:] or query + "-" in hum.binomial_name.lower()[len(query)+1:] or " " + query + " " in hum.binomial_name.lower() or " " + query + "-" in hum.binomial_name.lower() or "-" + query + " " in hum.binomial_name.lower() or query == hum.binomial_name.lower():
                    results.append(hum)
        if results:
            final_results = self.remove_duplicate_results(results)[:50]
            memcache.set("Q: " + query, final_results)
            return final_results
        if len(c_word_list) > 1 and len(c_word_list) < 7:
            for hum in hum_list:
               for word in c_word_list:
                   if word + " " in hum.common_name.lower()[:len(word)+1] or word + "-" in hum.common_name.lower()[:len(word)+1] or " " + word in hum.common_name.lower()[len(word)+1:] or word + "-" in hum.common_name.lower()[len(word)+1:] or " " + word + " " in hum.common_name.lower() or " " + word + "-" in hum.common_name.lower() or "-" + word + " " in hum.common_name.lower() or word == hum.common_name.lower():
                       results.append(hum)
                   if word + " " in hum.binomial_name.lower()[:len(word)+1] or word + "-" in hum.binomial_name.lower()[:len(word)+1] or " " + word in hum.binomial_name.lower()[len(word)+1:] or word + "-" in hum.binomial_name.lower()[len(word)+1:] or " " + word + " " in hum.binomial_name.lower() or " " + word + "-" in hum.binomial_name.lower() or "-" + word + " " in hum.binomial_name.lower() or word == hum.binomial_name.lower():
                       results.append(hum)
        if results:
            final_results = self.remove_duplicate_results(results)[:50]
            memcache.set("Q: " + query, final_results)
            return final_results
        else:
            memcache.set("Q: " + query, results)
            return results

    def strip_whitespace_in_lists(self, input_list):
        new_list = []
        for item in input_list:
            if item != " " and item != "":
                new_list.append(item.strip())
        return new_list

    def safe_url_name(self, name):
	character_list = ["'", '"', ",", ".", ";", ":", "!", "(", ")", "[", "]",
                          "~", "`", ">", "<", "*", "#", "$", "^", "&", "=", "?"]
	name = name.replace(" ", "-")
	for character in character_list:
            if character in name:
                name = name.replace(character, "")
	return urllib.quote(name.lower())

    def to_bool(self, value):
        if value == "True":
            return True
        else:
            return False

    def make_int(self, num):
        try:
            int(num)
        except:
            return False
        return int(num)

    def make_float(self, num):
        try:
            float(num)
        except:
            return False
        return float(num)

    def make_one_list(self, input_list):
	final_list = []
	for item in input_list:
	    if isinstance(item, list):
		for single_item in item:
		    final_list.append(single_item)
	    else:
		final_list.append(item)
	return final_list
        
    def get_cookie(self, name):
        if name in self.request.cookies:
            return self.request.cookies[name]
        else:
            return None

    def getPXSize(self, content, n):
	scalenum = ["scale1:","scale2:"][n]
	start = content.find(scalenum) + 7
	line1 = content[start:].find("\n") + 2
	line2 = content[start+line1+1:].find("\n") + 2
	end = content[start+line1+line2:].find("\n")
	return content[start+line1+line2:start+line1+line2+end]

    def getLine(self, content, n):
	return content.split("\n")[n]

    def getCommonName(self, content):
	return self.getLine(content, 0)

    def getBinomialName(self, content):
	return self.getLine(content, 1)

    def getSubfamily(self, content):
	return self.getLine(content, 2)

    def getLength(self, content, gender):
	if gender == "female":
		num = 3
	else:
		num = 4
	return float(self.getLine(content, num))

    def getLocations(self, content):
	return self.getLine(content, 5).split("|")

    def getRarityRank(self, content):
	return int(self.getLine(content, 6))

    def getDiscoveryDate(self, content):
	return int(self.getLine(content, 7))

    def getColors(self, content):
	return self.getLine(content, 8).replace("colors: ", "").split(",")

    def getDescription(self, content, type):
	begin = content.find(type) + 3
	end = content[begin:].find(type) - 1
	return content[begin:begin+end].replace("\n", "")

    def getVideos(self, content):
	begin = content.find("videos:") + 7
	end = content.find("scale1:")
	return content[begin:end].replace("\n", "").split("|")

    def getReferences(self, content):
	return self.getLine(content, -1).split(",")

    def getScalePics(self, content, type, common_name, prefix):
	if type == "scale1:":
		endtype = "scale2:"
	else:
		endtype = "reg1:"
	begin = content.find(type) + 7
	end = content[begin:].find(endtype) + begin
	lines = filter(None, content[begin:end].split("\n"))
	if " male" in lines[2]:
		male = True
	else:
		male = False
	link = "/images/hums/" + common_name.replace("'","") + "/" + prefix + type[:-1] + ".png"
	source = lines[0].strip()
	title = lines[2].strip()
	pic_type = "scale_pics"
	scale_size = int(lines[1].strip())
	return male, link, source, title, pic_type, scale_size

    def getRegPics(self, content, num, next_num, common_name, prefix):
	begin = content.find("reg" + num + ":") + 4 + len(num)
	end = content[begin:].find("reg" + next_num + ":")
	if end == -1:
	    end = content[begin:].find("flower:")
	end += begin
	lines = filter(None, content[begin:end].split("\n"))
	if " male" in lines[1]:
	    male = True
	else:
	    male = False
	link = "/images/hums/" + common_name.replace("'","") + "/" + prefix + "reg" + num + ".jpg"
	source = lines[0].strip()
	title = lines[1].strip()
	pic_type = "reg_pics"
	return male, link, source, title, pic_type

    def getThumbnailPic(self, content, common_name, prefix):
	begin = content.find("thumbnail:") + 11
	next = content[begin:].find("\n") + begin
	end = content[next+1:].find("\n") + next
	if " male" in content[next+1:end]:
		male = True
	else:
		male = False
	link = "/images/hums/" + common_name.replace("'","") + "/" + prefix + "thumb" + ".png"
	source = content[begin:next].strip()
	title = content[next+1:end+1].strip()
	pic_type = "thumbnail"
	return male, link, source, title, pic_type

    def getFlowerPic(self, content, common_name, prefix, flowername):
	begin = content.find("flower:") + 8
	next = content[begin:].find("\n") + begin
	end = content[next+1:].find("\n") + next
	link = "/images/hums/" + common_name.replace("'","") + "/" + flowername
	source = content[begin:next].strip()
	title = content[next+1:end+1].strip()
	pic_type = "flower_pic"
	return link, source, title, pic_type

    def get_game_list(self, dif_level):
        hum_list = self.get_hum_cache("full_hum_list")
        random.shuffle(hum_list)
        game_list = []
        if dif_level == "easy":
            for hum in hum_list:
                option_list = [hum.common_name]
                if random.randrange(1,3) == 1:
                    if hum.scale_pics[0].male:
                        new_pic = hum.scale_pics[0].link
                    else:
                        new_pic = hum.reg_pics[0].link
                else:
                    if hum.reg_pics[0].male:
                        new_pic = hum.reg_pics[0].link
                    else:
                        new_pic = hum.scale_pics[0].link
                rand_range = range(0, 342)
                random.shuffle(rand_range)
                for rand_num in rand_range:
                    if len(option_list) == 4:
                        break
                    if hum_list[rand_num].binomial_name.split()[0] != hum.binomial_name.split()[0]:
                        option_list.append(hum_list[rand_num].common_name)
                random.shuffle(option_list)
                game_list.append({'name': hum.common_name.encode('utf-8'),
                                  'link': new_pic.encode('utf-8'),
                                  'optionA': option_list[0].encode('utf-8'),
                                  'optionB': option_list[1].encode('utf-8'),
                                  'optionC': option_list[2].encode('utf-8'),
                                  'optionD': option_list[3].encode('utf-8')})
        if dif_level == "medium":
            for hum in hum_list:
                option_list = [hum.common_name]
                new_pic = ""
                rand_range = range(0,len(hum.reg_pics))
                random.shuffle(rand_range)
                for rand_num in rand_range:
                    if hum.reg_pics[rand_num].male:
                        new_pic = hum.reg_pics[rand_num].link
                if not new_pic:
                    new_pic = hum.reg_pics[random.randrange(0,len(hum.reg_pics))].link
                rand_range = range(0, 342)
                random.shuffle(rand_range)
                for rand_num in rand_range:
                    if len(option_list) == 4:
                        break
                    if hum_list[rand_num].binomial_name != hum.binomial_name:
                        option_list.append(hum_list[rand_num].common_name)
                random.shuffle(option_list)
                game_list.append({'name': hum.common_name.encode('utf-8'),
                                  'link': new_pic.encode('utf-8'),
                                  'optionA': option_list[0].encode('utf-8'),
                                  'optionB': option_list[1].encode('utf-8'),
                                  'optionC': option_list[2].encode('utf-8'),
                                  'optionD': option_list[3].encode('utf-8')})
        if dif_level == "hard":
            for hum in hum_list:
                option_list = [hum.common_name]
                rand_num = len(hum.reg_pics) - 1
                new_pic = hum.reg_pics[rand_num].link
                if hum.subfamily == "1st":
                    rand_range = range(0, 342)
                    random.shuffle(rand_range)
                    for rand_num in rand_range:
                        if len(option_list) == 4:
                            break
                        if hum_list[rand_num].subfamily == "1st" and hum_list[rand_num].binomial_name != hum.binomial_name:
                            option_list.append(hum_list[rand_num].common_name)
                else:
                    rand_range = range(0, 342)
                    random.shuffle(rand_range)
                    for rand_num in rand_range:
                        if len(option_list) == 4:
                            break
                        if hum_list[rand_num].binomial_name.split()[0] == hum.binomial_name.split()[0] and hum_list[rand_num].binomial_name != hum.binomial_name:
                            option_list.append(hum_list[rand_num].common_name)
                    if len(option_list) != 4:
                        rand_range = range(0, 342)
                        random.shuffle(rand_range)
                        for rand_num in rand_range:
                            if len(option_list) == 4:
                                break
                            if hum_list[rand_num].binomial_name != hum.binomial_name:
                                option_list.append(hum_list[rand_num].common_name)
                random.shuffle(option_list)
                game_list.append({'name': hum.common_name.encode('utf-8'),
                                  'link': new_pic.encode('utf-8'),
                                  'optionA': option_list[0].encode('utf-8'),
                                  'optionB': option_list[1].encode('utf-8'),
                                  'optionC': option_list[2].encode('utf-8'),
                                  'optionD': option_list[3].encode('utf-8')})
        return game_list

    def make_utf8(self, slideshow):
        new_slides = []
        slideshow.title = slideshow.title.encode('utf-8')
        for slide in slideshow.slides:
            new_slides.append({'image':slide['image'].encode('utf-8'),'title':slide['title'].encode('utf-8'),'source':slide['source'].encode('utf-8'),'link':slide['link'].encode('utf-8')})
        slideshow.slides = new_slides
        return slideshow
						 
### TEMPLATE STUFF ###
def count_tags(text, tag):
    count = 0
    index = 0
    while True:
        index = text.find(tag, index)
        if index == -1:
            break
        else:
            index += 1
            count += 1
    return count

def close_p_tag(text):
    open_tag_count = count_tags(text, '<p>')
    close_tag_count = count_tags(text, '</p>')
    if open_tag_count != close_tag_count:
        return True
    else:
        return False
		
jinja_environment.tests['unclosed_p_tag'] = close_p_tag

def strip_p_tags(text):
    text = text.replace('<p>', '')
    text = text.replace('</p>', '')
    return text.lstrip()

jinja_environment.filters['strip_p_tags'] = strip_p_tags

def make_safe_location_value(location):
    s_location = location.replace(" ", "-")
    return s_location.replace(",", "")

jinja_environment.filters['make_safe_location_value'] = make_safe_location_value

def urllib_quote_plus(text):
    return urllib.quote_plus(text)

jinja_environment.filters['urllib_quote_plus'] = urllib_quote_plus

def handle_404(request, response, exception):
    response.out.write(jinja_environment.get_template("error-404.html").render(pagetitle="Colibri Collection: 404"))
    response.set_status(404)

### DATABASES ###
class PicDB(ndb.Model):
    hum_id = ndb.IntegerProperty(required = True)
    male = ndb.BooleanProperty()
    link = ndb.StringProperty()
    source = ndb.StringProperty(required = True)
    title = ndb.StringProperty()
    pic_type = ndb.StringProperty(required = True)
    scale_size = ndb.IntegerProperty()

class SpeciesDB(ndb.Model):
    common_name = ndb.StringProperty(required = True)
    binomial_name = ndb.StringProperty(required = True)
    subfamily = ndb.StringProperty(required = True)
    male_length = ndb.FloatProperty(required = True)
    female_length = ndb.FloatProperty(required = True)
    locations = ndb.StringProperty(repeated = True)
    rarity_rank = ndb.IntegerProperty(required = True)
    discovery_date = ndb.IntegerProperty(required = True)
    colors = ndb.StringProperty(repeated = True)
    description = ndb.TextProperty(required = True)
    flower_description = ndb.TextProperty(required = True)
    videos = ndb.TextProperty(repeated = True)
    references = ndb.StringProperty(repeated = True)
    link = ndb.StringProperty()
    thumbnail = ndb.StructuredProperty(PicDB)
    scale_pics = ndb.StructuredProperty(PicDB, repeated = True)
    reg_pics = ndb.StructuredProperty(PicDB, repeated = True)
    flower_pic = ndb.StructuredProperty(PicDB)

class ResourcesDB(ndb.Model):
    link = ndb.StringProperty(required = True)
    title = ndb.StringProperty(required = True)
    resource_type = ndb.StringProperty(required = True)
	
class UserDB(ndb.Model):
    username = ndb.StringProperty(required = True)
    password = ndb.StringProperty(required = True)

class UserDataDB(ndb.Model):
    favorites_list = ndb.IntegerProperty(repeated = True)
    check_list = ndb.IntegerProperty(repeated = True)
    highscore = ndb.JsonProperty()

class VideoDB(ndb.Model):
    title = ndb.StringProperty(required = True)
    css_ID = ndb.StringProperty(required = True)
    synopsis = ndb.TextProperty(required = True)
    source = ndb.StringProperty(required = True)
    link = ndb.StringProperty(required = True)
    image = ndb.StringProperty(required = True)
    
class SlideshowDB(ndb.Model):
    title = ndb.StringProperty(required = True)
    slides = ndb.JsonProperty(repeated = True)
    link = ndb.StringProperty(required = True)
