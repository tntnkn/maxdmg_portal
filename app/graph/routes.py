from flask      import Blueprint, render_template, abort
from flask      import render_template, redirect, url_for

from .utils     import GraphHtml


graph_blueprint = Blueprint('graph', __name__, url_prefix='/graph')


@graph_blueprint.route('/')
def graph():
    return render_template(
            'graph.html',
            footer=GraphHtml.Get())

@graph_blueprint.route('/<path:path>')
def graph_redirect(path):
    return redirect( url_for('/graph/') )

@graph_blueprint.route('/test')
def graph_test():
    from ..storage import storage
    storage.GetGraphAll()
    return redirect( url_for('/graph/') )

