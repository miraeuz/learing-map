# Code signing policy — ICPC yoʻli

Windows installers of ICPC yoʻli are built automatically by GitHub Actions from the
public source code in this repository (`.github/workflows/build-desktop.yml`).
No binary is built or uploaded by hand.

- **Source:** https://github.com/miraeuz/learing-map
- **Build:** GitHub-hosted runners, workflow `Build desktop`
- **Committers and reviewers:** [muhammadiev](https://github.com/miraeuz)
- **Approvers of signing requests:** [muhammadiev](https://github.com/miraeuz)
- **Privacy policy:** [PRIVACY.md](PRIVACY.md) — the app sends data to another system only
  during activation, and only what is listed there.

When a code signing certificate is configured (see `README.md`, "Imzolash"), each release is
signed in the same workflow. Free code signing for this project may be provided by
[SignPath.io](https://about.signpath.io/), certificate by
[SignPath Foundation](https://signpath.org/).
