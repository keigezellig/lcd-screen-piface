from distutils.core import setup

setup(
    name='lcd-screen-piface',
    version='1.0.0',
    packages=['pager', 'simple_pager'],
    install_requires=['blinker',
    'git+https://github.com/piface/pifacecad/#egg=pifacecad'
    'git+https://github.com/piface/pifacecommon/#egg=pifacecommon'
    'python-lirc==1.2.1']

    url='https://github.com/keigezellig/lcd-screen-piface',
    license='THE APPRECIATION LICENSE',
    author='M. Joosten',
    author_email='',
    description='Some modules to create screens more easily for a Piface CAD 2'
)
