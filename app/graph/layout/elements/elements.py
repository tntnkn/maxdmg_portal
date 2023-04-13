import dash_cytoscape as cyto
from dash       import html, dcc
from ..         import styles


def make_drawable_graph():
    if "cyto" not in make_drawable_graph.__dict__: 
        make_drawable_graph.cyto = cyto.Cytoscape(
            id='graph_impl',
            layout={
                'name': 'breadthfirst',
                'fit' : False,
                'directed': True,
                'avoidOverlap': True,
                'spacingFactor' : 4,
            },
            style=styles.graph_style,
            stylesheet=styles.graph_stylesheet,
        )
    return make_drawable_graph.cyto

def update_drawable_graph(cytograph, cgraph):
    cytograph.elements=cgraph['impl']['elements']
    if cytograph.layout['name'] == 'breadthfirst':
        roots = ''
        for n_id in cgraph['always_open_ids']:
            roots += f"#{n_id}," 
        roots += f"#{cgraph['start_node_id']}"
        cytograph.layout['roots'] = roots
    return cytograph

def make_dropdown(options):
   return dcc.Dropdown(options, 
                       placeholder='Выберете таблицу',
                       id='graph_select')

def make_download_button():
    return html.Button('Загрузить', 
                      id='download_button', 
                      n_clicks=0,
                      className='btn btn-outline-primary btn-sm w-100',
                      disabled=True,
    )

def make_stores(options):
    stores      = list()
    """
    for o in options:
        store = dcc.Store(id=o+'_store')
        store.data = 'Нажмите "Загрузить", чтобы граф отобразился.' 
        stores.append(store)
    """
    stores.append( dcc.Store(id='download_trigger_store') )
    stores.append( dcc.Store(id='select_trigger_store') )
    stores.append( dcc.Store(id='graph_info_errors_store', data=None) )
    stores.append( dcc.Store(id='graph_info_info_store', data=None) )
    table_metadata = dcc.Store(id='mtdt_store')
    table_store    = dcc.Store(id='table_store')

    return table_metadata, table_store, stores

def make_main_title():
    return html.Span(
        id='main_title',
        children='Визуализатор',
        style=styles.main_title_style,
        className='h4',
    )

def make_graph_info():
    return html.Div(
        id='graph_info',
        children=[
            dcc.Tabs(
                id='graph_info_tabs',
                value='giit',
                children=[
                    dcc.Tab(
                        id='graph_info_info_tab',
                        label='Инфо',
                        value='giit',
                    ),
                    dcc.Tab(
                        id='graph_info_errors_tab',
                        label='Ошибки',
                        value='giet',
                    ),
                ],
            ),
            html.Div(
                id='graph_info_tabs_contents',
            ),
        ],
        style=styles.graph_info_style,
    )

def make_graph_area():
    return html.Div(
        id='graph_area',
        children=[
            make_drawable_graph(),
            make_graph_info(),
        ],
        style=styles.graph_area_style,
    )

def make_main_page():
    return html.Div(
        id='main_screen',
        children=[
            make_main_title(),
        ],
        style=styles.main_page_style
    )

