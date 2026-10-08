# Venue choice: regime-switching asset allocation paper

Researched 2026-10-08. Every line marked "verified" was read on the official page named next to it. Lines marked "inferred" are projections from past cycles. Lines marked "secondary" come from a mailing list or aggregator and should be rechecked.

## Recommendation: ACM ICAIF 2027 (8th ACM International Conference on AI in Finance)

Why this one:

1. **Fit.** ICAIF is the only archival venue on the list built for ML-in-finance work. The 2026 call lists "asset pricing, robo-advising, and portfolio optimization", "reinforcement learning", "financial time series forecasting" and "robustness and uncertainty quantification" as topics. The paper has an ML half (HMM / Markov-switching / statistical jump model comparison, a POMDP policy) and a finance half (spanning tests against volatility-managed and trend portfolios). ICAIF reviewers are drawn from both groups. AAAI and IJCAI reviewers would mostly see the ML half, and finance journals would mostly see the finance half.
2. **Timing.** ICAIF deadlines have landed in early August three years running (2026: Aug 2, extended to Aug 9). The 2027 deadline should fall around early August 2027, about 10 months out, with a decision by early October and the conference in mid-November. That fits the "deadline within 12 months" preference and leaves time to finish the 100-year real-time runs.
3. **Preprint policy is friendly.** arXiv posting is explicitly allowed. That lets the full-length version (proofs of the band-width law, the full model-family tables) live on arXiv while the 8-page version goes to review.
4. **Format overlap with the sibling papers.** ACM `acmart` is the same class the ACM EC sibling paper uses, so tooling and bib style carry over.
5. **Solo M.S. author.** ICAIF accepts practical, well-executed empirical work from industry and students. Management Science, JFEC and QF reward the same paper but take 6-18 months per round. A conference acceptance in Oct 2027 is a faster CV line.

Main risk: **8 pages total including references, and no appendices or supplementary material.** The submission has to be self-contained. Plan the cut early. A likely split: main text gets the real-time protocol, one headline table across model families, the no-trade band result with a proof sketch and the width law statement, and one spanning-test table. The full proofs, the per-decade tables and robustness go to the arXiv long version. The submission cannot cite that arXiv version (anonymity rule below).

Fallback if ICAIF 2027 rejects (or if the 8-page cut loses too much): **Quantitative Finance** (rolling, LaTeX-friendly, arXiv-friendly, two anonymous referees). If the econometrics side becomes the main story, JFEC is the stronger fit of the two.

Optional, non-conflicting exposure: submit a talk abstract to **SIAM FM27** by **Dec 15, 2026**. It is abstract-only with no proceedings, so it does not count as prior archival publication under ICAIF's dual-submission rule.

### ICAIF format rules (from the ICAIF 2026 call; the 2027 call has not been posted)

Source: https://icaif2026.org/call-for-papers.html (verified)

- Length: at most 8 pages in two-column ACM `sigconf`, **including all figures and references**.
- No supplementary material or appendices accepted. Paper must be self-contained.
- LaTeX must use the ACM `sigconf` two-column format, with the `anonymous` option. Word template also allowed; LaTeX preferred.
- Double-blind. Self-citations in third person ("Author et al. [x] found ..."). No rebuttal phase.
- Prior posting on arXiv or at non-archival workshops (AAAI, KDD, ICML, NeurIPS workshops named) is allowed, but **do not cite** the arXiv version in the submission.
- No concurrent submission to any other archival venue during the ICAIF review period; papers under review at a journal are ineligible.
- Accepted papers appear in the ACM proceedings (archival). ORCID required for all authors at camera-ready.
- 2026 dates: deadline Aug 2, extended to Aug 9, 2026 (AoE); notification extended to Oct 1, 2026; conference Nov 14-17, 2026, Milan (Bocconi), main program Nov 16-17.
- Submission via Microsoft CMT; at least one author must present in person. Source: CFP repost on ML-news, https://groups.google.com/g/ML-news/c/p1-BeV8KRAk (secondary, consistent with the official page).
- ICAIF 2025 (Singapore, Nov 15-18, 2025) main-track deadline was extended to Aug 3, 2025. Source: INFORMS forum CFP post, https://connect.informs.org/discussion/acm-icaif-2025-call-for-papers-and-participation-posted-on-behalf-of-professor-ke-wei-huang (secondary).
- **ICAIF 2027: no announcement found** as of 2026-10-08 (searched "ICAIF 2027", "ICAIF '27"). Expected deadline early August 2027, conference mid-November 2027 (inferred). Watch https://ai-finance.org/ and the ACM conference listing from about May 2027.

### documentclass lines

