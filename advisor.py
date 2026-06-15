#!/usr/bin/env python3
"""
small-business-loan-readiness-advisor
======================================
An AI-powered tool that helps underserved small business owners understand
their loan readiness, identify which funding programs they likely qualify for,
and receive a personalized action plan to strengthen their application —
before they ever walk into a lender's office.

Inspired by the mission of Pacific Community Ventures (PCV) and their
Radiant Data Hub, which uses ethical AI to expand access to capital for
entrepreneurs who have historically been excluded from traditional lending.

How it works:
    1. The business owner answers 12 questions about their business
    2. The tool scores their readiness across 5 dimensions
    3. Claude analyzes their profile against a database of real loan programs
    4. A full report is generated: score, matched programs, and action plan
    5. The report is saved to loan_readiness_report.txt

This tool does not replace a lender or financial advisor. It gives
entrepreneurs — especially those in underserved communities — the information
they need to walk into any lending conversation prepared and confident.

Usage:
    python3 advisor.py

Author: Sumalee Simmonds
GitHub: https://github.com/maleechanel/loan-readiness-advisor
"""

import anthropic
import datetime

# ─── Setup ────────────────────────────────────────────────────────────────────
client = anthropic.Anthropic()
MODEL  = "claude-sonnet-4-6"

# ─── Loan Program Database ────────────────────────────────────────────────────
# Real loan and capital programs available to small businesses,
# with a focus on CDFIs, mission-driven lenders, and programs specifically
# designed for underserved entrepreneurs in California and nationwide.

