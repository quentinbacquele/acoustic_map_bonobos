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
app = Dash(__name__)
server = app.server

@server.route('/segments/<path:filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

@server.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

# --- Custom CSS ---
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
            .Select-option:hover {
                background-color: #3a3a3a !important;
                color: #FFFFFF !important;
            }
            .Select-option.is-selected {
                background-color: #4a4a4a !important;
                color: #FFFFFF !important;
            }
            .Select-option.is-focused {
                background-color: #3a3a3a !important;
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

# --- Layout ---
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Mapping human perception of bonobo vocalizations refines emotional understanding across Hominoids",
                style={
                    'textAlign': 'center',
                    'margin': '0',
                    'color': '#FFFFFF',
                    'fontFamily': 'Space Grotesk, Inter, -apple-system, sans-serif',
                    'fontWeight': '700',
                    'fontSize': '24px',
                    'letterSpacing': '0.3px'
                })
    ], style={
        'backgroundColor': '#1a1a1a',
        'padding': '20px',
        'marginBottom': '20px'
    }),

    html.Div([
        # Left panel - Controls
        html.Div([
            html.Div([
                html.H3("Controls", style={
                    'color': '#FFFFFF',
                    'marginBottom': 20,
                    'fontFamily': 'Inter, sans-serif',
                    'fontWeight': '300',
                    'fontSize': '18px'
                }),

                # Audio player + Image viewer
                html.Div([
                    html.H4("Audio Player", style={'color': '#FFFFFF', 'marginBottom': 10, 'fontSize': 14, 'fontWeight': '300'}),
                    html.Audio(id='audio-player', controls=True, style={'width': '100%', 'marginBottom': 10, 'borderRadius': '4px'}),
                    html.Div(id='audio-info', style={'marginBottom': 25, 'fontSize': 11, 'color': '#888888', 'textAlign': 'center'}),

                    html.H4("Image Viewer", style={'color': '#FFFFFF', 'marginBottom': 10, 'fontSize': 14, 'fontWeight': '300'}),
                    html.Img(id='image-viewer', style={'width': '100%', 'borderRadius': '4px', 'marginBottom': 10}),
                    html.Div(id='image-info', style={'marginBottom': 25, 'fontSize': 11, 'color': '#888888', 'textAlign': 'center'})
                ], style={
                    'backgroundColor': 'rgba(255,255,255,0.05)',
                    'padding': '15px',
                    'borderRadius': '8px',
                    'marginBottom': '25px',
                    'border': '1px solid rgba(255,255,255,0.1)'
                }),

                # Visualization dropdown
                html.Label("Visualization:", style={
                    'fontWeight': '300', 'color': '#FFFFFF', 'fontSize': 12,
                    'marginBottom': 8, 'display': 'block', 'letterSpacing': '0.3px'
                }),
                html.Div([
                    dcc.Dropdown(
                        id='dimension-dropdown',
                        options=[{'label': '3D UMAP', 'value': '3d'}],
                        value='3d',
                        style={
                            'backgroundColor': '#2a2a2a', 'borderRadius': '4px',
                            'border': '1px solid rgba(255,255,255,0.1)', 'color': '#FFFFFF'
                        }
                    )
                ], style={'marginBottom': 25}),

                # Color by dropdown
                html.Label("Color by:", style={
                    'fontWeight': '300', 'color': '#FFFFFF', 'fontSize': 12,
                    'marginBottom': 8, 'display': 'block', 'letterSpacing': '0.3px'
                }),
                html.Div([
                    dcc.Dropdown(
                        id='color-dropdown',
                        options=[
                            {'label': 'Arousal', 'value': 'general_arousal'},
                            {'label': 'Valence', 'value': 'valence'},
                            {'label': 'Valence-Arousal', 'value': 'valence_arousal_refined'},
                            {'label': 'Context Complet', 'value': 'context_complet'},
                            {'label': 'Is playback?', 'value': 'Playback'},
                            {'label': 'Age class', 'value': 'age_class'},
                            {'label': 'Subject', 'value': 'subject'}
                        ],
                        value='valence_arousal_refined',
                        style={
                            'backgroundColor': '#2a2a2a', 'borderRadius': '4px',
                            'border': '1px solid rgba(255,255,255,0.1)', 'color': '#FFFFFF'
                        }
                    )
                ], style={'marginBottom': 25}),

                # Category highlight
                html.Div([
                    html.Label("Highlight Category:", style={
                        'fontWeight': '300', 'color': '#FFFFFF', 'fontSize': 12,
                        'marginBottom': 8, 'display': 'block', 'letterSpacing': '0.3px'
                    }),
                    html.Div([
                        dcc.Dropdown(
                            id='category-highlight',
                            options=[],
                            value='All',
                            placeholder="Select category to highlight",
                            style={
                                'backgroundColor': '#2a2a2a', 'borderRadius': '4px',
                                'border': '1px solid rgba(255,255,255,0.1)', 'color': '#FFFFFF'
                            }
                        )
                    ])
                ], id='category-highlight-container', style={'marginBottom': 25, 'display': 'none'}),

                # Point size slider
                html.Label("Point Size:", style={
                    'fontWeight': '300', 'color': '#FFFFFF', 'fontSize': 12,
                    'marginBottom': 8, 'display': 'block', 'letterSpacing': '0.3px'
                }),
                dcc.Slider(
                    id='size-slider', min=1, max=11, step=1, value=3,
                    marks={i: {'label': str(i), 'style': {'color': 'white'}} for i in range(1, 11, 2)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),

                # Opacity slider
                html.Label("Opacity:", style={
                    'fontWeight': '300', 'color': '#FFFFFF', 'fontSize': 12,
                    'marginTop': 25, 'marginBottom': 8, 'display': 'block', 'letterSpacing': '0.3px'
                }),
                dcc.Slider(
                    id='opacity-slider', min=0.3, max=1.0, step=0.1, value=1.0,
                    marks={i/10: {'label': f'{i/10:.1f}', 'style': {'color': 'white'}} for i in range(3, 11, 2)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),

            ], style={
                'backgroundColor': '#1a1a1a', 'padding': '20px',
                'borderRadius': '8px', 'border': '1px solid rgba(255,255,255,0.1)'
            })
        ], style={'width': '22%', 'padding': '10px'}),

        # Right panel - 3D Plot
        html.Div([
            dcc.Graph(
                id='3d-scatter',
                style={'height': '85vh', 'borderRadius': '8px', 'backgroundColor': '#1a1a1a'}
            )
        ], style={
            'width': '76%', 'marginLeft': '2%', 'padding': '10px',
            'backgroundColor': '#1a1a1a', 'borderRadius': '8px',
            'border': '1px solid rgba(255,255,255,0.1)'
        })

    ], style={
        'display': 'flex', 'marginTop': 10, 'gap': '10px', 'alignItems': 'flex-start'
    }),

    # Data Summary
    html.Div([
        html.H3("Data Summary", style={
            'color': '#FFFFFF', 'marginBottom': 15,
            'fontFamily': 'Inter, sans-serif', 'fontWeight': '300', 'fontSize': '16px'
        }),
        html.Div(id='data-summary', style={'color': '#FFFFFF'})
    ], style={
        'marginTop': 20, 'padding': '20px', 'backgroundColor': '#1a1a1a',
        'borderRadius': '8px', 'border': '1px solid rgba(255,255,255,0.1)'
    })
], style={
    'backgroundColor': '#0a0a0a', 'minHeight': '100vh',
    'fontFamily': 'Inter, -apple-system, sans-serif', 'padding': '0 15px 15px 15px'
})


