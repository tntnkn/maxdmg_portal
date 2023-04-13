import redis
import pickle


class RedisCache():
    def __init__(self, host, port):
        if len(port) > 0:
            r = redis.Redis(host=host, port=port)
        else:
            r = redis.Redis(host=host)
        r.flushdb()
        self.conn = r

    def GetMetadata(self, graph_name):
        return self.__GetFromHashTable('metadata', graph_name)

    def GetOneUserGraph(self, session_id, name):
        return self.__GetFromKey('gr_'+str(session_id)+name) 

    def GetUserGraphs(self, session_id):
        p = self.conn.hgetall('gr_'+str(session_id))
        if len(p) == 0:
            return None
        d = dict()
        for k,v in p.items():
            d[k.decode()] = pickle.loads(v)
        return d

    def GetGraphState(self, session_id, name, state_id):
        return self.__GetFromHashTable('st_'+name+str(session_id), 
                                       state_id)

    def GetGraphTransition(self, session_id, name, trs_id):
        return self.__GetFromHashTable('tr_'+name+str(session_id), 
                                       trs_id)

    def GetGraphForm(self, session_id, name, form_id):
        return self.__GetFromHashTable('fr_'+name+str(session_id), 
                                       form_id)

    def GetAllGraphErrors(self, session_id, name):
        return self.__GetFromKey('er_'+name+str(session_id)) 

    def SaveMetadata(self, name, metadata):
        self.conn.hset('metadata', name, pickle.dumps(metadata))

    def SaveOneUserGraph(self, session_id, name, graph):
        self.conn.set('gr_'+str(session_id)+name, 
                       pickle.dumps(graph))

    def SaveGraphStates(self, session_id, name, states):
        self.conn.hset(
            'st_'+name+str(session_id),
             mapping=self.__HMapping(states)
        )

    def SaveGraphTransitions(self, session_id, name, trs):
        self.conn.hset(
            'tr_'+name+str(session_id),
             mapping=self.__HMapping(trs)
        )

    def SaveGraphForms(self, session_id, name, forms):
        self.conn.hset(
            'fr_'+name+str(session_id),
             mapping=self.__HMapping(forms)
        )

    def SaveGraphErrors(self, session_id, name, errors):
        self.conn.set(
            'er_'+name+str(session_id),
            pickle.dumps(errors),
        )

    def __GetFromHashTable(self, h_name, key):
        p = self.conn.hget(h_name, key)
        if p:
            p = pickle.loads(p)
        return p

    def __GetFromKey(self, key):
        p = self.conn.get(key)
        if p:
            p = pickle.loads(p)
        return p

    def __HMapping(self, d):
        return { k:pickle.dumps(v) for k,v in d.items() }

