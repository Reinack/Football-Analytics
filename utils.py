import plotly.graph_objects as go


def add_football_field(fig):
    """Add a football pitch to a plotly figure using shapes."""
    shapes = [
        dict(type="rect", x0=0, y0=0, x1=105, y1=68,
             line=dict(color="white", width=2), fillcolor="#2d8a4e"),
        dict(type="line", x0=52.5, y0=0, x1=52.5, y1=68,
             line=dict(color="white", width=2)),
        dict(type="rect", x0=0, y0=13.84, x1=16.5, y1=54.16,
             line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)"),
        dict(type="rect", x0=88.5, y0=13.84, x1=105, y1=54.16,
             line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)"),
        dict(type="rect", x0=0, y0=24.84, x1=5.5, y1=43.16,
             line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)"),
        dict(type="rect", x0=99.5, y0=24.84, x1=105, y1=43.16,
             line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)"),
        dict(type="circle", x0=43.35, y0=24.85, x1=61.65, y1=43.15,
             line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)"),
        dict(type="circle", x0=10.7, y0=33.7, x1=11.3, y1=34.3,
             fillcolor="white", line=dict(color="white", width=1)),
        dict(type="circle", x0=93.7, y0=33.7, x1=94.3, y1=34.3,
             fillcolor="white", line=dict(color="white", width=1)),
    ]
    for shape in shapes:
        fig.add_shape(**shape)

    fig.update_xaxes(range=[-2, 107], showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(
        range=[-2, 70], showgrid=False, zeroline=False, showticklabels=False,
        scaleanchor="x", scaleratio=1,
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig
