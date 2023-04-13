from typing         import Dict, List, Union
from .Styling       import get_node_type_class, get_edge_type_class


class CytoGraph():
    def __init__(self, graph):
        self.start_node_id : Union[str, None] = graph.start_node_id
        self.end_node_ids  : List[str]        = graph.end_node_ids
        self.always_open_ids : List[str]      = graph.always_open_ids 

        self.impl = {
            'data'      : list(),
            'directed'  : True,
            'multigraph': False,
            'elements'  : {
                'nodes':  list(),
                'edges':  list(),
            },
        }

        self.nodes : Dict[str, Dict] = dict()
        self.edges : Dict[str, Dict] = dict()

        for state in graph.states.values():
            self.AddNode(state)
        for transition in graph.transitions.values():
            self.AddEdge(transition)

    def AddNode(self, state) -> Dict:
        if state['id'] in self.nodes:
            return self.nodes[state['id']] 

        node = {
            'data': {
                'id'    : state['id'], 
                'label' : state['name']
            },
            'classes': get_node_type_class(state['type'].value),
        }

        self.nodes[node['data']['id']] = state        
        self.impl['elements']['nodes'].append(node)

        return node

    def AddEdge(self, transition) -> Dict:
        if transition['id'] in self.edges:
            return self.edges[transition['id']]

        edge = {
            'data': {
                'id'    : transition['id'],
                'label' : transition['name'],
                'source': transition['source_id'], 
                'target': transition['target_id'],
            },
            'classes'   : get_edge_type_class(transition['type'].value)
        }
       
        self.edges[edge['data']['id']] = transition
        self.impl['elements']['edges'].append(edge)

        return edge


if __name__ == '__main__':
    pass

