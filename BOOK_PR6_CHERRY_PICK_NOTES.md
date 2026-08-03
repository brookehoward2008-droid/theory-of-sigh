# PR #6 Cherry-Pick Notes

Branch: `book-typography-fixes-from-pr6`

Purpose: carry forward the useful typography fixes from PR #6 without taking the full conflicted 207-file branch.

## Cherry-picked so far

- Conservative widow control for wrapped PDF text blocks.
- Synthesis body-type repair for the known drop from 9.2 pt / 13 leading back to the normal book body size of 10.4 pt / 14.5 leading.

## Kept out intentionally

- Full PR #6 merge.
- Mass image relabeling.
- Broad generated-output changes.
- Font folder churn.
- A3/page-size route changes.
- Route cleanup behavior that could alter generated folders.

## Safety rule

This branch should stay surgical. It should only receive the typography fixes needed for the current book proof unless Brooke explicitly approves broader layout or asset changes.