LOAN_PROGRAMS = """
=== SMALL BUSINESS LOAN & CAPITAL PROGRAM DATABASE ===

--- PACIFIC COMMUNITY VENTURES (PCV) — CALIFORNIA FOCUS ---

1. PCV Restorative Capital Loans
   Funder: Pacific Community Ventures
   Geography: California (statewide)
   Loan Range: $50,000 – $500,000
   Who qualifies:
     - Small businesses in low-to-moderate income communities
     - Businesses owned by people of color, women, or immigrants
     - Businesses creating or retaining quality jobs ("Good Jobs")
     - At least 1 year in business
     - Minimum annual revenue: $100,000
   Use of funds: Working capital, equipment, expansion, hiring
   Interest rate: Below-market (mission-driven pricing)
   Website: https://www.pacificcommunityventures.org/restorative-capital/
   Notes: PCV prioritizes entrepreneurs overlooked by traditional banks.
          Comes with free pro bono business advising. Best fit for
          mission-aligned businesses creating good jobs.

--- CDFI LOANS — CALIFORNIA ---

2. Accion Opportunity Fund — Small Business Loans
   Funder: Accion Opportunity Fund (CDFI)
   Geography: California and nationwide
   Loan Range: $5,000 – $250,000
   Who qualifies:
     - Minimum 1 year in business
     - Annual revenue: $50,000+
     - Credit score: 575+ (flexible)
     - Businesses in underserved communities prioritized
   Use of funds: Working capital, equipment, inventory, hiring
   Interest rate: 8.49% – 24.99% APR
   Website: https://www.aof.org/loans
   Notes: One of the most accessible CDFIs for entrepreneurs with
          imperfect credit. Strong support for Latino and Black-owned businesses.

3. California Rebuilding Fund
   Funder: State of California / CDFI coalition
   Geography: California only
   Loan Range: $5,000 – $100,000
   Who qualifies:
     - California-based businesses
     - Annual revenue under $2.5 million
     - Located in or serving low-to-moderate income communities
     - At least 1 year in operation
   Use of funds: Recovery, stabilization, growth
   Interest rate: 4% – 6%
   Website: https://carebuildingfund.org
   Notes: Specifically designed for small businesses that were impacted
          by economic disruptions. Very competitive rates.

4. Valley Economic Development Center (VEDC)
   Funder: VEDC (CDFI)
   Geography: Southern California and nationwide
   Loan Range: $10,000 – $500,000
   Who qualifies:
     - Minimum 2 years in business for larger loans
     - Credit score: 600+
     - Businesses owned by women, minorities, or veterans prioritized
   Use of funds: Equipment, real estate, working capital
   Website: https://vedc.org/loans/
   Notes: Strong track record with minority-owned businesses in LA area.

--- SBA LOAN PROGRAMS — NATIONWIDE ---

5. SBA 7(a) Loan Program
   Funder: U.S. Small Business Administration (through partner banks)
   Geography: Nationwide
   Loan Range: Up to $5,000,000
   Who qualifies:
     - For-profit business operating in the US
     - Owner has invested equity in the business
     - Exhausted other financing options
     - Credit score: 640+ preferred (varies by lender)
     - At least 2 years in business preferred (startups considered)
   Use of funds: Working capital, equipment, real estate, refinancing
   Interest rate: Prime + 2.25% to 4.75% (currently ~10-12%)
   Website: https://www.sba.gov/funding-programs/loans/7a-loans
   Notes: Most flexible SBA loan. Longer repayment terms (up to 25 years
          for real estate). Requires collateral for loans over $25,000.

6. SBA Microloan Program
   Funder: U.S. Small Business Administration (through nonprofit intermediaries)
   Geography: Nationwide
   Loan Range: Up to $50,000 (average: $13,000)
   Who qualifies:
     - Startups and early-stage businesses
     - No minimum credit score (but lender has discretion)
     - No minimum revenue requirement
     - Cannot use for real estate or refinancing
   Use of funds: Working capital, inventory, supplies, equipment
   Interest rate: 8% – 13%
   Website: https://www.sba.gov/funding-programs/loans/microloans
   Notes: Best option for very early stage businesses or those with
          limited credit history. Often paired with technical assistance.

7. SBA Community Advantage Loan (CA Pilot)
   Funder: SBA / Mission-driven lenders
   Geography: Nationwide (CDFIs and community lenders only)
   Loan Range: $50,000 – $350,000
   Who qualifies:
     - Businesses in underserved markets
     - Credit score: 620+
     - Businesses owned by veterans, women, or minorities prioritized
   Use of funds: Working capital, equipment, expansion
   Website: https://www.sba.gov/funding-programs/loans/community-advantage-loans
   Notes: Specifically designed to reach entrepreneurs in underserved
          communities. Less paperwork than standard 7(a).

--- GRANTS & EQUITY — NATIONWIDE ---

8. USDA Business & Industry Loan Guarantees
   Funder: U.S. Department of Agriculture
   Geography: Rural areas nationwide
   Loan Range: Up to $25,000,000
   Who qualifies:
     - Business located in a rural area (population under 50,000)
     - For-profit or nonprofit
     - US citizenship or legal residency
   Use of funds: Real estate, equipment, working capital, debt refinancing
   Website: https://www.rd.usda.gov/programs-services/business-programs/business-industry-loan-guarantees
   Notes: Only for rural businesses. Very large loan sizes available.

9. Kiva US — Zero-Interest Crowdfunded Loans
   Funder: Kiva (crowdfunding platform)
   Geography: Nationwide
   Loan Range: Up to $15,000
   Who qualifies:
     - Any small business owner
     - No minimum credit score
     - No minimum revenue
     - Must build a "trustee" network to vouch for you
   Interest rate: 0% (zero interest)
   Website: https://www.kiva.org/borrow
   Notes: Takes 30-60 days to fundraise. Great for businesses that
          cannot qualify elsewhere. Builds credit history.

10. Grameen America — Microloans for Women
    Funder: Grameen America (nonprofit)
    Geography: Major US cities (including Oakland/SF Bay Area)
    Loan Range: $2,000 – $15,000
    Who qualifies:
      - Women only
      - Household income at or below 200% of federal poverty line
      - Must join a borrowing group of 5 women
    Interest rate: 15% – 18%
    Website: https://www.grameenamerica.org
    Notes: Specifically serves low-income women entrepreneurs.
           No credit score required. Group lending model.

--- CALIFORNIA-SPECIFIC GRANTS ---

11. California Office of the Small Business Advocate (CalOSBA) Programs
    Funder: State of California
    Geography: California only
    Amount: Varies by program ($2,500 – $25,000 grants)
    Who qualifies:
      - California-based small businesses
      - Revenue under $5 million
      - Priority for disadvantaged businesses (women, minority, veteran-owned)
    Website: https://calosba.ca.gov/programs/
    Notes: Grants (not loans) — do not need to be repaid. Worth applying
           before taking on debt financing.

12. IBank Small Business Finance Center
    Funder: California Infrastructure and Economic Development Bank
    Geography: California only
    Loan Range: $500 – $1,000,000
    Who qualifies:
      - California businesses unable to obtain conventional bank financing
      - Disaster-affected businesses
      - Credit score: 600+
    Use of funds: Working capital, equipment, expansion
    Website: https://ibank.ca.gov/small-business/
    Notes: State-backed loan guarantees that help businesses access
           financing through traditional banks.
"""

