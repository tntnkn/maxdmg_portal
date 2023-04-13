from dataclasses    import dataclass
from dataclasses    import asdict


@dataclass
class User():
    id          : int
    name        : str 
    email       : str 
    password    : str
    is_admin    : bool 

    def ToDict(self):
        return asdict(self)


@dataclass
class GraphCredentials():
    id      :int
    user_id :int
    name    :str
    airtable_api_key                 :str
    airtable_base_id                 :str
    airtable_states_table_id         :str
    airtable_states_table_view_id    :str
    airtable_transitions_table_id    :str
    airtable_transition_table_view_id:str
    airtable_forms_table_id          :str
    airtable_forms_table_view_id     :str
    airtable_config_table_id         :str 
    airtable_config_table_view_id    :str

    def ToDict(self):
        return asdict(self)