Template: `acmart` v2.20 (2026/08/16), generated from the CTAN release, saved in `/Users/takakhoo/Dev/regime-research/paper/template/`.

| Use | Line |
|---|---|
| ICAIF submission (double-blind, line numbers) | `\documentclass[sigconf,review,anonymous]{acmart}` |
| ICAIF camera-ready | `\documentclass[sigconf]{acmart}` plus the `\setcopyright{...}`, `\copyrightyear`, `\acmYear`, `\acmDOI`, `\acmConference[ICAIF '27]{...}`, `\acmBooktitle`, `\acmISBN` lines ACM sends after the rights form |
| arXiv / personal-site preprint of the 8-page version | `\documentclass[sigconf,nonacm]{acmart}` (drops the ACM reference block, copyright box and running footers) |
| arXiv long version with appendices | `\documentclass[acmsmall,nonacm]{acmart}` (single column, reads better at 20+ pages) |

Notes:
- The call only names `sigconf` and `anonymous`. `review` adds line numbers, which reviewers like and which is harmless. Drop it if the 2027 call says otherwise.
- With `anonymous`, keep the real `\author{}` block in the source. acmart prints "Anonymous Author(s)" and hides affiliations. Also remove acknowledgments, code URLs and dataset paths that identify the author.
- Bibliography: `\bibliographystyle{ACM-Reference-Format}` with `\bibliography{refs}`.
- Tested: `samples/sigconf.tex` switched to `[sigconf,review,anonymous]` compiles with `tectonic -X compile` and prints "Anonymous Author(s)" with line numbers. TinyTeX on this machine does not have acmart installed; either keep `acmart.cls` next to the paper source (already done in `template/`) or run `tlmgr install acmart`.
- For arXiv, upload `acmart.cls` and `ACM-Reference-Format.bst` with the source so the class version is pinned.

### Template files

`/Users/takakhoo/Dev/regime-research/paper/template/`
- `acmart.cls` (generated with docstrip from `acmart.dtx` / `acmart.ins`, both kept alongside)
- `ACM-Reference-Format.bst`, biblatex files (`acmauthoryear.*`, `acmnumeric.*`, `acmdatamodel.dbx`), `acm-jdslogo.png`, `README`
- `samples/sigconf.tex`, `samples/sigconf-authordraft.tex`, `samples/sigconf.pdf`, `samples/sample-base.bib` and the sample images
- `docs/acmguide.pdf` (user guide), `docs/acmart.pdf` (class documentation)
- Source: https://mirrors.ctan.org/macros/latex/contrib/acmart.zip (CTAN, acmart v2.20). ACM's own bundle (https://www.acm.org/publications/proceedings-template, linked from the ICAIF call) returned 403 to scripted download; it ships the same class.

## Comparison of all venues checked

