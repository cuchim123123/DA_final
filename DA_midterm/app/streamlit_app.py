"""Interactive Streamlit dashboard for Telco Customer Churn Analytics."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

try:
    from app.helpers import (
        DashboardArtifacts,
        compute_filtered_kpis,
        compute_threshold_metrics,
        filter_customer_cohort,
        get_figure_path,
        load_dashboard_artifacts,
        score_hypothetical_customer,
        simulate_retention_scenario,
    )
except ModuleNotFoundError:
    from helpers import (  # type: ignore[no-redef]
        DashboardArtifacts,
        compute_filtered_kpis,
        compute_threshold_metrics,
        filter_customer_cohort,
        get_figure_path,
        load_dashboard_artifacts,
        score_hypothetical_customer,
        simulate_retention_scenario,
    )
from telco_churn.analysis.descriptive import compute_subgroup_rates
from telco_churn.config import CONTRACT_ORDER, INTERNET_ORDER, PAYMENT_ORDER


@st.cache_resource(show_spinner=False)
def _cached_artifacts() -> DashboardArtifacts:
    return load_dashboard_artifacts()


def _render_overview(art: DashboardArtifacts) -> None:
    st.subheader("1. Executive Overview & Data Quality Summary")
    kpis = art.summary["descriptive"]["kpis"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Subscribers", f"{kpis['n_customers']:,}", "100% unique IDs")
    c2.metric(
        "Observed Churn Rate",
        f"{kpis['overall_churn_rate_pct']:.2f}%",
        f"95% CI [{kpis['overall_churn_ci95_low_pct']:.1f}%, {kpis['overall_churn_ci95_high_pct']:.1f}%]",
    )
    c3.metric(
        "Churned Monthly Billing (Snapshot)",
        f"${kpis['monthly_revenue_at_risk_usd']:,.0f}",
        f"{kpis['monthly_revenue_at_risk_pct']:.2f}% of ${kpis['total_monthly_charges_usd']:,.0f}/mo billing",
    )
    c4.metric(
        "Median Tenure (Mo)",
        f"{kpis['median_tenure_months']:.0f} mo",
        f"Mean: {kpis['mean_tenure_months']:.1f} mo",
    )

    st.markdown(
        "**Analytical Narrative:** Churn is heavily concentrated in **Month-to-month** agreements "
        "(42.71% churn, generating 88.55% of all churners), **1-12 month early tenure** (47.68% churn), "
        "**Fiber optic** plans (41.89% churn), and **Electronic check** manual billing (45.29% churn). "
        "On untouched held-out accounts (n = 1,409), the calibrated risk ranking isolates 65.78% of all "
        "churners within the top 30% risk capacity tier (2.19x lift over untargeted outreach)."
    )

    col_left, col_right = st.columns([1.45, 1.0])
    with col_left:
        st.image(str(get_figure_path("fig01_churn_by_contract_payment.png")), width="stretch")
    with col_right:
        st.markdown("**Dataset Provenance & Quality Audit (IBM Sample CSV)**")
        st.dataframe(art.audit_df, width="stretch", hide_index=True)


def _render_explore_diagnose(art: DashboardArtifacts) -> None:
    st.subheader("2. Interactive Descriptive Exploration & Statistical Diagnostics")

    c_param = str(st.query_params.get("contract", "")).lower()
    default_contracts = (
        ["Month-to-month"]
        if c_param == "month-to-month"
        else CONTRACT_ORDER
    )
    t_max_q = st.query_params.get("tenure_max")
    default_tenure = (1, int(t_max_q)) if t_max_q and str(t_max_q).isdigit() else (0, 72)

    with st.expander("Cohort Filters (Dynamically Updates Observed Subgroup Metrics)", expanded=True):
        f1, f2, f3, f4 = st.columns(4)
        contracts = f1.multiselect("Contract Type", CONTRACT_ORDER, default=default_contracts, key=f"filter_contracts_{'_'.join(default_contracts)}")
        internet_types = f2.multiselect("Internet Service", INTERNET_ORDER, default=INTERNET_ORDER)
        payments = f3.multiselect("Payment Method", PAYMENT_ORDER, default=PAYMENT_ORDER)
        senior_opt = f4.selectbox(
            "Senior Citizen Filter",
            ["All", "Senior Citizens Only (1)", "Non-Seniors Only (0)"],
        )
        tenure_range = st.slider(
            "Customer Tenure Range (Months)",
            min_value=0,
            max_value=72,
            value=default_tenure,
            key=f"filter_tenure_{default_tenure[0]}_{default_tenure[1]}",
        )

    filtered = filter_customer_cohort(
        art.df_eda,
        contracts=contracts,
        internet_types=internet_types,
        payment_methods=payments,
        tenure_range=tenure_range,
        senior_filter=senior_opt,
    )
    fkpis = compute_filtered_kpis(filtered)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Filtered Subscribers", f"{fkpis['n_customers']:,}")
    m2.metric(
        "Filtered Churn Rate",
        f"{fkpis['churn_rate_pct']:.2f}%",
        f"CI [{fkpis['ci95_low_pct']:.1f}%, {fkpis['ci95_high_pct']:.1f}%]",
    )
    m3.metric("Churned Customers", f"{fkpis['n_churned']:,}")
    m4.metric("Churned Monthly Billing", f"${fkpis['monthly_rev_at_risk_usd']:,.0f}", "Historical snapshot billing (Churned)")

    if fkpis["n_customers"] == 0:
        st.warning("No subscribers match the active filter criteria. Widen at least one filter.")
        return

    group_dim = st.selectbox(
        "Break Down Filtered Cohort By Feature",
        ["Contract", "tenure_tier", "InternetService", "PaymentMethod", "OnlineSecurity", "TechSupport", "PaperlessBilling"],
        index=0,
    )
    sub_rates = compute_subgroup_rates(filtered, group_dim)

    c_chart, c_tbl = st.columns([1.15, 1.0])
    with c_chart:
        fig, ax = plt.subplots(figsize=(6.5, 4.0))
        y_vals = sub_rates["churn_rate_pct"].to_numpy()
        err_lo = y_vals - sub_rates["ci95_low_pct"].to_numpy()
        err_hi = sub_rates["ci95_high_pct"].to_numpy() - y_vals
        bars = ax.bar(sub_rates["category"], y_vals, yerr=[err_lo, err_hi], capsize=4, color="#2B5B84", edgecolor="black")
        ax.set_ylabel("Observed Churn Rate (%)")
        ax.set_xlabel(group_dim)
        ax.set_title(f"Filtered Churn Rate by {group_dim} (n = {fkpis['n_customers']:,})")
        ax.set_ylim(0, min(105, max(y_vals + err_hi) + 12))
        plt.xticks(rotation=15, ha="right")
        for bar, row in zip(bars, sub_rates.itertuples(), strict=True):
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                bar.get_height() + (row.ci95_high_pct - row.churn_rate_pct) + 1.5,
                f"{row.churn_rate_pct:.1f}%\n(n={row.n_customers})",
                ha="center",
                va="bottom",
                fontsize=8.2,
            )
        fig.tight_layout()
        st.pyplot(fig, width="stretch")
        plt.close(fig)

    with c_tbl:
        st.dataframe(
            sub_rates[["category", "n_customers", "n_churned", "churn_rate_pct", "ci95_low_pct", "ci95_high_pct", "monthly_revenue_at_risk_usd"]],
            width="stretch",
            hide_index=True,
        )

    tab_dist, tab_diag, tab_conf = st.tabs(
        ["Numeric Distributions & Hexbin", "Bivariate Diagnostic Tests", "Confounding Audit"]
    )
    with tab_dist:
        st.image(str(get_figure_path("fig02_numeric_distributions_kde.png")), width="stretch")
        col_a, col_b = st.columns(2)
        col_a.image(str(get_figure_path("fig03_charges_by_contract_churn_boxplot.png")), width="stretch")
        col_b.image(str(get_figure_path("fig04_tenure_violin_by_contract_churn.png")), width="stretch")
        st.image(str(get_figure_path("fig05_tenure_vs_monthly_charges_scatter.png")), width="stretch")
    with tab_diag:
        st.caption("Observational statistical associations (Pearson Chi-square with Holm-Bonferroni correction and Mann-Whitney U) do not imply causal treatment effects.")
        st.image(str(get_figure_path("fig06_diagnostic_association_heatmaps.png")), width="stretch")
        st.dataframe(art.cat_diag_df, width="stretch", hide_index=True)
        st.dataframe(art.cont_diag_df, width="stretch", hide_index=True)
    with tab_conf:
        st.markdown(
            "**Simpson-style Confounding Example:** Marginally, `TotalCharges` appears protective (unadjusted log-odds `-0.5349`) "
            "purely because cumulative charges grow with `tenure`. Once `tenure` and `MonthlyCharges` are controlled simultaneously, "
            "`TotalCharges` reverses sign (`+0.6703`)."
        )
        st.dataframe(art.conf_diag_df.head(16), width="stretch", hide_index=True)


def _render_predictive(art: DashboardArtifacts) -> None:
    st.subheader("3. Predictive Model Evaluation (Sealed Test Set n = 1,409) & Explainability")
    cv_det = art.summary["predictive"]["cv_details"]
    champ = cv_det["final_champion_label"]
    tau_val = float(cv_det["validation_optimal_threshold"])

    st.info(
        f"**Evaluation Protocol:** Stratified 80/20 split (5,634 dev / 1,409 untouched test; random_state=42). "
        f"Preprocessing fits inside CV/training folds only. Champion selected via 5-fold CV ROC-AUC: **{champ}**; "
        f"validation-tuned F1 cutoff: **{tau_val:.2f}**."
    )

    tab_bench, tab_thresh, tab_explain, tab_score = st.tabs(
        ["CV & Test Comparison", "Interactive Cutoff Explorer", "Explainability", "Single-Profile Educational Scorer"]
    )

    with tab_bench:
        st.markdown("**5-Fold Cross-Validation Summary (Training Set Only, n = 5,634)**")
        st.dataframe(art.cv_comp_df, width="stretch", hide_index=True)
        st.markdown("**Held-Out Test Benchmark (Sealed Set, n = 1,409)**")
        st.dataframe(art.test_comp_df, width="stretch", hide_index=True)
        st.image(str(get_figure_path("fig07_model_roc_pr_calibration_curves.png")), width="stretch")
        st.image(str(get_figure_path("fig08_confusion_matrices_heatmap.png")), width="stretch")

    with tab_thresh:
        col_s1, col_s2 = st.columns([1.2, 1.0])
        model_choice = col_s1.selectbox(
            "Select Precomputed Test Probability Stream",
            {
                "prob_champion": f"Champion ({champ})",
                "prob_hist_gradient_boosting": "HistGradientBoosting",
                "prob_logistic_baseline": "Logistic Regression (Baseline)",
            }.items(),
            format_func=lambda item: item[1],
        )[0]
        tau_q = st.query_params.get("tau")
        try:
            default_cutoff = float(tau_q) if tau_q else tau_val
        except (ValueError, TypeError):
            default_cutoff = tau_val
        cutoff = col_s2.slider(
            "Classification Decision Cutoff (tau)",
            min_value=0.15,
            max_value=0.75,
            value=default_cutoff,
            step=0.01,
            key=f"tau_cutoff_{default_cutoff}",
        )
        tm = compute_threshold_metrics(art.test_pred_df, model_choice, cutoff)
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Flagged Accounts", f"{tm['flagged_count']} ({tm['flagged_pct']:.1f}%)")
        k2.metric("Precision", f"{tm['precision']:.4f}")
        k3.metric("Recall", f"{tm['recall']:.4f}")
        k4.metric("F1 Score", f"{tm['f1_score']:.4f}")
        k5.metric("Accuracy", f"{tm['accuracy']:.4f}")
        st.markdown(
            f"**Test Confusion Counts at tau = {tm['threshold']:.2f}:** "
            f"True Positives (TP) = **{tm['tp']}** | False Negatives (FN) = **{tm['fn']}** | "
            f"False Positives (FP) = **{tm['fp']}** | True Negatives (TN) = **{tm['tn']}**"
        )

    with tab_explain:
        st.image(str(get_figure_path("fig09_model_explainability.png")), width="stretch")
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.markdown("**Held-Out Permutation Importance (19 Raw Predictors)**")
            st.dataframe(art.perm_imp_df, width="stretch", hide_index=True)
        with col_e2:
            st.markdown("**Logistic Regression Log-Odds Weights**")
            st.dataframe(art.logistic_or_df.head(20), width="stretch", hide_index=True)

    with tab_score:
        st.warning(
            "**Educational Benchmark Demonstration Only:** Scores one hypothetical profile using the exact saved "
            f"`{champ}` preprocessing + model pipeline. Output represents a retrospective pattern-based probability estimate, "
            "not a guaranteed future outcome or causal prediction."
        )
        prof_q = str(st.query_params.get("profile", "")).lower()
        if prof_q == "low_risk":
            def_contract_idx = 2  # Two year
            def_tenure = 60
            def_monthly = 52.0
            def_payment_idx = 2  # Bank transfer (automatic)
            def_internet_idx = 1  # DSL
            def_phone_idx = 0  # Yes
            def_mult_idx = 0  # No
            def_sec_idx = 1  # Yes
            def_tech_idx = 1  # Yes
        elif prof_q == "no_service":
            def_contract_idx = 0  # Month-to-month
            def_tenure = 4
            def_monthly = 20.0
            def_payment_idx = 0  # Electronic check
            def_internet_idx = 2  # No internet service
            def_phone_idx = 1  # No phone service
            def_mult_idx = 0
            def_sec_idx = 0
            def_tech_idx = 0
        else:  # default / high_risk
            def_contract_idx = 0  # Month-to-month
            def_tenure = 4
            def_monthly = 89.5
            def_payment_idx = 0  # Electronic check
            def_internet_idx = 0  # Fiber optic
            def_phone_idx = 0  # Yes
            def_mult_idx = 1  # Yes
            def_sec_idx = 0  # No
            def_tech_idx = 0  # No

        c1, c2, c3 = st.columns(3)
        contract_in = c1.selectbox("Contract", CONTRACT_ORDER, index=def_contract_idx)
        tenure_in = c1.slider("Tenure (Months)", 0, 72, def_tenure)
        monthly_in = c1.slider("Monthly Charges (USD)", 18.0, 120.0, def_monthly, step=0.5)
        total_in = c1.number_input("Total Charges (USD)", min_value=0.0, max_value=10000.0, value=float(round(tenure_in * monthly_in, 2)))
        payment_in = c2.selectbox("Payment Method", PAYMENT_ORDER, index=def_payment_idx)
        internet_in = c2.selectbox("Internet Service", INTERNET_ORDER, index=def_internet_idx)
        paperless_in = c2.selectbox("Paperless Billing", ["Yes", "No"], index=0)
        senior_in = c2.selectbox("Senior Citizen", [0, 1], format_func=lambda v: "Yes (1)" if v == 1 else "No (0)")

        phone_in = c3.selectbox("Phone Service", ["Yes", "No"], index=def_phone_idx)
        if phone_in == "No":
            mult_in = "No phone service"
            c3.info("MultipleLines automatically set to 'No phone service'.")
        else:
            mult_in = c3.selectbox("Multiple Lines", ["No", "Yes"], index=def_mult_idx)

        if internet_in == "No":
            sec_in = bkp_in = dev_in = tech_in = tv_in = mov_in = "No internet service"
            c3.info("Internet add-ons locked to 'No internet service'.")
        else:
            sec_in = c3.selectbox("Online Security", ["No", "Yes"], index=def_sec_idx)
            tech_in = c3.selectbox("Tech Support", ["No", "Yes"], index=def_tech_idx)
            bkp_in = c3.selectbox("Online Backup", ["No", "Yes"], index=0)
            dev_in = c3.selectbox("Device Protection", ["No", "Yes"], index=0)
            tv_in = c3.selectbox("Streaming TV", ["No", "Yes"], index=1)
            mov_in = c3.selectbox("Streaming Movies", ["No", "Yes"], index=1)

        c4a, c4b, c4c = st.columns(3)
        gender_in = c4a.selectbox("Gender", ["Female", "Male"])
        partner_in = c4b.selectbox("Partner", ["No", "Yes"])
        dependents_in = c4c.selectbox("Dependents", ["No", "Yes"])

        payload = {
            "gender": gender_in,
            "SeniorCitizen": senior_in,
            "Partner": partner_in,
            "Dependents": dependents_in,
            "tenure": tenure_in,
            "PhoneService": phone_in,
            "MultipleLines": mult_in,
            "InternetService": internet_in,
            "OnlineSecurity": sec_in,
            "OnlineBackup": bkp_in,
            "DeviceProtection": dev_in,
            "TechSupport": tech_in,
            "StreamingTV": tv_in,
            "StreamingMovies": mov_in,
            "Contract": contract_in,
            "PaperlessBilling": paperless_in,
            "PaymentMethod": payment_in,
            "MonthlyCharges": monthly_in,
            "TotalCharges": total_in,
        }
        scored = score_hypothetical_customer(art.champion_pipeline, payload, val_threshold=tau_val)
        st.success(
            f"**Estimated Churn Probability ({champ}):** `{scored['predicted_churn_probability_pct']:.2f}%` | "
            f"**Assigned Tier:** `{scored['risk_tier']}`"
        )


def _render_prescriptive(art: DashboardArtifacts) -> None:
    st.subheader("4. Prescriptive Retention Prioritization & Assumption-Labeled Scenario Simulator")
    st.caption(
        "Recommendations below trace directly to Descriptive, Diagnostic, and Predictive tables. "
        "Any cost/save/horizon numbers are explicit user-controlled assumptions, not measured causal treatment effects."
    )

    st.markdown("**Held-Out Risk Tier Calibration & Separation (Test n = 1,409)**")
    st.dataframe(art.risk_tiers_df, width="stretch", hide_index=True)

    st.markdown("**Capacity-Ranked Cumulative Capture & Lift**")
    st.dataframe(art.lift_df, width="stretch", hide_index=True)

    st.image(str(get_figure_path("fig10_prescriptive_targeting_lift.png")), width="stretch")

    st.markdown("### Interactive Retention Scenario Tool (Observed Exposure vs. Assumed Intervention)")
    cap_q = st.query_params.get("cap")
    cost_q = st.query_params.get("cost")
    save_q = st.query_params.get("save")
    horiz_q = st.query_params.get("horizon")

    try:
        def_cap = int(cap_q) if cap_q and str(cap_q).isdigit() else 30
    except (ValueError, TypeError):
        def_cap = 30
    try:
        def_cost = float(cost_q) if cost_q else 15.0
    except (ValueError, TypeError):
        def_cost = 15.0
    try:
        def_save = int(save_q) if save_q and str(save_q).isdigit() else 20
    except (ValueError, TypeError):
        def_save = 20
    try:
        def_horiz = int(horiz_q) if horiz_q and str(horiz_q).isdigit() else 6
    except (ValueError, TypeError):
        def_horiz = 6

    s1, s2, s3, s4 = st.columns(4)
    cap_pct = s1.slider("Outreach Capacity (% Top Risk)", 10, 100, def_cap, step=5, key=f"cap_slider_{def_cap}")
    cost_usd = s2.number_input("Assumed Cost per Contact (USD)", min_value=1.0, max_value=200.0, value=def_cost, step=1.0, key=f"cost_input_{def_cost}")
    save_pct = s3.slider("Assumed Save Rate on Churners (%)", 5, 50, def_save, step=5, key=f"save_slider_{def_save}")
    horizon_mo = s4.slider("Assumed Retention Horizon (Months)", 1, 12, def_horiz, step=1, key=f"horiz_slider_{def_horiz}")

    sim = simulate_retention_scenario(
        art.test_pred_df,
        outreach_capacity_pct=float(cap_pct),
        outreach_cost_per_customer_usd=float(cost_usd),
        assumed_save_rate=float(save_pct) / 100.0,
        assumed_horizon_months=int(horizon_mo),
    )

    obs1, obs2, assm1, assm2 = st.columns(4)
    obs1.metric("Observed: Churners Reached", f"{sim['observed_test_churners_reached']} / 374", f"{sim['observed_capture_rate_pct']:.1f}% capture")
    obs2.metric("Observed: Churned Billing Proxy", f"${sim['observed_targeted_monthly_rev_at_risk_usd']:,.2f}", f"{sim['customers_targeted']} test accounts contacted")
    assm1.metric("Assumed: Campaign Cost", f"${sim['assumed_campaign_cost_usd']:,.2f}", f"Assuming ${sim['assumed_outreach_cost_per_customer_usd']:.0f}/cust")
    assm2.metric("Assumed: Illustrative Net Value", f"${sim['assumed_net_value_usd']:,.2f}", f"Assuming {sim['assumed_save_rate_pct']:.0f}% save over {sim['assumed_horizon_months']} mo")

    st.markdown("### Traceable Retention Action Plan (Linking All Four Layers)")
    st.dataframe(art.recommendations_df, width="stretch", hide_index=True)


def main() -> None:
    st.set_page_config(page_title="Telco Customer Churn Analytics", layout="wide")
    st.title("Telco Customer Churn Analytics — Midterm Decision Support")
    st.warning(
        "**Provenance & Scope Notice:** Based on IBM's public *Telco Customer Churn* sample dataset (`N = 7,043`), "
        "which IBM describes as fictional telecommunications customer snapshot data. Statistical associations and "
        "predictive risk rankings do not establish causality or verified commercial intervention uplift."
    )

    art = _cached_artifacts()

    st.sidebar.header("Navigation")
    view_options = [
        "1. Executive Overview",
        "2. Explore & Diagnose",
        "3. Predictive Models & Explainability",
        "4. Prescriptive Prioritization",
    ]
    view_slug_map = {
        "overview": view_options[0],
        "explore": view_options[1],
        "predictive": view_options[2],
        "prescriptive": view_options[3],
    }
    requested_slug = str(st.query_params.get("view", "")).lower()
    default_view = view_slug_map.get(requested_slug, view_options[0])
    view = st.sidebar.radio(
        "Select Analytical View",
        view_options,
        index=view_options.index(default_view),
    )
    cv_det = art.summary["predictive"]["cv_details"]
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"**Active Champion Model:** `{cv_det['final_champion_label']}`\n\n"
        f"**Val-Tuned Cutoff:** `tau = {cv_det['validation_optimal_threshold']:.2f}`\n\n"
        f"**Hold-Out Test Size:** `n = 1,409 (20%)`"
    )

    if view.startswith("1."):
        _render_overview(art)
    elif view.startswith("2."):
        _render_explore_diagnose(art)
    elif view.startswith("3."):
        _render_predictive(art)
    else:
        _render_prescriptive(art)


if __name__ == "__main__":
    main()
