from reportlab.pdfgen import canvas


def generate_report(
    filename,
    score,
    ats_status,
    predicted_role,
    confidence,
    match_percentage,
    found_skills,
    missing_skills,
    suggestions
):

    pdf = canvas.Canvas(filename)

    y = 800

    pdf.drawString(50, y, "AI Resume Analyzer Report")
    y -= 40

    pdf.drawString(50, y, f"Resume Score: {score}/100")
    y -= 20

    pdf.drawString(50, y, f"ATS Status: {ats_status}")
    y -= 20

    pdf.drawString(50, y, f"Predicted Role: {predicted_role}")
    y -= 20

    pdf.drawString(50, y, f"Confidence: {confidence}%")
    y -= 20

    pdf.drawString(50, y, f"Resume Match: {match_percentage}%")
    y -= 40

    pdf.drawString(50, y, "Skills Found:")
    y -= 20

    for skill in found_skills:
        pdf.drawString(70, y, f"✓ {skill}")
        y -= 20

    y -= 20

    pdf.drawString(50, y, "Missing Skills:")
    y -= 20

    for skill in missing_skills:
        pdf.drawString(70, y, f"✗ {skill}")
        y -= 20

    y -= 20

    pdf.drawString(50, y, "Suggestions:")
    y -= 20

    for suggestion in suggestions:
        pdf.drawString(70, y, suggestion)
        y -= 20

    pdf.save()