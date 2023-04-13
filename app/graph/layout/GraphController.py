from .Graph     import CytoGraph
from .          import GraphErrors


class GraphController():
    @staticmethod
    def HandleNewGraph(storage, session_id, name, graph_info):
        cgraph = vars( CytoGraph(graph_info['graph']) )
        states = cgraph.pop('nodes')
        transitions = cgraph.pop('edges')
        forms  = graph_info['forms']
        errors = graph_info['errors']

        GraphController.SaveGraph(
                storage, session_id, name, cgraph)
        GraphController.SaveGraphStates(
                storage, session_id, name, states)
        GraphController.SaveGraphTransitions(
                storage, session_id, name, transitions)
        GraphController.SaveGraphForms(
                storage, session_id, name, forms)
        GraphController.SaveGraphErrors(
                storage, session_id, name, errors)

    @staticmethod
    def SaveGraph(where, session_id, name, cgraph):
        if cgraph:
            where.SaveOneUserGraph(session_id, name, cgraph) 

    @staticmethod
    def SaveGraphStates(where, session_id, name, states):
        if states and len(states) > 0:
            where.SaveGraphStates(session_id, name, states)

    @staticmethod
    def SaveGraphTransitions(where, session_id, name, trs):
        if trs and len(trs) > 0:
            where.SaveGraphTransitions(session_id, name, trs)

    @staticmethod
    def SaveGraphForms(where, session_id, name, forms):
        if forms and len(forms) > 0:
            where.SaveGraphForms(session_id, name, forms)

    @staticmethod
    def SaveGraphErrors(where, session_id, name, errors):
        if len(errors) > 0:
            err = GraphErrors.InterpretErrors(errors)
        else:
            err = ['Ошибок нет -- Вы прекрасны!',]
        print(err)
        where.SaveGraphErrors(session_id, name, err)

    @staticmethod
    def GetStateInfo(where, session_id, graph_name, state_id):
        state = where.GetGraphState(
            session_id, graph_name, state_id)
        state['type']     = state['type'].value
        state['behavior'] = state['behavior'].value
        forms = list()
        for f_id in state['forms_ids']:
            form = where.GetGraphForm(
                session_id, graph_name, f_id)
            form['type'] = form['type'].value
            forms.append(form)
        return {
            'info' : state,
            'forms': forms,
        }

    @staticmethod
    def GetTransitionInfo(where,session_id,graph_name,tr_id):
        tr = where.GetGraphTransition(
            session_id, graph_name, tr_id)
        tr['type'] = tr['type'].value
        forms = list()
        for f_id in tr['form_elem_ids']:
            form = where.GetGraphForm(
                session_id, graph_name, f_id)
            form['type'] = form['type'].value
            forms.append(form)
        return {
            'info' : tr,
            'forms': forms,
        }

    @staticmethod
    def GetAllGraphErrors(where, session_id, graph_name):
        return {
            'errors' : where.GetAllGraphErrors(session_id, graph_name),
        }
