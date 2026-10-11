"""Print how many pages each sheet prints to (headless Chrome print-to-PDF).

    python3 tools/pagecount.py grade-8/sheets/b28-latin-squares.html [...]

Sheets should print on 3 pages (answers on their own page); 4 is acceptable
when a figure needs the room. Needs Chrome/Chromium; set CHROME=/path if it is
not found automatically.
"""
import os, re, shutil, subprocess, sys, tempfile

CANDIDATES = [os.environ.get('CHROME', ''),
              '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
              shutil.which('google-chrome') or '', shutil.which('google-chrome-stable') or '',
              shutil.which('chromium') or '', shutil.which('chromium-browser') or '']
CHROME = next((c for c in CANDIDATES if c and os.path.exists(c)), None)


def pages(pdf):
    data = open(pdf, 'rb').read()
    return len(re.findall(rb'/Type\s*/Page[^s]', data))


def main():
    if not CHROME:
        sys.exit('Chrome not found; set CHROME=/path/to/chrome')
    tmp = tempfile.mkdtemp()
    for f in sys.argv[1:]:
        pdf = os.path.join(tmp, os.path.basename(f) + '.pdf')
        try:
            subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-sandbox', '--no-pdf-header-footer',
                            '--virtual-time-budget=12000', '--print-to-pdf=' + pdf,
                            '--user-data-dir=' + os.path.join(tmp, 'profile'), 'file://' + os.path.abspath(f)],
                           capture_output=True, timeout=90)
            n = pages(pdf)
        except subprocess.TimeoutExpired:
            n = 'TIMEOUT'
        print(n, f, flush=True)


if __name__ == '__main__':
    main()
