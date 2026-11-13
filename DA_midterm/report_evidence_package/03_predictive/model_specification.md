# Predictive Model Specifications & Held-Out Test Benchmarks (`03_predictive/`)

- **Algorithms Evaluated Fairly Under Identical Preprocessing (`n_test = 1,409`, `374` positive churners):**
  1. **No-Skill Floor (`DummyClassifier` most frequent):** Accuracy `0.7346`, Recall `0.0000`, ROC-AUC `0.5000`, PR-AUC `0.2654`. *(Reference only; not counted as a trained ML algorithm.)*
  2. **Simple Baseline Algorithm (`Logistic Regression`, L2 C=5.0):**
     - Default `0.50`: Test ROC-AUC **`0.8412`**, PR-AUC **`0.6286`**, Brier `0.1385`, Accuracy `0.8055`, F1 `0.6040` (`TP=209, FP=109, FN=165, TN=926`).
     - Own CV F1-Opt (`tau=0.325`): Precision `0.5335`, Recall `0.7246`, F1 `0.6145` (`TP=271, FP=237, FN=103, TN=798`).
  3. **Selected Champion Model (`Random Forest`, selected via highest 5-fold CV ROC-AUC=0.8480):**
     - Default `0.50`: Test ROC-AUC **`0.8440`**, PR-AUC **`0.6513`**, Brier **`0.1361`**, ECE **`0.0173`**, Accuracy `0.8020`, Precision `0.6727`, Recall `0.4947`, F1 `0.5701` (`TP=185, FN=189`).
     - Own CV F1-Opt (`tau=0.330`): Precision `0.5591`, Recall **`0.7460`** (`279/374` churners captured; `FN` drops from `189` to `95`), **F1 `0.6392`**, Accuracy `0.7764`.
  4. **Runner-Up Boosting Ensemble (`HistGradientBoosting`):**
     - Default `0.50`: Test ROC-AUC **`0.8461`**, PR-AUC **`0.6610`**, Brier `0.1354`, Accuracy `0.7977`, F1 `0.5753`.
     - Own CV F1-Opt (`tau=0.340`): Precision `0.5622`, Recall `0.7246`, **F1 `0.6332`** (`TP=271, FP=211, FN=103, TN=824`).
- **Critical Modeling Finding:** Linear `Logistic Regression` (`ROC-AUC=0.8412`) performs very close to tree ensembles (`0.8440`–`0.8461`) because churn propensity in the IBM sample is predominantly smooth and additive across contract length, tenure, and internet tier, with modest non-linear interaction gains (`HistGradientBoosting` PR-AUC `+0.0324` over baseline).
