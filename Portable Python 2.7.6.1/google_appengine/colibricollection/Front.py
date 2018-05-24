from Handler import *


class Front(Handler):
    def get(self):        
        user_check, user_ID = self.user_check()
        if user_check:
            #hum_list = self.get_hum_dropdown_html()
            #hum_locations = self.get_locations_html_cache()
            featured_hum = self.get_featured_hum()
            self.render("front.html",
                        pagetitle="Colibri Collection",
                        #hummingbird_list=hum_list,
                        #hummingbird_locations=hum_locations,
                        featured_hummingbird=featured_hum
                        )
        else:
            self.redirect("/login")
