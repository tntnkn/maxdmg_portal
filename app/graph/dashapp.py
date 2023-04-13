from dash       import Dash, html
from .layout    import request_layout, make_callbacks


def make_dash_app(server):
    from ..storage import storage
    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/graph/',
    )

    dash_app.layout = request_layout(storage)

    make_callbacks(dash_app)

    return dash_app

