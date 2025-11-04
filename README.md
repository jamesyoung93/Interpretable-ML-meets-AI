# 🎯 Enterprise Sales Intelligence Platform

**AI-Powered Pre-Call Planning with SHAP Explanations and Knowledge Base Synthesis**

An end-to-end sales intelligence system demonstrating how machine learning explainability (SHAP) combined with Large Language Models (Claude) creates powerful, actionable insights for B2B sales teams.

---

## 🌟 What This Is

This is a **complete, production-ready pipeline** that shows how modern AI can transform sales operations:

1. **Predictive Model**: Random Forest predicting expansion revenue potential
2. **Explainable AI**: SHAP values showing *why* each prediction is made
3. **Optimization**: Constrained allocation of sales actions across customers
4. **Visualization**: Waterfall charts and interaction plots
5. **Generative AI**: Claude synthesizing SHAP insights with company knowledge base

**Domain**: B2B Software Sales (Enterprise Cloud Platform)

---

## 🚀 Quick Start

### **Prerequisites**
```bash
Python 3.9+
pip install -r requirements.txt
```

### **Setup (Runs Steps 1-15)**
```bash
python setup.py
```

This will:
- Generate synthetic customer data
- Train and pickle the model
- Calculate SHAP values
- Allocate actions via optimization
- Create knowledge base PDFs

**Runtime**: ~2-3 minutes

### **Launch App (Steps 16-30)**
```bash
streamlit run app.py
```

Then:
1. Enter your Anthropic API key in the sidebar
2. Select a customer from the dropdown
3. Explore the three tabs:
   - **SHAP Waterfall**: See revenue drivers
   - **Feature Interactions**: Understand why actions are allocated
   - **Pre-Call Plan**: Generate AI-powered insights

---

## 📋 The 30-Step Process

### **Phase 1: Data & Model (Steps 1-5)**
Handled by `01_generate_and_train.py`

| Step | Description |
|------|-------------|
| 1 | Generate 500 synthetic B2B customers with 20+ features |
| 2 | Create target variable (expansion revenue potential) with realistic interactions |
| 3 | Train Random Forest model (80/20 train/test split) |
| 4 | Pickle trained model with metadata |
| 5 | Save customer dataset with predictions |

**Output**: `models/expansion_model.pkl`, `data/customers.csv`

---

### **Phase 2: Explainability & Allocation (Steps 6-10)**
Handled by `02_shap_and_allocation.py`

| Step | Description |
|------|-------------|
| 6 | Load trained model and customer data |
| 7 | Calculate SHAP values using TreeExplainer (all 500 customers) |
| 8 | Calculate action scores (revenue + urgency + fit + relationship) |
| 9 | Run constrained optimization to allocate 250 actions across customers (max 5 per customer) |
| 10 | Save final dataset with action allocations and SHAP values |

**Output**: `models/shap_values.pkl`, `data/customers_with_actions.csv`

**Constraint**: 250 total actions, max 5 per customer, prioritized by action score

---

### **Phase 3: Knowledge Base (Steps 11-15)**
Handled by `03_create_knowledge_pdfs.py`

| Step | Description |
|------|-------------|
| 11 | Create "Product Capabilities" PDF (7 sections, 2 pages) |
| 12 | Create "Competitive Intelligence" PDF (5 sections covering CloudControl, TechOps, etc.) |
| 13 | Create "Case Study: FinTech Success" PDF (6 sections with metrics) |
| 14 | Create "Industry Trends 2025" PDF (5 trend analyses) |
| 15 | Create "Best Practices" PDF (5 implementation guides) |

**Output**: 5 PDFs in `knowledgedb/` directory totaling ~20 pages of sales collateral

---

### **Phase 4: Streamlit App (Steps 16-30)**
Handled by `app.py`

| Step | Description |
|------|-------------|
| 16 | Load data (customers, SHAP, model, summary stats) |
| 17 | Create SHAP waterfall chart (baseline + top 5 features + "all else" + total) |
| 18 | Generate interaction plots showing SHAP vs feature value colored by action allocation |
| 19 | Extract text from all PDFs in knowledge base |
| 20 | Build context for Claude (SHAP drivers + customer profile + KB docs) |
| 21-25 | Claude synthesizes: executive summary, talking points, pain points, positioning, actions |
| 26-30 | Claude generates: success metrics, risk mitigation, formatting, quality checks, final output |

