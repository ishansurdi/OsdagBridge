from osdagbridge.core.reports.report_utils import _fig_embed, render_report_table
from osdagbridge.core.utils.common import (
    KEY_BOQ_BRACING_BOTTOM_QTY,
    KEY_BOQ_BRACING_BOTTOM_VOL_FORMULA,
    KEY_BOQ_BRACING_BOTTOM_VOL_TOTAL,
    KEY_BOQ_BRACING_BOTTOM_WT_SINGLE,
    KEY_BOQ_BRACING_BOTTOM_WT_TOTAL,
    KEY_BOQ_BRACING_DIAGONAL_QTY,
    KEY_BOQ_BRACING_DIAGONAL_VOL_FORMULA,
    KEY_BOQ_BRACING_DIAGONAL_VOL_TOTAL,
    KEY_BOQ_BRACING_DIAGONAL_WT_SINGLE,
    KEY_BOQ_BRACING_DIAGONAL_WT_TOTAL,
    KEY_BOQ_BRACING_TOP_QTY,
    KEY_BOQ_BRACING_TOP_VOL_FORMULA,
    KEY_BOQ_BRACING_TOP_VOL_TOTAL,
    KEY_BOQ_BRACING_TOP_WT_SINGLE,
    KEY_BOQ_BRACING_TOP_WT_TOTAL,
    KEY_BOQ_CONCRETE_DECK_QTY,
    KEY_BOQ_CONCRETE_DECK_VOL_FORMULA,
    KEY_BOQ_CONCRETE_DECK_VOL_TOTAL,
    KEY_BOQ_CONCRETE_DECK_WT_SINGLE,
    KEY_BOQ_CONCRETE_DECK_WT_TOTAL,
    KEY_BOQ_CONNECTIONS_QTY,
    KEY_BOQ_CONNECTIONS_VOL_FORMULA,
    KEY_BOQ_CONNECTIONS_VOL_TOTAL,
    KEY_BOQ_CONNECTIONS_WT_SINGLE,
    KEY_BOQ_CONNECTIONS_WT_TOTAL,
    KEY_BOQ_CRASH_BARRIER_QTY,
    KEY_BOQ_CRASH_BARRIER_VOL_FORMULA,
    KEY_BOQ_CRASH_BARRIER_VOL_TOTAL,
    KEY_BOQ_CRASH_BARRIER_WT_SINGLE,
    KEY_BOQ_CRASH_BARRIER_WT_TOTAL,
    KEY_BOQ_MATERIAL_QUANTITIES,
    KEY_BOQ_REBAR_DECK_QTY,
    KEY_BOQ_REBAR_DECK_VOL_FORMULA,
    KEY_BOQ_REBAR_DECK_VOL_TOTAL,
    KEY_BOQ_REBAR_DECK_WT_SINGLE,
    KEY_BOQ_REBAR_DECK_WT_TOTAL,
    KEY_BOQ_SHEAR_STUDS_QTY,
    KEY_BOQ_SHEAR_STUDS_VOL_FORMULA,
    KEY_BOQ_SHEAR_STUDS_VOL_TOTAL,
    KEY_BOQ_SHEAR_STUDS_WT_SINGLE,
    KEY_BOQ_SHEAR_STUDS_WT_TOTAL,
    KEY_BOQ_STEEL_GIRDERS_QTY,
    KEY_BOQ_STEEL_GIRDERS_VOL_FORMULA,
    KEY_BOQ_STEEL_GIRDERS_VOL_TOTAL,
    KEY_BOQ_STEEL_GIRDERS_WT_SINGLE,
    KEY_BOQ_STEEL_GIRDERS_WT_TOTAL,
    KEY_BOQ_STIFFENER_BEARING_QTY,
    KEY_BOQ_STIFFENER_BEARING_VOL_FORMULA,
    KEY_BOQ_STIFFENER_BEARING_VOL_TOTAL,
    KEY_BOQ_STIFFENER_BEARING_WT_SINGLE,
    KEY_BOQ_STIFFENER_BEARING_WT_TOTAL,
    KEY_BOQ_STIFFENER_INTERMEDIATE_QTY,
    KEY_BOQ_STIFFENER_INTERMEDIATE_VOL_FORMULA,
    KEY_BOQ_STIFFENER_INTERMEDIATE_VOL_TOTAL,
    KEY_BOQ_STIFFENER_INTERMEDIATE_WT_SINGLE,
    KEY_BOQ_STIFFENER_INTERMEDIATE_WT_TOTAL,
)


