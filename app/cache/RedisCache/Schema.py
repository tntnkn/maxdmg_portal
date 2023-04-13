from typing     import TypedDict, Dict


# this one is supposed to be looked upon with graph name
GraphsMetadata  = Dict[str, Dict]
# here exact graph is looked with name, and user's graphs -- with session id
Graphs          = Dict[str, Dict]
UserGraphs     = Dict[str, Graphs]

class Cache(TypedDict):
    metadata    : GraphsMetadata
    usersgraphs : UserGraphs

