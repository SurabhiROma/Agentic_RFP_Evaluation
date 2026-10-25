
from pathlib import Path
import pymupdf

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SUPPLIERS = [
    {
        "name": "Apex Systems",
        "filename": "apex_systems.pdf",
        "summary": (
            "Apex proposes a robust enterprise procurement platform "
            "with a strong focus on scalable architecture, secure "
            "integrations and controlled data access."
        ),
        "technical": (
            "Uses modular cloud architecture, documented REST APIs, "
            "role-based access and a scalable integration layer. "
            "Includes architecture diagrams in the final design phase."
        ),
        "timeline": (
            "12 weeks: discovery (2 weeks), design (3 weeks), "
            "configuration and integration (4 weeks), testing "
            "(2 weeks), and deployment (1 week). A project manager, "
            "solution architect and four engineers are proposed."
        ),
        "price": (
            "Implementation: INR 32,00,000. Annual support: "
            "INR 4,00,000. Third-party licenses are excluded. "
            "Travel expenses are billed separately."
        ),
        "security": (
            "Proposes encryption in transit and at rest, role-based "
            "access, audit logging and vulnerability testing. "
            "States that security controls are available, but current "
            "independent certification evidence must be verified."
        ),
        "support": (
            "Provides business-hours support, a proposed four-hour "
            "response for critical incidents and quarterly reviews. "
            "Two comparable enterprise implementations are referenced."
        ),
        "risks": (
            "Higher initial price; certification evidence and final "
            "service-level commitments require confirmation."
        ),
    },
    {
        "name": "BrightPath Tech",
        "filename": "brightpath_tech.pdf",
        "summary": (
            "BrightPath proposes a low-cost procurement solution "
            "with rapid implementation and a small delivery team."
        ),
        "technical": (
            "Offers a standard web application and basic API "
            "connectivity. Scalability limits, integration architecture "
            "and detailed performance testing are not documented."
        ),
        "timeline": (
            "6 weeks: configuration (2 weeks), integration "
            "(2 weeks), testing (1 week), and launch (1 week). "
            "The proposed team has one project lead and two developers. "
            "Staffing backup and contingency plans are not described."
        ),
        "price": (
            "Implementation: INR 12,00,000. Annual support: "
            "INR 2,00,000. Some integrations and future change requests "
            "may incur additional charges. The total cost assumptions "
            "are not fully specified."
        ),
        "security": (
            "Mentions password protection and standard access controls. "
            "Encryption details, audit logging, privacy controls, "
            "certifications and independent security testing are "
            "not evidenced in the proposal."
        ),
        "support": (
            "Offers email support during business hours. No detailed "
            "incident response targets, escalation structure or "
            "comparable enterprise references are supplied."
        ),
        "risks": (
            "Limited compliance evidence, unclear total cost assumptions, "
            "limited staffing and missing support commitments."
        ),
    },
    {
        "name": "NexaWorks",
        "filename": "nexaworks.pdf",
        "summary": (
            "NexaWorks proposes a balanced procurement platform "
            "with structured delivery governance, defined milestones "
            "and a comprehensive post-launch support model."
        ),
        "technical": (
            "Provides modular architecture, documented APIs, "
            "monitoring, integration testing and a staged scalability "
            "assessment. Detailed capacity targets will be agreed "
            "during discovery."
        ),
        "timeline": (
            "10 weeks: discovery (2 weeks), design (2 weeks), "
            "configuration and integration (3 weeks), testing "
            "(2 weeks), and deployment (1 week). The team includes "
            "a project manager, architect, business analyst and "
            "three engineers. Weekly milestone reviews are planned."
        ),
        "price": (
            "Implementation: INR 24,00,000. Annual support: "
            "INR 3,00,000. Training and standard documentation are "
            "included. Third-party license costs are excluded and "
            "listed as a procurement assumption."
        ),
        "security": (
            "Proposes encryption, least-privilege access, audit trails, "
            "vulnerability testing, incident response procedures "
            "and privacy reviews. Certification claims and final "
            "control evidence must be checked during due diligence."
        ),
        "support": (
            "Offers business-hours service desk, incident prioritization, "
            "a documented escalation path, monthly service reviews "
            "and knowledge-transfer sessions. Three comparable "
            "projects are described, with references available on request."
        ),
        "risks": (
            "Capacity targets, certification evidence and final service "
            "levels need agreement before contract signature."
        ),
    },
    {
        "name": "Orbit Digital",
        "filename": "orbit_digital.pdf",
        "summary": (
            "Orbit Digital proposes an enterprise procurement solution "
            "backed by experienced consultants and several customer "
            "references. Integration detail is limited."
        ),
        "technical": (
            "Describes a configurable enterprise platform and "
            "general connectivity options. Specific interface designs, "
            "data migration methods, API specifications and scalability "
            "benchmarks are not supplied."
        ),
        "timeline": (
            "11 weeks are estimated for discovery, configuration, "
            "integration, testing and deployment. Phase-level durations, "
            "staffing commitments, dependencies and contingency "
            "arrangements are not fully detailed."
        ),
        "price": (
            "Implementation: INR 25,00,000. Annual support: "
            "INR 3,50,000. Cloud hosting and third-party licenses "
            "are excluded. Change-request pricing is subject to "
            "commercial negotiation."
        ),
        "security": (
            "Mentions access controls, encrypted connections and "
            "standard enterprise security practices. Certification "
            "documents, audit procedures and detailed privacy controls "
            "are not attached."
        ),
        "support": (
            "Provides a named account manager, business-hours support "
            "and quarterly reviews. Five relevant customer projects "
            "and references are listed. Response and resolution "
            "service levels require confirmation."
        ),
        "risks": (
            "Vague integration approach, incomplete delivery milestones, "
            "missing detailed compliance evidence and unconfirmed "
            "support service levels."
        ),
    },
]

