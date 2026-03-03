from fpdf import FPDF
import re

def clean_text(text):
    # remove CGPA if present
    text = re.sub(r"cgpa[:\s]*[\d.]+", "", text, flags=re.IGNORECASE)
    return text.encode("latin-1", "ignore").decode("latin-1")


class ResumePDF(FPDF):
    def header(self):
        self.ln(6)


def generate_pdf(text, title):
    pdf = ResumePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=18)

    text = clean_text(text)
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # ================= HEADER =================
    # Name
    pdf.set_font("Arial", "B", 19)
    pdf.cell(0, 10, lines[0], ln=True, align="C")

    # Contact
    pdf.set_font("Arial", size=10.5)
    pdf.cell(0, 6, lines[1], ln=True, align="C")

    pdf.ln(10)

    # ================= BODY =================
    pdf.set_font("Arial", size=11)

    for line in lines[2:]:
        # SECTION HEADINGS
        if line.isupper() and len(line) <= 40:
            pdf.ln(6)
            pdf.set_font("Arial", "B", 12.5)
            pdf.cell(0, 7, line, ln=True)
            pdf.ln(2)
            pdf.set_draw_color(120, 120, 120)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            pdf.set_font("Arial", size=11)

        # BULLETS
        elif line.startswith("•") or line.startswith("-"):
            pdf.set_x(15)
            pdf.multi_cell(0, 6, f"• {line.lstrip('•- ').strip()}")
            pdf.ln(1)

        # NORMAL TEXT
        else:
            pdf.multi_cell(0, 6, line)
            pdf.ln(1)

    file_name = f"{title}.pdf"
    pdf.output(file_name)
    return file_name