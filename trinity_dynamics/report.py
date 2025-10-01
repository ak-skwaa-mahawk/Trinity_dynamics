"""
Trinity Dynamics Simulation Framework
Author: John Carroll Jr. (Two Mile Solutions LLC, Alaska)
Date: 2025-10-01
License: CC BY 4.0
Signature: κ/π ≈ 1.01 stabilization principle
Description: PDF reporting module with ReportLab, handling graceful degradation.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_report(metrics, results_df, out_pdf_path, png_path=None):
    """
    Generates a PDF report with metrics, sensitivity results, and visualization.
    Args:
        metrics (dict): Baseline metrics
        results_df (pd.DataFrame): Sensitivity results
        out_pdf_path (str): Output PDF path
        png_path (str, optional): Path to visualization PNG
    """
    try:
        os.makedirs(os.path.dirname(out_pdf_path), exist_ok=True)
        doc = SimpleDocTemplate(out_pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Trinity Dynamics — κ/π Principle Report", styles["Title"]))
        elements.append(Paragraph("Author: John Carroll Jr. (Two Mile Solutions LLC, Alaska)", styles["Normal"]))
        elements.append(Paragraph("License: CC BY 4.0 | Signature: κ/π ≈ 1.01", styles["Normal"]))
        elements.append(Spacer(1, 12))

        if metrics:
            elements.append(Paragraph("Baseline Metrics", styles["Heading2"]))
            table_data = [["Metric", "Value"]]
            for k in ["conv_time", "entropy", "osc_freq", "stability", "energy"]:
                v = metrics.get(k, "N/A")
                table_data.append([k, f"{v:.6g}" if isinstance(v, (int, float)) else str(v)])
            elements.append(Table(table_data, colWidths=[100, 100], style=[('GRID', (0, 0), (-1, -1), 0.5, colors.black)]))
            elements.append(Spacer(1, 12))

        if png_path and os.path.exists(png_path):
            try:
                elements.append(Paragraph("Visualization", styles["Heading2"]))
                elements.append(Image(png_path, width=480, height=360))
                elements.append(Spacer(1, 12))
            except Exception as e:
                print(f"Image load failed: {e}")

        if results_df is not None:
            elements.append(Paragraph("Sensitivity Summary (first 10 rows)", styles["Heading2"]))
            try:
                head = results_df.head(10)
                table_data = [list(head.columns)] + head.astype(str).values.tolist()
                elements.append(Table(table_data, colWidths=[40] * len(head.columns),
                                    style=[('GRID', (0, 0), (-1, -1), 0.5, colors.black)]))
            except Exception as e:
                elements.append(Paragraph(f"Table render failed: {e}", styles["Normal"]))

        try:
            doc.build(elements)
            print(f"PDF report saved: {out_pdf_path}")
        except Exception as e:
            print(f"PDF build failed: {e}")