PAGES = [
    [
        ("EXECUTIVE SUMMARY", "summary"),
        ("PROPOSED TECHNICAL SOLUTION", "technical"),
    ],
    [
        ("IMPLEMENTATION PLAN AND TEAM", "timeline"),
        ("COMMERCIAL PROPOSAL", "price"),
    ],
    [
        ("SECURITY AND COMPLIANCE", "security"),
        ("SUPPORT AND EXPERIENCE", "support"),
        ("KEY RISKS AND OPEN ITEMS", "risks"),
    ],
]


def create_supplier_pdf(supplier):
    pdf_path = OUTPUT_DIR / supplier["filename"]

    with pymupdf.open() as document:
        for page_number, sections in enumerate(PAGES, start=1):
            page = document.new_page()
            page.insert_text(
                (50, 45),
                f"CONFIDENTIAL - SYNTHETIC PROPOSAL | "
                f"{supplier['name']}",
                fontsize=10,
            )
            page.insert_text(
                (50, 75),
                f"Page {page_number}",
                fontsize=9,
            )

            y = 115

            for heading, field in sections:
                page.insert_text(
                    (50, y),
                    heading,
                    fontsize=13,
                )
                y += 22

                body = supplier[field]
                rectangle = pymupdf.Rect(50, y, 545, y + 145)

                page.insert_textbox(
                    rectangle,
                    body,
                    fontsize=10,
                    lineheight=1.4,
                )
                y += 175

        document.set_metadata({
            "title": f"{supplier['name']} Supplier Proposal",
            "author": supplier["name"],
            "subject": "Synthetic RFP evaluation training data",
        })
        document.save(str(pdf_path))

    print(f"Created: {pdf_path}")


if __name__ == "__main__":
    for supplier in SUPPLIERS:
        create_supplier_pdf(supplier)

    print("\nAll four synthetic supplier PDFs were created.")