**Output**: Interactive web app with visualizations and AI-generated pre-call plans

---



## 📊 Key Features

### **1. SHAP Waterfall Charts**
- **Baseline**: Expected value across all customers ($X)
- **Top 5 Contributors**: Features with highest absolute SHAP values
- **All Else**: Aggregated contribution of remaining features
- **Total**: Final predicted value

**Example**:
```
Baseline: $45K
+ Cloud Maturity Score: +$8.2K
+ Demo Requests: +$6.5K
+ Employee Count: +$4.1K
- Previous Churn Risk: -$2.3K
+ Tech Stack Size: +$3.8K
+ All Other Features: +$1.2K
= Predicted: $66.5K
```

### **2. Interaction Plots**
Shows relationship between feature value, SHAP contribution, and action allocation:
- **X-axis**: Feature value
- **Y-axis**: SHAP contribution (impact on prediction)
- **Color**: Number of actions allocated
- **Red star**: Currently selected customer

**Insight**: Customers with higher SHAP contributions receive more actions, explaining *why* the allocation is optimal.

### **3. AI Pre-Call Planning**
Claude synthesizes:
- SHAP analysis (quantitative drivers)
- Knowledge base (product capabilities, competitive intel, case studies, trends, best practices)
- Customer profile (firmographics, engagement, relationships)

Into an actionable plan:
1. Executive summary
2. Key talking points
3. Pain points & needs
4. Competitive positioning
5. Specific actions to propose
6. Success metrics
7. Risk mitigation

**Not a summary** - this is synthesis. Claude connects quantitative signals (SHAP) with qualitative context (KB) to create insights neither source provides alone.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Generation                         │
│  500 customers × 20 features → expansion_revenue_potential  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Model Training                            │
│  Random Forest → 80/20 split → pickle model                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 SHAP Calculation                            │
│  TreeExplainer → 500 customers × 20 features                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               Action Allocation                             │
│  Greedy optimization: 250 actions, max 5/customer           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Streamlit Application                          │
│  ┌──────────────────────────────────────────────┐          │
│  │  SHAP Waterfall  │  Interactions  │  AI Plan  │          │
│  └──────────────────────────────────────────────┘          │
│                         │                                    │
│                         ▼                                    │
│              ┌──────────────────────┐                       │
│              │   Claude API         │                       │
│              │   (Sonnet 4.5)       │                       │
│              └──────────────────────┘                       │
│                         │                                    │
│                         ▼                                    │
│              ┌──────────────────────┐                       │
│              │  Knowledge Base      │                       │
│              │  (5 PDFs)            │                       │
│              └──────────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
enterprise_sales_intelligence/
│
├── setup.py                          # Master orchestration script
├── requirements.txt                  # Python dependencies
│
├── 01_generate_and_train.py          # Steps 1-5
├── 02_shap_and_allocation.py         # Steps 6-10
├── 03_create_knowledge_pdfs.py       # Steps 11-15
├── app.py                            # Steps 16-30 (Streamlit)
│
├── data/
│   ├── customers.csv                 # Generated customers
│   ├── customers_with_actions.csv    # With allocations
│   └── allocation_summary.pkl        # Summary stats
│
├── models/
│   ├── expansion_model.pkl           # Trained Random Forest
│   └── shap_values.pkl               # SHAP explanations
│
└── knowledgedb/
    ├── product_capabilities.pdf
    ├── competitive_intelligence.pdf
    ├── case_study_fintech.pdf
    ├── industry_trends_2025.pdf
    └── best_practices_enterprise_deployment.pdf
