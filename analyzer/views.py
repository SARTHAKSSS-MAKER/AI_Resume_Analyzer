from django.http import FileResponse, HttpResponse
import pdfplumber
from django.shortcuts import render
from analyzer.ml_model import predict_role
from analyzer.pdf_generator import generate_report
report_data = {}
all_reports = {}


def home(request):
    return render(request, "analyzer/home.html")


def upload_resume(request):

    results = []

    extracted_text = ""
    predicted_role = ""
    confidence = 0
    confidence_status = ""
    job_role = "Full Stack Developer"
    job_description = ""

    found_skills = []
    missing_skills = []
    score = 0
    ats_status = ""
    suggestions = []
    match_percentage = 0

    if request.method == "POST":
        global all_reports
        all_reports = {}


        job_description = request.POST.get(
            "job_description",
            ""
        )

        resumes = request.FILES.getlist("resume")

        if not resumes:

         return render(
         request,
         "analyzer/upload.html",
         {
            "error": "Please upload at least one resume."
         }
    ) 

        if resumes:

            for resume in resumes:

                extracted_text = ""

                with pdfplumber.open(resume) as pdf:

                    for page in pdf.pages:

                        text = page.extract_text()

                        if text:
                            extracted_text += text + "\n"

                predicted_role, confidence = predict_role(
                    extracted_text
                )

                if confidence >= 80:
                    confidence_status = "High"

                elif confidence >= 50:
                    confidence_status = "Medium"

                else:
                    confidence_status = "Low"

                resume_text = extracted_text.lower().replace(
                    "\n",
                    " "
                )

                skills_db = [
                    "Python",
                    "Java",
                    "HTML",
                    "CSS",
                    "JavaScript",
                    "React",
                    "Node.js",
                    "Django",
                    "Flask",
                    "TensorFlow",
                    "PyTorch",
                    "Machine Learning",
                    "Deep Learning",
                    "Git",
                    "MySQL",
                    "PostgreSQL",
                    "MongoDB"
                ]

                current_found = []
                current_missing = []

                for skill in skills_db:

                    if skill.lower() in resume_text:
                        current_found.append(skill)

                    else:
                        current_missing.append(skill)

                if (len(current_found) + len(current_missing)) > 0:

                    current_score = int(
                        (
                            len(current_found)
                            /
                            (
                                len(current_found)
                                + len(current_missing)
                            )
                        ) * 100
                    )

                else:

                    current_score = 0

                if current_score >= 85:
                    current_ats = "Excellent"

                elif current_score >= 70:
                    current_ats = "Good"

                elif current_score >= 50:
                    current_ats = "Average"

                else:
                    current_ats = "Poor"

                current_suggestions = []

                if "Django" in current_missing:
                    current_suggestions.append(
                        "Learn Django for backend development."
                    )

                if "PostgreSQL" in current_missing:
                    current_suggestions.append(
                        "Add PostgreSQL to improve database skills."
                    )

                if current_score < 70:
                    current_suggestions.append(
                        "Add more technical skills to increase resume strength."
                    )

                jd_words = set(
                    job_description.lower().split()
                )

                resume_words = set(
                    extracted_text.lower().split()
                )

                matched_words = jd_words.intersection(
                    resume_words
                )

                if len(jd_words) > 0:

                    current_match = int(
                        (
                            len(matched_words)
                            /
                            len(jd_words)
                        ) * 100
                    )

                else:

                    current_match = 0

                results.append(
                    {
                        "name": resume.name,
                        "role": predicted_role,
                        "score": current_score,
                        "ats": current_ats,
                        "confidence": confidence,
                        "match": current_match,
                        "found": current_found,
                        "missing": current_missing,
                        "suggestions": current_suggestions,
                        "text": extracted_text
                    }
                )

                all_reports[resume.name] = {
                    "score": current_score,
                    "ats_status": current_ats,
                    "predicted_role": predicted_role,
                    "confidence": confidence,
                    "match_percentage": current_match,
                    "found_skills": current_found,
                    "missing_skills": current_missing,
                    "suggestions": current_suggestions
                }

        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        best = results[0]

        extracted_text = best["text"]
        predicted_role = best["role"]
        score = best["score"]
        ats_status = best["ats"]
        confidence = best["confidence"]
        match_percentage = best["match"]
        found_skills = best["found"]
        missing_skills = best["missing"]
        suggestions = best["suggestions"]

        global report_data

        report_data = {
            "score": score,
            "ats_status": ats_status,
            "predicted_role": predicted_role,
            "confidence": confidence,
            "match_percentage": match_percentage,
            "found_skills": found_skills,
            "missing_skills": missing_skills,
            "suggestions": suggestions
        }

    return render(
        request,
        "analyzer/upload.html",
        {
            "extracted_text": extracted_text,
            "found_skills": found_skills,
            "missing_skills": missing_skills,
            "score": score,
            "ats_status": ats_status,
            "suggestions": suggestions,
            "job_role": job_role,
            "job_description": job_description,
            "match_percentage": match_percentage,
            "predicted_role": predicted_role,
            "confidence": confidence,
            "confidence_status": confidence_status,
            "results": results
        }
    )

def download_report(request):

    global all_reports

    resume_name = request.GET.get("resume")

    if not resume_name:
        return HttpResponse("Resume not specified")

    if resume_name not in all_reports:
        return HttpResponse("Report not found")

    data = all_reports[resume_name]

    filename = f"{resume_name}_report.pdf"

    generate_report(
        filename,
        data["score"],
        data["ats_status"],
        data["predicted_role"],
        data["confidence"],
        data["match_percentage"],
        data["found_skills"],
        data["missing_skills"],
        data["suggestions"]
    )

    return FileResponse(
        open(filename, "rb"),
        as_attachment=True
    )