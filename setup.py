from setuptools import find_packages, setup

setup(
    name="edit-list-check",
    version="0.1.0",
    description="Validate simple CSV video edit lists before rendering",
    packages=find_packages(),
    python_requires=">=3.10",
    entry_points={"console_scripts": ["edit-list-check=edit_list_check.cli:main"]},
)
