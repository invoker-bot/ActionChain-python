from actionchain import __version__
from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='actionchain',
    version=f'{__version__}.0.dev1', # dev[n] .alpha[n] .beta[n] .rc[n] .post[n] .final
    author='Invoker Bot',
    author_email='invoker-bot@outlook.com',
    description='A robust Python library for sequentially executing tasks with a probabilistic failure rate, featuring strategic retries and error handling.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/invoker-bot/ActionChain-python',
    packages=find_packages(),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: The Unlicense (Unlicense)',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    install_requires=[

    ],
    tests_require=[
        'pytest',
        'flake8',
    ],
    license='MIT',
    # entry_points={}
)