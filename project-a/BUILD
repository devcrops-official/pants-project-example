python_sources(
    name="lib", 
    sources=["my_module/**/*.py"], 
    resolve="project-a"
)

python_tests(
    name="tests",
    sources=["tests/**/test_*.py"],
    resolve="project-a"
)

python_distribution(
    name="dist",
    dependencies=[
        ':lib',
        '//:project-a-3dparty-requirements#docker-compose',
        '//:project-a-3dparty-requirements#awscli'
        ],
    provides=python_artifact(
        name="my_module-a",
        description="A tool.",
        long_description_file="README.md",
    ),
    generate_setup = True,
    wheel_config_settings={"--global-option": ["--python-tag", "py37.py38.py39"]},
)