```

---

## 🎓 Why This Matters

### **1. Explainability Drives Adoption**
Sales teams don't trust black boxes. SHAP values show *exactly* why a customer is prioritized:
- "This customer has high cloud maturity (+$8.2K impact)"
- "They've requested 3 demos (+$6.5K impact)"

This builds trust and enables coaching.

### **2. Optimization Scales Human Judgment**
Manual prioritization doesn't scale beyond 50 accounts. Constrained optimization:
- Allocates 250 actions across 500 customers in seconds
- Respects capacity constraints (max 5 actions/customer)
- Maximizes expected revenue

### **3. LLMs Synthesize Context**
Raw SHAP values + PDF summaries = information overload.

Claude synthesizes:
- "Their high cloud maturity score (+$8.2K) suggests they're ready for advanced features. Based on our case study with FinTech Innovations (similar profile), emphasize our automated compliance capabilities..."

This is **synthesis**, not **summary**.

### **4. End-to-End Demonstration**
Most ML demos stop at prediction. This shows:
- Training → Explanation → Optimization → Visualization → Action

Real-world ML requires the full pipeline.

---

## 🔧 Technical Details

### **Model**
- **Algorithm**: Random Forest Regressor
- **Features**: 20 (firmographic, engagement, product fit, relationship, market)
- **Target**: Expansion revenue potential ($5K - $200K)
- **Performance**: R² = 0.85-0.90 (synthetic data)

### **SHAP Calculation**
- **Method**: TreeExplainer with interventional feature perturbation
- **Background**: 50 samples (for speed)
- **Output**: 500 customers × 20 features = 10,000 SHAP values
- **Runtime**: ~30 seconds

### **Action Allocation**
- **Method**: Greedy allocation by action score
- **Constraints**: 250 total, max 5 per customer
- **Score**: `predicted_revenue + 5×demos + 2×cloud_maturity + 1.5×csm_score`

### **Claude Integration**
- **Model**: Claude Sonnet 4.5 (claude-sonnet-4-20250514)
- **Context Window**: ~8K tokens (customer + SHAP + 5 PDFs)
- **Output**: 1-2K tokens (structured pre-call plan)
- **Cost**: ~$0.10 per plan generation

---

## 💡 Use Cases

### **Sales Operations**
- Territory planning
- Account prioritization
- Resource allocation

### **Account Executives**
- Pre-call preparation
- Objection handling
- Value proposition tailoring

### **Sales Leadership**
- Pipeline analysis
- Coaching insights
- Strategy refinement

### **Other Industries**
With minor modifications:
- **Healthcare**: Patient prioritization
- **Financial Services**: Wealth management outreach
- **Retail**: Customer lifetime value optimization
- **Real Estate**: Property/client matching

---

## 🚨 Limitations & Future Work

### **Current Limitations**
- Synthetic data (not real customer data)
- Single model (no ensemble)
- Greedy allocation (not true optimization)
- Static knowledge base (no vector search)

### **Future Enhancements**
- Real data integration
- XGBoost/LightGBM comparison
- Linear programming for optimal allocation
- RAG with vector database
- SHAP interaction values (2nd order effects)
- A/B testing framework
- Integration with CRM (Salesforce, HubSpot)

---

## 📖 Learning Resources

### **SHAP (SHapley Additive exPlanations)**
- Paper: "A Unified Approach to Interpreting Model Predictions" (Lundberg & Lee, 2017)
- Library: https://github.com/slundberg/shap
- Tutorial: https://shap.readthedocs.io/

### **Claude AI**
- Anthropic: https://www.anthropic.com
- Documentation: https://docs.anthropic.com
- Prompt Engineering: https://docs.anthropic.com/claude/docs/prompt-engineering

### **Optimization**
- Linear Programming: scipy.optimize.linprog
- Constraint Satisfaction: OR-Tools (Google)

---

## 🤝 Contributing

This is a demonstration project. If you'd like to extend it:

1. **Data**: Replace synthetic data with real data
2. **Models**: Add XGBoost, neural networks, etc.
3. **Features**: Add time-series, NLP features
4. **Optimization**: Implement true linear programming
5. **RAG**: Add vector database for knowledge base
6. **UI**: Enhance visualizations, add filters

---

## ⚠️ Disclaimer

This project uses **synthetic data** for demonstration purposes. Do not use for actual business decisions without:
- Real customer data
- Proper validation
- Domain expert review
- Compliance approval
- Ongoing monitoring

Machine learning models can be wrong. SHAP values explain the model, not ground truth. Always combine AI insights with human judgment.

---

## 📄 License

MIT License - Free for commercial and educational use.

---

## 🙏 Acknowledgments

- **Anthropic** for Claude AI
- **Scott Lundberg** for SHAP
- **Streamlit** for the app framework
- **Plotly** for interactive visualizations

---

## 📞 Questions?

Built to demonstrate modern AI in sales operations. The 30-step process shows how predictive modeling, explainable AI, optimization, and large language models work together to create actionable intelligence.

**Key Insight**: The power isn't in any single technology - it's in the synthesis.

---

**⭐ If this helps you understand SHAP + LLMs, give it a star!**

*Built with 🎯 using Claude AI, SHAP, Plotly, and Streamlit*
