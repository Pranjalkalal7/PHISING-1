"""
PhishGuard - Cybersecurity Awareness Training & Phishing Simulator
Streamlit Application
"""

import json
import os
import random
from datetime import datetime
from pathlib import Path
import streamlit as st

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="PhishGuard - Cybersecurity Awareness Training",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# Custom CSS for Cybersecurity Theme
# ==============================================================================
st.markdown(
    """
    <style>
    /* Main container enhancements */
    .stApp {
        background-color: #101923;
        color: #edf7f6;
    }
    
    /* Top banner */
    .pg-header {
        background: linear-gradient(135deg, #172332 0%, #1e3347 100%);
        border: 1px solid #2d455d;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .pg-title {
        color: #21b6a8;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
    }
    
    .pg-subtitle {
        color: #9cb3c5;
        font-size: 1.05rem;
        margin-top: 6px;
    }
    
    /* Message inspection container */
    .message-container {
        background: #172332;
        border: 1px solid #365164;
        border-radius: 10px;
        padding: 20px;
        margin: 16px 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    }
    
    .message-header-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 14px;
    }
    
    .tag-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .tag-type { background: #223c52; color: #7ad1f5; border: 1px solid #386485; }
    .tag-category { background: #2d3b2a; color: #9ae89c; border: 1px solid #4a6345; }
    .tag-easy { background: #1a382c; color: #52e396; border: 1px solid #2d6b51; }
    .tag-medium { background: #3d351a; color: #e5b94c; border: 1px solid #6b5a26; }
    .tag-hard { background: #3d1d1f; color: #f87171; border: 1px solid #703337; }
    
    .email-meta {
        background: #121c27;
        border-radius: 6px;
        padding: 12px 16px;
        font-family: monospace;
        font-size: 0.92rem;
        color: #c9d8e5;
        margin-bottom: 14px;
        border-left: 3px solid #21b6a8;
    }
    
    .email-body {
        background: #101822;
        border-radius: 6px;
        padding: 18px;
        color: #e5edf4;
        font-size: 1.05rem;
        line-height: 1.6;
        margin-bottom: 16px;
        border: 1px solid #283a4c;
    }
    
    .simulated-link-box {
        background: #1c2b3c;
        border: 1px dashed #3f607d;
        border-radius: 8px;
        padding: 14px;
        margin-top: 10px;
    }
    
    /* Stat cards */
    .metric-card {
        background: #172332;
        border: 1px solid #2a4155;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #21b6a8;
        margin: 4px 0;
    }
    
    .metric-label {
        font-size: 0.88rem;
        color: #8da4b8;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    /* Feedback boxes */
    .feedback-correct {
        background: #122c22;
        border: 1px solid #1f7a55;
        border-radius: 10px;
        padding: 18px;
        margin: 16px 0;
    }
    
    .feedback-incorrect {
        background: #331619;
        border: 1px solid #852b31;
        border-radius: 10px;
        padding: 18px;
        margin: 16px 0;
    }
    
    /* Lesson card */
    .lesson-card {
        background: #172332;
        border: 1px solid #2a4155;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
        height: 100%;
    }
    
    .lesson-title {
        color: #21b6a8;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .safety-banner {
        background: #1f3329;
        border: 1px solid #36664e;
        border-radius: 8px;
        padding: 14px 18px;
        color: #c9eedd;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# Training Lessons Dataset
# ==============================================================================
LESSONS = [
    {
        "title": "Email Phishing",
        "summary": "Deceptive emails designed to make people click, open malicious files, or reveal credentials.",
        "details": "Check the sender address, tone, request, links, and attachments before acting. Attackers often create a false sense of panic or urgency.",
        "signs": [
            "Unexpected requests for sensitive info",
            "Urgent or threatening language",
            "Suspicious or spoofed sender address",
            "Mispelled or look-alike domain",
            "Unusual attachment",
        ],
        "action": "Do not click immediately. Verify through an independent, trusted channel (such as a bookmarked portal or published phone number).",
    },
    {
        "title": "Spear Phishing",
        "summary": "Targeted phishing that uses personal or workplace context to appear highly credible.",
        "details": "These messages feel authentic because attackers research the victim via professional networks, LinkedIn, or company publications.",
        "signs": [
            "Relevant colleague or executive names",
            "Specific workplace project context",
            "Subtle pressure to act quickly",
            "Requests for payment or sensitive internal documents",
        ],
        "action": "Confirm requests through a known phone number, in-person check, or official internal approval workflow.",
    },
    {
        "title": "Smishing (SMS Phishing)",
        "summary": "Phishing attacks delivered through SMS text or mobile messaging apps.",
        "details": "Short mobile messages often hide suspicious links and exploit people on the move when they are less likely to inspect URLs.",
        "signs": [
            "Shortened links (bit.ly, tinyurl, unfamiliar domains)",
            "Fake package delivery fee requests",
            "Urgent bank security alerts",
            "Unusual or spoofed sender ID",
        ],
        "action": "Never click SMS links. Open the official courier or bank app directly from your mobile device.",
    },
    {
        "title": "Vishing (Voice Phishing)",
        "summary": "Voice phishing that manipulates victims over telephone calls.",
        "details": "Attackers impersonate IT support, banking fraud prevention teams, government agencies, or senior leadership.",
        "signs": [
            "Urgent pressure to stay on the line",
            "Requests for one-time passcodes (OTPs)",
            "Threats of legal penalties or account suspension",
            "Caller ID spoofing",
        ],
        "action": "Hang up immediately and contact the organization using an independently verified phone number from your billing statement or card.",
    },
    {
        "title": "Credential Phishing",
        "summary": "Attempts to harvest usernames, passwords, MFA tokens, or recovery questions.",
        "details": "A fake login page may look pixel-perfect but silently sends your credentials directly to an attacker's server.",
        "signs": [
            "Unexpected password reset prompts",
            "Fake login or verification pages",
            "Requests for one-time passwords (OTPs)",
            "Look-alike or typosquatted domains",
        ],
        "action": "Navigate independently to the service using bookmarked URLs and never share MFA/OTP codes with anyone.",
    },
    {
        "title": "Social Engineering",
        "summary": "Psychological manipulation exploiting human trust, fear, curiosity, greed, or helpfulness.",
        "details": "Attackers target human psychology rather than software vulnerabilities.",
        "signs": [
            "Authority impersonation (CEO, IT Director, Law Enforcement)",
            "Emotional bait (fear of penalty, excitement of reward)",
            "Too-good-to-be-true job offers or gifts",
            "Demands for secrecy or skipping standard steps",
        ],
        "action": "Pause, verify the requester's identity through secondary channels, and strictly adhere to established company policies.",
    },
    {
        "title": "Malicious Attachments",
        "summary": "Files containing malware, macros, ransomware, or scripts disguised as invoices or agendas.",
        "details": "Risky files often arrive with pressure, fake invoices, or unexpected administrative notices.",
        "signs": [
            "ZIP / ISO / RAR archive files",
            "Office documents prompting to 'Enable Content/Macros'",
            "Unexpected invoices, shipping slips, or resumes",
            "Instructions to run executable scripts",
        ],
        "action": "Do not download or open unexpected attachments. Submit them to IT security for analysis.",
    },
    {
        "title": "Fake Websites & Typosquatting",
        "summary": "Imitation sites built to mimic trusted portals and harvest user credentials.",
        "details": "The visual page design might be copied, but the browser URL bar reveals the true destination.",
        "signs": [
            "Typosquatting (e.g., paypa1.example, micros0ft.example)",
            "Suspicious top-level domains",
            "Link text differs from destination URL",
            "Missing or invalid SSL certificates",
        ],
        "action": "Carefully inspect the full domain name in the address bar before typing any credentials.",
    },
    {
        "title": "Business Email Compromise (BEC)",
        "summary": "Impersonation of executives, vendors, or internal departments to divert funds or records.",
        "details": "Attackers compromise an email account or register a nearly identical domain to request urgent wire transfers.",
        "signs": [
            "Requests for wire transfer or banking changes",
            "Bypass of standard approval procedures",
            "Urgent executive tone",
            "Requests sent outside normal business hours",
        ],
        "action": "Always verify wire transfer or vendor bank account changes via verbal confirmation using established phone numbers.",
    },
]

# ==============================================================================
# Complete Fallback Scenarios Dataset (Ensures 100% Resilience)
# ==============================================================================
FALLBACK_SCENARIOS = [
    {
        "id": "phishing-bank-001",
        "title": "Urgent Account Security Alert",
        "type": "email",
        "category": "Credential Phishing",
        "difficulty": "easy",
        "sender": "security@examplebank-alert.example",
        "recipient": "learner@example.test",
        "subject": "URGENT: Your account will be suspended today",
        "message": "We detected unusual activity on your ExampleBank account. You must verify your account immediately or access will be suspended within two hours.",
        "linkText": "Verify your account",
        "simulatedUrl": "https://examplebank-security.example/verify",
        "attachment": None,
        "isPhishing": True,
        "indicators": [
            "Urgent language",
            "Look-alike domain",
            "Unexpected verification request",
            "Suspicious link",
            "Threatening language",
        ],
        "explanation": "The message uses pressure and a look-alike domain to push the learner toward a fake verification page.",
        "recommendedAction": "Do not click the link. Open the official banking app or manually type the known website address, then verify the alert through a trusted channel.",
    },
    {
        "id": "phishing-password-002",
        "title": "Password Reset You Did Not Request",
        "type": "email",
        "category": "Credential Phishing",
        "difficulty": "easy",
        "sender": "helpdesk@acme-password.example",
        "recipient": "learner@example.test",
        "subject": "Password reset required before 5 PM",
        "message": "Your Acme Corporation password is out of sync. Confirm your current password and choose a new one to avoid losing mail access.",
        "linkText": "Reset password now",
        "simulatedUrl": "https://acme-login.example/reset",
        "attachment": None,
        "isPhishing": True,
        "indicators": [
            "Requests for passwords",
            "Suspicious sender address",
            "Urgent language",
            "Unexpected account verification",
        ],
        "explanation": "A legitimate help desk should never ask you to confirm your current password through an email link.",
        "recommendedAction": "Use the approved password portal from a bookmarked address or contact IT through the published support channel.",
    },
    {
        "id": "phishing-social-003",
        "title": "Social Account Warning",
        "type": "social media notification",
        "category": "Social Engineering",
        "difficulty": "medium",
        "sender": "alerts@social-hub-review.example",
        "recipient": "learner@example.test",
        "subject": "Your creator page has been reported",
        "message": "Your page will be unpublished unless you appeal the copyright complaint. Submit your login details to verify page ownership.",
        "linkText": "Appeal report",
        "simulatedUrl": "https://socialhub-appeals.example/case",
        "attachment": None,
        "isPhishing": True,
        "indicators": [
            "Authority impersonation",
            "Emotional manipulation",
            "Requests for passwords",
            "Suspicious links",
        ],
        "explanation": "The message exploits fear of losing an account and asks for login details through an unofficial appeal page.",
        "recommendedAction": "Open the social platform directly and review account alerts from inside the official app.",
    },
    {
        "id": "phishing-delivery-004",
        "title": "Missed Delivery Fee",
        "type": "SMS",
        "category": "Smishing",
        "difficulty": "easy",
        "sender": "QuickShip Notice",
        "recipient": "training-phone",
        "subject": "Package held",
        "message": "QuickShip: Your package is held for a 1.99 redelivery fee. Pay now to avoid return to sender.",
        "linkText": "Pay redelivery fee",
        "simulatedUrl": "https://quickship-payments.example/release",
        "attachment": None,
        "isPhishing": True,
        "indicators": [
            "Unusual payment requests",
            "Suspicious link",
            "Urgent language",
            "Unexpected communication channel",
        ],
        "explanation": "Small unexpected fees are commonly used to make victims enter card details quickly.",
        "recommendedAction": "Check tracking from the courier app or official website using the tracking number you already have.",
    },
    {
        "id": "phishing-recruiting-005",
        "title": "Instant Job Offer",
        "type": "job/recruitment message",
        "category": "Social Engineering",
        "difficulty": "medium",
        "sender": "hiring@examplejobs-careers.example",
        "recipient": "learner@example.test",
        "subject": "Remote role approved - send identity documents",
        "message": "Congratulations. You were selected without an interview. Send a copy of your identity card and pay a refundable equipment processing fee.",
        "linkText": "Accept offer",
        "simulatedUrl": "https://examplejobs-onboarding.example/accept",
        "attachment": "Offer_Letter.zip",
        "isPhishing": True,
        "indicators": [
            "Unexpected attachments",
            "Unusual payment requests",
            "Requests for financial information",
            "Emotional manipulation",
        ],
        "explanation": "The offer is too fast, asks for payment, and includes a compressed attachment from an unverified recruiter.",
        "recommendedAction": "Verify the recruiter through the employer's official careers site and never pay to receive a job offer.",
    },
    {
        "id": "phishing-cloud-006",
        "title": "Shared Cloud Document",
        "type": "cloud-storage notification",
        "category": "Fake Websites",
        "difficulty": "medium",
        "sender": "share@securecl0ud.example",
        "recipient": "learner@example.test",
        "subject": "SecureCloud file shared: Payroll_Adjustments",
        "message": "A confidential payroll document has been shared with you. Sign in again to view before the link expires.",
        "linkText": "Open shared file",
        "simulatedUrl": "https://securecl0ud.example/documents",
        "attachment": None,
        "isPhishing": True,
        "indicators": [
            "Typosquatting",
            "Fake login pages",
            "Urgent language",
            "Link text/destination mismatch",
        ],
        "explanation": "The sender uses a zero instead of the letter o and baits the reader with sensitive payroll language.",
        "recommendedAction": "Access cloud files only through the official portal and confirm unexpected shares with the sender.",
    },
    {
        "id": "phishing-it-007",
        "title": "IT Support MFA Bypass",
        "type": "IT support message",
        "category": "Business Email Compromise",
        "difficulty": "hard",
        "sender": "it.support@acme-helpdesk.example",
        "recipient": "learner@example.test",
        "subject": "MFA test - send code to technician",
        "message": "We are testing your account migration. Reply with the one-time code from your authenticator so we can keep your access active.",
        "linkText": "View migration details",
        "simulatedUrl": "https://acme-helpdesk.example/mfa",
        "attachment": None,
        "isPhishing": True,
        "indicators": [
            "Requests for OTPs",
            "Requests to bypass normal security procedures",
            "Authority impersonation",
            "Suspicious sender address",
        ],
        "explanation": "No real support team should ask for one-time codes. That request is a strong account-takeover indicator.",
        "recommendedAction": "Do not share MFA codes. Report the message and contact IT through the official help desk.",
    },
    {
        "id": "phishing-tax-008",
        "title": "Tax Refund Notice",
        "type": "government/tax notification",
        "category": "Email Phishing",
        "difficulty": "medium",
        "sender": "refunds@exampletax-services.example",
        "recipient": "learner@example.test",
        "subject": "Refund approved - banking details needed",
        "message": "ExampleTax Services approved a refund in your name. Submit your bank account and card number within 24 hours to receive payment.",
        "linkText": "Claim refund",
        "simulatedUrl": "https://exampletax-refund.example/claim",
        "attachment": None,
        "isPhishing": True,
        "indicators": [
            "Requests for financial information",
            "Urgent language",
            "Suspicious links",
            "Unexpected account verification",
        ],
        "explanation": "The message asks for sensitive financial details through a link and pressures the reader with a short deadline.",
        "recommendedAction": "Use official tax portals directly and be skeptical of unexpected refund messages.",
    },
    {
        "id": "legit-password-009",
        "title": "Scheduled Password Expiration Reminder",
        "type": "email",
        "category": "Credential Phishing",
        "difficulty": "medium",
        "sender": "identity-notices@acme.example",
        "recipient": "learner@example.test",
        "subject": "Password expires in 10 days",
        "message": "Your Acme Corporation password expires in 10 days. Please use the bookmarked company identity portal or Settings app to update it. IT will never ask for your current password.",
        "linkText": "Open security guidance",
        "simulatedUrl": "https://intranet.acme.example/security-guidance",
        "attachment": None,
        "isPhishing": False,
        "indicators": [
            "Known internal domain",
            "No password request",
            "No urgent threat",
            "Uses established process",
        ],
        "explanation": "The reminder avoids collecting credentials and directs employees to established internal channels.",
        "recommendedAction": "Use the official company portal or app. If uncertain, verify through the internal directory.",
    },
    {
        "id": "legit-delivery-010",
        "title": "Delivery Window Update",
        "type": "SMS",
        "category": "Smishing",
        "difficulty": "medium",
        "sender": "QuickShip",
        "recipient": "training-phone",
        "subject": "Delivery update",
        "message": "QuickShip: Your package QS-20418 is scheduled today between 14:00 and 16:00. Manage delivery from your QuickShip app.",
        "linkText": "Open app instructions",
        "simulatedUrl": "https://quickship.example/help/app",
        "attachment": None,
        "isPhishing": False,
        "indicators": [
            "No fee request",
            "References official app",
            "Specific tracking context",
            "No credential request",
        ],
        "explanation": "The message does not request payment, credentials, or sensitive data and points to the official app path.",
        "recommendedAction": "Use the installed courier app or manually visit the known courier site.",
    },
    {
        "id": "legit-it-011",
        "title": "Internal IT Maintenance",
        "type": "IT support message",
        "category": "Business Email Compromise",
        "difficulty": "easy",
        "sender": "it-notices@acme.example",
        "recipient": "learner@example.test",
        "subject": "VPN maintenance Saturday",
        "message": "VPN access may be unavailable Saturday from 01:00 to 03:00. No action is required. Service status will be posted on the internal status page.",
        "linkText": "View internal status page",
        "simulatedUrl": "https://status.acme.example/vpn",
        "attachment": None,
        "isPhishing": False,
        "indicators": [
            "No action required",
            "Known sender pattern",
            "No sensitive data request",
            "Clear maintenance window",
        ],
        "explanation": "The notice is informational, uses normal IT language, and does not pressure the recipient into unsafe behavior.",
        "recommendedAction": "Review the internal status page if needed and avoid replying with account details.",
    },
    {
        "id": "legit-cloud-012",
        "title": "Project Folder Shared",
        "type": "cloud-storage notification",
        "category": "Fake Websites",
        "difficulty": "hard",
        "sender": "notifications@securecloud.example",
        "recipient": "learner@example.test",
        "subject": "A folder was shared with you",
        "message": "Morgan Lee shared the folder Q3-Roadmap with your work account. Access is restricted to Acme SSO. No password will be requested by email.",
        "linkText": "Open through SecureCloud",
        "simulatedUrl": "https://securecloud.example/shared/q3-roadmap",
        "attachment": None,
        "isPhishing": False,
        "indicators": [
            "Expected collaboration context",
            "Official domain",
            "No credential collection",
            "Mentions SSO",
        ],
        "explanation": "The sender domain is the official fictional service and the message sets safe expectations about SSO.",
        "recommendedAction": "Open SecureCloud from a trusted bookmark or app and confirm with Morgan if the share was unexpected.",
    },
    {
        "id": "legit-job-013",
        "title": "Interview Confirmation",
        "type": "job/recruitment message",
        "category": "Spear Phishing",
        "difficulty": "medium",
        "sender": "recruiting@examplejobs.example",
        "recipient": "learner@example.test",
        "subject": "Interview confirmation for Security Analyst role",
        "message": "Your interview for the Security Analyst role is confirmed for Tuesday at 10:00. The agenda is attached as a PDF. We will not request payment or identity documents by email.",
        "linkText": "View interview portal",
        "simulatedUrl": "https://careers.examplejobs.example/candidate",
        "attachment": "Interview_Agenda.pdf",
        "isPhishing": False,
        "indicators": [
            "Expected process",
            "No payment request",
            "Official careers subdomain",
            "Benign PDF agenda",
        ],
        "explanation": "The message aligns with a normal hiring workflow and clearly avoids unsafe requests.",
        "recommendedAction": "Use the candidate portal from the official careers site and verify attachments if unexpected.",
    },
    {
        "id": "legit-security-014",
        "title": "New Device Notification",
        "type": "email",
        "category": "Credential Phishing",
        "difficulty": "hard",
        "sender": "security@examplebank.example",
        "recipient": "learner@example.test",
        "subject": "New sign-in detected",
        "message": "A new sign-in was detected on your ExampleBank profile. If this was not you, open the ExampleBank app or call the number on your card. We will never ask for your password by email.",
        "linkText": "Learn how to secure your account",
        "simulatedUrl": "https://examplebank.example/security",
        "attachment": None,
        "isPhishing": False,
        "indicators": [
            "Official domain",
            "Independent verification advice",
            "No direct login demand",
            "No sensitive data request",
        ],
        "explanation": "The notification explains the event and gives safer independent verification steps.",
        "recommendedAction": "Use the bank app or a verified phone number, especially if you did not recognize the sign-in.",
    },
    {
        "id": "legit-maintenance-015",
        "title": "Software Maintenance Notice",
        "type": "email",
        "category": "Malicious Attachments",
        "difficulty": "easy",
        "sender": "updates@acme.example",
        "recipient": "learner@example.test",
        "subject": "Time tracking maintenance completed",
        "message": "The scheduled maintenance for TimeTrack is complete. You may need to refresh your browser. No download is required.",
        "linkText": "Read release notes",
        "simulatedUrl": "https://intranet.acme.example/timetrack/release-notes",
        "attachment": None,
        "isPhishing": False,
        "indicators": [
            "No attachment",
            "No download request",
            "Known internal domain",
            "Routine operational notice",
        ],
        "explanation": "This is a routine internal maintenance message and does not ask the user to install software or provide credentials.",
        "recommendedAction": "Refresh the app from the official internal launcher if you need to use it.",
    },
    {
        "id": "legit-newsletter-016",
        "title": "Company Security Newsletter",
        "type": "email",
        "category": "Email Phishing",
        "difficulty": "medium",
        "sender": "security-awareness@acme.example",
        "recipient": "learner@example.test",
        "subject": "Monthly security tips",
        "message": "This month's topic is reporting suspicious messages. Use the report button in mail, verify unusual payment requests by phone, and never share one-time codes.",
        "linkText": "Read on intranet",
        "simulatedUrl": "https://intranet.acme.example/security/newsletter",
        "attachment": None,
        "isPhishing": False,
        "indicators": [
            "Educational content",
            "Known internal domain",
            "No sensitive request",
            "Encourages safe reporting",
        ],
        "explanation": "The newsletter reinforces security practices and does not attempt to collect information.",
        "recommendedAction": "Read the guidance and use the report button for suspicious messages.",
    },
]


@st.cache_data
def load_scenarios():
    """Load scenarios from JSON file or fall back to embedded data."""
    paths_to_try = [
        Path("public/data/scenarios.json"),
        Path("data/scenarios.json"),
        Path(__file__).parent / "public" / "data" / "scenarios.json",
    ]
    for p in paths_to_try:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return FALLBACK_SCENARIOS


SCENARIOS = load_scenarios()

# ==============================================================================
# Helper Functions
# ==============================================================================
def difficulty_points(difficulty: str) -> int:
    return {"hard": 200, "medium": 150, "easy": 100}.get(difficulty.lower(), 100)


def calculate_stats(records):
    total = len(records)
    if total == 0:
        return {
            "total": 0,
            "correct": 0,
            "incorrect": 0,
            "score": 0,
            "phishing": 0,
            "legitimate": 0,
            "accuracy": 0,
            "categories": [],
        }

    correct = sum(1 for r in records if r["correct"])
    incorrect = total - correct
    score = sum(r.get("points", 0) for r in records)
    phishing = sum(1 for r in records if r["answer"] is True)
    legitimate = sum(1 for r in records if r["answer"] is False)
    accuracy = round((correct / total) * 100)
    categories = sorted(list({r["category"] for r in records if "category" in r}))

    return {
        "total": total,
        "correct": correct,
        "incorrect": incorrect,
        "score": score,
        "phishing": phishing,
        "legitimate": legitimate,
        "accuracy": accuracy,
        "categories": categories,
    }


def init_challenge():
    phishing = random.sample([s for s in SCENARIOS if s["isPhishing"]], 5)
    legitimate = random.sample([s for s in SCENARIOS if not s["isPhishing"]], 5)
    combined = phishing + legitimate
    random.shuffle(combined)
    st.session_state.challenge = {
        "ids": [s["id"] for s in combined],
        "index": 0,
        "records": [],
        "finished": False,
    }
    st.session_state.challenge_feedback = None


# ==============================================================================
# Session State Initialization
# ==============================================================================
if "completed" not in st.session_state:
    st.session_state.completed = {}

if "practice_idx" not in st.session_state:
    st.session_state.practice_idx = 0

if "practice_feedback" not in st.session_state:
    st.session_state.practice_feedback = None

if "challenge" not in st.session_state:
    st.session_state.challenge = None

if "challenge_feedback" not in st.session_state:
    st.session_state.challenge_feedback = None

if "challenge_history" not in st.session_state:
    st.session_state.challenge_history = []


# ==============================================================================
# Sidebar Navigation & User Metrics
# ==============================================================================
with st.sidebar:
    st.markdown("### 🛡️ PhishGuard")
    st.caption("Cybersecurity Awareness Training & Simulation")

    menu = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "🎯 Practice Simulation",
            "⚡ 10-Question Challenge",
            "📚 Training Modules",
            "🔐 Simulated Login Test",
            "ℹ️ About & Security",
        ],
        index=0,
    )

    st.markdown("---")
    st.markdown("#### 📈 Your Progress")
    current_stats = calculate_stats(list(st.session_state.completed.values()))

    col_s1, col_s2 = st.columns(2)
    col_s1.metric("Score", f"{current_stats['score']} pts")
    col_s2.metric("Accuracy", f"{current_stats['accuracy']}%")

    solved_ratio = f"{current_stats['total']} / {len(SCENARIOS)}"
    st.caption(f"Scenarios Practiced: **{solved_ratio}**")
    pct_complete = min(100, int((current_stats["total"] / len(SCENARIOS)) * 100))
    st.progress(pct_complete / 100)

    st.markdown("---")
    if st.button("🔄 Reset Progress", use_container_width=True):
        st.session_state.completed = {}
        st.session_state.practice_idx = 0
        st.session_state.practice_feedback = None
        st.session_state.challenge = None
        st.session_state.challenge_feedback = None
        st.rerun()

    st.caption(
        "🔒 *Simulation only. All links & dummy credentials remain inside this training app.*"
    )

# ==============================================================================
# Render Page: Dashboard
# ==============================================================================
if menu == "📊 Dashboard":
    st.markdown(
        """
        <div class="pg-header">
            <h1 class="pg-title">🛡️ Security Awareness Dashboard</h1>
            <p class="pg-subtitle">Real-time training readiness, accuracy metrics, and threat detection proficiency.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    s = calculate_stats(list(st.session_state.completed.values()))

    # Top metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total Score</div>
                <div class="metric-value">{s['score']}</div>
                <small style="color:#7ad1f5">difficulty based</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Accuracy Rate</div>
                <div class="metric-value">{s['accuracy']}%</div>
                <small style="color:#52e396">{s['correct']} correct / {s['total']} total</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        completion_pct = round((s["total"] / len(SCENARIOS)) * 100)
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Coverage</div>
                <div class="metric-value">{completion_pct}%</div>
                <small style="color:#e5b94c">{s['total']} of {len(SCENARIOS)} scenarios</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Detection Ratio</div>
                <div class="metric-value">{s['phishing']}/{s['legitimate']}</div>
                <small style="color:#9cb3c5">phishing / legitimate</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    col_dash1, col_dash2 = st.columns([1, 1])

    with col_dash1:
        st.subheader("🎯 Covered Attack Categories")
        if s["categories"]:
            cats_html = " ".join(
                f"<span class='tag-badge tag-category'>{c}</span>"
                for c in s["categories"]
            )
            st.markdown(
                f"<div style='margin-top:10px;'>{cats_html}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.info(
                "No scenarios completed yet. Launch Practice Simulation or the Challenge to start tracking coverage."
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🚀 Quick Actions")
        qcol1, qcol2 = st.columns(2)
        with qcol1:
            if st.button("🎯 Open Practice Mode", use_container_width=True):
                st.session_state["practice_feedback"] = None
                st.info("Switch to '🎯 Practice Simulation' from the sidebar!")
        with qcol2:
            if st.button("⚡ Start 10-Q Challenge", use_container_width=True):
                init_challenge()
                st.info("Challenge prepared! Select '⚡ 10-Question Challenge' from the sidebar.")

    with col_dash2:
        st.subheader("📋 Recent Performance")
        recent = sorted(
            st.session_state.completed.values(),
            key=lambda x: x.get("timestamp", ""),
            reverse=True,
        )[:6]

        if recent:
            table_data = []
            for r in recent:
                result_badge = "✅ Correct" if r["correct"] else "❌ Review"
                table_data.append(
                    {
                        "Scenario": r["title"],
                        "Result": result_badge,
                        "Category": r.get("category", "General"),
                        "Points": f"+{r.get('points', 0)}",
                    }
                )
            st.table(table_data)
        else:
            st.write("Complete scenarios to see your recent performance history here.")

# ==============================================================================
# Render Page: Practice Simulation
# ==============================================================================
elif menu == "🎯 Practice Simulation":
    st.markdown(
        """
        <div class="pg-header">
            <h1 class="pg-title">🎯 Interactive Phishing Simulation</h1>
            <p class="pg-subtitle">Analyze realistic messages, inspect indicators, and classify each as Phishing or Legitimate.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Scenario navigation bar
    col_nav1, col_nav2 = st.columns([3, 1])
    with col_nav1:
        scenario_titles = [
            f"Scenario {i+1}: {s['title']} ({s['category']})"
            for i, s in enumerate(SCENARIOS)
        ]
        selected_scenario_idx = st.selectbox(
            "Select Scenario to Inspect:",
            range(len(SCENARIOS)),
            format_func=lambda i: scenario_titles[i],
            index=st.session_state.practice_idx % len(SCENARIOS),
        )
        if selected_scenario_idx != st.session_state.practice_idx:
            st.session_state.practice_idx = selected_scenario_idx
            st.session_state.practice_feedback = None

    with col_nav2:
        st.write("")
        st.write("")
        if st.button("Next Scenario ➡️", use_container_width=True):
            st.session_state.practice_idx = (
                st.session_state.practice_idx + 1
            ) % len(SCENARIOS)
            st.session_state.practice_feedback = None
            st.rerun()

    scenario = SCENARIOS[st.session_state.practice_idx]

    # Tag badges
    diff_class = f"tag-{scenario['difficulty'].lower()}"
    st.markdown(
        f"""
        <div class="message-header-row">
            <span class="tag-badge tag-type">{scenario['type']}</span>
            <span class="tag-badge tag-category">{scenario['category']}</span>
            <span class="tag-badge {diff_class}">{scenario['difficulty'].upper()} ({difficulty_points(scenario['difficulty'])} PTS)</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Message container
    st.markdown(
        f"""
        <div class="message-container">
            <div class="email-meta">
                <b>From:</b> {scenario['sender']}<br>
                <b>To:</b> {scenario['recipient']}<br>
                <b>Subject:</b> {scenario['subject']}
            </div>
            <div class="email-body">
                {scenario['message']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Attachment notice if any
    if scenario.get("attachment"):
        st.warning(f"📎 **Attached File:** `{scenario['attachment']}`")

    # Interactive simulated link inspection
    with st.expander(f"🔍 Inspect Destination Link: {scenario['linkText']}"):
        st.markdown(
            f"""
            <div class="simulated-link-box">
                <p><b>Simulated Target URL:</b> <code>{scenario['simulatedUrl']}</code></p>
                <p style="color:#9cb3c5; font-size:0.9rem;">
                    🛡️ <i>This link is contained entirely inside PhishGuard. It is never opened in an external browser.</i>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 🤔 Your Decision:")
    st.write("Does this communication exhibit indicators of a phishing attempt?")

    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        if st.button("🔴 Classify as Phishing", use_container_width=True, type="primary"):
            user_choice = True
            is_correct = user_choice == scenario["isPhishing"]
            pts = difficulty_points(scenario["difficulty"]) if is_correct else 0
            st.session_state.practice_feedback = {
                "correct": is_correct,
                "points": pts,
                "user_choice": "Phishing",
            }
            st.session_state.completed[scenario["id"]] = {
                "id": scenario["id"],
                "title": scenario["title"],
                "answer": user_choice,
                "correct": is_correct,
                "points": pts,
                "category": scenario["category"],
                "indicators": scenario["indicators"],
                "timestamp": datetime.now().isoformat(),
            }
            st.rerun()

    with btn_col2:
        if st.button("🟢 Classify as Legitimate", use_container_width=True):
            user_choice = False
            is_correct = user_choice == scenario["isPhishing"]
            pts = difficulty_points(scenario["difficulty"]) if is_correct else 0
            st.session_state.practice_feedback = {
                "correct": is_correct,
                "points": pts,
                "user_choice": "Legitimate",
            }
            st.session_state.completed[scenario["id"]] = {
                "id": scenario["id"],
                "title": scenario["title"],
                "answer": user_choice,
                "correct": is_correct,
                "points": pts,
                "category": scenario["category"],
                "indicators": scenario["indicators"],
                "timestamp": datetime.now().isoformat(),
            }
            st.rerun()

    # Display Feedback
    fb = st.session_state.practice_feedback
    if fb:
        st.markdown("---")
        if fb["correct"]:
            st.success(f"🎉 **Correct Decision! (+{fb['points']} points)**")
        else:
            st.error(
                "⚠️ **Incorrect Decision.** Review the security indicators below to see what gave this away."
            )

        st.markdown(
            f"**Actual Classification:** `{'🔴 Phishing' if scenario['isPhishing'] else '🟢 Legitimate'}`"
        )
        st.markdown(f"**Explanation:** {scenario['explanation']}")

        st.markdown("**Key Indicators:**")
        for ind in scenario["indicators"]:
            st.markdown(f"- 🚩 {ind}")

        st.markdown(f"**Recommended Safe Action:** {scenario['recommendedAction']}")

        if st.button("Continue to Next Scenario ➡️", key="practice_next"):
            st.session_state.practice_idx = (
                st.session_state.practice_idx + 1
            ) % len(SCENARIOS)
            st.session_state.practice_feedback = None
            st.rerun()

# ==============================================================================
# Render Page: 10-Question Challenge
# ==============================================================================
elif menu == "⚡ 10-Question Challenge":
    st.markdown(
        """
        <div class="pg-header">
            <h1 class="pg-title">⚡ 10-Question Timed Challenge</h1>
            <p class="pg-subtitle">Test your skills across 10 randomized scenarios (5 phishing, 5 legitimate). Aim for 90%+ accuracy!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.challenge is None or st.session_state.challenge.get("finished"):
        st.info("Ready to assess your cybersecurity instincts?")
        if st.button("🚀 Start New 10-Question Challenge", type="primary"):
            init_challenge()
            st.rerun()
    else:
        ch = st.session_state.challenge
        idx = ch["index"]
        total_questions = len(ch["ids"])

        if idx >= total_questions:
            # Challenge finished! Show results screen
            ch["finished"] = True
            records = ch["records"]
            stats = calculate_stats(records)
            st.session_state.challenge_history.append(
                {"at": datetime.now().isoformat(), "stats": stats}
            )

            st.balloons()
            st.markdown("## 🏆 Challenge Complete!")

            # Determine grade
            acc = stats["accuracy"]
            if acc >= 90:
                grade = "🌟 Excellent (Expert Defender)"
                alert_type = st.success
            elif acc >= 75:
                grade = "👍 Good (Proficient Defender)"
                alert_type = st.info
            elif acc >= 50:
                grade = "⚠️ Needs Improvement (Vulnerable)"
                alert_type = st.warning
            else:
                grade = "🚨 High Risk (Urgent Training Recommended)"
                alert_type = st.error

            alert_type(f"**Final Evaluation:** {grade}")

            # Summary metrics
            res1, res2, res3, res4 = st.columns(4)
            res1.metric("Final Score", f"{stats['score']} pts")
            res2.metric("Accuracy", f"{stats['accuracy']}%")
            res3.metric("Correct", f"{stats['correct']} / {total_questions}")
            res4.metric("Mistakes", f"{stats['incorrect']}")

            # Missed categories & indicators analysis
            mistakes = [r for r in records if not r["correct"]]
            if mistakes:
                st.markdown("---")
                st.subheader("🔍 Focus Areas & Diagnostic Review")
                missed_cats = list({r["category"] for r in mistakes})
                missed_inds = list(
                    {
                        ind
                        for r in mistakes
                        for ind in r.get("indicators", [])
                    }
                )[:6]

                st.write(
                    f"**Categories where errors occurred:** {', '.join(missed_cats)}"
                )
                if missed_inds:
                    st.write("**Key indicators you missed:**")
                    for ind in missed_inds:
                        st.markdown(f"- ⚠️ {ind}")

                st.markdown(
                    """
                    **Key Recommendations:**
                    - Always slow down when a message creates urgency or threatens account suspension.
                    - Inspect domains carefully for typosquatting (`paypa1.example`, `acme-security.example`).
                    - Remember that legitimate organizations never ask for one-time passcodes (OTPs) or passwords over email or phone.
                    """
                )
            else:
                st.success("🎯 Flawless score! You identified every threat and legitimate communication correctly.")

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🔄 Retake Challenge", use_container_width=True):
                    init_challenge()
                    st.rerun()
            with col_btn2:
                if st.button("📊 View Overall Dashboard", use_container_width=True):
                    st.session_state.challenge = None
                    st.rerun()

        else:
            # Active question
            scenario_id = ch["ids"][idx]
            scenario = next(s for s in SCENARIOS if s["id"] == scenario_id)

            ch_stats = calculate_stats(ch["records"])
            progress_pct = int((idx / total_questions) * 100)

            st.progress(progress_pct / 100)
            st.caption(
                f"Question **{idx + 1} of {total_questions}** | Current Score: **{ch_stats['score']} pts** | Live Accuracy: **{ch_stats['accuracy']}%**"
            )

            # Tag badges
            diff_class = f"tag-{scenario['difficulty'].lower()}"
            st.markdown(
                f"""
                <div class="message-header-row">
                    <span class="tag-badge tag-type">{scenario['type']}</span>
                    <span class="tag-badge tag-category">{scenario['category']}</span>
                    <span class="tag-badge {diff_class}">{scenario['difficulty'].upper()} ({difficulty_points(scenario['difficulty'])} PTS)</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Message container
            st.markdown(
                f"""
                <div class="message-container">
                    <div class="email-meta">
                        <b>From:</b> {scenario['sender']}<br>
                        <b>To:</b> {scenario['recipient']}<br>
                        <b>Subject:</b> {scenario['subject']}
                    </div>
                    <div class="email-body">
                        {scenario['message']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if scenario.get("attachment"):
                st.warning(f"📎 **Attached File:** `{scenario['attachment']}`")

            with st.expander(f"🔍 Inspect Destination Link: {scenario['linkText']}"):
                st.code(scenario["simulatedUrl"])
                st.caption("Contained within simulation.")

            # Decision
            if st.session_state.challenge_feedback is None:
                st.markdown("### 🤔 Your Decision:")
                b1, b2 = st.columns(2)
                with b1:
                    if st.button(
                        "🔴 Phishing", use_container_width=True, type="primary"
                    ):
                        is_correct = scenario["isPhishing"] is True
                        pts = (
                            difficulty_points(scenario["difficulty"])
                            if is_correct
                            else 0
                        )
                        record = {
                            "id": scenario["id"],
                            "title": scenario["title"],
                            "answer": True,
                            "correct": is_correct,
                            "points": pts,
                            "category": scenario["category"],
                            "indicators": scenario["indicators"],
                        }
                        ch["records"].append(record)
                        st.session_state.completed[scenario["id"]] = record
                        st.session_state.challenge_feedback = record
                        st.rerun()
                with b2:
                    if st.button("🟢 Legitimate", use_container_width=True):
                        is_correct = scenario["isPhishing"] is False
                        pts = (
                            difficulty_points(scenario["difficulty"])
                            if is_correct
                            else 0
                        )
                        record = {
                            "id": scenario["id"],
                            "title": scenario["title"],
                            "answer": False,
                            "correct": is_correct,
                            "points": pts,
                            "category": scenario["category"],
                            "indicators": scenario["indicators"],
                        }
                        ch["records"].append(record)
                        st.session_state.completed[scenario["id"]] = record
                        st.session_state.challenge_feedback = record
                        st.rerun()
            else:
                cfb = st.session_state.challenge_feedback
                if cfb["correct"]:
                    st.success(f"✅ **Correct! (+{cfb['points']} pts)**")
                else:
                    st.error("❌ **Incorrect.**")

                st.markdown(f"**Explanation:** {scenario['explanation']}")
                st.markdown("**Key Indicators:**")
                for ind in scenario["indicators"]:
                    st.markdown(f"- 🚩 {ind}")

                if st.button("Continue Challenge ➡️", type="primary", use_container_width=True):
                    ch["index"] += 1
                    st.session_state.challenge_feedback = None
                    st.rerun()

# ==============================================================================
# Render Page: Training Modules
# ==============================================================================
elif menu == "📚 Training Modules":
    st.markdown(
        """
        <div class="pg-header">
            <h1 class="pg-title">📚 Core Phishing & Social Engineering Modules</h1>
            <p class="pg-subtitle">Study the 9 fundamental social engineering and phishing methodologies to recognize attacks instantly.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    search_query = st.text_input("🔍 Search Techniques or Indicators", "")

    filtered_lessons = [
        l
        for l in LESSONS
        if search_query.lower() in l["title"].lower()
        or search_query.lower() in l["summary"].lower()
        or any(search_query.lower() in sign.lower() for sign in l["signs"])
    ]

    for lesson in filtered_lessons:
        with st.expander(f"📖 {lesson['title']}", expanded=True):
            st.markdown(f"**Overview:** {lesson['summary']}")
            st.markdown(f"**How it works:** {lesson['details']}")

            col_l1, col_l2 = st.columns(2)
            with col_l1:
                st.markdown("#### 🚩 Common Red Flags")
                for sign in lesson["signs"]:
                    st.markdown(f"- {sign}")
            with col_l2:
                st.markdown("#### 🛡️ Recommended Safe Response")
                st.info(lesson["action"])

# ==============================================================================
# Render Page: Simulated Login Test
# ==============================================================================
elif menu == "🔐 Simulated Login Test":
    st.markdown(
        """
        <div class="pg-header">
            <h1 class="pg-title">🔐 Simulated Credential Interceptor</h1>
            <p class="pg-subtitle">Experience how credential-harvesting pages trick users and how to defend against them.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="safety-banner">
            🛡️ <b>SAFETY NOTICE:</b> This is an interactive educational sandbox. Dummy credentials entered here are strictly intercepted in memory and never logged, stored, or transmitted anywhere.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_sim1, col_sim2 = st.columns([1, 1])

    with col_sim1:
        st.subheader("Simulated Corporate SSO Portal")
        st.caption("URL: https://identity-sso.acme-login.example/auth (Look-alike)")

        with st.form("safe_sim_login"):
            username = st.text_input("Username or Corporate Email", "training-user")
            password = st.text_input("Password", type="password", value="password123")
            submitted = st.form_submit_button("Sign In to Portal")

            if submitted:
                st.error(
                    """
                    🛑 **SIMULATION WARNING - CREDENTIAL EXPOSURE PREVENTED!**
                    
                    In a real attack, typing your password into an unverified page allows cybercriminals to take over your account, bypass standard protections, and pivot into corporate systems.
                    
                    **What you should do instead:**
                    1. Check the browser address bar for the exact domain name (watch out for `acme-login.example` instead of `acme.example`).
                    2. Never access sensitive login pages through unverified email or SMS links.
                    3. Use an authorized password manager; password managers refuse to autofill on look-alike domains!
                    """
                )

    with col_sim2:
        st.subheader("💡 How Credential Harvesting Works")
        st.markdown(
            """
            1. **The Bait:** Attackers send an urgent alert claiming your account has been locked or that a payroll document requires re-authentication.
            2. **The Look-Alike:** The link directs you to an exact visual clone of your organization's login portal hosted on a domain they control.
            3. **The Harvest:** When you enter credentials, the attacker logs them in real time and may immediately request your MFA token.
            4. **The Defense:**
               - **Bookmark Official Portals:** Never click email links to reach login pages.
               - **Hardware Security Keys (FIDO2 / WebAuthn):** Cryptographically bound to the real domain, immune to phishing proxies!
            """
        )

# ==============================================================================
# Render Page: About & Ethics
# ==============================================================================
elif menu == "ℹ️ About & Security":
    st.markdown(
        """
        <div class="pg-header">
            <h1 class="pg-title">ℹ️ About PhishGuard</h1>
            <p class="pg-subtitle">Safe, ethical, and defensive cybersecurity awareness training platform.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        ### Educational Purpose & Ethics
        PhishGuard is built strictly for **defensive cybersecurity training** and educational awareness.
        
        #### Core Safety Guardrails:
        - **No Real Phishing:** PhishGuard does not send unsolicited emails, SMS messages, or voice calls.
        - **Contained Links:** All scenario links point to fictional `.example` (RFC 2606) domains and are contained within this application.
        - **No Data Harvesting:** Form fields intercept submissions purely for demonstration and never store or transmit sensitive data.
        - **Transparent Learning:** Every scenario provides immediate, actionable feedback with indicators, safe actions, and explanations.
        
        ---
        ### Deploying to Streamlit Community Cloud
        1. Push this repository to **GitHub**.
        2. Visit [share.streamlit.io](https://share.streamlit.io).
        3. Connect your repository and set the main file path to `streamlit_app.py`.
        4. Streamlit will install the dependencies in `requirements.txt` and launch your live application!
        """
    )

