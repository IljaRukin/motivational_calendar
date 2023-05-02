from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen import canvas
import calendar
import ghostscript

#background
doc = canvas.Canvas('background.pdf', pagesize=letter)
doc.setFillColorRGB(0.4,0.4,0.4)
#x,y(left/bottom;0/0 -> right/top;615/795)
doc.setFillColorRGB(0.7,0.7,0.7) #choose your font colour
doc.setFont("Helvetica-Bold", 150) #choose your font type and font size
doc.drawString(0,685,"<<<<<")
doc.drawString(100,480,"NO")
doc.drawString(100,330,"DAYS")
doc.drawString(100,180,"OFF")
doc.drawString(170,0,">>>>>")
doc.showPage()
doc.save()

#calendar
doc = SimpleDocTemplate('calendar.pdf', pagesize=letter)

cal = [['','','','','2','0','2','3','','','',''],
       ['Jan','Feb','Mar','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dec']]

for nn in range(1,31+1):
    days = 12*[str(nn)]
    if nn==29:
#        days[2-1]='(29)'
        if input('has february 29 days ? (type True or False):')=='True':
            days[2-1]='29'
        else:
            days[2-1]=''
    if nn>29:
        days[2-1]=''
    if nn==31:
        days[4-1]=''
        days[6-1]=''
        days[9-1]=''
        days[11-1]=''
    cal.append(days)

w, h = 12*[45], len(cal)*[20]
h[0] = 55
h[1] = 30
table = Table(cal, w, h)

table.setStyle(TableStyle([
    ('FONT', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 14.5),
    ('FONT', (0, 0), (-1, 1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 1), 20),
    ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 40),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#    ('TEXTCOLOR', (0, 0), (-1, -1), 'grey'),
#    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
#    ('BOX', (0, 0), (-1, -1), 0.25, colors.green),
    ]))

doc.topMargin = 0

#create the pdf with this
doc.build([table])

# add page 4 from input1, but first add a watermark from another pdf:
import PyPDF2
document = PyPDF2.PdfFileReader(open("calendar.pdf", "rb")).getPage(0)
watermark = PyPDF2.PdfFileReader(open("background.pdf", "rb")).getPage(0)
watermark.mergePage(document)

pdfWriter = PyPDF2.PdfFileWriter()
pdfWriter.addPage(watermark)
resultPdf = open('complete_calendar.pdf', 'wb')
pdfWriter.write(resultPdf)
resultPdf.close()