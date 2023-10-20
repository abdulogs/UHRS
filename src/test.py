from .helpers import *
from .main import *


@app.route("/test", methods=["GET"])
def test():
    name = "cancer"
    url = f"https://medbroadcast.com/condition/getcondition/{name}"
    soup = crawler(requests.get(url).content, 'html5lib')
    data = soup.find('div', attrs={'class': 'article-body'})
    disease = {}
    for row in data.find_all('h2'):
        entity = row.text.lower()
        print(entity)
        if "symptoms" in entity:
            disease["symptoms"] = translate(siblinginfo(row))

        if "facts" in entity:
            disease["symptoms"] = translate(siblinginfo(row))

        if "treatment" in entity:
            disease["symptoms"] = translate(siblinginfo(row))

    return render_template('test.html', html=disease)
