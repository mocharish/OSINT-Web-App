import os
import xlsxwriter
from datetime import datetime

def export_scan_to_excel(domain: str, scan_data: dict) -> str:
    export_dir = os.path.join(os.getcwd(), "exports")
    os.makedirs(export_dir, exist_ok=True)

    filename = os.path.join(export_dir, f"{domain}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.xlsx")

    workbook = xlsxwriter.Workbook(filename)
    summary_sheet = workbook.add_worksheet("Summary")
    tools_sheet = workbook.add_worksheet("Tools")
    artifacts_sheet = workbook.add_worksheet("Artifacts")

    # Summary
    summary_sheet.write("A1", "Domain")
    summary_sheet.write("B1", domain)
    summary_sheet.write("A2", "Start Time")
    summary_sheet.write("B2", scan_data.get("start"))
    summary_sheet.write("A3", "End Time")
    summary_sheet.write("B3", scan_data.get("end"))

    summary_sheet.write("A5", "Artifact Type")
    summary_sheet.write("B5", "Count")
    for i, (key, value) in enumerate(scan_data.get("summary", {}).items(), start=6):
        summary_sheet.write(f"A{i}", key)
        summary_sheet.write(f"B{i}", value)

    # Tools
    tools_sheet.write("A1", "Tool")
    tools_sheet.write("B1", "Output (truncated)")
    for i, (tool_name, result) in enumerate(scan_data.get("tools", {}).items(), start=2):
        tools_sheet.write(f"A{i}", tool_name)
        tools_sheet.write(f"B{i}", str(result)[:3000])  # Truncate if large

    # Artifacts
    row = 0
    for artifact_type, items in scan_data.get("artifacts", {}).items():
        artifacts_sheet.write(row, 0, artifact_type)
        for i, item in enumerate(items):
            artifacts_sheet.write(row, i + 1, item)
        row += 1

    workbook.close()
    return filename
