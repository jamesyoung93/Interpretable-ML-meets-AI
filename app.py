"""
Step 16-20: Enterprise Sales Intelligence App
Main Streamlit application with SHAP waterfalls, interactions, and AI-powered pre-call planning
"""
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import anthropic
import os
import PyPDF2

# Page config
st.set_page_config(
    page_title="Enterprise Sales Intelligence",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Enterprise Sales Intelligence Platform")
st.markdown("*AI-powered pre-call planning with SHAP-based insights*")

# Load data and models
@st.cache_data
def load_data():
    """Step 16: Load customer data and SHAP values"""
    df = pd.read_csv('data/customers_with_actions.csv')
    
    with open('models/shap_values.pkl', 'rb') as f:
        shap_artifact = pickle.load(f)
    
    with open('models/expansion_model.pkl', 'rb') as f:
        model_artifact = pickle.load(f)
    
    with open('data/allocation_summary.pkl', 'rb') as f:
        summary = pickle.load(f)
    
    return df, shap_artifact, model_artifact, summary

try:
    df, shap_artifact, model_artifact, summary = load_data()
    
    shap_values = shap_artifact['shap_values']
    expected_value = shap_artifact['expected_value']
    feature_names = shap_artifact['feature_names']
    
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Run `python 01_generate_and_train.py` and `python 02_shap_and_allocation.py` first")
    st.stop()

# Sidebar - Customer Selection
st.sidebar.header("Customer Selection")

# Filter to customers with actions
customers_with_actions = df[df['allocated_actions'] > 0].copy()
customers_with_actions = customers_with_actions.sort_values('action_score', ascending=False)

selected_customer_id = st.sidebar.selectbox(
    "Select Customer",
    customers_with_actions['customer_id'].values,
    format_func=lambda x: f"{x} ({customers_with_actions[customers_with_actions['customer_id']==x]['company_name'].values[0]})"
)

# Get customer data
customer_row = df[df['customer_id'] == selected_customer_id].iloc[0]
customer_idx = df[df['customer_id'] == selected_customer_id].index[0]
customer_shap = shap_values[customer_idx]

st.sidebar.markdown("---")
st.sidebar.metric("Allocated Actions", int(customer_row['allocated_actions']))
st.sidebar.metric("Predicted Expansion", f"${customer_row['predicted_expansion_revenue']:.1f}K")
st.sidebar.metric("Action Score", f"{customer_row['action_score']:.1f}")
st.sidebar.markdown("**Recommended Promotion:**")
st.sidebar.info(customer_row['recommended_promotion'])

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"📊 {customer_row['company_name']}")
    st.caption(f"Customer ID: {selected_customer_id}")

with col2:
    # Claude API key
    api_key = st.text_input("🔑 Anthropic API Key", type="password", key="api_key")
    if api_key:
        st.success("API key configured")

st.markdown("---")

# Tab layout
tab1, tab2, tab3 = st.tabs(["📈 SHAP Waterfall", "🔄 Feature Interactions", "📋 Pre-Call Plan"])

