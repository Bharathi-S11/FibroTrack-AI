# ==============================
# IMPORTS
# ==============================
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import shap

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# ==============================
# LOAD MODEL
# ==============================
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# ==============================
# EXPLANATION FUNCTION (FINAL FIX)
# ==============================
def generate_explanation(pred, shap_values, input_data):

    feature_names = input_data.columns

    # Handle multi-class SHAP correctly
    try:
        values = shap_values.values[0][:, pred]
    except:
        values = shap_values[pred][0]

    importance = sorted(
        zip(feature_names, values),
        key=lambda x: abs(float(x[1])),
        reverse=True
    )[:3]

    explanation = []
    for f, val in importance:
        if val > 0:
            explanation.append(f"{f} is increasing fibrosis risk")
        else:
            explanation.append(f"{f} is reducing fibrosis risk")

    return explanation


# ==============================
# RECOMMENDATION FUNCTION
# ==============================
def get_indian_recommendation(stage, age):

    plan = {}

    # =========================
    # F0–F1 (Healthy / Mild)
    # =========================
    if stage <= 1:

        plan["diet"] = {
            "Breakfast": [
                "Idli with sambar",
                "Vegetable upma",
                "Oats with milk"
            ],
            "Lunch": [
                "2 chapati , dal ,vegetable curry",
                "Brown rice and sambar , salad",
                "Curd (small portion)"
            ],
            "Dinner": [
                "Light khichdi",
                "Vegetable soup , roti"
            ],
            "Snacks": [
                "Fruits (papaya, apple)",
                "Coconut water",
                "Buttermilk"
            ]
        }

        plan["lifestyle"] = [
            "Walk 30–40 minutes daily (morning)",
            "Drink 2.5–3 liters water",
            "Avoid packaged foods",
            "Sleep before 11 PM"
        ]

        plan["reason"] = (
            "Early-stage liver stress can be reversed with balanced diet and hydration."
        )

    # =========================
    # F2 (Moderate)
    # =========================
    elif stage == 2:

        plan["diet"] = {
            "Breakfast": [
                "Steamed idli or poha (low oil)",
                "Boiled sprouts",
                "Herbal tea (no sugar)"
            ],
            "Lunch": [
                "1–2 chapati , dal , leafy vegetables (palak, methi)",
                "Avoid white rice or reduce quantity",
                "Low-fat curd"
            ],
            "Dinner": [
                "Moong dal khichdi",
                "Vegetable soup"
            ],
            "Snacks": [
                "Roasted chana",
                "Fruits (avoid very sweet fruits)",
                "Buttermilk"
            ]
        }

        plan["lifestyle"] = [
            "Strictly avoid alcohol",
            "Daily yoga (pranayama + breathing)",
            "Reduce stress (meditation 10–15 mins)",
            "Avoid late-night eating"
        ]

        plan["reason"] = (
            "Moderate fibrosis requires reducing liver load and controlling inflammation. "
            "Refer to a doctor for medical guidance and Follow the diet plan properly."
        )

    # =========================
    # F3–F4 (Severe)
    # =========================
    else:

        plan["diet"] = {
            "Breakfast": [
                "Soft foods (daliy  oats)",
                "Steamed vegetables"
            ],
            "Lunch": [
                "Very light khichdi",
                "Boiled vegetables",
                "Low salt diet"
            ],
            "Dinner": [
                "Clear vegetable soup",
                "Soft roti (minimal oil)"
            ],
            "Snacks": [
                "Coconut water",
                "Fruit pulp (easy digestion)"
            ]
        }

        plan["lifestyle"] = [
            "Complete alcohol restriction",
            "Frequent medical checkups",
            "Avoid heavy physical activity",
            "Take adequate rest (7–8 hrs sleep)"
        ]

        plan["reason"] = (
            "Severe fibrosis requires minimizing liver workload and preventing further damage. "
            "Refer to a doctor first for urgent specialist care and treatment planning."
        )

    # =========================
    # PERSONALIZATION
    # =========================
    if age > 50:
        plan["lifestyle"].append("Liver function test every 6 months")

    return plan


# ==============================
# PDF GENERATOR
# ==============================

