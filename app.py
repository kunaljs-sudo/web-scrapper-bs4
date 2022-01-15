import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq


from markupsafe import Markup

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST"])  # route with allowed methods as GET and POST
def index_page():
    return render_template("index.html")


@app.route("/show", methods=["POST", "GET"])
def show():
    review_ls = []
    if request.method == "POST":
        try:
            search_string = "Samsung mobiles"
            search_string = str(request.form["search"])
            search_string = search_string.strip().replace(" ", "+")
            flipkart_url = "https://www.flipkart.com/search?q=" + search_string

            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")

            bigboxes = flipkart_html.find_all(
                "div", {"class": "_1YokD2 _3Mn1Gg"}
            )  # div containing all the products
            product_div = bigboxes[0].find_all(
                "div", {"class": "_1AtVbE col-12-12"}
            )  # div containing oly products
            link_to_search_product = product_div[0].a[
                "href"
            ]  # first product on the web page

            prodct = uReq("https://www.flipkart.com" + link_to_search_product)
            prod_html = bs(prodct, "html.parser")
            # print(prod_html)

            review_col_in_product_page = prod_html.find_all(
                "div", {"class": "col JOpGWq"}
            )

            reviews = review_col_in_product_page[0].find_all("div", {"class": ""})
            del reviews[0:5]

            print(reviews)
            str_ = " ".join([str(elem) for elem in reviews])

            markup = Markup(str_)
            bs_ = bs(markup, "html.parser")
            ls = str(bs_.text)
            ls = ls.replace("READ MORE", "--->")
            ls = ls.split("--->")
            for i in ls:
                review_ls.append(i)

            return render_template("result.html", data=review_ls)

        except Exception as e:

            return "<h1>Something is wrong please try again later</h1>"
    else:
        render_template("index.html")


port = int(os.getenv("PORT"))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
    #app.run(port=8080, debug=True)
