from Handler import *

class Sort(Handler):
    def get(self):
        user_check, user_ID = self.user_check()
        if user_check:
            user_data = UserDataDB.get_by_id(user_ID)
            sort_type = self.request.get("sort-type")

            if sort_type not in ["alphabetical",
                                 "smallest-to-largest",
                                 "largest-to-smallest",
                                 "date-discovered",
                                 "subfamily-genus",
                                 "rarity"]:
                sort_type = "alphabetical"
                

            if sort_type == "alphabetical":
                content_html = self.make_alphabetical_html(user_data)
            elif sort_type == "subfamily-genus":
                content_html = self.make_subfamily_html(user_data)
            else:
                content_html = self.make_other_sort_html(sort_type, user_data)
            
            self.render("sort.html",
                        pagetitle="Colibri Collection: " + sort_type,
                        sort_type=sort_type,
                        content_html=content_html
                        )
        else:
            self.redirect("/login")