def _wrap_multiply(value):
    text = str(value)
    times = r"\allowbreak{}\times\allowbreak{}" if "$" in text else r"\allowbreak{}$\times$\allowbreak{}"
    return text.replace(r"\times", r"\allowbreak{}\times\allowbreak{}").replace("×", times).replace(" x ", f" {times} ")


def _qty_header(text):
    return r"\parbox[t][1.75cm][c]{\linewidth}{\centering " + text + "}"


def ch7_quantities(input_dict, output_dict=None, chart_paths=None):
    if chart_paths is None and isinstance(output_dict, dict) and (
            "steel" in output_dict or "concrete_rebar" in output_dict):
        chart_paths, output_dict = output_dict, None
    quantities = (output_dict or {}).get(KEY_BOQ_MATERIAL_QUANTITIES, {})
    chart_paths = chart_paths or {}
    chart_figures = ""
    if chart_paths:
        chart_figures = (
            "\n\\vspace{1em}\n"
            + _fig_embed(chart_paths.get("steel"),
                         "Structural Steel Tonnage Summary",
                         width=r"0.82\textwidth", numbered=True)
            + "\n\\vspace{0.5em}\n"
            + _fig_embed(chart_paths.get("concrete_rebar"),
                         "Concrete Volume and Reinforcement Steel Summary",
                         width=r"0.82\textwidth", numbered=True)
        )

    def val(key):
        return str(quantities.get(key, "N.A."))

    rows = [
        ["1", "Structural Steel (IS 2062) for Girders", _wrap_multiply(val(KEY_BOQ_STEEL_GIRDERS_VOL_FORMULA)), val(KEY_BOQ_STEEL_GIRDERS_QTY), val(KEY_BOQ_STEEL_GIRDERS_VOL_TOTAL), val(KEY_BOQ_STEEL_GIRDERS_WT_SINGLE), val(KEY_BOQ_STEEL_GIRDERS_WT_TOTAL)],
        ["2(a)", "Cross Bracing - Top Chord", _wrap_multiply(val(KEY_BOQ_BRACING_TOP_VOL_FORMULA)), val(KEY_BOQ_BRACING_TOP_QTY), val(KEY_BOQ_BRACING_TOP_VOL_TOTAL), val(KEY_BOQ_BRACING_TOP_WT_SINGLE), val(KEY_BOQ_BRACING_TOP_WT_TOTAL)],
        ["2(b)", "Cross Bracing - Bottom Chord", _wrap_multiply(val(KEY_BOQ_BRACING_BOTTOM_VOL_FORMULA)), val(KEY_BOQ_BRACING_BOTTOM_QTY), val(KEY_BOQ_BRACING_BOTTOM_VOL_TOTAL), val(KEY_BOQ_BRACING_BOTTOM_WT_SINGLE), val(KEY_BOQ_BRACING_BOTTOM_WT_TOTAL)],
        ["2(c)", "Cross Bracing - Diagonal Chord", _wrap_multiply(val(KEY_BOQ_BRACING_DIAGONAL_VOL_FORMULA)), val(KEY_BOQ_BRACING_DIAGONAL_QTY), val(KEY_BOQ_BRACING_DIAGONAL_VOL_TOTAL), val(KEY_BOQ_BRACING_DIAGONAL_WT_SINGLE), val(KEY_BOQ_BRACING_DIAGONAL_WT_TOTAL)],
        ["3(a)", "Stiffeners - Bearing", _wrap_multiply(val(KEY_BOQ_STIFFENER_BEARING_VOL_FORMULA)), val(KEY_BOQ_STIFFENER_BEARING_QTY), val(KEY_BOQ_STIFFENER_BEARING_VOL_TOTAL), val(KEY_BOQ_STIFFENER_BEARING_WT_SINGLE), val(KEY_BOQ_STIFFENER_BEARING_WT_TOTAL)],
        ["3(b)", "Stiffeners - Intermediate", _wrap_multiply(val(KEY_BOQ_STIFFENER_INTERMEDIATE_VOL_FORMULA)), val(KEY_BOQ_STIFFENER_INTERMEDIATE_QTY), val(KEY_BOQ_STIFFENER_INTERMEDIATE_VOL_TOTAL), val(KEY_BOQ_STIFFENER_INTERMEDIATE_WT_SINGLE), val(KEY_BOQ_STIFFENER_INTERMEDIATE_WT_TOTAL)],
        ["4", "Connections", _wrap_multiply(val(KEY_BOQ_CONNECTIONS_VOL_FORMULA)), val(KEY_BOQ_CONNECTIONS_QTY), val(KEY_BOQ_CONNECTIONS_VOL_TOTAL), val(KEY_BOQ_CONNECTIONS_WT_SINGLE), val(KEY_BOQ_CONNECTIONS_WT_TOTAL)],
        ["5", "Concrete (M40) for Deck Slab", _wrap_multiply(val(KEY_BOQ_CONCRETE_DECK_VOL_FORMULA)), val(KEY_BOQ_CONCRETE_DECK_QTY), val(KEY_BOQ_CONCRETE_DECK_VOL_TOTAL), val(KEY_BOQ_CONCRETE_DECK_WT_SINGLE), val(KEY_BOQ_CONCRETE_DECK_WT_TOTAL)],
        ["6", "Reinforcement Steel (Fe 500)", _wrap_multiply(val(KEY_BOQ_REBAR_DECK_VOL_FORMULA)), val(KEY_BOQ_REBAR_DECK_QTY), val(KEY_BOQ_REBAR_DECK_VOL_TOTAL), val(KEY_BOQ_REBAR_DECK_WT_SINGLE), val(KEY_BOQ_REBAR_DECK_WT_TOTAL)],
        ["7", "Shear Stud Connectors", _wrap_multiply(val(KEY_BOQ_SHEAR_STUDS_VOL_FORMULA)), val(KEY_BOQ_SHEAR_STUDS_QTY), val(KEY_BOQ_SHEAR_STUDS_VOL_TOTAL), val(KEY_BOQ_SHEAR_STUDS_WT_SINGLE), val(KEY_BOQ_SHEAR_STUDS_WT_TOTAL)],
        ["8", "Crash Barrier", _wrap_multiply(val(KEY_BOQ_CRASH_BARRIER_VOL_FORMULA)), val(KEY_BOQ_CRASH_BARRIER_QTY), val(KEY_BOQ_CRASH_BARRIER_VOL_TOTAL), val(KEY_BOQ_CRASH_BARRIER_WT_SINGLE), val(KEY_BOQ_CRASH_BARRIER_WT_TOTAL)],
    ]

    return r"""
\chapter{Bill of Materials}
\label{ch:material-takeoff}
""" + render_report_table(
        "Bill of Materials for Superstructure", rows,
        header_rows=[[_qty_header("S.N."), _qty_header(r"Item\\Description"),
                      _qty_header("Volume"), _qty_header("Quantity"),
                      _qty_header(r"Total\\Volume\\(m$^3$)"),
                      _qty_header(r"Weight\\(t)"), _qty_header(r"Total\\Weight\\(t)")]],
        widths=[1.0, 3.8, 2.5, 2.1, 1.8, 1.7, 1.8],
        align=["C", "L", "C", "C", "C", "C", "C"],
        longtable=True, escape=False) + chart_figures
