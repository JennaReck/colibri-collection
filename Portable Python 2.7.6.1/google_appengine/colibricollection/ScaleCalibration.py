from Handler import *

class ScaleCalibration(Handler):
    def get(self):
        if self.user_check():
            scale_ratio = self.get_cookie("scaleRatio")
            self.render("calibrate.html",
                        pagetitle="Colibri Collection: Scale Calibration",
                        scale_ratio=scale_ratio
                        )
        else:
            self.redirect("/login")
