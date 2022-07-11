import os.path
import logging
from pathlib import Path

from pants.engine.fs import DigestContents, GlobMatchErrorBehavior, PathGlobs
from pants.engine.rules import Get, collect_rules, rule
from pants.engine.unions import UnionRule
from pants.backend.python.goals.setup_py import SetupKwargsRequest, SetupKwargs
from pants.engine.target import Target
from pants.base.build_environment import get_buildroot

class CustomSetupKwargsRequest(SetupKwargsRequest):
    @classmethod
    def is_applicable(cls, _: Target) -> bool:
        return True

@rule
async def setup_kwargs_plugin(request: CustomSetupKwargsRequest) -> SetupKwargs:
    original_kwargs = request.explicit_kwargs.copy()

    # Validation step
    long_description_relpath = original_kwargs.pop("long_description_file", None)
    if not long_description_relpath:
        raise ValueError(
            f"The python_distribution target {request.target.address} did not include "
            "`long_description_file` in its python_artifact's kwargs. Our plugin requires this! "
            "Please set to a path relative to the BUILD file, e.g. `ABOUT.md`."
        )
    
    custom_description = original_kwargs.pop("description", None)
    if not custom_description:
        raise ValueError(
            f"The python_distribution target {request.target.address} did not include "
            "`description` in its python_artifact's kwargs. Our plugin requires this! "
            "Please set `description field` to the BUILD file, e.g. `Only another python library`."
        )

    # Version management
    default_version = Path(get_buildroot(), "VERSION").read_text()
    custom_version = original_kwargs.pop("version", None)
    artifact_version = custom_version if custom_version else default_version


    build_file_path = request.target.address.spec_path
    long_description_path = os.path.join(build_file_path, long_description_relpath)
    digest_contents = await Get(
        DigestContents,
        PathGlobs(
            [long_description_path],
            description_of_origin=f"the 'long_description_file' kwarg in {request.target.address}",
            glob_match_error_behavior=GlobMatchErrorBehavior.error,
        ),
    )
    description_content = "\n".join(file_content.content.decode() for file_content in digest_contents)
    

    # Hardcode certain kwargs and validate that they weren't already set.
    hardcoded_kwargs = dict(
        version=artifact_version,
        long_description=description_content,
        long_description_content_type="text/markdown",
        author="Pierluigi Dell'Arciprete",
        author_email="@devcrops",
        description=custom_description,
        url="https://github.com/devcrops-official/pants-project-example",
        license="Apache License, Version 2.0",
        platform="OS Independent",
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "Operating System :: OS Independent",
        ]
    )

    conflicting_hardcoded_kwargs = set(original_kwargs.keys()).intersection(hardcoded_kwargs.keys())
    if conflicting_hardcoded_kwargs:
        raise ValueError(
            f"These kwargs should not be set in the `provides` field for {request.target.address} "
            "because Pants's internal plugin will automatically set them: "
            f"{sorted(conflicting_hardcoded_kwargs)}"
        )
    original_kwargs.update(hardcoded_kwargs)

    return SetupKwargs(original_kwargs, address=request.target.address)
    #return SetupKwargs(
    #    {**original_kwargs, "long_description": description_content},
    #    address=request.target.address
    #)

def rules():
    return (*collect_rules(), UnionRule(SetupKwargsRequest, CustomSetupKwargsRequest))


    