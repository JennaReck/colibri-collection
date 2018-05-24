from Handler import *

class UploadResources(Handler):
    def get(self):
        if self.admin_user_check():
            self.render("upload-resources.html",
                        pagetitle="Colibri Collection: Upload Resources"
                        )
        else:
            self.redirect("/login")

    def post(self):
        if self.admin_user_check():
            link = self.request.get("link")
            title = self.request.get("title")
            resource_type = self.request.get("type")
            redirect_location = self.request.get("redirect-location")

            resourcedata = ResourcesDB(link=link,
                                       title=title,
                                       resource_type=resource_type
                                       )
            resourcedata.put()

            if redirect_location == "continue":
                self.redirect("/upload-resources")
            else:
                self.redirect("/other-resources")
        else:
            self.redirect("/login")
        
