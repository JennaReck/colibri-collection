from Handler import *

class Slideshow(Handler):
    def get(self):
        if self.user_check():
            chosen_slideshow = self.request.get("view", "none")
            slideshow_list = memcache.get("slideshow_list")
            main_slideshow = []
            if not slideshow_list:
                slideshow_list = SlideshowDB.query().fetch()
                memcache.set("slideshow_list", slideshow_list)
            slideshow_num = 0
            for slideshow in slideshow_list:
                if chosen_slideshow in slideshow.link:
                    if slideshow.slides != [{}]:
                        main_slideshow = self.make_utf8(slideshow)
                if "all-species" in slideshow.link:
                    main_alt = slideshow
                if slideshow.slides != [{}]:
                    slideshow_num += 1
            if not main_slideshow:
                main_slideshow = self.make_utf8(main_alt)
            self.render("slideshow.html",
                        pagetitle="Colibri Collection: Slideshow",
                        main_slideshow=main_slideshow,
                        slideshow_list=slideshow_list,
                        slideshow_num=slideshow_num
                        )
        else:
            self.redirect("/login")
