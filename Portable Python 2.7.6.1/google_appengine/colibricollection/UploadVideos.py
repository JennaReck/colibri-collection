from Handler import *

class UploadVideos(Handler):
    def get(self):
        if self.admin_user_check():
            self.render("upload-videos.html",
                        pagetitle="Colibri Collection: Upload Videos"
                        )
        else:
            self.redirect("/login")

    def post(self):
        if self.admin_user_check():
            video_title = self.request.get("video-title")
            css_id = self.request.get("css-id")
            video_synopsis = self.request.get("video-synopsis")
            video_source = self.request.get("video-source")
            video_link = self.request.get("video-link")
            video_image = self.request.get("video-image")

            videodata = VideoDB(title=video_title,
                                css_ID=css_id,
                                synopsis=video_synopsis,
                                source=video_source,
                                link="/v_resources/" + video_link,
                                image="/v_resources/" + video_image)
            videodata.put()
            self.redirect("/upload-videos")
        else:
            self.redirect("/login")
        
