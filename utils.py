import plotly.graph_objects as go


FIELD_SHAPES = [
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


def add_football_field(fig):
    """Field with scaleanchor=x — for position marker charts (page 1)."""
    for shape in FIELD_SHAPES:
        fig.add_shape(**shape)
    fig.update_xaxes(range=[-2, 107], showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(
        range=[-2, 70], showgrid=False, zeroline=False, showticklabels=False,
        scaleanchor="x", scaleratio=1,
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig


def add_football_field_scatter(fig):
    """Field without scaleanchor — for scatter/goal charts (page 2).
    Returns fixed width/height to preserve pitch proportions."""
    for shape in FIELD_SHAPES:
        fig.add_shape(**shape)
    fig.update_xaxes(range=[0, 105], showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(range=[0, 68], showgrid=False, zeroline=False, showticklabels=False)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        width=735,   # 105/68 * 475 ≈ 735  →  correct pitch aspect ratio
        height=475,
        autosize=False,
    )
    return fig
