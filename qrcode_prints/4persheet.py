#tring to print QE codes.
# use pip install qrcode
#using qrcode version 5.1
#also
#pip install svglib
#pip install svgwrite
#pip install svgutils

import qrcode
import qrcode.image.svg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import svgwrite

#http://stackoverflow.com/questions/23139709/svgwrite-how-to-enable-write-add-other-objects-as-layers-of-an-existing-svg-f
import svgutils.transform as st



test_input = """http://ideamache.ecologylab.net/e/Rli2dBm5Rp/
http://ideamache.ecologylab.net/e/BMvsYlXWvE/
http://ideamache.ecologylab.net/e/ZQYprJJKub/
http://ideamache.ecologylab.net/e/DBqyDso0W5/
http://ideamache.ecologylab.net/e/RHrpJBt1kA/""".split()





def saveQrCodeSVG(filename,text, ptext):
    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(text, image_factory=factory,box_size=30, border=4)
    svf = open(filename,"w")
    img.save(svf,"SVG")
    svf.close()
    
    text_svg_fname = filename+".text.svg"
    merged_svg_name = filename+'.merged.svg'
    svg_document = svgwrite.Drawing(filename = text_svg_fname,
                                    size = ("41mm", "41mm"))
    
#    svg_document.add(svg_document.rect(insert = (0, 0),
#                                       size = ("41mm", "41mm"),
#                                       stroke_width = "1",
#                                       stroke = "black",
#                                       fill = "rgb(240,240,240)"))
    
    svg_document.add(svg_document.text(ptext,
                                       insert = (106, 10),
                                       fill = "rgb(0,0,0)",
                                       style = "font-size:1mm; font-family:Arial"))
    svg_document.add(svg_document.text(text,
                                       insert = (7.5, 117),
                                       fill = "rgb(0,0,0)",
                                       style = "font-size:1.8mm; font-family:Arial"))
    svg_document.save()

#    dwg.add(dwg.text('Test', insert=(0, 0.2), fill='red'))

#    ##PDF
#    drawing = svg2rlg(filename)
#    renderPDF.drawToFile(drawing, filename+".pdf")
    
    template = st.fromfile(text_svg_fname)
    second_svg = st.fromfile(filename)
    template.append(second_svg)
    template.save(merged_svg_name)
    drawing = svg2rlg(merged_svg_name)
    renderPDF.drawToFile(drawing, filename+".pdf")

i = 0
for line in test_input:
    print line.split("/")[-2]
    fname = "out/"+str(i)+".svg"
    saveQrCodeSVG(fname,line,'{0:03d}'.format(i))
    i += 1

#saveQrCodeSVG("out/test.svg","test")

print "done"