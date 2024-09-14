import os
import cairosvg

def svg2pdf(svg_file):
    pdf_file = os.path.basename(svg_file).replace('.svg','.pdf')
    cairosvg.svg2pdf(url=svg_file,write_to=pdf_file)

# 当前文件所在文件夹下的所有svg文件转换为pdf文件

current_dir = os.path.dirname(os.path.abspath(__file__))

for file in os.listdir(current_dir):
    if file.endswith('.svg'):
        svg_file = os.path.join(current_dir, file)
        svg2pdf(svg_file)
