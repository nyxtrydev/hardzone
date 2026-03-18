from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import openpyxl
from expenses.models import Expense

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def export_expenses_to_excel(expenses):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Expenses"
    
    headers = ['ID', 'Employee', 'Category', 'Amount', 'Status', 'Date']
    ws.append(headers)
    
    for exp in expenses:
        ws.append([exp.id, exp.employee.username, exp.category.name, exp.amount, exp.status, exp.submitted_at.replace(tzinfo=None)])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=expenses.xlsx'
    wb.save(response)
    return response