# --- Callbacks ---
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

CUSTOM_DATA_COLS = [
    'subject', 'context', 'valence_arousal_refined', 'file',
    'has_audio', 'has_image', 'context_complet', 'context_general'
]


@callback(
    [Output('3d-scatter', 'figure'),
     Output('data-summary', 'children'),
     Output('category-highlight-container', 'style'),
     Output('category-highlight', 'options')],
    [Input('dimension-dropdown', 'value'),
     Input('color-dropdown', 'value'),
     Input('size-slider', 'value'),
     Input('opacity-slider', 'value'),
     Input('category-highlight', 'value')]
)
def update_plot(dimension, color_by, point_size, opacity, highlight_category):
    # Build custom_data columns list
    hover_valence = 'valence_arousal_refined'
    custom_cols = ['subject', 'context', hover_valence, 'file', 'has_audio', 'has_image', 'context_complet', 'context_general']

    # Determine color map
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

    # Category orders for valence_arousal_refined
    cat_orders = {'valence_arousal_refined': refined_category_order} if color_by == 'valence_arousal_refined' else None

    # Create 3D scatter plot
    fig = px.scatter_3d(
        vis_data,
        x='UMAP_1', y='UMAP_2', z='UMAP_3',
        color=color_by,
        color_discrete_map=cmap,
        category_orders=cat_orders,
        labels=labels_dict,
        hover_name='file',
        custom_data=custom_cols,
        title=f"3D Acoustic Feature Space - {labels_dict.get(color_by, color_by.replace('_', ' ').title())}"
    )

    # Apply category highlighting
    if highlight_category and highlight_category != 'All' and color_by in ['valence_arousal_refined']:
        fig.data = [t for t in fig.data if t.name == highlight_category]

    # Update markers and hover
    fig.update_traces(
        marker=dict(size=point_size, opacity=opacity, line=dict(width=0, color='rgba(0,0,0,0)')),
        hovertemplate='<b>%{hovertext}</b><br><br>'
                      '<b>Subject:</b> %{customdata[0]}<br>'
                      '<b>Context General:</b> %{customdata[7]}<br>'
                      '<b>Context:</b> %{customdata[6]}<br>'
                      '<b>Valence-Arousal:</b> %{customdata[2]}<br>'
                      '<extra></extra>'
    )

    # 3D layout
    x_range = [vis_data['UMAP_1'].min() - 0.1, vis_data['UMAP_1'].max() + 0.1]
    y_range = [vis_data['UMAP_2'].min() - 0.1, vis_data['UMAP_2'].max() + 0.1]
    z_range = [vis_data['UMAP_3'].min() - 0.1, vis_data['UMAP_3'].max() + 0.1]

    fig.update_layout(
        scene=dict(
            xaxis_title="Dimension 1", yaxis_title="Dimension 2", zaxis_title="Dimension 3",
            bgcolor='#1a1a1a',
            xaxis=dict(backgroundcolor="#1a1a1a", gridcolor="rgba(255,255,255,0.1)",
                       showgrid=True, gridwidth=1,
                       title_font=dict(color='#FFFFFF', size=12),
                       tickfont=dict(color='#888888', size=10), range=x_range),
            yaxis=dict(backgroundcolor="#1a1a1a", gridcolor="rgba(255,255,255,0.1)",
                       showgrid=True, gridwidth=1,
                       title_font=dict(color='#FFFFFF', size=12),
                       tickfont=dict(color='#888888', size=10), range=y_range),
            zaxis=dict(backgroundcolor="#1a1a1a", gridcolor="rgba(255,255,255,0.1)",
                       showgrid=True, gridwidth=1,
                       title_font=dict(color='#FFFFFF', size=12),
                       tickfont=dict(color='#888888', size=10), range=z_range),
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.8))
        ),
        paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a',
        height=800, margin=dict(l=10, r=10, t=40, b=10),
        title=dict(
            font=dict(size=16, color='#FFFFFF', family='Inter, sans-serif', weight=300),
            x=0.5, xanchor='center'
        ),
        legend=dict(
            bgcolor='rgba(26,26,26,0.9)', bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1, font=dict(size=14, color='#FFFFFF'),
            itemsizing='constant', itemwidth=50
        )
    )

    # Summary stats
    summary_stats = html.Div([
        html.Div([
            html.Div([
                html.H2(f"{len(vis_data)}", style={'margin': 0, 'color': '#FFFFFF', 'fontSize': 24, 'fontWeight': '300'}),
                html.P("Total Calls", style={'margin': 0, 'color': '#888888', 'fontSize': 10, 'letterSpacing': '0.5px'})
            ], style={'textAlign': 'center', 'flex': 1}),
            html.Div([
                html.H2(f"{vis_data['has_audio'].sum()}", style={'margin': 0, 'color': '#FFFFFF', 'fontSize': 24, 'fontWeight': '300'}),
                html.P("Audio Available", style={'margin': 0, 'color': '#888888', 'fontSize': 10, 'letterSpacing': '0.5px'})
            ], style={'textAlign': 'center', 'flex': 1}),
            html.Div([
                html.H2(f"{vis_data['subject'].nunique()}", style={'margin': 0, 'color': '#FFFFFF', 'fontSize': 24, 'fontWeight': '300'}),
                html.P("Bonobos", style={'margin': 0, 'color': '#888888', 'fontSize': 10, 'letterSpacing': '0.5px'})
            ], style={'textAlign': 'center', 'flex': 1}),
            html.Div([
                html.H2(f"{vis_data['context'].nunique()}", style={'margin': 0, 'color': '#FFFFFF', 'fontSize': 24, 'fontWeight': '300'}),
                html.P("Contexts", style={'margin': 0, 'color': '#888888', 'fontSize': 10, 'letterSpacing': '0.5px'})
            ], style={'textAlign': 'center', 'flex': 1})
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': 15}),
        html.Hr(style={'border': '1px solid rgba(255,255,255,0.1)', 'margin': '15px 0'}),
        html.H4("Valence-Arousal Distribution", style={
            'color': '#FFFFFF', 'fontWeight': '300', 'marginBottom': 10, 'fontSize': 14
        }),
        html.Div([
            html.Div([
                html.Span(f"{cat.replace('_', ' ').title()}: ", style={'fontWeight': '300', 'color': '#FFFFFF', 'fontSize': 11}),
                html.Span(f"{vis_data['valence_arousal_refined'].value_counts().get(cat, 0)}", style={'color': '#888888', 'fontSize': 11})
            ], style={'marginBottom': 5, 'padding': '3px 8px', 'backgroundColor': 'rgba(255,255,255,0.03)', 'borderRadius': '3px'})
            for cat in refined_category_order if cat in vis_data['valence_arousal_refined'].values
        ])
    ])

    # Category highlight options
    if color_by in ['valence_arousal_refined']:
        container_style = {'marginBottom': 25, 'display': 'block'}
        category_options = [{'label': 'All Categories', 'value': 'All'}] + \
                           [{'label': cat.replace('_', ' ').title(), 'value': cat}
                            for cat in refined_category_order if cat in vis_data['valence_arousal_refined'].values]
    else:
        container_style = {'marginBottom': 25, 'display': 'none'}
        category_options = []

    return fig, summary_stats, container_style, category_options


@callback(
    [Output('audio-player', 'src'),
     Output('audio-info', 'children'),
     Output('image-viewer', 'src'),
     Output('image-info', 'children')],
    [Input('3d-scatter', 'clickData')]
)
def update_media(clickData):
    if clickData is None:
        return None, "Click on a data point to play audio", None, "Click on a data point to view image"

    point = clickData['points'][0]
    file_name = point['customdata'][3]
    has_audio = point['customdata'][4]
    has_image = point['customdata'][5]

    if has_audio:
        audio_src = f"/segments/{file_name}"
        audio_text = f"Playing: {file_name}"
    else:
        audio_src = None
        audio_text = f"Audio not found: {file_name}"

    if has_image:
        image_name = file_name.replace('.wav', '.png')
        image_src = f"/images/{image_name}"
        image_text = f"Displaying: {image_name}"
    else:
        image_src = None
        image_text = f"Image not found: {file_name}"

    return audio_src, audio_text, image_src, image_text


if __name__ == '__main__':
    app.run(debug=True, port=8050)
