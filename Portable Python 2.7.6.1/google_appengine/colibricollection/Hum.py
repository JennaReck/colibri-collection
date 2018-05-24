from Handler import *

class Hum(Handler):
    def get(self, hum_id, url_name):
        user_check, user_ID = self.user_check()
        if user_check:
            user_data = UserDataDB.get_by_id(user_ID)
            scale_ratio = self.make_float(self.get_cookie("scaleRatio"))
            hum_id = self.make_int(hum_id[1:])
            if hum_id:
                hum = SpeciesDB.get_by_id(hum_id)
                if hum:
                    if self.safe_url_name(hum.common_name) != url_name[1:]:
                        self.redirect(hum.link)
                    else:
                        if hum_id not in user_data.check_list:
                            user_data.check_list.append(hum_id)
                            user_data.put()
                            memcache.delete("alphabetical_sort")
                            memcache.delete("subfamily_sort")
                            memcache.delete("smallest-to-largest_sort")
                            memcache.delete("largest-to-smallest_sort")
                            memcache.delete("date-discovered_sort")
                            memcache.delete("rarity_sort")
                            memcache.delete("f_html_alphabetical")
                            memcache.delete("f_html_recent")
                        if hum_id in user_data.favorites_list:
                            is_favorite = True
                        else:
                            is_favorite = False
                        self.render("species.html",
                                pagetitle="Colibri Collection: " + hum.common_name,
                                hum=hum,
                                scale_ratio=scale_ratio,
                                is_favorite=is_favorite
                                )
        else:
            self.redirect("/login")