# ─── Readiness Dimensions ─────────────────────────────────────────────────────
# The five areas Claude uses to score the business's loan readiness.
# Based on standard CDFI and SBA underwriting criteria.

READINESS_DIMENSIONS = [
    "Business Stability & Track Record",
    "Revenue & Financial Health",
    "Credit & Debt Profile",
    "Loan Purpose & Use of Funds",
    "Community Impact & Mission Alignment",
]


# ─── Input Collection ─────────────────────────────────────────────────────────

def collect_business_profile() -> dict:
    """
    Collect comprehensive information about the business owner and their
    business through a structured intake form.

    Asks 12 questions covering business basics, financials, credit,
    loan purpose, and community impact — the same dimensions that
    mission-driven lenders like PCV use to evaluate applications.

    Returns:
        dict: Complete business profile ready to pass to Claude for analysis.
    """
    print("\n" + "=" * 62)
    print("  SMALL BUSINESS LOAN READINESS ADVISOR")
    print("  Inspired by Pacific Community Ventures")
    print("=" * 62)
    print("""
  This tool will analyze your business profile and tell you:
    1. Your loan readiness score (out of 100)
    2. Which loan programs you likely qualify for
    3. A personalized action plan to strengthen your application

  Answer each question as honestly as possible.
  There are no wrong answers — this is a tool to help you,
  not to judge you.
""")
    print("-" * 62)
    print("  SECTION 1: Your Business")
    print("-" * 62)

    business_name  = input("\n  Business name: ").strip()
    industry       = input("  Industry / type of business: ").strip()
    location       = input("  City and state: ").strip()
    years_operating = input("  How many years have you been in business?: ").strip()
    num_employees  = input("  How many employees do you have (including yourself)?: ").strip()
    legal_structure = input("  Business legal structure (LLC, sole proprietor, S-Corp, etc.): ").strip()

    print("\n" + "-" * 62)
    print("  SECTION 2: Finances")
    print("-" * 62)

    annual_revenue  = input("\n  Approximate annual revenue (last 12 months): $").strip()
    monthly_revenue = input("  Approximate average monthly revenue: $").strip()
    profitable      = input("  Is your business currently profitable? (yes / no / breaking even): ").strip()
    existing_debt   = input("  Do you have any existing business loans or debt? (yes / no): ").strip()

    print("\n" + "-" * 62)
    print("  SECTION 3: Credit & Loan Purpose")
    print("-" * 62)

    credit_score = input("""
  Approximate personal credit score:
    1 = Below 550 (limited/damaged credit)
    2 = 550-619 (fair)
    3 = 620-679 (good)
    4 = 680-739 (very good)
    5 = 740+ (excellent)
  Enter 1-5: """).strip()

    loan_amount  = input("\n  How much funding are you seeking? $").strip()
    loan_purpose = input("  What would you use the loan for? (be specific): ").strip()

    print("\n" + "-" * 62)
    print("  SECTION 4: About You & Your Community")
    print("-" * 62)

    owner_background = input("""
  Which of the following describes you? (select all that apply,
  separated by commas):
    - Woman-owned
    - Minority/POC-owned
    - Immigrant-owned
    - Veteran-owned
    - Low-income community
    - None of the above
  Your answer: """).strip()

    community_impact = input("""
  How does your business benefit your community?
  (e.g. jobs created, services provided, neighborhoods served): """).strip()

    return {
        "business_name":    business_name,
        "industry":         industry,
        "location":         location,
        "years_operating":  years_operating,
        "num_employees":    num_employees,
        "legal_structure":  legal_structure,
        "annual_revenue":   annual_revenue,
        "monthly_revenue":  monthly_revenue,
        "profitable":       profitable,
        "existing_debt":    existing_debt,
        "credit_score":     credit_score,
        "loan_amount":      loan_amount,
        "loan_purpose":     loan_purpose,
        "owner_background": owner_background,
        "community_impact": community_impact,
    }


