from Handler import *

class Checklist(Handler):
    def get(self):
        user_check, user_ID = self.user_check()
        if user_check:
            user_data = UserDataDB.get_by_id(user_ID)
            sort_type = self.request.get("sort-type")
            if sort_type not in ["unchecked", "checked", "both"]:
                sort_type = "both"
            content_html = self.make_checklist_html(sort_type, user_data)
            
            self.render("checklist.html",
                        pagetitle="Colibri Collection: Checklist",
                        sort_type=sort_type,
                        content_html=content_html
                        )
        else:
            self.redirect("/login")

    def post(self):
        user_check, user_ID = self.user_check()
        if user_check:
            clear_checklist = self.request.get("clear-checklist")
            user_data = UserDataDB.get_by_id(user_ID)
            if clear_checklist:
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
                user_data.check_list = []
                user_data.put()
                self.write("Success")
            else:
                self.write("Error")
        else:
            self.redirect("/login")
            
