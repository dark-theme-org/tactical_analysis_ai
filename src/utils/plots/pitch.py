def drawPitch(x=120,
              y=80,
              num_zones_x = None,
              num_zones_y = None,
              c1='black',
              c2='grey',
              linewidth1=2,
              linewidth2=1,
              pitchcolor=0):

    if num_zones_x is None:
        num_zones_x = x
    if num_zones_y is None:
        num_zones_y = y

    shapes = []

    # Campo de futebol
    shapes.append({
        'type': 'rect',
        'x0': 0, 'y0': 0, 'x1': x, 'y1': y,
        'line': {'color': c1, 'width': linewidth1*2},
        'fillcolor': None
    })

    # Gol 1
    shapes.append({
        'type': 'rect',
        'x0': 0, 'y0': (y - y * 7.32 / 68) / 2, 'x1': -1.5, 'y1': (y * 7.32 / 68) + (y - y * 7.32 / 68) / 2,
        'line': {'color': c1, 'width': linewidth1*2},
        'fillcolor': None
    })

    # Gol 2
    shapes.append({
        'type': 'rect',
        'x0': x, 'y0': (y - y * 7.32 / 68) / 2, 'x1': x + 1.5, 'y1': (y * 7.32 / 68) + (y - y * 7.32 / 68) / 2,
        'line': {'color': c1, 'width': linewidth1*2},
        'fillcolor': None
    })

    # Áreas de 5 jardas
    shapes.append({
        'type': 'rect',
        'x0': x - x * 5.5 / 105, 'y0': y * 24 / 68, 'x1': x - x * 5.5 / 105 + x * 5.5 / 105, 'y1': y * 44 / 68,
        'line': {'color': c1, 'width': linewidth1},
        'fillcolor': None
    })
    shapes.append({
        'type': 'rect',
        'x0': 0, 'y0': y * 24 / 68, 'x1': x * 5.5 / 105, 'y1': y * 44 / 68,
        'line': {'color': c1, 'width': linewidth1},
        'fillcolor': None
    })

    # Áreas de pênalti
    shapes.append({
        'type': 'rect',
        'x0': x - x * 16.5 / 105, 'y0': y * 14 / 68, 'x1': x - x * 16.5 / 105 + x * 16.5 / 105, 'y1': y * 54 / 68,
        'line': {'color': c1, 'width': linewidth1},
        'fillcolor': None
    })
    shapes.append({
        'type': 'rect',
        'x0': 0, 'y0': y * 14 / 68, 'x1': x * 16.5 / 105, 'y1': y * 54 / 68,
        'line': {'color': c1, 'width': linewidth1},
        'fillcolor': None
    })

    # Marcas de pênalti
    shapes.append({
        'type': 'circle',
        'x0': x - (11 / 105) * x - 0.25, 'y0': y / 2 - 0.25, 'x1': x - (11 / 105) * x + 0.25, 'y1': y / 2 + 0.25,
        'line': {'color': 'black', 'width': linewidth1},
        'fillcolor': 'black'
    })
    shapes.append({
        'type': 'circle',
        'x0': (11 / 105) * x - 0.25, 'y0': y / 2 - 0.25, 'x1': (11 / 105) * x + 0.25, 'y1': y / 2 + 0.25,
        'line': {'color': 'black', 'width': linewidth1},
        'fillcolor': 'black'
    })

    # Círculos de pênalti
    shapes.append({
        'type': 'path',
        'path': f"M {x - (11 / 105) * x} {y / 2} A {(20 / 68) * y} {(20 / 68) * y} 0 0 0 {x - (11 / 105) * x} {y / 2}",
        'line': {'color': 'black', 'width': linewidth1}
    })
    shapes.append({
        'type': 'path',
        'path': f"M {(11 / 105) * x} {y / 2} A {(20 / 68) * y} {(20 / 68) * y} 0 0 1 {(11 / 105) * x} {y / 2}",
        'line': {'color': 'black', 'width': linewidth1}
    })

    # Círculo central
    shapes.append({
        'type': 'circle',
        'x0': x / 2 - (20 / 68) * y / 2, 'y0': y / 2 - (20 / 68) * y / 2,
        'x1': x / 2 + (20 / 68) * y / 2, 'y1': y / 2 + (20 / 68) * y / 2,
        'line': {'color': 'black', 'width': linewidth1},
        'fillcolor': None
    })

    # Linha central
    shapes.append({
        'type': 'line',
        'x0': x / 2, 'y0': 0, 'x1': x / 2, 'y1': y,
        'line': {'color': c1, 'width': linewidth1}
    })

    # Linhas de zona
    num_zones_x += 1
    num_zones_y += 1

    zones_shapes_x = [{
            'type': 'line',
            'x0': i * x / num_zones_x, 'y0': 0, 'x1': i * x / num_zones_x, 'y1': y,
            'line': {'color': c2, 'width': linewidth2, 'dash': 'dot'}
        } for i in range(1, num_zones_x)]

    zones_shapes_y = [{
            'type': 'line',
            'x0': 0, 'y0': i * y / num_zones_y, 'x1': x, 'y1': i * y / num_zones_y,
            'line': {'color': c2, 'width': linewidth2, 'dash': 'dot'}
        } for i in range(1, num_zones_y)]

    shapes += zones_shapes_x + zones_shapes_y

    # Colorindo o campo, se necessário
    if pitchcolor == 1:
        shapes.append({
            'type': 'rect',
            'x0': 0, 'y0': 0, 'x1': x, 'y1': y,
            'fillcolor': '#00FF00',
            'layer': 'below'
        })

    return shapes
