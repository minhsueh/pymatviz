# %%
from typing import cast

import matplotlib.pyplot as plt
from matminer.datasets import load_dataset
from mp_api.client import MPRester
from pymatgen.core import Structure

import pymatviz as pmv
from pymatviz.enums import ElemColorScheme, Key


struct: Structure  # for type hinting

df_steels = load_dataset("matbench_steels")
df_phonons = load_dataset("matbench_phonons")


# %% Plot Matbench phonon structures
n_structs = 12
fig, axs = pmv.structure_2d(
    df_phonons[Key.structure].iloc[:n_structs],
    show_bonds=True,
    bond_kwargs=dict(facecolor="gray", linewidth=2, linestyle="dotted"),
    elem_colors=ElemColorScheme.jmol,
)
title = f"{n_structs} Matbench phonon structures"
fig.suptitle(title, fontweight="bold", fontsize=20)
# pmv.io.save_and_compress_svg(fig, "matbench-phonons-structures-2d")
fig.show()


# %% Plot some disordered structures in 2D
disordered_structs = {
    mp_id: MPRester().get_structure_by_material_id(mp_id, conventional_unit_cell=True)
    for mp_id in ["mp-19017", "mp-12712"]
}

for mp_id, struct in disordered_structs.items():
    for site in struct:  # disorder structures in-place
        if "Fe" in site.species:
            site.species = {"Fe": 0.4, "C": 0.4, "Mn": 0.2}
        elif "Zr" in site.species:
            site.species = {"Zr": 0.5, "Hf": 0.5}

    ax = cast(plt.Axes, pmv.structure_2d(struct))
    _, spacegroup = struct.get_space_group_info()

    formula = struct.formula.replace(" ", "")
    text = f"{formula}\ndisordered {mp_id}, {spacegroup = }"
    href = f"https://materialsproject.org/materials/{mp_id}"
    ax.text(
        0.5, 1, text, url=href, ha="center", transform=ax.transAxes, fontweight="bold"
    )

    ax.figure.set_size_inches(8, 8)

    pmv.io.save_and_compress_svg(ax, f"struct-2d-{mp_id}-{formula}-disordered")
    plt.show()
