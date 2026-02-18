# -*- coding: utf-8 -*-
"""
Bonobo Acoustic Space Visualization - Deployable Dash App
Mapping human perception of bonobo vocalizations refines emotional understanding across Hominoids
"""

import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, callback
from flask import send_from_directory
import os
import warnings
warnings.filterwarnings('ignore')

# --- Data Loading ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
vis_data = pd.read_csv(os.path.join(BASE_DIR, 'data_precomputed.csv'))

AUDIO_DIR = os.path.join(BASE_DIR, 'audio')
IMAGE_DIR = os.path.join(BASE_DIR, 'spider_plots')

# --- Color Maps ---
color_map_refined = {
    'positive_high': '#CA5A94',
    'positive_low': '#D59428',
    'negative_high': '#176C92',
    'negative_low': '#138866',
}

refined_category_order = ['positive_high', 'positive_low', 'negative_low', 'negative_high']

color_map_valence = {'positive': '#669bbc', 'negative': '#a06cd5'}
color_map_arousal = {'high': '#C33149', 'low': '#A8C256'}
color_map_playback = {'Yes': '#99e2b4', 'No': '#036666'}

# --- App Setup ---
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

@server.route('/segments/<path:filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

@server.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

# --- Custom HTML/CSS ---
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Bonobo Acoustic Space</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            html, body { overflow: hidden; height: 100vh; }
            /* Legacy Select classes */
            .Select-control {
                background-color: #2a2a2a !important;
                border: 1px solid rgba(255,255,255,0.1) !important;
                color: #FFFFFF !important;
            }
            .Select-input { color: #FFFFFF !important; }
            .Select-placeholder { color: #888888 !important; }
            .Select-value-label { color: #FFFFFF !important; }
            .Select-arrow { border-color: #FFFFFF transparent transparent !important; }
            .Select-menu-outer {
                background-color: #2a2a2a !important;
                border: 1px solid rgba(255,255,255,0.1) !important;
            }
            .Select-option {
                background-color: #2a2a2a !important;
                color: #FFFFFF !important;
                padding: 8px 10px !important;
            }
            .Select-option:hover, .Select-option.is-focused {
                background-color: #3a3a3a !important;
            }
            .Select-option.is-selected {
                background-color: #4a4a4a !important;
            }
            /* Modern Dash dropdown classes */
            .dash-dropdown .Select-control,
            .VirtualizedSelectFocusedOption {
                background-color: #2a2a2a !important;
                color: #FFFFFF !important;
            }
            .VirtualizedSelectOption {
                background-color: #2a2a2a !important;
                color: #FFFFFF !important;
            }
            .VirtualizedSelectFocusedOption {
                background-color: #3a3a3a !important;
            }
            /* Dash 2.x dropdown overrides */
            .Select.is-open > .Select-control { background-color: #2a2a2a !important; }
            .Select-menu { background-color: #2a2a2a !important; }
            .Select--single > .Select-control .Select-value { color: #FFFFFF !important; }
            .has-value.Select--single > .Select-control .Select-value .Select-value-label {
                color: #FFFFFF !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# --- Home Page ---
home_page = html.Div([
    # Full-screen hero with image background
    html.Div([
        # Dark overlay
        html.Div(style={
            'position': 'absolute', 'top': 0, 'left': 0, 'right': 0, 'bottom': 0,
            'background': 'linear-gradient(135deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.5) 50%, rgba(0,0,0,0.85) 100%)',
            'zIndex': 1
        }),
        # Content centered
        html.Div([
            html.P("Interactive Visualization", style={
                'color': 'rgba(255,255,255,0.5)',
                'fontSize': '13px',
                'letterSpacing': '4px',
                'textTransform': 'uppercase',
                'marginBottom': '24px',
                'fontFamily': 'Space Grotesk, sans-serif',
                'fontWeight': '300'
            }),
            html.H1("Mapping human perception of bonobo vocalizations refines emotional understanding across Hominoids", style={
                'color': '#FFFFFF',
                'fontFamily': 'Space Grotesk, sans-serif',
                'fontWeight': '600',
                'fontSize': 'clamp(22px, 3vw, 38px)',
                'lineHeight': '1.3',
                'maxWidth': '800px',
                'margin': '0 auto 40px auto',
                'textAlign': 'center'
            }),
            html.Div([
                html.Span(f"{len(vis_data)}", style={'color': '#FFFFFF', 'fontWeight': '600', 'fontSize': '18px'}),
                html.Span(" vocalizations", style={'color': 'rgba(255,255,255,0.6)', 'fontSize': '14px'}),
                html.Span("  |  ", style={'color': 'rgba(255,255,255,0.2)', 'fontSize': '14px', 'margin': '0 8px'}),
                html.Span(f"{vis_data['subject'].nunique()}", style={'color': '#FFFFFF', 'fontWeight': '600', 'fontSize': '18px'}),
                html.Span(" bonobos", style={'color': 'rgba(255,255,255,0.6)', 'fontSize': '14px'}),
                html.Span("  |  ", style={'color': 'rgba(255,255,255,0.2)', 'fontSize': '14px', 'margin': '0 8px'}),
                html.Span(f"{vis_data['context'].nunique()}", style={'color': '#FFFFFF', 'fontWeight': '600', 'fontSize': '18px'}),
                html.Span(" contexts", style={'color': 'rgba(255,255,255,0.6)', 'fontSize': '14px'}),
            ], style={'marginBottom': '48px', 'textAlign': 'center'}),
            html.Button("Explore the Acoustic Space", id='enter-btn', n_clicks=0, style={
                'padding': '14px 40px',
                'fontSize': '15px',
                'fontFamily': 'Space Grotesk, sans-serif',
                'fontWeight': '500',
                'color': '#FFFFFF',
                'backgroundColor': 'transparent',
                'border': '1px solid rgba(255,255,255,0.4)',
                'borderRadius': '4px',
                'cursor': 'pointer',
                'letterSpacing': '1px',
                'transition': 'all 0.3s ease',
                'backdropFilter': 'blur(4px)'
            })
        ], style={
            'position': 'relative', 'zIndex': 2,
            'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center',
            'justifyContent': 'center', 'height': '100vh', 'padding': '20px'
        })
    ], style={
        'position': 'relative',
        'height': '100vh',
        'backgroundImage': 'url(/assets/bonobo.jpg)',
        'backgroundSize': 'cover',
        'backgroundPosition': 'center 30%'
    })
], id='home-page')

# --- Visualization Page ---
viz_page = html.Div([
    # Compact header bar
    html.Div([
        html.Span("Bonobo Acoustic Space", style={
            'color': '#FFFFFF',
            'fontFamily': 'Space Grotesk, sans-serif',
            'fontWeight': '600',
            'fontSize': '15px',
            'letterSpacing': '0.5px'
        }),
        html.Button("Home", id='home-btn', n_clicks=0, style={
            'padding': '5px 16px',
            'fontSize': '12px',
            'fontFamily': 'Space Grotesk, sans-serif',
            'fontWeight': '400',
            'color': 'rgba(255,255,255,0.7)',
            'backgroundColor': 'transparent',
            'border': '1px solid rgba(255,255,255,0.2)',
            'borderRadius': '3px',
            'cursor': 'pointer',
            'letterSpacing': '0.5px'
        })
    ], style={
        'backgroundColor': '#1a1a1a',
        'padding': '10px 20px',
        'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
        'borderBottom': '1px solid rgba(255,255,255,0.08)'
    }),

    # Main content
    html.Div([
        # Left panel - Controls
        html.Div([
            # Audio player + Image viewer
            html.Div([
                html.H4("Audio Player", style={'color': '#FFFFFF', 'marginBottom': 8, 'fontSize': 12, 'fontWeight': '400', 'letterSpacing': '0.5px'}),
                html.Audio(id='audio-player', controls=True, style={'width': '100%', 'marginBottom': 6, 'borderRadius': '4px'}),
                html.Div(id='audio-info', style={'marginBottom': 16, 'fontSize': 10, 'color': '#666', 'textAlign': 'center'}),
                html.H4("Spider Plot", style={'color': '#FFFFFF', 'marginBottom': 8, 'fontSize': 12, 'fontWeight': '400', 'letterSpacing': '0.5px'}),
                html.Img(id='image-viewer', style={'width': '100%', 'borderRadius': '4px', 'marginBottom': 6}),
                html.Div(id='image-info', style={'marginBottom': 12, 'fontSize': 10, 'color': '#666', 'textAlign': 'center'})
            ], style={
                'backgroundColor': 'rgba(255,255,255,0.03)',
                'padding': '12px',
                'borderRadius': '6px',
                'marginBottom': '16px',
                'border': '1px solid rgba(255,255,255,0.06)'
            }),

            # Color by
            html.Label("Color by", style={
                'fontWeight': '400', 'color': 'rgba(255,255,255,0.5)', 'fontSize': 11,
                'marginBottom': 6, 'display': 'block', 'letterSpacing': '1px', 'textTransform': 'uppercase'
            }),
            dcc.Dropdown(
                id='color-dropdown',
                options=[
                    {'label': 'Valence-Arousal', 'value': 'valence_arousal_refined'},
                    {'label': 'Arousal', 'value': 'general_arousal'},
                    {'label': 'Valence', 'value': 'valence'},
                    {'label': 'Context', 'value': 'context_complet'},
                    {'label': 'Playback', 'value': 'Playback'},
                    {'label': 'Age class', 'value': 'age_class'},
                    {'label': 'Subject', 'value': 'subject'}
                ],
                value='valence_arousal_refined',
                style={'backgroundColor': '#2a2a2a', 'borderRadius': '4px',
                       'border': '1px solid rgba(255,255,255,0.1)', 'color': '#FFFFFF',
                       'marginBottom': 16}
            ),

            # Category highlight
            html.Div([
                html.Label("Highlight", style={
                    'fontWeight': '400', 'color': 'rgba(255,255,255,0.5)', 'fontSize': 11,
                    'marginBottom': 6, 'display': 'block', 'letterSpacing': '1px', 'textTransform': 'uppercase'
                }),
                dcc.Dropdown(
                    id='category-highlight',
                    options=[],
                    value='All',
                    style={'backgroundColor': '#2a2a2a', 'borderRadius': '4px',
                           'border': '1px solid rgba(255,255,255,0.1)', 'color': '#FFFFFF'}
                )
            ], id='category-highlight-container', style={'marginBottom': 16, 'display': 'none'}),

            # Point size
            html.Label("Point size", style={
                'fontWeight': '400', 'color': 'rgba(255,255,255,0.5)', 'fontSize': 11,
                'marginBottom': 6, 'display': 'block', 'letterSpacing': '1px', 'textTransform': 'uppercase'
            }),
            dcc.Slider(
                id='size-slider', min=1, max=11, step=1, value=3,
                marks={i: {'label': str(i), 'style': {'color': '#555', 'fontSize': '10px'}} for i in range(1, 12, 2)},
                tooltip={"placement": "bottom", "always_visible": False}
            ),

            # Opacity
            html.Label("Opacity", style={
                'fontWeight': '400', 'color': 'rgba(255,255,255,0.5)', 'fontSize': 11,
                'marginTop': 16, 'marginBottom': 6, 'display': 'block', 'letterSpacing': '1px', 'textTransform': 'uppercase'
            }),
            dcc.Slider(
                id='opacity-slider', min=0.3, max=1.0, step=0.1, value=1.0,
                marks={i/10: {'label': f'{i/10:.1f}', 'style': {'color': '#555', 'fontSize': '10px'}} for i in range(3, 11, 2)},
                tooltip={"placement": "bottom", "always_visible": False}
            ),
        ], style={
            'width': '240px', 'minWidth': '240px',
            'padding': '12px',
            'backgroundColor': '#111',
            'overflowY': 'auto',
            'height': 'calc(100vh - 45px)'
        }),

        # Right panel - 3D Plot (fills remaining space)
        html.Div([
            dcc.Graph(
                id='3d-scatter',
                style={'height': 'calc(100vh - 45px)', 'backgroundColor': '#1a1a1a'},
                config={'displayModeBar': True, 'displaylogo': False}
            )
        ], style={
            'flex': 1,
            'backgroundColor': '#1a1a1a'
        })
    ], style={
        'display': 'flex',
        'height': 'calc(100vh - 45px)'
    }),

    # Hidden dummy for dimension dropdown (kept for callback compatibility)
    dcc.Dropdown(id='dimension-dropdown', value='3d', style={'display': 'none'})
], id='viz-page', style={'display': 'none'})


# --- Main Layout ---
app.layout = html.Div([
    home_page,
    viz_page
], style={
    'backgroundColor': '#0a0a0a',
    'height': '100vh',
    'overflow': 'hidden',
    'fontFamily': 'Inter, -apple-system, sans-serif'
})


# --- Navigation Callbacks ---
@callback(
    [Output('home-page', 'style'),
     Output('viz-page', 'style')],
    [Input('enter-btn', 'n_clicks'),
     Input('home-btn', 'n_clicks')]
)
def navigate(enter_clicks, home_clicks):
    from dash import ctx
    if ctx.triggered_id == 'enter-btn' and enter_clicks:
        return {'display': 'none'}, {'display': 'block'}
    return {}, {'display': 'none'}


# --- Plot Callback ---
labels_dict = {
    'general_arousal': 'Arousal', 'valence': 'Valence',
    'valence_arousal_refined': 'Valence-Arousal',
    'context_complet': 'Context', 'age_class': 'Age Class', 'subject': 'Subject',
    'high': 'High Arousal', 'low': 'Low Arousal',
    'positive': 'Positive Valence', 'negative': 'Negative Valence',
    'positive_high': 'Positive-High', 'positive_low': 'Positive-Low',
    'negative_high': 'Negative-High', 'negative_low': 'Negative-Low',
    'Agonistic_victim': 'Agonistic victim',
    'Agonistic_third-party': 'Agonistic third party',
    'Agonistic_aggressor': 'Agonistic aggressor',
    'Romm_shift': 'Change in enclosure',
    'External-event': 'External event',
    'Post_conflict': 'Post conflict',
    'Infant_Begging_to_mother': 'Infant begging to mother'
}


@callback(
    [Output('3d-scatter', 'figure'),
     Output('category-highlight-container', 'style'),
     Output('category-highlight', 'options')],
    [Input('color-dropdown', 'value'),
     Input('size-slider', 'value'),
     Input('opacity-slider', 'value'),
     Input('category-highlight', 'value')]
)
def update_plot(color_by, point_size, opacity, highlight_category):
    custom_cols = ['subject', 'context', 'valence_arousal_refined', 'file', 'has_audio', 'has_image', 'context_complet', 'context_general']

    if color_by == 'valence_arousal_refined':
        cmap = color_map_refined
    elif color_by == 'valence':
        cmap = color_map_valence
    elif color_by == 'general_arousal':
        cmap = color_map_arousal
    elif color_by == 'Playback':
        cmap = color_map_playback
    else:
        cmap = None

    cat_orders = {'valence_arousal_refined': refined_category_order} if color_by == 'valence_arousal_refined' else None

    fig = px.scatter_3d(
        vis_data,
        x='UMAP_1', y='UMAP_2', z='UMAP_3',
        color=color_by,
        color_discrete_map=cmap,
        category_orders=cat_orders,
        labels=labels_dict,
        hover_name='file',
        custom_data=custom_cols
    )

    if highlight_category and highlight_category != 'All' and color_by == 'valence_arousal_refined':
        fig.data = [t for t in fig.data if t.name == highlight_category]

    fig.update_traces(
        marker=dict(size=point_size, opacity=opacity, line=dict(width=0, color='rgba(0,0,0,0)')),
        hovertemplate='<b>%{hovertext}</b><br><br>'
                      '<b>Subject:</b> %{customdata[0]}<br>'
                      '<b>Context General:</b> %{customdata[7]}<br>'
                      '<b>Context:</b> %{customdata[6]}<br>'
                      '<b>Valence-Arousal:</b> %{customdata[2]}<br>'
                      '<extra></extra>'
    )

    x_range = [vis_data['UMAP_1'].min() - 0.1, vis_data['UMAP_1'].max() + 0.1]
    y_range = [vis_data['UMAP_2'].min() - 0.1, vis_data['UMAP_2'].max() + 0.1]
    z_range = [vis_data['UMAP_3'].min() - 0.1, vis_data['UMAP_3'].max() + 0.1]

    fig.update_layout(
        scene=dict(
            xaxis_title="Dimension 1", yaxis_title="Dimension 2", zaxis_title="Dimension 3",
            bgcolor='#1a1a1a',
            xaxis=dict(backgroundcolor="#1a1a1a", gridcolor="rgba(255,255,255,0.06)",
                       showgrid=True, gridwidth=1,
                       title_font=dict(color='#888', size=11),
                       tickfont=dict(color='#555', size=9), range=x_range),
            yaxis=dict(backgroundcolor="#1a1a1a", gridcolor="rgba(255,255,255,0.06)",
                       showgrid=True, gridwidth=1,
                       title_font=dict(color='#888', size=11),
                       tickfont=dict(color='#555', size=9), range=y_range),
            zaxis=dict(backgroundcolor="#1a1a1a", gridcolor="rgba(255,255,255,0.06)",
                       showgrid=True, gridwidth=1,
                       title_font=dict(color='#888', size=11),
                       tickfont=dict(color='#555', size=9), range=z_range),
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.8))
        ),
        paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            bgcolor='rgba(26,26,26,0.95)', bordercolor='rgba(255,255,255,0.08)',
            borderwidth=1, font=dict(size=12, color='#CCC'),
            itemsizing='constant', itemwidth=40
        )
    )

    if color_by == 'valence_arousal_refined':
        container_style = {'marginBottom': 16, 'display': 'block'}
        category_options = [{'label': 'All Categories', 'value': 'All'}] + \
                           [{'label': cat.replace('_', ' ').title(), 'value': cat}
                            for cat in refined_category_order if cat in vis_data['valence_arousal_refined'].values]
    else:
        container_style = {'marginBottom': 16, 'display': 'none'}
        category_options = []

    return fig, container_style, category_options


@callback(
    [Output('audio-player', 'src'),
     Output('audio-info', 'children'),
     Output('image-viewer', 'src'),
     Output('image-info', 'children')],
    [Input('3d-scatter', 'clickData')]
)
def update_media(clickData):
    if clickData is None:
        return None, "Click a point to play audio", None, "Click a point to view spider plot"

    point = clickData['points'][0]
    file_name = point['customdata'][3]
    has_audio = point['customdata'][4]
    has_image = point['customdata'][5]

    if has_audio:
        audio_src = f"/segments/{file_name}"
        audio_text = file_name
    else:
        audio_src = None
        audio_text = f"No audio: {file_name}"

    if has_image:
        image_name = file_name.replace('.wav', '.png')
        image_src = f"/images/{image_name}"
        image_text = image_name
    else:
        image_src = None
        image_text = f"No image: {file_name}"

    return audio_src, audio_text, image_src, image_text


if __name__ == '__main__':
    app.run(debug=True, port=8050)
