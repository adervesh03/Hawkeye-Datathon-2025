import pandas as pd
import shap
import matplotlib.pyplot as plt

# --- 1. Load your Model and Data ---

# model_tweedie = joblib.load('your_tweedie_model.pkl')
# X_train_final = pd.read_csv('your_final_training_features.csv')

print("\n--- Starting SHAP Analysis for Tweedie Model ---")

# --- 2. Create the SHAP Explainer ---
# We use TreeExplainer for XGBoost, Random Forest, etc. ; shap.KernelExplainer is for other models but is *very* slow.
try:
    explainer = shap.TreeExplainer(model_tweedie)
    print("Successfully created TreeExplainer.")
except Exception as e:
    print(f"Could not create TreeExplainer ({e}).")
    print("If this is not a tree-based model, use shap.KernelExplainer(model.predict, X_train_final).")


# --- 3. Calculate SHAP Values ---
# This runs the explainer on your entire training set to get a global view
print("Calculating SHAP values... (This may take a few minutes)")
shap_values = explainer(X_train_final)

print("SHAP calculations complete.")

# --- 4. Plot 1: Feature Importance (Bar Chart) ---
# This is the "Executive Summary" plot. It shows the mean absolute SHAP value for each feature.
plt.figure()
plt.title("Global Feature Importance (Mean Absolute SHAP)")
shap.summary_plot(
    shap_values, 
    X_train_final, 
    plot_type="bar",
    show=False
)
plt.show()

# --- 5. Plot 2: Feature Impact (Beeswarm Plot) ---
# This is the "Deep Dive" plot. It shows HOW a feature impacts the model (positively or negatively) and is much more insightful.
plt.figure()
plt.title("SHAP Beeswarm Summary Plot (Feature Impact)")
shap.summary_plot(
    shap_values, 
    X_train_final, 
    plot_type="dot", # 'dot' is also known as 'beeswarm'
    show=False
)
plt.show()
