import json
from dash       import (
    html, dcc
)
from .elements  import (
    make_dropdown, 
    make_stores, 
    make_download_button,
    make_graph_area,
    make_main_page,
)
from .styles    import (
    graph_loading_menu,
)


def request_layout(storage):
    def make_layout():
        graph_creds = storage.GetGraphAll() 
        graphs_data = {
            gr.name : gr.ToDict() for gr in graph_creds

        }

        graph_names = list( graphs_data.keys() )
        drop = make_dropdown(graph_names)

        mt_store, table_store, other_stores = make_stores(graph_names)
        tbl = { k : None for k in graph_names  }
        mt_store.data = json.dumps( graphs_data )
        table_store.data = json.dumps(tbl)

        main_page = make_main_page()
        main_page.children.extend([
            html.Div(
                id='graph_control_menu',
                children=[
                    html.Div(
                        id='graph_loading_menu',
                        children=[
                            html.Div(children=[drop]), 
                            dcc.Loading(
                                children=[make_download_button()],
                                type='circle',
                                style={
                                    'width' : '100%',
                                },
                            )
                        ],
                        style=graph_loading_menu,
                    ),
                ],
            ),
            make_graph_area(),
            mt_store, table_store, *other_stores,
        ])

        return main_page
        """
        return html.Div(
                children=[
                html.Div(children=[label, drop]), 
                download_button,
                graph_area,
                mt_store,
                table_store,
            ],
        )
        """
    return make_layout

