import pip

def install(package):
    pip.main(['install', package])

try:
    import xlwt
except ImportError:
    print('Installing the Excel-Python Package')
    install('xlwt')
