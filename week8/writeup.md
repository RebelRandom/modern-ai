# Week 8 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Lucas Deng** \
This assignment took me about **2** hours to do. 


## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
> https://github.com/RebelRandom/modern-ai/pull/1
> https://github.com/ydrcai/modern-ai/commit/b774805af2a49468f8b2b95f92938c829f9cafd2 (?)

b. PR Description
> Implemented additional API endpoints and improved validation:
> - Added GET endpoint for individual action items
> - Added DELETE endpoints for notes and action items
> - Added validation for blank fields, pagination parameters, and sorting fields
> - Added tests covering the new endpoints and validation behavior
> - Ran pytest -q backend/tests, all tests pass

c. Graphite Diamond generated code review
> Graphite Diamond reviewed changes and marked PR as passing. No additional comments or suggested changes provided.

## Task 2: Extend extraction logic
a. Links to relevant commits/issues
> https://github.com/RebelRandom/modern-ai/pull/2
> https://github.com/ydrcai/modern-ai/commit/295a13d0ef7249cb515f82ec91ae98adfda48032 (?)

b. PR Description
> Extended action item extraction logic with more advanced pattern recognition:
> - Added support for additional action item prefixes such as TASK, FIXME, and Follow Up
> - Added support for markdown checkboxes and imperative sentences
> - Added metadata extraction for priority, assignees, and due dates
> - Added tests for the new extraction behavior
> - Ran pytest -q backend/tests, all tests pass

c. Graphite Diamond generated code review
> Graphite Diamond reviewed changes and marked PR as passing. No additional comments or suggested changes provided.

## Task 3: Try adding a new model and relationships
a. Links to relevant commits/issues
> https://github.com/RebelRandom/modern-ai/pull/3
> https://github.com/ydrcai/modern-ai/commit/f97bb493a7af705f6cff897014db5cc828a107e8 (?)

b. PR Description
> Added tags as a new model and implemented note/tag relationships:
> - Added Tag database model
> - Added many-to-many relationship between notes and tags
> - Added endpoints for adding and removing tags from notes
> - Updated schemas and seed data to support tags
> - Ran pytest -q backend/tests, all tests pass

c. Graphite Diamond generated code review
> Graphite Diamond reviewed changes and marked PR as passing. No additional comments or suggested changes provided.

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> https://github.com/RebelRandom/modern-ai/pull/4
> https://github.com/ydrcai/modern-ai/commit/7866907e46e71d76cfd5b3c88532313ccce1b4da (?)

b. PR Description
> Expanded pagination and sorting test coverage across the application:
> - Added tests for pagination boundaries
> - Added tests for ascending and descending sorting
> - Added tests combining filtering/searching with pagination and sorting
> - Improved coverage of edge cases such as empty results
> - Ran pytest -q backend/tests, all tests pass

c. Graphite Diamond generated code review
> Graphite Diamond reviewed changes and marked PR as passing. No additional comments or suggested changes provided.

## Brief Reflection 
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> - Reviews focused mostly on correctness, test coverage, API behavior, and whether the implementation matched the requirements of each task.
> - Checked new endpoints returned appropriate errors, validation handled edge cases correctly, and new functionality had enough tests.
> - Reviewed if changes fit the existing structure of the codebase.

b. A comparison of **your** comments vs. **Graphite’s** AI-generated comments for each PR.
> Mine:
> - more focused on understanding purpose of changes and checking whether implementation matched assignment requirements.
> Graphite Diamond's:
> - automated review feedback and marked each PR as passing.
> - For most PRs, Graphite did not provide additional comments. (mine was manually checking implementation details)
> Main exception was Task 2, with extraction logic requiring more consideration of behavior and false positives.

c. When the AI reviews were better/worse than yours (cite specific examples)
> Graphite's reviews helped as a second set of eyes, but they were less helpful for design decisions that required understanding intended behavior.
> Example: in Task 2, treating every @mention as an action item can create many false positives; required reasoning about application's expected behavior and not just looking for code issues.
> Graphite did not identify issue because it was more related to product behavior than typical code defects.

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
> Fairly comfortable using AI reviews as an additional review step, but not reliable as a replacement for manual review.
> AI can help with catching common mistakes, missing tests, and code quality issues, but, humans are still needed for understanding requirements, architecture, and design tradeoffs.

