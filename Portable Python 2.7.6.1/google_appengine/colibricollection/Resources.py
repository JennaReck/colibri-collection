from Handler import *

class Resources(Handler):
    def get(self):
        if self.user_check():
            articles_blogs = self.get_other_resources("articles/blogs")
            images_graphics = self.get_other_resources("images/graphics")
            photographer_websites = self.get_other_resources("photographer websites")
            photos = self.get_other_resources("photos")
            videos = self.get_other_resources("videos")
            wallpapers = self.get_other_resources("wallpapers")
            wikis_information_resources = self.get_other_resources("wikis/information resources")
            misc = self.get_other_resources("misc.")
            
            self.render("other-resources.html",
                        pagetitle="Colibri Collection: Other Resources",
                        articles_blogs=articles_blogs,
                        images_graphics=images_graphics,
                        photographer_websites=photographer_websites,
                        photos=photos,
                        videos=videos,
                        wallpapers=wallpapers,
                        wikis_information_resources=wikis_information_resources,
                        misc=misc
                        )
        else:
            self.redirect("/login")
