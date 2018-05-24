from Handler import *

class Videos(Handler):
    def get(self):
        user_check, user_ID = self.user_check()
        if user_check:
            video_list = memcache.get("video_list")
            if not video_list:
                video_list = VideoDB.query().order(VideoDB.title).fetch()
                memcache.set("video_list", video_list)
            self.render("videos.html",
                        pagetitle="Colibri Collection: Videos",
                        video_list=video_list
                        )
        else:
            self.redirect("/login")
