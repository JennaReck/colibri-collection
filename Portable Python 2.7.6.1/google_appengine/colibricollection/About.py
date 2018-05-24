from Handler import *

class About(Handler):
    def get(self):
        if self.user_check():
            self.render("about.html",
                        pagetitle="Colibri Collection: About Page"
                        )
        else:
            self.redirect("/login")
