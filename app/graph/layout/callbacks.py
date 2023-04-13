import json
from maxdmg_resource    import MaxDmgLoader

from dash       import (
    Input, 
    Output, 
    State, 
    no_update, 
    callback_context,
)
from ..utils    import make_graph
from .elements  import make_drawable_graph, update_drawable_graph 
from .GraphController       import GraphController
from .GraphInfoPresentrer   import GraphInfoPresenter


def make_callbacks(dashapp):

    @dashapp.callback(
        Output('graph_impl', 'elements'),
        Output('download_button', 'disabled', allow_duplicate=True),
        Output('graph_info_info_store',   'data', allow_duplicate=True),
        Output('graph_info_errors_store', 'data', allow_duplicate=True),
        Output('graph_info_tabs_contents','data', allow_duplicate=True),
        Output('select_trigger_store',    'data', allow_duplicate=True),
        Input('graph_select', 'value'),
        prevent_initial_call=True,
    )
    def select_graph(sel_opt):
        if sel_opt is None:
            return dict(), True, None, None, None, sel_opt
        session_id = dashapp.server.auth.GetCurUserId()
        cgraph     = dashapp.server.cache.GetOneUserGraph(
            session_id, sel_opt)
        if not cgraph:
            return dict(), False, None, None, None, sel_opt

        layout={
            'name': 'breadthfirst',
            'fit' : False,
            'directed': True,
            'avoidOverlap': True,
            'spacingFactor' : 4,
        }
        roots = ''
        for n_id in cgraph['always_open_ids']:
            roots += f"#{n_id}," 
        roots += f"#{cgraph['start_node_id']}"

        layout['roots'] = roots
        return cgraph['impl']['elements'], False, None, None, None, sel_opt


    @dashapp.callback(
        Output('graph_info_tabs_contents', 'children', allow_duplicate=True),
        Input('graph_info_tabs', 'value'),
        Input('select_trigger_store', 'data'),
        State('graph_info_info_store', 'data'),
        State('graph_info_errors_store', 'data'),
        prevent_initial_call=True,
    )
    def render_content(tab, sel_opt, info, errors):
        print('TAB!!', tab)
        if tab == 'giit':
            return info 
        elif tab == 'giet':
            print('GIET', errors)
            session_id = dashapp.server.auth.GetCurUserId()
            errors = GraphController.GetAllGraphErrors(
                                           dashapp.server.cache, 
                                           session_id, 
                                           sel_opt)
            return GraphInfoPresenter.ProcessGraphErrors(
                                           errors['errors'])


    @dashapp.callback(
        Output('download_button', 'disabled', allow_duplicate=True),
        Output('graph_select', 'disabled', allow_duplicate=True),
        Output('graph_select', 'value'),
        Input('download_trigger_store', 'data'),
        State('mtdt_store', 'data'),
        State('graph_select', 'value'),
        prevent_initial_call=True,
    )
    def download_graph(n_clicks, mtdt, sel_opt):
        md = json.loads(mtdt)
        td = md[sel_opt]

        loader  = MaxDmgLoader()
        td.pop('id')
        td.pop('user_id')
        td.pop('name')
        td = {
            k.upper(): v for k, v in td.items()
        }

        res        = loader.Load(**td)
        print('TESTTESTTEST')
        print(res.keys())
        session_id = dashapp.server.auth.GetCurUserId()
        GraphController.HandleNewGraph(dashapp.server.cache,
                                       session_id, sel_opt, res)
        return False, False, sel_opt


    @dashapp.callback(
        Output('download_trigger_store', 'data'),
        Output('download_button', 'disabled', allow_duplicate=True),
        Output('graph_select', 'disabled', allow_duplicate=True),
        Input('download_button', 'n_clicks'),
        prevent_initial_call=True,
    )
    def download_button_trigger(n_clicks):
        return n_clicks, True, True


    @dashapp.callback(
        Output('graph_info_tabs_contents', 'children', allow_duplicate=True),
        Input('graph_info_info_store','data'),
        State('graph_info_tabs', 'value'),
        prevent_initial_call=True,
    )
    def storeGraphInfo(data, tab):
        if tab != 'giit':
            return no_update
        return data


    @dashapp.callback(
        Output('graph_info_info_store', 'data', allow_duplicate=True),
        Input('graph_impl', 'tapNodeData'),
        State('graph_select', 'value'),
        State('graph_info_tabs', 'value'),
        prevent_initial_call=True,
    )
    def displayTapNodeData(data, sel_opt, tab):
        if not data:
            return no_update
        session_id = dashapp.server.auth.GetCurUserId()
        data_id = data['id']
        info = GraphController.GetStateInfo(
            dashapp.server.cache,session_id,sel_opt,data_id)
        return GraphInfoPresenter.ProcessStateInfo(info)


    @dashapp.callback(
        Output('graph_info_info_store', 'data', allow_duplicate=True),
        Input('graph_impl', 'tapEdgeData'),
        State('graph_select', 'value'),
        State('graph_info_tabs', 'value'),
        prevent_initial_call=True,
    )
    def displayTapEdgeData(data, sel_opt, tab):
        if not data:
            return no_update
        session_id = dashapp.server.auth.GetCurUserId()
        data_id = data['id']
        info = GraphController.GetTransitionInfo(
            dashapp.server.cache,session_id,sel_opt,data_id)
        return GraphInfoPresenter.ProcessTransitionInfo(info)