| Venue | Fit | Format | Review | Next deadline | Preprints |
|---|---|---|---|---|---|
| **ICAIF 2027** (ACM) | Strong: AI in finance, portfolio optimization and RL listed as topics | ACM sigconf, 8 pp incl. refs, no appendix | Double-blind | ~early Aug 2027 (inferred; 2026 was Aug 9) | arXiv allowed, do not cite it |
| AAAI-27 / AAAI-28 | Weak: no finance track; special tracks are AI for Social Impact and AI Alignment | 7 pp + up to 2 pp refs (AAAI author kit) | Double-blind (standard for AAAI; not re-verified on this page) | AAAI-27 closed Jul 28, 2026. AAAI-28 likely late Jul 2027 (inferred) | Not stated on the call page |
| IJCAI-27 | Weak: no finance special track since IJCAI-PRICAI 2020 "AI in FinTech"; 2026 special tracks were Human-Centred AI, AI for Social Good, AI4Tech, AI and Health, AI and Robotics | IJCAI style (7 + 2 pp in recent years; 2027 not posted) | Double-blind | 2027 CFP not out. 2026 full papers were due Jan 19, 2026, so ~mid-Jan 2027 (inferred). Conference Kyoto Aug 7-13, 2027 plus Hengqin Aug 15-17 | Not checked (CFP not posted) |
| NeurIPS 2027 workshops | Medium if a finance workshop runs; usually non-archival | Varies, typically 4-9 pp NeurIPS style | Usually double-blind | 2027 list not out. NeurIPS 2026 accepted 102 workshops (Dec 11-13, 2026) and no finance-titled one appeared in the visible part of the list; NeurIPS 2025 had "Generative AI in Finance". Workshop deadlines typically late Aug-Sep (inferred) | Non-archival, so compatible with ICAIF if timed after ICAIF review |
| SIAM FM27 | Good audience (financial math, ML in finance) | Abstract only; no proceedings | Co-chair approval | Minisymposium proposals Nov 17, 2026; contributed talk/poster abstracts **Dec 15, 2026**; decisions Jan 2027; conference Jun 15-18, 2027, Arlington VA, in person only | No paper published, no conflict |
| J. Financial Econometrics (OUP / SoFiE) | Strong for the Markov-switching / real-time forecasting side | Typically ≤40 double-spaced pp incl. refs and tables; LaTeX PDF accepted, OUP "Modern Small" template recommended; code and data required for acceptance | Not stated on the page | Rolling | Author's Original Version may stay online; update with DOI after acceptance |
| Quantitative Finance (T&F) | Strong: portfolio choice, regime models, transaction costs | T&F "Interact" LaTeX class, QF-specific reference style (chronological citation order) | Two anonymous referees (single vs double not stated) | Rolling | T&F allows arXiv preprints of the original manuscript; cite the preprint in the submission |
| J. Portfolio Management (PMR) | Medium: practitioner audience | Target 4,000 words; under 2,500 or over 7,500 rarely accepted; Word preferred for math; Chicago author-date | Editor screen then referees; no submission fee | Rolling | **Must remove all prior versions, including SSRN and personal sites, on acceptance**. Conflicts with an arXiv preprint |
| J. Financial Data Science (PMR) | Medium-strong on topic, but same PMR rules | Same PMR memo as JPM | Editor screen, 1-2 reviewers | Rolling | Same removal rule as JPM |
| Financial Analysts Journal (CFA / T&F) | Medium: practitioner audience, technical exposition discouraged | Word limit not found on the pages read | Anonymized files for review | Rolling (avg 64 days to post-review decision) | Not stated on the CFA page |
| Management Science (INFORMS) | Strong topic fit (finance department), very high bar for a solo M.S. paper | 11 pt, 1-inch margins, 1.5 or double spacing; invited revisions capped at 32 pp (1.5 sp) or 47 pp (double); online appendix excluded | Double-anonymous | Rolling; submission fee since Aug 1, 2025 | Not stated in what was read |

## Sources

- ICAIF 2026 CFP (official): https://icaif2026.org/call-for-papers.html
- ICAIF 2026 CFP repost with location, CMT link and in-person rule: https://groups.google.com/g/ML-news/c/p1-BeV8KRAk
- ICAIF 2025 CFP post: https://connect.informs.org/discussion/acm-icaif-2025-call-for-papers-and-participation-posted-on-behalf-of-professor-ke-wei-huang
- ICAIF site (2024 edition and proceedings links): https://ai-finance.org/
- ACM proceedings template page: https://www.acm.org/publications/proceedings-template
- acmart on CTAN: https://mirrors.ctan.org/macros/latex/contrib/acmart.zip
- AAAI-27 main track call: https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/
- IJCAI-27 dates: https://www.ijcai.org/
- IJCAI-ECAI 2026 special tracks: https://2026.ijcai.org/?p=2117
- IJCAI-PRICAI 2020 AI in FinTech track: https://ijcai20.org/call-for-papers-fintech/
- NeurIPS 2026 workshops announcement: https://blog.neurips.cc/2026/08/10/announcing-the-neurips-2026-workshops/
- SIAM FM27: https://www.siam.org/conferences-events/siam-conferences/fm27/ and https://www.siam.org/conferences-events/siam-conferences/fm27/submissions/ (pages return 403 to scripted fetch; details read through search indexing of these pages)
- JFEC instructions: https://academic.oup.com/jfec/pages/General_Instructions
- Quantitative Finance about page: https://www.tandfonline.com/journals/rquf20/about-this-journal
- QF reference style: https://files.taylorandfrancis.com/ref_rquf.pdf
- T&F preprint policy: https://authorservices.taylorandfrancis.com/preprint-servers/
- PMR (JPM, JFDS) submission memo: https://www.pm-research.com/sites/default/files/2023-03/PMR_Article_Submission_Guidelines_2023.pdf
- JPM author page: https://jpm.pm-research.com/authors
- JFDS author page: https://jfds.pm-research.com/authors
- FAJ submission guide: https://rpc.cfainstitute.org/research/financial-analysts-journal/submit-to-financial-analysts-journal
- Management Science guidelines: https://pubsonline.informs.org/page/mnsc/submission-guidelines

## To recheck later

- ICAIF 2027 CFP (host city, exact deadline, whether the 8-page and no-appendix rules carry over). Check from May 2027.
- Quantitative Finance word limit and whether review is single- or double-anonymous (T&F instructions page blocked scripted access).
- Whether QF or JFEC would accept an extended journal version of an ICAIF paper, since ICAIF proceedings are archival.
