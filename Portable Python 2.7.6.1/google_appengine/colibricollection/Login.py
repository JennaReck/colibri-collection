from Handler import *

class Login(Handler):
    def get(self):
        error = self.request.get("error")
        if error:
            error = "Invalid login."
        self.render("login.html",
                    error=error
                    )

    def post(self):
        if not self.locked_out():
            username = self.request.get("username").lower()
            password = self.request.get("password")

            fetched_user = UserDB.query(UserDB.username == username).get()
            if fetched_user and username == fetched_user.username and self.valid_password(fetched_user.username,
                                                                                          password,
                                                                                          fetched_user.password):
                user_cookie, user_hash = self.make_cookie(fetched_user)
                self.response.headers.add_header("Set-Cookie","username=%s|%s; expires=315360000; path=/"
                                                    %(user_cookie, user_hash))
                if username == "jean":
                    self.redirect("/")
                elif username == "jreck21":  
                    self.redirect("/admin-panel")
            else:
                self.update_failed_logins()
                self.redirect("/login?error=y")
        else:
            self.redirect("/login?error=y")
        
class Logout(Handler):
    def get(self):
        self.response.headers.add_header("Set-Cookie","username=; path=/")
        self.redirect("/login")
