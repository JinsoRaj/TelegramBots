from .__init__ import *


def fetch_posts():
    response = requests.get("https://internfreak.co/")

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        post_info = dict()
        posts = soup.select("div.post-entry.d-block.small-post-entry-v")
        for post in posts:
            try:
                title = post.find("h2", class_="heading").getText()
            except:
                title = "N/A"
            try:
                batch = post.find("p").getText()
            except:
                batch = "N/A"
            try:
                offer = post.find("a", class_="category").getText()
            except:
                offer = "N/A"
            try:
                date = post.find("span", class_="date").getText()
            except:
                date = "N/A"
            try:
                thumbnail = "https://internfreak.co/" + \
                    post.find("img", class_="img-fluid")["src"]
            except:
                thumbnail = "Assets/error.jpg"
            try:
                link = "https://internfreak.co/" + \
                    post.find("h2", class_="heading").findChildren()[0]["href"]
            except:
                link = "https://internfreak.co/"

            post_info[title] = {
                "batch": batch,
                "offer": offer,
                "date": date,
                "thumbnail": thumbnail,
                "link": link,
            }
        return post_info
    else:
        return False
