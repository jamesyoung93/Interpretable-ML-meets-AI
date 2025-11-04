"""
Step 6-10: Calculate SHAP values and allocate actions via constrained optimization
"""
import pandas as pd
import numpy as np
import pickle
import shap
from scipy.optimize import linprog

print("Step 6: Loading model and data...")
with open('models/expansion_model.pkl', 'rb') as f:
    model_artifact = pickle.load(f)

model = model_artifact['model']
feature_cols = model_artifact['feature_cols']

df = pd.read_csv('data/customers.csv')
X = df[feature_cols]

print(f"  Loaded model with {len(feature_cols)} features")
print(f"  Loaded {len(df)} customers")

# Step 7: Calculate SHAP values
print("\nStep 7: Calculating SHAP values (TreeExplainer)...")

# Sample background for speed
background = shap.sample(X, 50)
explainer = shap.TreeExplainer(model, background, feature_perturbation='interventional')

# Calculate for all customers
shap_values = explainer.shap_values(X, check_additivity=False)
expected_value = explainer.expected_value

print(f"  SHAP values shape: {shap_values.shape}")
print(f"  Expected (baseline) value: ${expected_value:.2f}K")

# Save SHAP artifacts
shap_artifact = {
    'shap_values': shap_values,
    'expected_value': expected_value,
    'feature_names': feature_cols,
    'customer_ids': df['customer_id'].values
}

with open('models/shap_values.pkl', 'wb') as f:
    pickle.dump(shap_artifact, f)

print("  SHAP values saved to models/shap_values.pkl")

# Step 8: Calculate action scores
print("\nStep 8: Calculating action scores for allocation...")

# Action score = predicted revenue + urgency + fit
df['action_score'] = (
    df['predicted_expansion_revenue'] +  # Revenue potential
    df['demo_requests'] * 5 +            # Engagement urgency
    df['cloud_maturity_score'] * 2 +     # Product fit
    df['csm_relationship_score'] * 1.5   # Relationship strength
)

# Normalize to 0-100
df['action_score'] = (
    (df['action_score'] - df['action_score'].min()) / 
    (df['action_score'].max() - df['action_score'].min()) * 100
)

print(f"  Action scores range: {df['action_score'].min():.1f} - {df['action_score'].max():.1f}")

# Step 9: Constrained action allocation
print("\nStep 9: Running constrained optimization for action allocation...")

# Constraint: 250 total actions across all customers, max 5 per customer
total_actions = 250
max_actions_per_customer = 5

# Sort by action score
df_sorted = df.sort_values('action_score', ascending=False).copy()

# Greedy allocation (simplified for demonstration)
df_sorted['allocated_actions'] = 0
remaining_actions = total_actions

for idx in df_sorted.index:
    # Allocate proportional to score, but capped
    score = df_sorted.loc[idx, 'action_score']
    allocation = min(
        int(np.ceil(score / 20)),  # Higher scores get more
        max_actions_per_customer,
        remaining_actions
    )
    df_sorted.loc[idx, 'allocated_actions'] = allocation
    remaining_actions -= allocation
    
    if remaining_actions <= 0:
        break

# Sort back to original order
df = df_sorted.sort_index()

print(f"  Allocated {df['allocated_actions'].sum()} actions across {(df['allocated_actions'] > 0).sum()} customers")
print(f"  Actions per customer: min={df['allocated_actions'].min()}, max={df['allocated_actions'].max()}, mean={df['allocated_actions'].mean():.2f}")

# Step 10: Save final dataset
print("\nStep 10: Saving final dataset with allocations...")

# Load original data to preserve promotion columns
df_original = pd.read_csv('data/customers.csv')
promotion_cols = ['recommended_promotion_idx', 'recommended_promotion']
df_with_promotions = df.join(df_original[promotion_cols])

df_with_promotions.to_csv('data/customers_with_actions.csv', index=False)
print("  Saved to data/customers_with_actions.csv")

# Save summary stats
summary = {
    'total_customers': len(df),
    'total_actions_allocated': int(df['allocated_actions'].sum()),
    'customers_with_actions': int((df['allocated_actions'] > 0).sum()),
    'avg_predicted_revenue': float(df['predicted_expansion_revenue'].mean()),
    'total_pipeline_value': float(df['predicted_expansion_revenue'].sum())
}

with open('data/allocation_summary.pkl', 'wb') as f:
    pickle.dump(summary, f)

print("\n✓ Steps 6-10 complete!")
print(f"\n📊 Summary:")
print(f"  Total pipeline value: ${summary['total_pipeline_value']/1000:.1f}M")
print(f"  Actions allocated: {summary['total_actions_allocated']}")
print(f"  Customers receiving actions: {summary['customers_with_actions']}")
