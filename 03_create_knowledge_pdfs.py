"""
Step 11-15: Generate knowledge base PDFs for B2B Software Sales context
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
import os

output_dir = 'knowledgedb'
os.makedirs(output_dir, exist_ok=True)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=11, leading=14))

def create_pdf(filename, title, content_sections):
    """Helper to create a PDF document"""
    doc = SimpleDocTemplate(f"{output_dir}/{filename}", pagesize=letter,
                          rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    Story = []
    
    # Title
    Story.append(Paragraph(f"<b>{title}</b>", styles['Title']))
    Story.append(Spacer(1, 0.2*inch))
    
    # Content sections
    for section_title, section_text in content_sections:
        Story.append(Paragraph(f"<b>{section_title}</b>", styles['Heading2']))
        Story.append(Spacer(1, 0.1*inch))
        Story.append(Paragraph(section_text, styles['Justify']))
        Story.append(Spacer(1, 0.2*inch))
    
    doc.build(Story)
    print(f"  Created {filename}")

# Step 11: Product capabilities PDF
print("Step 11: Creating product capabilities document...")

create_pdf('product_capabilities.pdf', 'Enterprise Cloud Platform - Product Capabilities', [
    ('Overview', 
     'Our Enterprise Cloud Platform is a comprehensive solution designed for mid-market to enterprise organizations seeking to modernize their technology infrastructure. The platform combines infrastructure automation, application deployment, security compliance, and observability into a unified system that reduces operational complexity while improving reliability and scalability.'),
    
    ('Core Infrastructure Automation',
     'The platform provides automated provisioning and configuration management across multi-cloud environments including AWS, Azure, and Google Cloud. Infrastructure-as-Code (IaC) templates allow teams to define resources declaratively, with automatic drift detection and remediation. Policy-based governance ensures compliance with organizational standards while maintaining developer velocity.'),
    
    ('Application Deployment & CI/CD',
     'Built-in continuous integration and deployment pipelines support modern development practices with automated testing, security scanning, and progressive delivery strategies like blue-green and canary deployments. Native support for containerized workloads (Kubernetes), serverless functions, and traditional VM-based applications provides flexibility for diverse application portfolios.'),
    
    ('Security & Compliance Framework',
     'Enterprise-grade security includes role-based access control (RBAC), secrets management, encryption at rest and in transit, and comprehensive audit logging. Pre-built compliance templates for SOC 2, HIPAA, PCI-DSS, and GDPR accelerate certification processes. Continuous compliance monitoring with automated remediation reduces security risks and audit burden.'),
    
    ('Observability & Performance',
     'Unified observability combines metrics, logs, and distributed tracing into a single pane of glass. AI-powered anomaly detection identifies issues before they impact users. Cost optimization recommendations help organizations right-size infrastructure and reduce cloud spending by 20-40% on average.'),
    
    ('Integration Ecosystem',
     'REST and GraphQL APIs enable deep integration with existing tools. Pre-built connectors for popular systems like ServiceNow, Jira, Slack, and Microsoft Teams ensure seamless workflow integration. Webhook-based event system allows real-time automation across the technology stack.'),
    
    ('Enterprise Support Model',
     '24/7 technical support with guaranteed response times based on severity. Dedicated Customer Success Manager for accounts with 500+ employees. Quarterly business reviews assess platform utilization and identify optimization opportunities. Professional services available for migration planning, custom integrations, and team training.')
])

# Step 12: Competitive intelligence PDF
print("\nStep 12: Creating competitive intelligence document...")

create_pdf('competitive_intelligence.pdf', 'Competitive Landscape Analysis - Q4 2025', [
    ('Market Position',
     'The enterprise cloud management market is experiencing 35% YoY growth, driven by multi-cloud adoption and increasing operational complexity. Three major players dominate: CloudControl (25% market share), TechOps Suite (18%), and our platform (12%). The remaining market is fragmented across 50+ vendors. Our strongest differentiator is the unified security and compliance framework, which competitors bolt on through third-party integrations.'),
    
    ('CloudControl Comparison',
     'CloudControl leads in market presence and brand recognition, particularly in Fortune 500 accounts. Their strengths include mature enterprise sales organization, extensive partner ecosystem, and 15+ years of market presence. However, customers cite complexity as a major pain point - average implementation takes 8-12 months vs. our 3-4 months. Their security model requires separate products (CloudControl Security Suite) creating integration friction. Pricing is 40-60% higher for comparable functionality. Win against CloudControl by emphasizing faster time-to-value, unified security, and total cost of ownership.'),
    
    ('TechOps Suite Comparison',
     'TechOps Suite targets DevOps-centric organizations with strong CI/CD capabilities. They excel in developer experience and have significant open-source community support. Weaknesses include limited enterprise governance features, complex pricing model based on usage metrics that creates unpredictable costs, and minimal professional services organization. Their compliance framework is immature - only SOC 2 certified, lacking HIPAA and PCI-DSS. Win against TechOps by emphasizing enterprise governance, predictable pricing, and comprehensive compliance support.'),
    
    ('Open Source Alternatives',
     'Organizations sometimes consider building platforms using open-source tools (Terraform, Ansible, Kubernetes, etc.). This appeals to technical teams but significantly underestimates total cost of ownership. Internal platform teams require 5-8 engineers, costing $1-1.5M annually vs. $200-400K for our platform. Maintenance burden, security patching, and integration work create hidden costs. Win by conducting TCO analysis showing 3-year savings of $2-4M compared to self-built solutions.'),
    
    ('Emerging Threats',
     'Several well-funded startups are entering the market with AI-first approaches. CloudAI and AutoStack have raised significant funding and are gaining traction in mid-market. Their automation capabilities are impressive but lack enterprise features and proven track record at scale. Monitor closely - these could disrupt the market in 18-24 months if they mature rapidly.')
])

# Step 13: Case study PDF
print("\nStep 13: Creating case study document...")

create_pdf('case_study_fintech.pdf', 'Case Study: FinTech Innovations - Cloud Migration Success', [
    ('Customer Profile',
     'FinTech Innovations is a digital payments processor serving 5,000 merchant customers across North America. With 800 employees and $500M in transaction volume, they faced increasing infrastructure costs and compliance complexity managing their legacy data center infrastructure. Their technology team of 40 engineers was spending 60% of time on operational tasks rather than product development.'),
    
    ('Business Challenge',
     'FinTech needed to migrate to cloud infrastructure to improve scalability, reduce costs, and accelerate product velocity. However, as a PCI-DSS Level 1 service provider, they required rigorous security controls and audit capabilities. Previous attempts to migrate using native cloud tools failed due to compliance gaps and lack of automation. They evaluated CloudControl and TechOps Suite before selecting our platform.'),
    
    ('Solution Implementation',
     'Implementation took 4 months with a phased approach. Phase 1 (6 weeks): Platform setup, team training, and pilot with non-production environments. Phase 2 (8 weeks): Production workload migration using automated tooling, starting with stateless applications. Phase 3 (4 weeks): Database migration and cutover. Our professional services team worked alongside their engineers, transferring knowledge throughout. The PCI-DSS compliance template accelerated certification - they achieved compliance 3 months ahead of schedule.'),
    
    ('Business Results',
     'Infrastructure costs reduced by 35% ($450K annual savings) through automated right-sizing and reserved instance management. Engineering productivity improved dramatically - operational tasks dropped from 60% to 20% of team capacity, freeing 1,600 engineering hours per month for product work. This acceleration enabled them to launch 3 major features 4 months earlier than planned, contributing to 15% customer growth. Deployment frequency increased 10x (from weekly to multiple times daily) while incident rates dropped 60%. System uptime improved from 99.7% to 99.95%.'),
    
    ('Customer Testimonial',
     '"The platform transformed our engineering organization. We went from spending most of our time fighting fires to actually innovating on our product. The compliance features were game-changing - we achieved PCI recertification in half the time with 80% less manual work. I wish we had made this move two years earlier." - Sarah Chen, CTO, FinTech Innovations'),
    
    ('Lessons Learned',
     'Success factors included executive sponsorship from the CTO, clear success metrics defined upfront, and staged migration reducing risk. The combination of powerful automation with hands-on professional services support enabled rapid adoption. FinTech has since expanded usage to development environments and is piloting our cost optimization AI.')
])

# Step 14: Industry trends PDF
print("\nStep 14: Creating industry trends document...")

create_pdf('industry_trends_2025.pdf', 'Enterprise Technology Trends 2025-2026', [
    ('Multi-Cloud is the New Normal',
     'Organizations are abandoning single-cloud strategies. 78% of enterprises now operate workloads across 2-3 cloud providers, up from 45% in 2023. Drivers include avoiding vendor lock-in, optimizing costs through cloud arbitrage, and meeting data residency requirements. However, this creates operational complexity - managing different APIs, security models, and billing structures. Unified cloud management platforms that abstract multi-cloud differences are seeing accelerated adoption. Organizations with mature cloud management platforms report 40% lower operational overhead compared to those using native cloud tools.'),
    
    ('Security & Compliance Automation',
     'The shift from compliance as annual audit event to continuous compliance is accelerating. Regulations like NIS2 in Europe and SEC cybersecurity rules in US are driving demand for real-time compliance monitoring and automated evidence collection. Manual compliance processes cannot scale with modern deployment velocity - organizations pushing dozens or hundreds of changes daily. Platforms offering automated compliance as code are seeing 100%+ YoY growth. CISOs are prioritizing solutions that reduce audit preparation time from weeks to days while improving security posture.'),
    
    ('FinOps & Cost Optimization',
     'Cloud cost overruns remain a top concern. 65% of organizations exceeded cloud budgets by 20%+ in 2024. FinOps practices are maturing from basic tagging and reporting to sophisticated optimization with AI-driven recommendations. Key capabilities include automated right-sizing, commitment term optimization (reserved instances, savings plans), zombie resource detection, and show-back/chargeback models. Organizations with mature FinOps practices reduce cloud spend by 25-35% without impacting performance. Executive visibility into unit economics (cost per transaction, per customer) is becoming standard requirement.'),
    
    ('AI/ML Infrastructure Requirements',
     'AI/ML workloads are driving infrastructure evolution. Organizations need GPU-optimized infrastructure for model training, inference optimization for cost-effective deployment, and MLOps pipelines for model versioning and deployment. 42% of enterprises are running AI workloads in production, up from 18% in 2023. Key challenges include GPU cost management (10-20x higher than CPU instances) and specialized expertise requirements. Platforms that simplify AI infrastructure provisioning and cost optimization have significant competitive advantage.'),
    
    ('Platform Engineering Movement',
     'Organizations are shifting from siloed tools to integrated developer platforms. Internal platform teams are building "golden paths" that provide self-service infrastructure while maintaining governance. Platform engineering combines infrastructure automation, security guardrails, and developer experience. Successful platforms reduce cognitive load on developers, improve deployment velocity, and ensure compliance. 68% of organizations with 500+ engineers have platform engineering initiatives. This trend favors comprehensive platforms over point solutions requiring integration work.')
])

# Step 15: Best practices PDF
print("\nStep 15: Creating best practices document...")

create_pdf('best_practices_enterprise_deployment.pdf', 'Best Practices: Enterprise Platform Deployment', [
    ('Executive Sponsorship & Organizational Readiness',
     'Successful enterprise platform deployments require C-level sponsorship - typically CTO or CIO. Executive support ensures resource allocation, resolves organizational conflicts, and maintains momentum through challenges. Before technical implementation, assess organizational readiness: Is there clarity on goals and success metrics? Does the organization have cloud skills, or is training needed? Are there political barriers between teams? Conduct stakeholder analysis and create RACI matrix early. Organizations that invest 2-3 weeks in organizational preparation see 50% shorter implementations and higher adoption rates.'),
    
    ('Phased Approach with Early Wins',
     'Avoid big-bang deployments. Start with pilot project on non-critical system to prove capabilities and build confidence. Choose pilot with clear success criteria and 4-6 week timeline. Early win creates momentum and generates internal champions. Phase 1: Platform setup and team training (4-6 weeks). Phase 2: Pilot application migration (4-6 weeks). Phase 3: Production rollout (8-12 weeks). Phase 4: Optimization and expansion (ongoing). This phased approach reduces risk, allows learning, and maintains business continuity.'),
    
    ('Security & Compliance First',
     'Address security and compliance requirements from day one, not as afterthought. Engage security and compliance teams early in planning. Document compliance requirements and create mapping to platform capabilities. Implement least-privilege access controls, enable audit logging, and establish security baseline before deploying workloads. For regulated industries, engage auditors early for guidance. Organizations that integrate security from start spend 60% less time on audit preparation and have fewer security incidents.'),
    
    ('Skills Development & Change Management',
     'Technology transition requires skills development. Assess team capabilities and create training plan. Combine instructor-led training with hands-on practice. Establish internal champions who can assist colleagues. Documentation alone is insufficient - people learn by doing. Plan for 20-30 hours of training per engineer over first 3 months. Create safe environment for experimentation in development environments. Consider external consulting for knowledge transfer - brings best practices and accelerates learning curve.'),
    
    ('Metrics & Continuous Improvement',
     'Define success metrics upfront: deployment frequency, lead time for changes, mean time to recovery, infrastructure costs, engineering productivity. Establish baseline before implementation to measure improvement. Implement regular retrospectives to identify optimization opportunities. Track adoption metrics - which teams are using platform, what features drive value. Share success stories internally to drive adoption. Organizations that measure and communicate results see 2x higher adoption rates and better ROI realization.')
])

print("\n✓ Steps 11-15 complete!")
print(f"  Created 5 knowledge base PDFs in {output_dir}/")