# ─── Analysis ─────────────────────────────────────────────────────────────────

def generate_analysis(profile: dict) -> str:
    """
    Send the business profile to Claude for comprehensive loan readiness
    analysis. Claude acts as an experienced CDFI loan officer evaluating
    the business across five key dimensions.

    Args:
        profile (dict): Complete business profile from collect_business_profile().

    Returns:
        str: Full analysis report as a formatted string, including readiness
             score, matched loan programs, dimension scores, and action plan.
    """
    credit_score_map = {
        "1": "Below 550 (limited or damaged credit)",
        "2": "550-619 (fair credit)",
        "3": "620-679 (good credit)",
        "4": "680-739 (very good credit)",
        "5": "740+ (excellent credit)",
    }
    credit_label = credit_score_map.get(
        profile["credit_score"], profile["credit_score"]
    )

    dimensions_list = "\n".join(
        f"  {i+1}. {d}" for i, d in enumerate(READINESS_DIMENSIONS)
    )

    analysis_prompt = f"""You are a compassionate, experienced CDFI loan officer at Pacific Community 
Ventures — a mission-driven lender that specializes in supporting underserved 
small business owners, particularly women, people of color, and immigrants.

A small business owner has submitted the following profile seeking loan readiness 
guidance. Your job is to give them an honest, specific, encouraging, and actionable 
analysis that empowers them to move forward — not to gatekeep or discourage.

BUSINESS PROFILE:
  Business Name:       {profile['business_name']}
  Industry:            {profile['industry']}
  Location:            {profile['location']}
  Years in Business:   {profile['years_operating']}
  Employees:           {profile['num_employees']}
  Legal Structure:     {profile['legal_structure']}
  Annual Revenue:      ${profile['annual_revenue']}
  Monthly Revenue:     ${profile['monthly_revenue']}
  Profitable:          {profile['profitable']}
  Existing Debt:       {profile['existing_debt']}
  Credit Profile:      {credit_label}
  Loan Amount Sought:  ${profile['loan_amount']}
  Loan Purpose:        {profile['loan_purpose']}
  Owner Background:    {profile['owner_background']}
  Community Impact:    {profile['community_impact']}

LOAN PROGRAM DATABASE:
{LOAN_PROGRAMS}

Please produce a complete Loan Readiness Report with the following sections:

---

1. OVERALL READINESS SCORE (out of 100)
   Give a score and a 2-sentence summary of what it means.

2. DIMENSION SCORES
   Score each of these 5 dimensions from 1-10 with one sentence explanation:
{dimensions_list}

3. TOP LOAN PROGRAM MATCHES
   Identify the top 3-5 loan programs from the database that best fit this 
   business profile. For each one:
     - Program name and funder
     - Why this business likely qualifies
     - One thing to watch out for or prepare
     - Estimated timeline to funding

4. STRENGTHS
   List 3-4 specific strengths of this application that lenders will respond to.
   Be specific — reference actual details from their profile.

5. AREAS TO STRENGTHEN
   List 3-4 specific areas where the application could be improved, with concrete
   steps the owner can take. Be honest but encouraging. Reference specific 
   programs where stronger profile would unlock better options.

6. 90-DAY ACTION PLAN
   Give a realistic 30/60/90-day plan with specific actions the business owner
   can take to improve their readiness and move toward submitting an application.
   Make this concrete and achievable — not generic advice.

7. ENCOURAGEMENT NOTE
   End with a warm, personal note that acknowledges any challenges in their
   profile honestly, affirms their strengths, and reminds them that mission-driven
   lenders like PCV exist specifically to support entrepreneurs like them.

Format the report cleanly with clear section headers. Use plain language —
this report is for the business owner, not a financial expert.
Avoid jargon. Be specific, warm, and actionable throughout."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=3000,
        messages=[{"role": "user", "content": analysis_prompt}],
    )

    return response.content[0].text


# ─── Report Saving ────────────────────────────────────────────────────────────

def save_report(profile: dict, analysis: str) -> str:
    """
    Save the full loan readiness report to a text file with a timestamp.

    Args:
        profile  (dict): The business profile collected from the owner.
        analysis (str):  The Claude-generated analysis report.

    Returns:
        str: The filename the report was saved to.
    """
    timestamp   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename    = f"loan_readiness_report_{timestamp}.txt"
    business    = profile.get("business_name", "your business").replace(" ", "_")

    header = f"""LOAN READINESS REPORT
