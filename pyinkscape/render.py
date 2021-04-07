import logging
import platform
import subprocess
from pathlib import Path

WIN_EXE_POTENTIAL_PATHS = [
    "C:\\Program Files\\Inkscape\\inkscape.exe",
    "C:\\Program Files\\Inkscape\\bin\\inkscape.exe"
]
if platform.system() == "Windows":
    INKSCAPE_PATH = None
    for _potential_path in WIN_EXE_POTENTIAL_PATHS:
        if Path(_potential_path).is_file():
            INKSCAPE_PATH = _potential_path
    if not INKSCAPE_PATH:
        # use any inkscape.exe in PATH as backup solution
        INKSCAPE_PATH = "inkscape.exe"
else:
    INKSCAPE_PATH = "/usr/bin/inkscape"

try:
    from PyPDF2 import PdfFileMerger
    PYPDF2_ENABLED = True
except Exception as e:
    PYPDF2_ENABLED = False


def getLogger():
    return logging.getLogger(__name__)


def _verify_pypdf():
    ''' Verify that it is possible to merge PDF files with current setup (PyPDF2, pdfunite, etc.) '''
    if not PYPDF2_ENABLED:
        if platform.system() == "Windows":
            logging.getLogger(__name__).error("pyInkscape requires PyPDF2 when running on Windows")
            raise e
        else:
            logging.getLogger(__name__).warning("PyPDF2 is not available. PDF files will be merged using `pdfunite`")
            # TODO: Verify that pdfunite is available at runtime
            return False
    else:
        return True


def prepare_output_dir(output_dir='ouput', mkdir=False):
    output_dir = Path(output_dir)
    if mkdir and not output_dir.exists():
        output_dir.mkdir(parents=True)
    return output_dir


def svg_to_pdf(filename, overwrite=False, inkscape_path=INKSCAPE_PATH):
    ''' Convert an SVG file into PDF using Inkscape '''
    _inkscape_path_obj = Path(inkscape_path)
    if not _inkscape_path_obj.is_file():
        getLogger().error(f"Inkscape binary is not available at {inkscape_path}")
    svg_file = Path(filename)
    output_dir = svg_file.parent
    pdf_file = output_dir / (svg_file.stem + ".pdf")
    if not overwrite and pdf_file.exists():
        getLogger().warning(f"WARNING: File {pdf_file} exists. SKIPPED")
    else:
        output = subprocess.run([inkscape_path, f"{svg_file}", f"--export-filename={pdf_file}", "--export-area-drawing"])
        if output.returncode != 0:
            getLogger().warning(f"Abnomal Inkscape exit code: {output.returncode}")


def merge_pdf(output_path, input_paths, **kwargs):
    ''' Merge differnt PDF files into one '''
    if _verify_pypdf():
        merger = PdfFileMerger()
        file_objects = []
        for input_path in input_paths:
            input_file = open(input_path, "rb")
            file_objects.append(input_file)
            merger.append(input_file)
        with open(output_path, "wb") as output_file:
            merger.write(output_file)
        for file_obj in file_objects:
            file_obj.close()
    else:
        # use pdfunite command to merge PDF files
        subprocess.run(["pdfunite"] + input_paths + [output_path])

