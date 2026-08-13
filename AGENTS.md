# AI Development Workflows

Autonomous tasks must use the workflow that matches the GitHub Issue.

## New Agent Skill workflow

Use this workflow when the GitHub Issue requests creation of a new Agent Skill.

Execute sequentially:

1. Skill Creator
   - Use `skill-creator`.
   - Create the new Agent Skill requested by the Issue.
   - Keep implementation limited to the new Skill and strictly necessary supporting files.
   - Do not use this workflow for modification or maintenance of an existing Skill.

2. Skill Reviewer
   - Use `skill-reviewer`.
   - Review the newly created Skill against the Issue and the reviewer instructions.
   - The Skill Reviewer must not implement fixes.
   - If the result is FAIL, return the findings to Skill Creator and repeat Skill Creator -> Skill Reviewer.
   - Maximum 3 Creator/Reviewer cycles.

3. Pull Request
   - After Skill Reviewer returns PASS or PASS WITH COMMENTS, review the final diff, commit and push the task branch, and create a Pull Request against `main`.
   - Never merge the Pull Request automatically.
   - Stop after creating/updating the Pull Request for human review.

Expected flow:

Issue -> Skill Creator -> Skill Reviewer -> Pull Request -> Human review

Repair flow:

Skill Reviewer FAIL -> Skill Creator -> Skill Reviewer

There is no Architect, Developer, general Reviewer, or Tester stage in the new-Agent-Skill workflow.

## Standard development workflow

For all other autonomous development tasks, execute sequentially:

1. Architect
2. Developer
3. Reviewer
4. Tester

Only after Tester reports READY FOR PR may changes be committed, pushed and opened as a Pull Request.

Never merge the Pull Request automatically.

Stop and report the blocker if the selected workflow cannot reach a valid result.
