def chart_col(item, title=None):
    ''' Takes given as 'item' column chart object
    and formats the chart to wanted style.
    Can add title to the chart.'''

    item.set_title({
        'name': title,
        'name_font': {
            'name': 'Calibri',
            'bold': False,
            'color': '#595959',
            'size': 10,
        },
    })
    item.set_chartarea({
        'border': {'none': True},
        'fill':   {'color': '#ffffff'}
    })

    item.set_plotarea({
        'border': {'none': True},
        'fill':   {'color': '#ffffff'}
    })

    item.set_y_axis({
        'num_format': '0%',
        'min': 0,
        'line': {
            'none': True,
        },
        'major_gridlines': {
            'visible': True,
            'line': {
                'width': 0.75,
                'dash_type': 'solid',
                'color': '#D9D9D9'},
        },
        'num_font': {
            'name': 'Calibri',
            'bold': False,
            'color': '#595959',
            'size': 9,
        },
    })

    item.set_x_axis({
        'major_tick_mark': 'outside',
        'line': {
            'dash_type': 'solid',
            'color': '#D9D9D9'
        },
        'major_gridlines': {
            'visible': False,
        },
        'num_font': {
            'name': 'Calibri',
            'bold': False,
            'color': '#595959',
            'size': 9,
        },
    })

    if len(item.series) <= 1:
        item.set_legend({'none': True})
    else:
        item.set_legend({
            'position': 'top',
            'font': {
                'size': 9,
                'color': '#595959',
            },
        })

    return item


series = {
    'line': {
        'color': '#ffffff',
        'transparency': 0,
        'width': 1.5,
    },
    'data_labels': {
        'value': True,
        'num_format': '#,#0.0%',
        'font': {
            'name': 'Calibri',
            'size': 7,
            'color': '#404040',
        },
    },
    'gap': 100,
    'overlap': 0,
}
