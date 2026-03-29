from .plot_gdd import plot_gdd

def test_plot_gdd():
    gdd_totals = [9.5, 12.7, 23.5, 35.7, 48.7]
    gdd_daily = [9.5, 3.2, 10.8, 12.2, 13.0]
    days = ["2026-01-01","2026-01-02","2026-01-03","2026-01-04","2026-01-05"]
    lifestages = [{"Emergence": 15.0}, {"Maturity": 30.0}]
    html = plot_gdd(gdd_totals, gdd_daily,days, lifestages)
    assert html is not None
