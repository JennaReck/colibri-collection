from Handler import *

class ColorGen(Handler):
    def get(self):
        if self.admin_user_check():    
            color_output = ""
            self.render("color-gen.html",
                        pagetitle="Colibri Collection: Color Generator",
                        hum={},
                        second_color_form=True,
                        color_output=color_output
                        )
        else:
            self.redirect("/login")

    def post(self):
        if self.admin_user_check():
            color_output = self.request.get_all("colors")
            hum_list = []
            hum = {}
            self.render("color-gen.html",
                        pagetitle="Colibri Collection: Color Generator",
                        hum={},
                        second_color_form=True,
                        color_output=color_output
                        )
        else:
            self.redirect("/login")
        
