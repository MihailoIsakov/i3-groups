import os
import setuptools

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')

with open(README_PATH, encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name='i3-groups',
    version="0.0.1",
    description='Manage i3wm workspaces and groups',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/MihailoIsakov/i3-groups',
    author='MihailoIsakov',
    author_email='isakov.m@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='i3 i3wm extensions add-ons',
    packages=setuptools.find_packages(exclude=['tests']),
    install_requires=['i3-py ~= 0.6.4', ],
    extras_require={
        'dev': [
            'pytest ~= 7.1',
        ]
    },
    scripts=[
        'scripts/i3-rename-workspace.py',
        'scripts/i3-assign-to-group.py',
        'scripts/i3-next-in-group.py',
        'scripts/i3-move-container-to-workspace.py',
        'scripts/i3-change-group.py',
    ],
)
