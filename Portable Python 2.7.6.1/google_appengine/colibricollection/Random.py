from Handler import *

class Random(Handler):
    def get(self):
        if self.user_check():
            hum_id = random.randrange(1,343)
            self.redirect("/species/" + str(hum_id) + "/")
        else:
            self.redirect("/login")
