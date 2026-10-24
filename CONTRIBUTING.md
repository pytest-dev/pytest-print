# Contributing

Use a feature branch and open a pull request against `main`. Add a Markdown file under `changelog.d` for a user-facing
change. The filename may start with a short name, so you do not need a PR number before opening the pull request. The
release preparation step links merged fragments to their squash PRs.

Name files `<name>.<category>.md`. The available categories are `feature` (new capabilities and Python version additions
or removals), `change` (changed behavior), `bugfix`, `doc`, `breaking`, `security`, `performance`, `deprecation`,
`removal`, and `packaging`. Write one change per file, with a short sentence from the user's point of view. Do not add a
fragment for CI, tooling, or dependency maintenance unless the change affects users. Maintainers can apply the
`skip news` label to such PRs. Bot PRs without fragments receive that label automatically.

Run `tox run -e fix`, `tox run -e type`, `tox run -e pkg_meta`, and `tox run -e 3.15` before requesting review. The
release workflow calculates the next version from the pending fragments. `feature` changes select a minor version;
`breaking` changes select a major version; all other categories select a patch version. The maintainer can choose an
explicit bump for exceptional cases.
