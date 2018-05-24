from Handler import *

class Find(Handler):
    def get(self):
        user_check, user_ID = self.user_check()
        if user_check:
            user_data = UserDataDB.get_by_id(user_ID)
            location = self.request.get("location").replace("-"," ").replace("+",",")
            colors = self.request.get('colors', allow_multiple=True)
            title = "Find Hummingbirds"
                    
            if location:
                title += " in" + location
            elif colors:
                title += " by Color"
            content_html = self.make_find_by_html(user_data, location=location, colors=colors)
                
            self.render("find.html",
                        pagetitle="Colibri Collection: " + title,
                        content_html=content_html
                        )
        else:
            self.redirect("/login")
