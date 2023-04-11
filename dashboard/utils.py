from fpdf import FPDF, HTMLMixin
import base64
import streamlit as st


class MyFPDF(FPDF, HTMLMixin):
    pass


def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a style="padding: 10px; border: 1px solid #fff; text-decoration: none;" href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">🚀 Export Report</a>'


def generate_pdf(html_file):
    pdf = MyFPDF()
    pdf.add_page()
    pdf.set_font('helvetica', size=12)
    html = open(html_file, 'r', encoding='utf-8').read()
    pdf.write_html(html)
    pdf_link = create_download_link(pdf.output(dest="S"), "report")
    return pdf_link
