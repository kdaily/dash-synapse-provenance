import synapseutils
import synapseutils.provenance
from prov.dot import prov_to_dot

import dash
import dash_html_components as html
import dash_core_components as dcc

import base64

app = dash.Dash()

app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([

    html.Label('Synapse ID'),
    dcc.Input(id="my-id", value='', type='text'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Img(id='prov-graph')
])

@app.callback(dash.dependencies.Output(component_id='prov-graph', component_property='src'),
              [dash.dependencies.Input('submit-button', 'n_clicks')],
              [dash.dependencies.State(component_id='my-id', component_property='value')])
def generate_provenance_graph(n_clicks, id):
    p = synapseutils.provenance.SynapseProvenanceDocument(id,
                                                          annotations=[])
    dot = prov_to_dot(p.prov_doc)
    image_filename = 'article-prov.png'
    dot.write_png(image_filename)

    encoded_image = base64.b64encode(open(image_filename, 'rb').read())

    return 'data:image/png;base64,{}'.format(encoded_image)


if __name__ == '__main__':
    app.run_server(debug=True)
