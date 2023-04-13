from dash       import html, dcc
import dash_mantine_components as dmc


class GraphInfoPresenter():
    @staticmethod
    def ProcessStateInfo(info):
        forms = info['forms']
        acc   = dmc.Accordion(
          children=[ 
            dmc.AccordionItem(
              [
                dmc.AccordionControl(form['name']),
                dmc.AccordionPanel(form['text']),
              ],
              value=form['name'],
            ) for form in forms 
          ],
        )
        return acc

    @staticmethod
    def ProcessTransitionInfo(info):
        forms = info['forms']
        acc   = dmc.Accordion(
          children=[ 
            dmc.AccordionItem(
              [
                dmc.AccordionControl(form['name']),
                dmc.AccordionPanel(
                  dmc.List([
                    dmc.ListItem( dmc.Text(tag) )
                    for tag in form['tags'].split(",")
                  ])
                ),
              ],
              value=form['name'],
            ) for form in forms 
          ],
        )

        title =  info['info']['type']
        if title == 'CONDITIONAL':
            title = 'Условный'
        if title == 'UNCONDITIONAL':
            title = 'Безусловный'
        if title == 'STRICT':
            title = 'Строгий'

        return html.Div([title, acc])

    @staticmethod
    def ProcessGraphErrors(info):
        if info is None:
            rows = [
                html.Tr([html.Td('')])
            ]
        else:
            rows = [
                html.Tr([html.Td(i)]) for i in info
            ]
        return dmc.Table([html.Tbody(rows)])

