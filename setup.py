from distutils.core import setup

setup(name='SSXLQC',
      version='0.4.5',
      description='SSXL automatic QC data analysis',
      long_description='SSXL automatic QC data analysis',
      author='William Makinen',
      author_email='wmakinen@opex.com, wmakinen@princeton.edu willtmakinen78@gmail.com',
      url='https://www.opex.com/',
      platforms=['Windows'],
      license='OPEX Internal Use',
      package_dir={'ssxlqc': 'ssxlqc', 'tests': 'tests'},
      packages=['ssxlqc', 'ssxlqc.autogui', 'ssxlqc.chart', 'ssxlqc.sum', 'ssxlqc.unpack', 'tests'],
      package_data={'ssxlqc': ['data/rf/summary/*.csv', 'data/track/summary/*.csv',
                    'data/conveyer/summary/*.csv', 'data/rf/charts/*.png', 'data/track/charts/*.png',
                    'data/conveyer/charts/*.png', 'data/gui/*', 'chart/*.ini', 'requirements.txt']},
      data_files=['SSXLQC.bat', 'SSXLQC_Auto_Backup.cmd'],
     )