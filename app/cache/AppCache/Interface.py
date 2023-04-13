from .Schema        import (
    GraphsMetadata,
    UserGraphs,
)


class AppCache():
    def __init__(self):
        self.metadata       : GraphsMetadata = dict()
        self.user_graphs    : UserGraphs    = dict()

    def GetMetadata(self, graph_name):
        return self.metadata.get(graph_name, None)

    def GetUserGraphs(self, session_id):
        return self.user_graphs.get(session_id, None)

    def SaveMetadata(self, name, metadata):
        self.metadata[namne] = metadata

    def SaveOneUserGraph(self, session_id, name, graph):
        if not self.user_graphs.get(session_id, None):
            self.user_graphs[session_id] = dict()
        self.user_graphs[session_id][name] = graph

