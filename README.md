# Small Business Loan Readiness Advisor

An AI-powered tool that helps underserved small business owners understand
their loan readiness, discover which funding programs they qualify for,
and get a personalized 90-day action plan — before they ever walk into
a lender's office.

Built in alignment with the mission of Pacific Community Ventures (PCV)
and their Radiant Data Hub. Read the full impact statement: IMPACT.md

---

## The problem

Black and Latino small business owners are denied loans at roughly twice
the rate of white business owners — not because their businesses are less
viable, but because they often lack access to the guidance that helps an
application succeed.

A well-connected entrepreneur gets this information free from their network.
This tool gives it to everyone.

---

## What it produces

After answering 12 questions, the business owner receives a full report:

  1. OVERALL READINESS SCORE (out of 100)
     An honest snapshot of where they stand today.

  2. DIMENSION SCORES
     Scored across 5 areas lenders actually evaluate:
       - Business Stability and Track Record
       - Revenue and Financial Health
       - Credit and Debt Profile
       - Loan Purpose and Use of Funds
       - Community Impact and Mission Alignment

  3. TOP LOAN PROGRAM MATCHES
     3-5 specific programs from a database of 12 real lenders,
     with reasoning, watch-outs, and estimated funding timelines.

  4. STRENGTHS
     What lenders will respond positively to in this profile.

  5. AREAS TO STRENGTHEN
     Honest gaps, with concrete steps to address each one.

  6. 90-DAY ACTION PLAN
     A realistic 30/60/90-day roadmap toward submitting an application.

  7. ENCOURAGEMENT NOTE
     A personal closing note from a mission-driven lending perspective.

The full report is saved to a timestamped text file for reference.

---

## Loan program database covers

  California-focused:
    - PCV Restorative Capital Loans
    - Accion Opportunity Fund
    - California Rebuilding Fund
    - Valley Economic Development Center
    - California Rebuilding Fund
    - IBank Small Business Finance Center
    - CalOSBA Grant Programs

  Nationwide:
    - SBA 7(a) Loan Program
    - SBA Microloan Program
    - SBA Community Advantage Loan
    - Kiva US (zero-interest crowdfunded loans)
    - Grameen America (women entrepreneurs)
    - USDA Business and Industry Guarantees (rural)

---

## Setup

Requirements: Python 3.9 or higher, Anthropic API key

  git clone https://github.com/maleechanel/loan-readiness-advisor.git
  cd loan-readiness-advisor
  pip3 install anthropic
  export ANTHROPIC_API_KEY="sk-ant-your-key-here"
  python3 advisor.py

---

## Sample output (excerpt)

  OVERALL READINESS SCORE: 67 / 100

  You have a solid foundation — your two years of operation,
  consistent revenue, and strong community impact are real
  strengths. Your primary opportunity for improvement is in
  your credit profile and formalizing your financial records.

  TOP LOAN MATCHES:

  1. PCV Restorative Capital Loans (Best fit)
     Why you qualify: Woman-owned, immigrant background, community
     focus, and revenue above $100K threshold. PCV specifically
     prioritizes entrepreneurs with your profile.
     Watch out for: Prepare 2 years of business bank statements.
     Timeline: 6-10 weeks from application to funding.

  2. SBA Microloan Program
     Why you qualify: No minimum credit score. Startup-friendly.
     Amount range matches your request.
     Watch out for: Cannot use for real estate purchases.
     Timeline: 4-8 weeks.

  90-DAY ACTION PLAN:

  Days 1-30:
    - Pull your free credit report at annualcreditredit.gov
    - Dispute any errors with the credit bureaus
    - Open a dedicated business checking account if you haven't

  Days 31-60:
    - Contact PCV at pacificcommunityventures.org for a free consultation
    - Gather 12 months of bank statements and tax returns
    - Register with SAM.gov if pursuing any government-backed loans

  Days 61-90:
    - Submit application to PCV Restorative Capital
    - Apply to SBA Microloan as a parallel track
    - Apply for CalOSBA grant (does not need to be repaid)

---

## Why this matters for ethical AI

Traditional lending algorithms have been shown to perpetuate racial
and gender bias in lending decisions. This tool takes the opposite
approach: it explicitly weights community impact and mission alignment
as strengths, surfaces programs designed for underserved entrepreneurs,
and names bias directly in the IMPACT.md file.

AI should expand access to opportunity, not replicate existing inequality.

---

## Disclaimer

This tool generates AI-assisted reports for educational purposes only.
It is not a loan approval, denial, or official financial advice. Always
verify current program requirements directly with lenders before applying.

---

## License

MIT — free to use, adapt, and share. Especially encouraged for CDFIs,
community organizations, and nonprofits serving small business owners.
