"""Сборка отчёта по скважине: факт, прогноз, рабочая точка."""


def build_report(server, well_id: str, horizon_months: int = 12) -> dict:
    """У каждого числа в отчёте — единица и инструмент-источник."""
    history = server.call("get_production_history", well_id=well_id, months=24)
    forecast = server.call("forecast_production", well_id=well_id, horizon_months=horizon_months)
    model = server.call("open_well_model", well_id=well_id)
    nodal = server.call("run_nodal_analysis", session_id=model["session_id"])

    report = {
        "fact": {
            **history["points"][-1],
            "units": history["units"],
            "source": "get_production_history",
        },
        "forecast": {
            "first": forecast["points"][0],
            "last": forecast["points"][-1],
            "annual_decline": forecast["fit"]["annual_decline"],
            "r2": forecast["fit"]["r2"],
            "units": {**forecast["units"], "r2": "безразмерный"},
            "source": "forecast_production",
        },
        "operating_point": {
            **nodal["operating_point"],
            "units": nodal["units"],
            "source": "run_nodal_analysis",
        },
    }
    return report
