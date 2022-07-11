python_sources(
    name="lib", 
    sources=["my_module/**/*.py"], 
    resolve="project-b"
)

python_tests(
    name="tests",
    sources=["tests/**/test_*.py"],
    resolve="project-b"
)

python_distribution(
    name="dist",
    dependencies=[
        ':lib',
        '//:project-b-3dparty-requirements#numpy',
        ],
    provides=python_artifact(
        name="my_module-b",
        description="B tool.",
        long_description_file="README.md",
    ),
    generate_setup = True,
    wheel_config_settings={"--global-option": ["--python-tag", "py37.py38.py39"]},
)

