from Handler import *

class NameMatch(Handler):
    def get(self):
        user_check, user_ID = self.user_check()
        if user_check:
            user_data = UserDataDB.get_by_id(user_ID)
            dif_level = self.request.get("level")
            if dif_level not in ["easy", "medium", "hard"]:
                dif_level = "easy"
            game_list = self.get_game_list(dif_level)
           
            self.render("name-match.html",
                        pagetitle="Colibri Collection: Name Match",
                        game_list=game_list,
                        highscore=user_data.highscore[dif_level],
                        level=dif_level
                        )
        else:
            self.redirect("/login")

    def post(self):
        user_check, user_ID = self.user_check()
        if user_check:
            user_data = UserDataDB.get_by_id(user_ID)
            new_highscore = self.make_int(self.request.get("highscore"))
            if new_highscore == False:
                new_highscore = 0
            dif_level = self.request.get("level")
            if dif_level not in ["easy", "medium", "hard"]:
                dif_level = "easy"
            if new_highscore > user_data.highscore[dif_level]:
                user_data.highscore[dif_level] = new_highscore
                user_data.put()
            self.write("Success")
        else:
            self.write("Error")
        