Generated by: Small Business Loan Readiness Advisor
Powered by: Anthropic Claude AI
Inspired by: Pacific Community Ventures (pacificcommunityventures.org)
Date: {datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")}
Business: {profile.get('business_name', 'N/A')}
Location: {profile.get('location', 'N/A')}

IMPORTANT DISCLAIMER:
This report is an AI-generated starting point for educational purposes only.
It is not a loan approval, denial, or official financial advice. Loan decisions
are made by lenders based on complete applications and additional verification.
Always speak with a CDFI or financial advisor before making funding decisions.

{'=' * 62}

"""

    with open(filename, "w") as f:
        f.write(header)
        f.write(analysis)
        f.write(f"\n\n{'=' * 62}\n")
        f.write("Next steps:\n")
        f.write("  1. Review this report carefully\n")
        f.write("  2. Visit pacificcommunityventures.org to learn about PCV loans\n")
        f.write("  3. Contact a CDFI near you for a free consultation\n")
        f.write("  4. Gather the documents your top-matched programs require\n")
        f.write(f"\n  Report saved: {filename}\n")

    return filename


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    """
    Run the full loan readiness advisor workflow:
        1. Collect business profile through structured intake
        2. Send to Claude for analysis against loan program database
        3. Display the full report
        4. Save report to file for reference
    """
    try:
        # Step 1: Collect business information
        profile = collect_business_profile()

        # Step 2: Generate analysis
        print("\n" + "=" * 62)
        print("  Analyzing your business profile...")
        print("  Matching against loan programs...")
        print("  Generating your personalized report...")
        print("  This may take 20-30 seconds...")
        print("=" * 62)

        analysis = generate_analysis(profile)

        # Step 3: Display report
        print("\n" + "=" * 62)
        print("  YOUR LOAN READINESS REPORT")
        print(f"  {profile.get('business_name', 'Your Business')}")
        print("=" * 62 + "\n")
        print(analysis)

        # Step 4: Save to file
        filename = save_report(profile, analysis)
        print("\n" + "=" * 62)
        print(f"  Report saved to: {filename}")
        print("  Share this with a business advisor or CDFI counselor.")
        print("=" * 62 + "\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n  Session ended. Good luck with your business journey!")


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
