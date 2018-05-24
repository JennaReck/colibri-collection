from Handler import *

class Error404(Handler):
    def get(self):
        if self.user_check():
            url = self.request.url
            begin = url[10:].find('/')
            uri = url[10+begin:]
            if uri != '/404':
                self.redirect('/404')
            self.render("error-404.html",
                        pagetitle="Colibri Collection: 404"
                        )
        else:
            self.redirect("/login")
