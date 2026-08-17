# AI Development Workflows

Autonomous tasks must use the workflow that matches the GitHub Issue.

## Runtime skill dependencies

This repository declares the Agent Skills needed to work on Agent Skill creation in `.agents/required-skills.json`.

The platform resolves and provisions those skills before the first agent run. Do not commit runtime-provisioned `.agents/skills/` or `.agents/skill-provenance.json` files.

## New Agent Skill workflow

Use this workflow when the GitHub Issue requests creation of a new Agent Skill.

Execute sequentially:

1. Skill Creator
   - Use `skill-creator`.
   - Create the new Agent Skill requested by the Issue under `skills/<skill-name>/` using the standard Agent Skills structure.
   - Keep implementation limited to the new Skill and strictly necessary supporting files.
   - Do not use this workflow for modification or maintenance of an existing Skill.
   - Register the new Skill exactly once in `.plugin/marketplace.json`.
   - The marketplace entry name must match the Skill frontmatter `name`.
   - The marketplace entry `source` must point to the Skill directory using the existing relative-source convention, normally `./skills/<skill-name>`.
   - Do not add repository URLs, commit SHAs or runtime installation paths to the marketplace manifest.

2. Skill Reviewer
   - Use `skill-reviewer`.
   - Review the newly created Skill against the Issue and the reviewer instructions.
   - Verify the Skill is correctly and uniquely registered in `.plugin/marketplace.json`, with matching name and valid relative source path.
   - The Skill Reviewer must not implement fixes.
   - If the result is FAIL, return the findings to Skill Creator and repeat Skill Creator -> Skill Reviewer.
   - Maximum 3 Creator/Reviewer cycles.

3. Pull Request
   - After Skill Reviewer returns PASS or PASS WITH COMMENTS, review the final diff, including both the Skill and its marketplace registration.
   - Commit and push the task branch and create a Pull Request against `main`.
   - Never merge the Pull Request automatically.
   - Stop after creating/updating the Pull Request for human review.

Expected flow:

Issue -> Skill Creator -> Skill Reviewer -> Pull Request -> Human review

Repair flow:

Skill Reviewer FAIL -> Skill Creator -> Skill Reviewer

## DENY non-Agent-Skill work

This repository is only for Agent Skill-related activities.

If the GitHub Issue is not directly related to creating, reviewing, modifying, maintaining, validating, or otherwise managing Agent Skills in this repository:

1. DENY the task.
2. Do not modify any files.
3. Do not commit or push any changes.
4. Do not create or update a Pull Request.
5. Report that the Issue is outside the Agent Skill scope of this repository.
6. Stop immediately and perform no further work.

Stop and report the blocker if a skill-related Issue does not match a defined repository workflow.
