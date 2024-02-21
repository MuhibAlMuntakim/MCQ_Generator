from setuptools import find_packages,setup

setup(
    name='MCQ_Generator',
    version='0.0.1',
    author='Muhib Al Muntakim',
    author_email='muhibmugdha@gmail.com',
    install_requires=["google.generativeai","langchain","streamlit","python-dotenv","PyPDF2","langchain_google_genai"],
    packages=find_packages()
)