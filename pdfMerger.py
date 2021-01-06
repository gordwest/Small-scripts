import os
from PyPDF2 import PdfFileMerger

def mergePDFs(source_dir, output):
    """
    Combines all PDFs in a given directory in their current order

    Params
        source_dir: string - path to directory with PDFs
        output: string - filename and path for merged output
    """
        
    merger = PdfFileMerger()

    for filename in os.listdir(source_dir):
        
        merger.append(source_dir + filename)
    
    merger.write(output)
    merger.close()

mergePDFs('c:/users/gordi/Desktop/Hoffer_mdm13h_PDFs/', 'c:/users/gordi/Desktop/Hoffer_mdm13h_PDFs/combined.pdf')