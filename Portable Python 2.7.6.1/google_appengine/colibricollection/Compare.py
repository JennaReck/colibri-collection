from Handler import *

class Compare(Handler):
    def get(self):
        if self.user_check():
            scale_ratio = self.make_int(self.get_cookie("scaleRatio"))
            hum_list = self.get_hum_cache("full_hum_list")
            humid1 = self.make_int(self.request.get("humid1"))
            if humid1:
                hum1 = SpeciesDB.get_by_id(humid1)
            else:
                hum1 = False
            humid2 = self.make_int(self.request.get("humid2"))
            if humid2:
                hum2 = SpeciesDB.get_by_id(humid2)
            else:
                hum2 = False
            self.render("compare.html",
                        pagetitle="Colibri Collection: Compare Species",
                        scale_ratio=scale_ratio,
                        hum_list=hum_list,
                        hum1=hum1,
                        hum2=hum2,
                        humid1=humid1,
                        humid2=humid2
                        )
        else:
            self.redirect("/login")
