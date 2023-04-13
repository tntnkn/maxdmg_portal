from bs4             import BeautifulSoup
from maxdmg_resource import MaxDmgLoader


class GraphHtml():
    html = ''
    def Get():
        return GraphHtml.html

    def Set(index):
        soup = BeautifulSoup(index, 'html.parser')
        GraphHtml.html = soup.footer


class make_graph():
    pass
