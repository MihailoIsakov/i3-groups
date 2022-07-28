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
    # packages=setuptools.find_packages(exclude=['tests']),
    packages=['i3_groups'],
    install_requires=['i3-py ~= 0.6.4', ],
    extras_require={
        'dev': [
            'pytest ~= 7.1',
        ]
    },
    entry_points={
        'console_scripts': [
            'rename-workspace     = i3_groups.commands:rename_workspace',
            'move-ws-to-group     = i3_groups.commands:move_workspace_to_group',
            'next-ws-in-group     = i3_groups.commands:goto_next_workspace_in_group',
            'move-container-to-ws = i3_groups.commands:move_container_to_workspace',
            'change-active-group  = i3_groups.commands:change_group',
            'make-workspace       = i3_groups.commands:new_workspace',
            'i3-groups-polybar    = i3_groups.commands:polybar',
        ]
    }
)
