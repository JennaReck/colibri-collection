from Handler import *

class AdminPanel(Handler):
    def get(self):
        if self.admin_user_check():
            self.render("admin-panel.html",
                        pagetitle="Colibri Collection: Admin Panel"
                        )
        else:
            self.redirect("/login")
