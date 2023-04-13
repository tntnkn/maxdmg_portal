from .dashapp   import make_dash_app
from .routes    import graph_blueprint
from .utils     import GraphHtml


def init_dash(server):
    with server.app_context():
        server.register_blueprint(graph_blueprint)
    
    dash_app = make_dash_app(server) 
    GraphHtml.Set( dash_app.index() )

    return dash_app.server