def generate_full_report(
    patient_name, stage, risk, explanation, plan, story,
    age, gender, before_stage=None, after_stage=None, before_risk=None, after_risk=None
):

    file_path = "FibroTrack_Report.pdf"

    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        textColor=colors.darkblue
    )

    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        textColor=colors.HexColor("#2E86C1")
    )

    normal_style = styles['Normal']

    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    content = []

    # =========================
    # HEADER
    # =========================
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1D3557"),
        fontSize=24,
        spaceAfter=6
    )
    
    subheader_style = ParagraphStyle(
        'SubheaderStyle',
        parent=styles['Heading3'],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#457B9D"),
        fontSize=12,
        spaceAfter=12
    )
    
    content.append(Paragraph("FibroTrack AI", header_style))
    content.append(Paragraph("AI-Powered Liver Health Report", subheader_style))
    content.append(Spacer(1, 15))

    # =========================
    # PATIENT INFO TABLE
    # =========================
    data = [
        [
            Paragraph("<b>Patient Name</b>", normal_style),
            Paragraph(str(patient_name), normal_style)
        ],
        [
            Paragraph("<b>Age</b>", normal_style),
            Paragraph(str(age), normal_style)
        ],
        [
            Paragraph("<b>Gender</b>", normal_style),
            Paragraph(gender, normal_style)
        ],
        [
            Paragraph("<b>Predicted Stage</b>", normal_style),
            Paragraph(stage, normal_style)
        ],
        [
            Paragraph("<b>Risk (%)</b>", normal_style),
            Paragraph(f"{risk}%", normal_style)
        ]
    ]

    table = Table(data, colWidths=[150, 250])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E7F0FF")),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F8FBFF")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#1F2937")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#D1D5DB")),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor("#F8FBFF"), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10)
    ]))

    content.append(table)
    content.append(Spacer(1, 18))

    # =========================
    # RISK HIGHLIGHT BOX
    # =========================
    if "F0" in stage:
        risk_color = colors.HexColor("#10B981")
        risk_text = "Low Risk"
    elif "F1" in stage or "F2" in stage:
        risk_color = colors.HexColor("#F59E0B")
        risk_text = "Moderate Risk"
    else:
        risk_color = colors.HexColor("#EF4444")
        risk_text = "High Risk"

    risk_style = ParagraphStyle(
        'RiskStyle',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        textColor=colors.white,
        fontSize=13,
        fontName='Helvetica-Bold'
    )
    
    risk_box = Table([[Paragraph(f"Risk Level: {risk_text}", risk_style)]],
                     colWidths=[350])
    risk_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), risk_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('BORDER', (0,0), (-1,-1), 0)
    ]))

    content.append(risk_box)
    content.append(Spacer(1, 18))

    # =========================
    # EXPLANATION
    # =========================
    content.append(Paragraph("AI Explanation", heading_style))
    for e in explanation:
        content.append(Paragraph(f"• {e}", normal_style))
    content.append(Spacer(1, 12))

    # =========================
    # DAILY STORY
    # =========================
    content.append(Paragraph("Daily Guidance", heading_style))
    content.append(Paragraph(story, normal_style))
    content.append(Spacer(1, 12))

    # =========================
    # DIET PLAN
    # =========================
    content.append(Paragraph("Diet Plan", heading_style))

    for meal, items in plan["diet"].items():
        content.append(Paragraph(f"<b>{meal}</b>", normal_style))
        for i in items:
            content.append(Paragraph(f"- {i}", normal_style))
        content.append(Spacer(1, 6))

    content.append(Spacer(1, 12))

    # =========================
    # AVOID FOODS
    # =========================
    content.append(Paragraph("Foods to Avoid", heading_style))
    for a in plan["avoid"]:
        content.append(Paragraph(f"- {a}", normal_style))

    content.append(Spacer(1, 12))

    # =========================
    # LIFESTYLE
    # =========================
    content.append(Paragraph("Lifestyle Recommendations", heading_style))
    for l in plan["lifestyle"]:
        content.append(Paragraph(f"- {l}", normal_style))

    content.append(Spacer(1, 12))

    # =========================
    # SIMULATION
    # =========================
    if before_stage != after_stage:
        content.append(Paragraph("Diet Impact Simulation", heading_style))
        content.append(Paragraph(
            f"Stage changed from <b>{before_stage}</b> to <b>{after_stage}</b>.<br/>"
            f"Risk reduced from <b>{before_risk}%</b> to <b>{after_risk}%</b>.",
            normal_style
        ))
        content.append(Spacer(1, 12))

    # =========================
    # FOOTER
    # =========================
    content.append(Spacer(1, 20))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor("#6B7280"),
        alignment=TA_CENTER
    )
    content.append(Paragraph(
        "This report is AI-generated and intended for guidance only. "
        "Consult a healthcare professional for medical advice.",
        footer_style
    ))

    doc.build(content)

    return file_path


# ==============================
# UI
# ==============================
st.set_page_config(page_title="FibroTrack AI", layout="wide")

st.title("🧬 FibroTrack AI")
st.subheader("Liver Fibrosis Stage Prediction + Explainable AI")

# Sidebar Inputs
st.sidebar.header("Patient Details")

