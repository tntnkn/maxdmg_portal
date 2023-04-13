from typing             import List
from flask_sqlalchemy   import SQLAlchemy
from .Schema            import init_schema
from .Models            import User, GraphCredentials


class Storage():
    def __init__(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DB_URI']
        self.db = SQLAlchemy()
        self.db.init_app(app)

        self.schema = init_schema(app, self)

    def GetUser(self, key, value) -> User:
        usr = self.__GetUser(key, value)
        if not usr:
            return None
        return User(
            id=usr.id,
            name=usr.name,
            email=usr.email,
            password=usr.password,
            is_admin=usr.is_admin,
        )

    def CreateUser(self, user) -> None:
        user_schema = self.schema.users(
            **self.__CleanModel(user)
        )
        self.db.session.add(user_schema)
        self.db.session.commit()
        user.id = user_schema.id
        return user

    def UpdateUserPassword(self, user_id, new_password):
        usr = self.__GetUser('id', user_id)
        usr.password = new_password
        self.db.session.commit()

    def GetGraphAll(self) -> List[GraphCredentials]:
        graph_t = self.schema.graph_cred
        db = self.db
        creds = db.session.scalars( db.select(graph_t) ).all()
        ret = [
            GraphCredentials(
                id      =c.id,
                user_id ='DUMMY',
                name    =c.name,
                airtable_api_key                 =\
                    c.airtable_api_key,
                airtable_base_id                 =\
                    c.airtable_base_id,
                airtable_states_table_id         =\
                    c.airtable_states_table_id,
                airtable_states_table_view_id    =\
                    c.airtable_states_table_view_id,
                airtable_transitions_table_id    =\
                    c.airtable_transitions_table_id,
                airtable_transition_table_view_id=\
                    c.airtable_transition_table_view_id,
                airtable_forms_table_id          =\
                    c.airtable_forms_table_id,
                airtable_forms_table_view_id     =\
                    c.airtable_forms_table_view_id,
                airtable_config_table_id         =\
                    c.airtable_config_table_id,
                airtable_config_table_view_id    =\
                    c.airtable_config_table_view_id
            ) for c in creds
        ]
        return ret

    def CreateGraph(self, graph) -> None:
        graph_schema = self.schema.graph_cred(
            **self.__CleanModel(graph)
        )
        self.db.session.add(graph_schema)
        self.db.session.commit()
        graph.id = graph_schema.id
        return graph

    def __CleanModel(self, model) -> dict:
        v = vars(model)
        v.pop('id')
        return v

    def __GetUser(self, key, value):
        users_t = self.schema.users
        db = self.db
        usr = self.db.session.scalars(
                  db.select(users_t)\
                  .where(getattr(users_t, key, 'id') == value)\
                  ).first()
        return usr

