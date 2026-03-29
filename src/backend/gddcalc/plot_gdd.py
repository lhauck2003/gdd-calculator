import matplotlib.pyplot as plt
import mpld3
from typing import Optional, Union, List, Dict
from time import strptime

# Expects:
# gdd_totals [1, 2, 3, ...]
# gdd_daily [1, 1, 1, ...]
# days ["YYYY-MM-DD", ...]
# life_stages [{"Lifestage1": GDD}, {"Life_stage2": GDD}, ...]
#
# Returns: html code for plot
def plot_gdd(
        gdd_totals: Optional[List[float]] = None, 
        gdd_daily: Optional[List[float]] = None, 
        days: Optional[List[str]] = None,
        life_stages: Optional[List[Dict[str, float]]] = None # Life stages of crop [{"Lifestage": GDD value},...]
        ):
    fig, ax = plt.subplots()
    if gdd_totals is None and gdd_daily is None:
        return
    
    if days is None:
        raise Exception("Must specify days")
    #timedays = [strptime(day,"%Y-%m-%d") for day in days]
    
    if gdd_totals:
        ax.plot(days, gdd_totals,"r-", label="GDD Cumulative")

    if gdd_daily:
        ax.plot(days, gdd_daily, "b-", label="GDD Daily") 
    
    if life_stages:
        for life_stage in life_stages:
            x = days
            y = [list(life_stage.values())[0] for _ in range(len(days))]
            label = list(life_stage.keys())[0]
            ax.plot(x, y, color="g")
            ax.text(x[-1], y[-1], label, fontsize=8, rotation=45)
    
    ax.set_xlabel("Days", fontsize=20)
    ax.set_ylabel("GDD", fontsize=20)
    ax.set_xlim([days[0], days[-1]])
    ax.legend()

    plt.show()
    html_code = mpld3.fig_to_html(fig)
    return html_code
