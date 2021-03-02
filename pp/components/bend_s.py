import pp
from pp.component import Component
from pp.components.bezier import bezier
from pp.tech import TECH_SILICON_C, Tech


@pp.cell
def bend_s(
    height: float = 2.0,
    length: float = 10.0,
    nb_points: int = 99,
    tech: Tech = TECH_SILICON_C,
) -> Component:
    """S bend with bezier curve

    Args:
        height: in y direction
        length: in x direction
        layer: gds number
        nb_points: number of points
        tech: Technology

    .. plot::
      :include-source:

      import pp

      c = pp.c.bend_s(height=20)
      c.plot()

    """
    l, h = length, height
    width = tech.wg_width
    layer = tech.layer_wg
    layers_cladding = tech.layers_cladding
    cladding_offset = tech.cladding_offset

    c = bezier(
        width=width,
        control_points=[(0, 0), (l / 2, 0), (l / 2, h), (l, h)],
        npoints=nb_points,
        layer=layer,
    )
    c.add_port(name="W0", port=c.ports.pop("0"))
    c.add_port(name="E0", port=c.ports.pop("1"))

    y = cladding_offset
    points = [
        [c.xmin, c.ymin - y],
        [c.xmax, c.ymin - y],
        [c.xmax, c.ymax + y],
        [c.xmin, c.ymax + y],
    ]
    for layer in layers_cladding:
        c.add_polygon(points, layer=layer)

    # c.ports["W0"] = c.ports.pop("0")
    # c.ports["E0"] = c.ports.pop("1")
    # print(c.min_bend_radius)
    return c


if __name__ == "__main__":
    c = bend_s()
    c.pprint()
    # c = bend_s_biased()
    # print(c.info["min_bend_radius"])
    c.show()
