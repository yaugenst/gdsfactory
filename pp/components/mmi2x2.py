import pp
from pp.cell import cell
from pp.component import Component
from pp.components.taper import taper as taper_function
from pp.tech import TECH_SILICON_C, Tech
from pp.types import ComponentFactory


@cell
def mmi2x2(
    width_taper: float = 0.95,
    length_taper: float = 10.0,
    length_mmi: float = 15.45,
    width_mmi: float = 2.1,
    gap_mmi: float = 0.2,
    taper: ComponentFactory = taper_function,
    tech: Tech = TECH_SILICON_C,
) -> Component:
    r"""Mmi 2x2

    Args:
        width_taper: interface between input waveguides and mmi region
        length_taper: into the mmi region
        length_mmi: in x direction
        width_mmi: in y direction
        gap_mmi: (width_taper + gap between tapered wg)/2
        taper: taper function

    .. plot::
      :include-source:

      import pp
      c = pp.c.mmi2x2(length_mmi=15.45, width_mmi=2.1)
      c.plot()


    .. code::

                   length_mmi
                    <------>
                    ________
                   |        |
                __/          \__
                __            __
                  \          /_ _ _ _
                  |         | _ _ _ _| gap_mmi
                __/          \__
                __            __
                  \          /
                   |________|

                 <->
            length_taper

    """
    wg_width = tech.wg_width
    layers_cladding = tech.layers_cladding
    layer = tech.layer_wg
    cladding_offset = tech.cladding_offset

    component = pp.Component()
    w_mmi = width_mmi
    w_taper = width_taper

    taper = taper(length=length_taper, width1=wg_width, width2=w_taper, tech=tech)

    a = gap_mmi / 2 + width_taper / 2
    mmi = pp.c.rectangle(
        size=(length_mmi, w_mmi),
        layer=layer,
        centered=True,
        ports={
            "E": [(+length_mmi / 2, -a, w_taper), (+length_mmi / 2, +a, w_taper)],
            "W": [(-length_mmi / 2, -a, w_taper), (-length_mmi / 2, +a, w_taper)],
        },
    )
    if layers_cladding:
        for layer_cladding in layers_cladding:
            clad = component << pp.c.rectangle(
                size=(length_mmi, w_mmi + 2 * cladding_offset),
                layer=layer_cladding,
                centered=True,
            )
            component.absorb(clad)

    mmi_section = component.add_ref(mmi)

    for port_name, port in mmi_section.ports.items():
        taper_ref = component << taper
        taper_ref.connect(port="2", destination=port)
        component.add_port(name=port_name, port=taper_ref.ports["1"])
        component.absorb(taper_ref)

    component.simulation_settings = dict(port_width=1.5e-6)
    component.absorb(mmi_section)
    return component


@cell
def mmi2x2_biased(
    wg_width=0.5,
    width_taper=0.95,
    length_taper=10,
    length_mmi=15.45,
    width_mmi=2.1,
    gap_mmi=0.2,
    layer=pp.LAYER.WG,
):
    return mmi2x2(
        wg_width=pp.bias.width(wg_width),
        width_taper=pp.bias.width(width_taper),
        length_taper=length_taper,
        length_mmi=length_mmi,
        width_mmi=pp.bias.width(width_mmi),
        gap_mmi=pp.bias.gap(gap_mmi),
        layer=layer,
    )


def test_mmi2x2():
    c = mmi2x2()
    pp.write_gds(c)


if __name__ == "__main__":
    c = mmi2x2()
    # c = mmi2x2_biased()
    # pp.write_to_libary("mmi1x2", width_mmi=10, overwrite=True)
    # print(c.get_optical_ports())
    print(c.get_settings())
    c.show()
