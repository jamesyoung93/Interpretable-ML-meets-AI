#!/usr/bin/env python3
"""
Master Setup Script: Runs all 30 steps to prepare the Enterprise Sales Intelligence platform

This script orchestrates:
- Steps 1-5: Data generation and model training
- Steps 6-10: SHAP calculation and action allocation
- Steps 11-15: Knowledge base PDF creation
- Steps 16-30: Handled by the Streamlit app (app.py)
"""

import subprocess
import sys
import os

def run_step(step_name, script_path):
    """Run a Python script and handle errors"""
    print(f"\n{'='*80}")
    print(f"Running: {step_name}")
    print(f"{'='*80}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✓ {step_name} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {step_name} failed!")
        print(f"Error: {e}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              ENTERPRISE SALES INTELLIGENCE PLATFORM                          ║
║                     30-Step Setup Process                                    ║
║                                                                              ║
║  This will generate synthetic data, train models, calculate SHAP values,    ║
║  allocate actions, and create a knowledge base for AI-powered pre-call      ║
║  planning in B2B software sales.                                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    input("Press Enter to begin setup... ")
    
    # Check we're in the right directory
    if not os.path.exists('01_generate_and_train.py'):
        print("\n✗ Error: Must run from enterprise_sales_intelligence directory")
        print("  Current directory:", os.getcwd())
        return False
    
    # Run the pipeline
    steps = [
        ("Steps 1-5: Generate Data & Train Model", "01_generate_and_train.py"),
        ("Steps 6-10: Calculate SHAP & Allocate Actions", "02_shap_and_allocation.py"),
        ("Steps 11-15: Create Knowledge Base PDFs", "03_create_knowledge_pdfs.py"),
    ]
    
    for step_name, script_path in steps:
        if not run_step(step_name, script_path):
            print("\n" + "="*80)
            print("Setup failed. Please fix the error and try again.")
            print("="*80)
            return False
    
    # Success!
    print(f"\n{'='*80}")
    print("✓ ALL SETUP STEPS COMPLETE!")
    print(f"{'='*80}\n")
    
    print("""
Generated Files:
  📁 data/
     ├── customers.csv                    (500 B2B customers)
     ├── customers_with_actions.csv       (with action allocations)
     └── allocation_summary.pkl           (summary statistics)
  
  📁 models/
     ├── expansion_model.pkl              (trained Random Forest)
     └── shap_values.pkl                  (SHAP explanations)
  
  📁 knowledgedb/
     ├── product_capabilities.pdf         (platform features)
     ├── competitive_intelligence.pdf     (market positioning)
     ├── case_study_fintech.pdf           (customer success story)
     ├── industry_trends_2025.pdf         (market trends)
     └── best_practices_enterprise_deployment.pdf (implementation guide)

Next Steps (Steps 16-30):
  
  1. Install dependencies (if not already done):
     pip install -r requirements.txt
  
  2. Launch the Streamlit app:
     streamlit run app.py
  
  3. Enter your Anthropic API key in the sidebar
  
  4. Select a customer and explore:
     - SHAP waterfall charts (baseline + top 5 + all else)
     - Feature interaction plots (why actions are allocated)
     - AI-generated pre-call plans (Claude + knowledge base synthesis)

The app handles Steps 16-30:
  - Step 16-17: Load data and create SHAP waterfalls
  - Step 18: Generate interaction plots
  - Step 19-20: Extract PDF text and generate pre-call plans
  - Steps 21-30: Handled within the app's interactive features

Enjoy your Enterprise Sales Intelligence Platform! 🎯
    """)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
