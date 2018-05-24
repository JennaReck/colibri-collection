from Handler import *

class SearchResults(Handler):
    def get(self):
        user_check, user_ID = self.user_check()
        if user_check:
            user_data = UserDataDB.get_by_id(user_ID)
            query = urllib.quote_plus(self.request.get('q'))
            c_query = query.replace("%27s","'s").replace("+"," ")
            page = self.request.get('p')

            #set stuff to default empty, no results, in case no query or results
            content_html = ""
            pagination = ""
            result_num = 0
                
            if query:
                result_list = self.search_hums(c_query)
                result_num = len(result_list)
                if result_num > 0:
                    pagination = self.make_pagination(page, "?q=" + query, result_list, 20)
                    if not pagination:
                        self.redirect("/404")
                    current_result_list = self.next_content(page, result_list, 20)
                    content_html = self.make_name_only_hum_container(current_result_list, user_data)
                else:
                    content_html = "<span class='center'>Your search terms returned no results. Please try different keywords.</span>"
            self.render("search-results.html",
                        pagetitle="Colibri Collection: " + c_query,
                        query=c_query,
                        result_num=result_num,
                        content_html=content_html,
                        pagination=pagination
                        )
        else:
            self.redirect("/login")

    def post(self):
        if self.user_check():
            query = self.request.get('q')
            if query:
                self.redirect("/search?q=" + urllib.quote_plus(query))
            else:
                self.redirect("/search")
        else:
            self.redirect("/login")