patient_name = st.sidebar.text_input("Patient Name", "Patient")
age = st.sidebar.slider("Age", 10, 100, 45)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
gender_val = 1 if gender == "Male" else 0

tb = st.sidebar.number_input("Total Bilirubin", 0.1, 10.0, 1.0)
db = st.sidebar.number_input("Direct Bilirubin", 0.1, 5.0, 0.3)
alk = st.sidebar.number_input("Alkaline Phosphatase", 50, 300, 150)
ast = st.sidebar.number_input("AST", 10, 200, 40)
alt = st.sidebar.number_input("ALT", 10, 200, 40)
tp = st.sidebar.number_input("Total Proteins", 2.0, 10.0, 6.5)
alb = st.sidebar.number_input("Albumin", 1.0, 6.0, 3.5)
agr = st.sidebar.number_input("A/G Ratio", 0.1, 3.0, 1.0)

# Input DataFrame
input_data = pd.DataFrame([[
    age, gender_val, tb, db, alk, ast, alt, tp, alb, agr
]], columns=[
    'Age','Gender','Total_Bilirubin','Direct_Bilirubin',
    'Alkaline_Phosphatase','AST','ALT',
    'Total_Proteins','Albumin','A_G_Ratio'
])

# ==============================
# PREDICTION
# ==============================
if st.button("Predict Stage"):

    input_scaled = scaler.transform(input_data)

    pred = model.predict(input_scaled)[0]
    probs = model.predict_proba(input_scaled)[0]
    risk_score = int(np.max(probs) * 100)

    stage_map = {
        0: "F0 - Healthy",
        1: "F1 - Mild",
        2: "F2 - Moderate",
        3: "F3 - Severe",
        4: "F4 - Advanced"
    }

    # Clinical Risk (based on stage)
    if pred == 0:
        clinical_risk = "Low Risk"
    elif pred in [1, 2]:
        clinical_risk = "Moderate Risk"
    else:
        clinical_risk = "High Risk"

    st.warning(f"Clinical Risk Level: {clinical_risk}")

    st.success(f"Predicted Stage: {stage_map[pred]}")

    if pred in [0, 1]:
        st.info("Your liver is in good health. Maintain a balanced diet and regular checkups.")
    elif pred == 2:
        st.info("Moderate fibrosis detected. Follow the recommended diet and lifestyle changes to prevent progression.")    
    else:
        st.info("Severe fibrosis detected. Urgently consult a healthcare professional for further evaluation and treatment.")   
        st.info(f"Risk Percentage: {risk_score}%")

    # ==============================
    # SHAP EXPLANATION
    # ==============================
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(input_scaled)

    explanation = generate_explanation(pred, shap_values, input_data)

    st.subheader("🧠 Explanation")
    for e in explanation:
        st.write("•", e)

    # ==============================
    # RECOMMENDATIONS
    # ==============================
    rec = get_indian_recommendation(pred, age)

    st.subheader("🥗 Indian Diet Plan")

    diet_rows = []

    for meal, items in rec["diet"].items():
        diet_rows.append({
            "Meal Time": meal,
            "Recommended Foods": ", ".join(items)
    })

    diet_df = pd.DataFrame(diet_rows)

    # Styled Table
    styled_table = diet_df.style.set_properties(**{
        'text-align': 'left',
        'padding': '12px',
        'font-size': '15px'
    }).set_table_styles([
    {
        'selector': 'th',
        'props': [
            ('background-color', '#27AE60'),
            ('color', 'white'),
            ('font-size', '16px'),
            ('text-align', 'center'),
            ('padding', '12px')
        ]
    },
    {
        'selector': 'td',
        'props': [
            ('border', '1px solid #D6EAF8')
        ]
    }
    ])

    st.dataframe(
        styled_table,
        use_container_width=True,
        hide_index=True
    )


    st.subheader("🧘 Lifestyle Routine")
    for l in rec["lifestyle"]:
        st.write("•", l)

    st.subheader("🧠 Medical Insight")
    st.info(rec["reason"])

    # ==============================
    # PDF DOWNLOAD
    # ==============================
    story = (
        "Follow a balanced diet, stay hydrated, and maintain regular checkups "
        "for better liver health."
    )
    plan = rec.copy()
    plan["avoid"] = [
        "Processed foods",
        "Sugary drinks",
        "Alcohol",
        "High-sodium snacks"
    ]

    pdf_file = generate_full_report(
        patient_name,
        stage_map[pred],
        risk_score,
        explanation,
        plan,
        story,
        age,
        gender
    )
    with open(pdf_file, "rb") as f:
        st.download_button(
            "📄 Download Patient Report",
            f,
            file_name="FibroTrack_Report.pdf"
        )