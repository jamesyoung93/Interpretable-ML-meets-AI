# 🚀 Quick Start Guide

## Get Running in 3 Minutes

### Step 1: Install Dependencies (30 seconds)
```bash
pip install -r requirements.txt
```

### Step 2: Data is Already Generated! ✓
The following files are included and ready to use:
- ✓ 500 synthetic B2B customers
- ✓ Trained Random Forest model (R² = 0.58)
- ✓ SHAP values calculated for all customers
- ✓ 250 actions allocated across 55 high-priority customers
- ✓ 5 knowledge base PDFs (20 pages of sales collateral)

**You can skip `python setup.py` - everything is ready!**

### Step 3: Launch the App (5 seconds)
```bash
streamlit run app.py
```

### Step 4: Configure API Key
1. Get your Anthropic API key from https://console.anthropic.com/
2. Enter it in the sidebar of the app
3. Select a customer and explore!

---

## What You'll See

### Tab 1: SHAP Waterfall 📊
- Baseline: $88.5K (average prediction)
- Top 5 features driving this customer's prediction
- "All else" aggregated
- Final predicted expansion revenue

### Tab 2: Feature Interactions 🔄
- 3 scatter plots showing SHAP value vs feature value
- Color indicates action allocation (darker = more actions)
- Red star = your selected customer
- **Insight**: See why certain customers get more actions

### Tab 3: Pre-Call Plan 📋
- Click "Generate Pre-Call Plan"
- Claude synthesizes:
  - SHAP quantitative insights
  - 5 knowledge base PDFs
  - Customer profile
- Creates 7-section actionable plan:
  1. Executive summary
  2. Key talking points
  3. Pain points & needs
  4. Competitive positioning
  5. Specific actions
  6. Success metrics
  7. Risk mitigation

---

## Example Customer to Try

Try **CUST_00042**:
- High cloud maturity (+$12.3K SHAP impact)
- Multiple demo requests (+$8.7K impact)
- Large tech stack (+$6.2K impact)
- **Prediction**: $127.5K expansion potential
- **Allocated**: 5 actions (max)

The pre-call plan will explain why this customer is prioritized and what specific capabilities to emphasize based on their drivers.

---

## File Overview

```
📁 enterprise_sales_intelligence/
├── app.py                     ← Main Streamlit app (Steps 16-30)
├── setup.py                   ← Optional: Regenerate data
├── README.md                  ← Full 30-step documentation
├── QUICKSTART.md              ← This file
│
├── 📁 data/
│   ├── customers.csv                      ← 500 customers with features
│   ├── customers_with_actions.csv         ← With action allocations
│   └── allocation_summary.pkl             ← Summary stats
│
├── 📁 models/
│   ├── expansion_model.pkl                ← Trained Random Forest
│   └── shap_values.pkl                    ← SHAP explanations
│
└── 📁 knowledgedb/
    ├── product_capabilities.pdf           ← Platform features
    ├── competitive_intelligence.pdf       ← Market analysis
    ├── case_study_fintech.pdf             ← Customer success
    ├── industry_trends_2025.pdf           ← Market trends
    └── best_practices_enterprise_deployment.pdf
```

---

## Regenerating Data (Optional)

If you want to create fresh synthetic data:

```bash
python setup.py
```

This will:
- Generate new customers with different random features
- Train a new model
- Calculate new SHAP values
- Allocate actions differently
- Recreate knowledge base PDFs

**Runtime**: ~2-3 minutes

---

## Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt --break-system-packages
```

### "API key invalid"
- Get key from https://console.anthropic.com/
- Ensure you have credits in your account
- Key should start with "sk-ant-"

### "No data files"
Run the setup:
```bash
python setup.py
```

### App runs but no customers
Check that `data/customers_with_actions.csv` exists and has `allocated_actions > 0`

---

## Cost Estimate

### Using Existing Data (Recommended)
- **Data**: Already included ✓
- **API Costs**: ~$0.10 per pre-call plan generated
- **Total**: $5-10 for 50-100 plan generations

### Regenerating Data
- **Computation**: Free (runs locally)
- **Time**: ~2-3 minutes
- **API Costs**: Same as above

---

## Next Steps

1. **Try different customers** - Each has unique SHAP drivers
2. **Compare interaction plots** - See patterns in action allocation
3. **Generate multiple plans** - Compare Claude's synthesis
4. **Modify knowledge base** - Add your own PDFs to `knowledgedb/`
5. **Customize features** - Edit `01_generate_and_train.py`

---

## Questions?

- **Full Documentation**: See `README.md` for complete 30-step breakdown
- **Code Comments**: Each script is well-documented
- **SHAP Tutorial**: https://shap.readthedocs.io/
- **Claude Docs**: https://docs.anthropic.com/

---

**🎯 Ready to see AI-powered sales intelligence in action!**

Run `streamlit run app.py` and explore!
