from Handler import *

class UploadHum(Handler):
    def get(self):
        if self.admin_user_check():
            self.render("upload-hum.html",
                        pagetitle="Colibri Collection: Upload Hummingbird Species",
                        hum_list=[]
                        )
        else:
            self.redirect("/login")

    def post(self):
        if self.admin_user_check():
            humtxt = self.request.get("hum-txt").decode('utf-8', 'ignore')
            prefix = self.request.get("hum-prefix")
            regpics = self.request.get("reg-pics")
            flowername = self.request.get("flower-name")
            hum_id = int(self.request.get("hum-id"))
            
            common_name = self.getCommonName(humtxt)
            binomial_name = self.getBinomialName(humtxt)
            subfamily = self.getSubfamily(humtxt)
            male_length = self.getLength(humtxt, "male")
            female_length = self.getLength(humtxt, "female")
            locations = self.getLocations(humtxt)
            rarity_rank = self.getRarityRank(humtxt)
            discovery_date = self.getDiscoveryDate(humtxt)
            colors = self.getColors(humtxt)
            description = self.getDescription(humtxt, "---")
            flower_description = self.getDescription(humtxt, "===")
            videos = self.getVideos(humtxt)
            references = self.getReferences(humtxt)

            humdata = SpeciesDB(common_name=common_name,
                                binomial_name=binomial_name,
                                subfamily=subfamily,
                                male_length=male_length,
                                female_length=female_length,
                                locations=locations,
                                rarity_rank=rarity_rank,
                                discovery_date=discovery_date,
                                colors=colors,
                                description=description,
                                flower_description=flower_description,
                                videos=videos,
                                references=references,
                                id=hum_id)

            humdata.put()
            link = "/species/" + str(hum_id) + "/" + self.safe_url_name(common_name)
            humdata.link = link

            male1, link1, source1, title1, pic_type1, scale_size1 = self.getScalePics(humtxt, "scale1:", common_name, prefix)
            scale1imagedata = PicDB(hum_id=hum_id,
                              male=male1,
                              link=link1,
                              source=source1,
                              title=title1,
                              pic_type=pic_type1,
                              scale_size=scale_size1
                            )
            #scale1imagedata.put()
            humdata.scale_pics.append(scale1imagedata)
            male2, link2, source2, title2, pic_type2, scale_size2 = self.getScalePics(humtxt, "scale2:", common_name, prefix)
            scale2imagedata = PicDB(hum_id=hum_id,
                              male=male2,
                              link=link2,
                              source=source2,
                              title=title2,
                              pic_type=pic_type2,
                              scale_size=scale_size2
                            )
            #scale2imagedata.put()
            humdata.scale_pics.append(scale2imagedata)

            for num in range(1, int(regpics)+1):
                male3, link3, source3, title3, pic_type3 = self.getRegPics(humtxt, str(num), str(num+1), common_name, prefix)
                regimagedata = PicDB(hum_id=hum_id,
                                  male=male3,
                                  link=link3,
                                  source=source3,
                                  title=title3,
                                  pic_type=pic_type3
                                )
                #regimagedata.put()
                humdata.reg_pics.append(regimagedata)
                
            male4, link4, source4, title4, pic_type4 = self.getThumbnailPic(humtxt, common_name, prefix)
            thumbimagedata = PicDB(hum_id=hum_id,
                              male=male4,
                              link=link4,
                              source=source4,
                              title=title4,
                              pic_type=pic_type4
                            )
            #thumbimagedata.put()
            humdata.thumbnail = thumbimagedata

            link5, source5, title5, pic_type5 = self.getFlowerPic(humtxt, common_name, prefix, flowername)
            flowerimagedata = PicDB(hum_id=hum_id,
                              link=link5,
                              source=source5,
                          title=title5,
                          pic_type=pic_type5
                        )
            #flowerimagedata.put()
            humdata.flower_pic = flowerimagedata
            humdata.put()
            self.redirect("/upload-hum")
        else:
            self.redirect("/login")
        
