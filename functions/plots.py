
import plotly.graph_objects as go

def setup_figure_layout(target):
    target.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ), height=650, margin=dict(t=1))

def add_2d_line_trace(target, x, y, trace_name):
    target.add_trace(go.Scatter(
        x = x,
        y = y,
        name = trace_name,
        marker = dict(size=2),
        line = dict(color='cyan', width=2),
        mode = 'lines',
        showlegend = True
    ))
    setup_figure_layout(target)

def add_3d_line_trace(target, x, y, z, trace_name):
    target.add_trace(go.Scatter3d(
        x = x,
        y = y,
        z = z,
        name = trace_name,
        marker = dict(size=2),
        line = dict(color='cyan', width=2),
        mode = 'lines',
        showlegend = True
    ))
    setup_figure_layout(target)


__all__ = ["add_2d_line_trace", "add_3d_line_trace"]
