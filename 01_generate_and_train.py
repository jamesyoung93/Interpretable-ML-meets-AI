"""
Step 1-5: Generate customer data and train model for B2B Software Sales
"""
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

np.random.seed(42)

# Generate synthetic customer data
n_customers = 500

print("Step 1: Generating customer features...")
data = {
    'customer_id': [f'CUST_{i:05d}' for i in range(n_customers)],
    'company_name': [f'Company_{i}' for i in range(n_customers)],
    
    # Firmographic features
    'employee_count': np.random.lognormal(6, 1.5, n_customers).astype(int),
    'annual_revenue_m': np.random.lognormal(4, 1.2, n_customers),
    'tech_stack_size': np.random.poisson(12, n_customers),
    'cloud_maturity_score': np.random.beta(2, 2, n_customers) * 10,
    
    # Engagement features
    'website_visits_30d': np.random.poisson(8, n_customers),
    'whitepaper_downloads': np.random.poisson(2, n_customers),
    'demo_requests': np.random.binomial(3, 0.3, n_customers),
    'email_open_rate': np.random.beta(3, 2, n_customers),
    'webinar_attendance': np.random.poisson(1.5, n_customers),
    
    # Product fit features
    'competitor_product_count': np.random.poisson(2, n_customers),
    'integration_needs': np.random.poisson(5, n_customers),
    'security_compliance_req': np.random.choice([0, 1], n_customers, p=[0.3, 0.7]),
    'api_usage_intent': np.random.beta(2, 3, n_customers),
    
    # Relationship features
    'relationship_age_months': np.random.gamma(3, 4, n_customers),
    'previous_churn_risk': np.random.beta(2, 5, n_customers),
    'support_tickets_90d': np.random.poisson(3, n_customers),
    'csm_relationship_score': np.random.beta(4, 2, n_customers) * 10,
    
    # Market features
    'industry_growth_rate': np.random.normal(0.05, 0.03, n_customers),
    'competitive_pressure_idx': np.random.beta(2, 2, n_customers) * 10,
    'budget_cycle_quarter': np.random.choice(['Q1', 'Q2', 'Q3', 'Q4'], n_customers),
    
    # Promotional sensitivity features
    'discount_sensitivity': np.random.beta(3, 2, n_customers),  # 0-1, higher = more price sensitive
    'sla_sensitivity': np.random.beta(2, 2, n_customers),  # 0-1, higher = values service guarantees
    'training_sensitivity': np.random.beta(2, 3, n_customers),  # 0-1, higher = needs training/support
    'implementation_support_sensitivity': np.random.beta(2.5, 2, n_customers),  # 0-1, higher = needs help
}

df = pd.DataFrame(data)

# Add some categorical encoding
df['budget_cycle_q1'] = (df['budget_cycle_quarter'] == 'Q1').astype(int)
df['budget_cycle_q2'] = (df['budget_cycle_quarter'] == 'Q2').astype(int)
df['budget_cycle_q3'] = (df['budget_cycle_quarter'] == 'Q3').astype(int)
df['budget_cycle_q4'] = (df['budget_cycle_quarter'] == 'Q4').astype(int)

print(f"  Generated {len(df)} customers with {len(df.columns)} features")

# Step 2: Create target variable (expansion revenue potential)
print("\nStep 2: Creating target variable (expansion revenue potential)...")

# Complex interaction between features
df['expansion_revenue_potential'] = (
    df['annual_revenue_m'] * 0.02 +
    df['employee_count'] * 0.001 +
    df['tech_stack_size'] * 2.0 +
    df['cloud_maturity_score'] * 3.0 +
    df['website_visits_30d'] * 0.5 +
    df['demo_requests'] * 5.0 +
    df['email_open_rate'] * 10.0 +
    df['integration_needs'] * 1.5 +
    df['security_compliance_req'] * 8.0 +
    df['csm_relationship_score'] * 2.0 +
    df['industry_growth_rate'] * 50.0 +
    np.random.normal(0, 5, n_customers)  # noise
)

# Add some interaction effects
df['expansion_revenue_potential'] += (
    df['demo_requests'] * df['cloud_maturity_score'] * 0.5 +
    df['employee_count'] * df['tech_stack_size'] * 0.0001
)

# Clip to reasonable range
df['expansion_revenue_potential'] = np.clip(df['expansion_revenue_potential'], 5, 200)

# Step 2b: Determine recommended promotion based on sensitivities
print(f"  Target range: ${df['expansion_revenue_potential'].min():.1f}K - ${df['expansion_revenue_potential'].max():.1f}K")

print("\nStep 2b: Determining optimal promotion strategy per customer...")
sensitivities = df[['discount_sensitivity', 'sla_sensitivity', 'training_sensitivity', 'implementation_support_sensitivity']]
promotion_map = {
    0: 'Price Discount (15-20%)',
    1: 'Extended SLA (99.99% uptime)',
    2: 'Training Credits ($10K)',
    3: 'Implementation Support (40 hours)'
}

# Recommend promotion with highest sensitivity
df['recommended_promotion_idx'] = sensitivities.values.argmax(axis=1)
df['recommended_promotion'] = df['recommended_promotion_idx'].map(promotion_map)

print(f"  Promotion distribution:")
for promo, count in df['recommended_promotion'].value_counts().items():
    print(f"    {promo}: {count} customers")

# Step 3: Train Random Forest model
print("\nStep 3: Training Random Forest model...")

feature_cols = [c for c in df.columns if c not in [
    'customer_id', 'company_name', 'budget_cycle_quarter', 'expansion_revenue_potential',
    'recommended_promotion_idx', 'recommended_promotion'
]]

X = df[feature_cols]
y = df['expansion_revenue_potential']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"  Train R²: {train_score:.3f}")
print(f"  Test R²: {test_score:.3f}")

# Add predictions to dataframe
df['predicted_expansion_revenue'] = model.predict(X)

# Step 4: Save model
print("\nStep 4: Saving trained model...")
model_artifact = {
    'model': model,
    'feature_cols': feature_cols,
    'train_score': train_score,
    'test_score': test_score
}

with open('models/expansion_model.pkl', 'wb') as f:
    pickle.dump(model_artifact, f)

print("  Model saved to models/expansion_model.pkl")

# Step 5: Save customer data
print("\nStep 5: Saving customer data...")
df.to_csv('data/customers.csv', index=False)
print(f"  Saved {len(df)} customers to data/customers.csv")

print("\n✓ Steps 1-5 complete!")