# Step 17: SHAP Waterfall Chart
with tab1:
    st.subheader("SHAP Waterfall: Revenue Drivers")
    st.caption("Shows how each feature contributes to the prediction vs. baseline")
    
    # Get top 5 features by absolute SHAP value
    abs_shap = np.abs(customer_shap)
    top_indices = np.argsort(abs_shap)[::-1][:5]
    
    # Calculate "all else"
    top_shap_sum = customer_shap[top_indices].sum()
    all_else = customer_shap.sum() - top_shap_sum
    
    # Build waterfall data
    categories = ['Baseline']
    values = [expected_value]
    
    # Add top 5
    for idx in top_indices:
        categories.append(feature_names[idx].replace('_', ' ').title())
        values.append(customer_shap[idx])
    
    # Add "all else"
    categories.append('All Other Features')
    values.append(all_else)
    
    # Add total
    categories.append('Predicted Value')
    values.append(customer_row['predicted_expansion_revenue'])
    
    # Create waterfall
    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute"] + ["relative"]*6 + ["total"],
        x=categories,
        text=[f"${v:.1f}K" for v in values],
        textposition="outside",
        y=values,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#00CC96"}},
        decreasing={"marker": {"color": "#EF553B"}},
        totals={"marker": {"color": "#636EFA"}}
    ))
    
    fig.update_layout(
        height=500,
        title=f"Revenue Contribution Waterfall (${expected_value:.1f}K → ${customer_row['predicted_expansion_revenue']:.1f}K)",
        showlegend=False,
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Feature details
    with st.expander("📋 Feature Details"):
        detail_df = pd.DataFrame({
            'Feature': [feature_names[i] for i in top_indices],
            'Customer Value': [customer_row[feature_names[i]] for i in top_indices],
            'SHAP Contribution': [f"${customer_shap[i]:.2f}K" for i in top_indices],
            'Impact': ['Positive' if customer_shap[i] > 0 else 'Negative' for i in top_indices]
        })
        st.dataframe(detail_df, use_container_width=True)
    
    # Promotional sensitivity analysis
    st.markdown("---")
    st.subheader("🎯 Promotional Strategy Recommendation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Bar chart of sensitivities
        sensitivity_data = {
            'Promotion Type': ['Price Discount', 'Extended SLA', 'Training Credits', 'Implementation Support'],
            'Sensitivity Score': [
                customer_row['discount_sensitivity'],
                customer_row['sla_sensitivity'],
                customer_row['training_sensitivity'],
                customer_row['implementation_support_sensitivity']
            ]
        }
        
        fig_promo = go.Figure(go.Bar(
            x=sensitivity_data['Sensitivity Score'],
            y=sensitivity_data['Promotion Type'],
            orientation='h',
            marker=dict(
                color=sensitivity_data['Sensitivity Score'],
                colorscale='Viridis',
                showscale=False
            ),
            text=[f"{s:.2f}" for s in sensitivity_data['Sensitivity Score']],
            textposition='auto'
        ))
        
        fig_promo.update_layout(
            title="Customer Promotional Sensitivities",
            xaxis_title="Sensitivity (0-1, higher = more responsive)",
            yaxis_title="",
            height=250,
            showlegend=False
        )
        
        st.plotly_chart(fig_promo, use_container_width=True)
    
    with col2:
        st.markdown("**Recommended:**")
        st.success(customer_row['recommended_promotion'])
        st.caption("Based on highest sensitivity score. Use this promotion to maximize conversion probability.")

# Step 18: Interaction Plots
with tab2:
    st.subheader("Feature Interactions: Why This Customer?")
    st.caption("Interaction between top features and allocated actions")
    
    # Get top 3 features
    top_3_indices = top_indices[:3]
    top_3_names = [feature_names[i] for i in top_3_indices]
    
    # Create interaction plots
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=[n.replace('_', ' ').title() for n in top_3_names]
    )
    
    for i, feature_idx in enumerate(top_3_indices):
        feature_name = feature_names[feature_idx]
        
        # Get all customers' SHAP values for this feature
        all_feature_shap = shap_values[:, feature_idx]
        all_feature_values = df[feature_name].values
        all_actions = df['allocated_actions'].values
        
        # Color by action allocation
        colors = all_actions
        
        fig.add_trace(
            go.Scatter(
                x=all_feature_values,
                y=all_feature_shap,
                mode='markers',
                marker=dict(
                    size=8,
                    color=colors,
                    colorscale='Viridis',
                    showscale=(i == 0),
                    colorbar=dict(title="Actions<br>Allocated") if i == 0 else None,
                    line=dict(width=0.5, color='white')
                ),
                text=[f"Actions: {a}" for a in all_actions],
                hovertemplate='<b>Value: %{x:.2f}</b><br>SHAP: %{y:.2f}<br>%{text}<extra></extra>',
                showlegend=False
            ),
            row=1, col=i+1
        )
        
        # Highlight selected customer
        fig.add_trace(
            go.Scatter(
                x=[customer_row[feature_name]],
                y=[customer_shap[feature_idx]],
                mode='markers',
                marker=dict(
                    size=15,
                    color='red',
                    symbol='star',
                    line=dict(width=2, color='darkred')
                ),
                name='Selected Customer',
                showlegend=(i == 0),
                hovertemplate=f'<b>This Customer</b><br>Value: %{{x:.2f}}<br>SHAP: %{{y:.2f}}<extra></extra>'
            ),
            row=1, col=i+1
        )
        
        # Update axes
        fig.update_xaxes(title_text=feature_name.replace('_', ' ').title(), row=1, col=i+1)
        if i == 0:
            fig.update_yaxes(title_text="SHAP Value", row=1, col=i+1)
    
    fig.update_layout(
        height=400,
        title_text="Feature Interactions: Higher actions allocated to customers with stronger SHAP contributions",
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **💡 Interpretation Guide:**
    - **X-axis**: Feature value for each customer
    - **Y-axis**: SHAP contribution (impact on prediction)
    - **Color**: Number of actions allocated
    - **Red star**: Currently selected customer
    
    Customers with higher SHAP contributions (more positive impact) receive more actions.
    This explains *why* certain customers are prioritized for engagement.
    """)

# Step 19-20: Pre-Call Plan with Claude
with tab3:
    st.subheader("🤖 AI-Powered Pre-Call Plan")
    st.caption("Synthesizes SHAP insights with knowledge base for actionable recommendations")
    
    if not api_key:
        st.warning("Please enter your Anthropic API key in the sidebar to generate pre-call plans")
    else:
        if st.button("Generate Pre-Call Plan", type="primary"):
            with st.spinner("Analyzing customer data and knowledge base..."):
                # Step 19: Read PDFs from knowledge base
                def extract_pdf_text(pdf_path):
                    """Extract text from PDF"""
                    try:
                        with open(pdf_path, 'rb') as file:
                            pdf_reader = PyPDF2.PdfReader(file)
                            text = ""
                            for page in pdf_reader.pages:
                                text += page.extract_text()
                            return text
                    except Exception as e:
                        return f"Error reading {pdf_path}: {e}"
                
                # Load knowledge base
                knowledge_docs = {}
                kb_dir = 'knowledgedb'
                if os.path.exists(kb_dir):
                    for filename in os.listdir(kb_dir):
                        if filename.endswith('.pdf'):
                            pdf_path = os.path.join(kb_dir, filename)
                            knowledge_docs[filename] = extract_pdf_text(pdf_path)
                
                # Build context for Claude
                top_5_features = []
                for idx in top_indices:
                    top_5_features.append({
                        'feature': feature_names[idx],
                        'value': float(customer_row[feature_names[idx]]),
                        'shap_contribution': float(customer_shap[idx]),
                        'impact_direction': 'positive' if customer_shap[idx] > 0 else 'negative'
                    })
                
                customer_context = {
                    'customer_id': selected_customer_id,
                    'company_name': customer_row['company_name'],
                    'predicted_revenue': float(customer_row['predicted_expansion_revenue']),
                    'allocated_actions': int(customer_row['allocated_actions']),
                    'action_score': float(customer_row['action_score']),
                    'recommended_promotion': customer_row['recommended_promotion'],
                    'promotional_sensitivities': {
                        'discount_sensitivity': float(customer_row['discount_sensitivity']),
                        'sla_sensitivity': float(customer_row['sla_sensitivity']),
                        'training_sensitivity': float(customer_row['training_sensitivity']),
                        'implementation_support_sensitivity': float(customer_row['implementation_support_sensitivity'])
                    },
                    'top_5_shap_drivers': top_5_features,
                    'baseline_value': float(expected_value)
                }
                
                # Step 20: Generate pre-call plan with Claude
                try:
                    client = anthropic.Anthropic(api_key=api_key)
                    
                    # Build prompt
                    prompt = f"""You are an expert enterprise sales strategist. Create a compelling pre-call plan for an account executive preparing to engage with this B2B software customer.

CUSTOMER PROFILE:
{customer_context}

SHAP ANALYSIS INSIGHTS:
The model predicts ${customer_context['predicted_revenue']:.1f}K expansion revenue potential (vs. ${customer_context['baseline_value']:.1f}K baseline).

Top 5 Revenue Drivers:
"""
                    for feat in top_5_features:
                        direction = "increases" if feat['impact_direction'] == 'positive' else 'decreases'
                        prompt += f"- {feat['feature'].replace('_', ' ').title()}: {feat['value']:.2f} ({direction} revenue by ${abs(feat['shap_contribution']):.1f}K)\n"
                    
                    prompt += f"\nThis customer has been allocated {customer_context['allocated_actions']} high-priority actions.\n\n"
                    
                    prompt += f"RECOMMENDED PROMOTION:\n{customer_context['recommended_promotion']}\n"
                    prompt += f"Promotional Sensitivities:\n"
                    prompt += f"- Price Discount: {customer_context['promotional_sensitivities']['discount_sensitivity']:.2f}\n"
                    prompt += f"- Extended SLA: {customer_context['promotional_sensitivities']['sla_sensitivity']:.2f}\n"
                    prompt += f"- Training Credits: {customer_context['promotional_sensitivities']['training_sensitivity']:.2f}\n"
                    prompt += f"- Implementation Support: {customer_context['promotional_sensitivities']['implementation_support_sensitivity']:.2f}\n\n"
                    
                    prompt += "KNOWLEDGE BASE:\n\n"
                    for doc_name, doc_content in knowledge_docs.items():
                        prompt += f"--- {doc_name} ---\n{doc_content[:3000]}...\n\n"  # Truncate for context length
                    
                    prompt += """
CREATE A PRE-CALL PLAN that:

1. **Executive Summary**: 2-3 sentences on why this customer is high-priority and what the meeting should accomplish

2. **Key Talking Points**: Based on SHAP drivers, what specific capabilities or solutions should you emphasize? 
   IMPORTANT: Cite specific knowledge base documents when referencing information using format [Source: document_name]

3. **Customer Pain Points & Needs**: What does the SHAP analysis reveal about their situation? What problems are they likely facing?

4. **Competitive Positioning**: Based on the knowledge base, how should you position against competitors? Include citations.

5. **Promotional Strategy**: Explain why the recommended promotion ({}) aligns with this customer's sensitivities and buying preferences.

6. **Specific Actions to Propose**: Concrete next steps (demos, POCs, workshops, case studies) that align with their drivers

7. **Success Metrics**: How to measure engagement success

8. **Risk Mitigation**: Potential objections and how to address them. Cite relevant knowledge base content.

CRITICAL: When referencing information from the knowledge base PDFs, cite the source using this format: [Source: product_capabilities.pdf] or [Source: competitive_intelligence.pdf], etc.

Make this practical and actionable. Reference specific knowledge base content where relevant and ALWAYS cite your sources.""".format(customer_context['recommended_promotion'])

                    message = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=8000,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    plan = message.content[0].text
                    
                    # Display the plan
                    st.markdown(plan)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Pre-Call Plan",
                        data=plan,
                        file_name=f"precall_plan_{selected_customer_id}.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"Error generating plan: {e}")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Pipeline", f"${summary['total_pipeline_value']/1000:.1f}M")
with col2:
    st.metric("Customers with Actions", summary['customers_with_actions'])
with col3:
    st.metric("Total Actions Allocated", summary['total_actions_allocated'])

st.caption("Enterprise Sales Intelligence Platform • Powered by SHAP + Claude AI")
