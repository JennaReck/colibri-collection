from Handler import *

class Favorites(Handler):
    def get(self):
        user_check, user_ID = self.user_check()
        if user_check:
            user_data = UserDataDB.get_by_id(user_ID)
            sort_type = self.request.get("sort-type")
            if sort_type not in ['alphabetical', 'recent']:
                sort_type = "alphabetical"
            content_html = self.make_favorite_html(sort_type, user_data)
            
            self.render("favorites.html",
                        pagetitle="Colibri Collection: Favorites",
                        content_html=content_html,
			sort_type=sort_type
                        )
        else:
            self.redirect("/login")

    def post(self):
        user_check, user_ID = self.user_check()
        if user_check:
            clear_favorites = self.request.get("clear-favorites")
            hum_id = self.make_int(self.request.get("hum-id"))
            user_data = UserDataDB.get_by_id(user_ID)
            memcache.delete("alphabetical_sort")
            memcache.delete("subfamily_sort")
            memcache.delete("smallest-to-largest_sort")
            memcache.delete("largest-to-smallest_sort")
            memcache.delete("date-discovered_sort")
            memcache.delete("rarity_sort")
            memcache.delete("f_html_alphabetical")
            memcache.delete("f_html_recent")
            memcache.delete("checklist_checked")
            memcache.delete("checklist_unchecked")
            memcache.delete("checklist_both")
            memcache.delete("slideshow_list")
            if clear_favorites:
                user_data.favorites_list = []
                user_data.put()
                self.write("Success")
            elif hum_id:
                if hum_id not in user_data.favorites_list:
                    user_data.favorites_list.append(hum_id)
                else:
                    user_data.favorites_list.remove(hum_id)
                user_data.put()
                self.write("Success")
            else:
                self.write("Error")
            slideshow = SlideshowDB.get_by_id(user_data.key.id())
            slides = []
            for hum_id in user_data.favorites_list:
                hum = SpeciesDB.get_by_id(hum_id)
                slides.append({"image": hum.reg_pics[0].link.encode('utf-8'),
				"source": hum.reg_pics[0].source.encode('utf-8'),
				"title": hum.reg_pics[0].title.encode('utf-8'),
				"link": hum.link.encode('utf-8')})
            if not user_data.favorites_list:
                slides.append({})
            slideshow.slides = slides
            slideshow.put()
            
        else:
            self.redirect("/login")
