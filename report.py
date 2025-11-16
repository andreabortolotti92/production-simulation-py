def summarize(plan_df, daily_capacity_total):
    """Restituisce un dizionario con gli indicatori principali della simulazione."""

    # Calcolo dei KPI principali dalla tabella del piano
    total_days = int(plan_df["day"].max())
    total_minutes = int(plan_df["alloc_minutes"].sum())

    # Utilizzo medio della capacità totale
    if daily_capacity_total > 0:
        # Sommo la capacità allocata per ciascun giorno e dividiamo per la cap totale
        day_usage = (plan_df.groupby("day", as_index=False)["alloc_minutes"].sum().rename(columns={"alloc_minutes": "alloc_minutes_total"}))
        day_usage["utilization_pct"] = (day_usage["alloc_minutes_total"] / float(daily_capacity_total) * 100.0)
        avg_daily_utilization = float(day_usage["utilization_pct"].mean())
    else:
        avg_daily_utilization = None

    # Verifica completamento lotti: rimanenze finali tutte a 0 (prendiamo l'ultima riga per prodotto in ordine di "day")
    last_by_product = (plan_df.sort_values(["product", "day"]).groupby("product", as_index=False).tail(1))
    completed_all = bool((last_by_product["remaining_qty"] == 0).all())

    return {
        "total_days": total_days,
        "total_minutes": total_minutes,
        "avg_daily_utilization": avg_daily_utilization,
        "completed_all": completed_all,
    }


def make_tables(plan_df,params_df,daily_capacity_total):
    """Restituisce due tabelle di riepilogo, una per prodotto e l'altra per giorno"""

    tables= {}

    # ---------- RIEPILOGO PER PRODOTTO ----------
    by_product = (plan_df.groupby("product", as_index=False)[["alloc_minutes", "produced_qty"]].sum()
                  .rename(columns={
                      "alloc_minutes": "minutes_used",
                      "produced_qty": "produced_total",
                      }))

    # Giorni in cui la produzione era effettivamente attiva per quello specifico prodotto (giorni "attivi")
    active_days = (plan_df[plan_df["produced_qty"] > 0].groupby("product", as_index=False)["day"].nunique().rename(columns={"day": "active_days"}))

    # Merge tra by_product e active_days sul campo product
    product_summary = by_product.merge(active_days, on="product", how="left").fillna(0)

    # Aggiungiamo quantità di lotto e tempi unitari
    sel = params_df[["product", "lot_qty", "unit_time"]].copy()
    product_summary = sel.merge(product_summary, on="product", how="left")
    # Calcoliamo rimanenza finale per completezza (lot_qty - produced_total)
    product_summary["remaining_final"] = (product_summary["lot_qty"] - product_summary["produced_total"])

    tables["product_summary_df"] = product_summary

    # ---------- RIEPILOGO PER GIORNO ----------
    day_summary = (plan_df.groupby("day", as_index=False)["alloc_minutes"].sum().rename(columns={"alloc_minutes": "alloc_minutes_total"}))

    if daily_capacity_total > 0:
        day_summary["capacity_total"] = daily_capacity_total
        day_summary["unused_minutes"] = (day_summary["capacity_total"] - day_summary["alloc_minutes_total"]).clip(lower=0)
        day_summary["utilization_pct"] = (day_summary["alloc_minutes_total"] / float(daily_capacity_total) * 100.0)
    else:
        day_summary["capacity_total"] = None
        day_summary["unused_minutes"] = None
        day_summary["utilization_pct"] = None

    tables["day_summary_df"] = day_summary

    return tables


