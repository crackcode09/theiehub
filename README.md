<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/the-ie-hub-logo-on-dark.svg">
    <img src=".github/assets/the-ie-hub-logo-on-light.svg" alt="The IE Hub" width="360">
  </picture>
</p>

# The IE Hub

**theiehub.com** · home of the **IE Knowledgebase**: free, open courses on industrial engineering, quality and continuous improvement. Courses are grouped into the same categories used by the IISE professional course catalog, plus a few added for subjects it does not cover, under `courses/<category>/<course>/`.

**32 courses built**, covering 33 of the 102 catalog topics. All are `draft` until a reviewer verifies them (see [Status, review and legal](#status-review-and-legal)). Read them on the site: <https://theiehub.com/>.

## Courses

New to industrial engineering? Start with [Introduction to Industrial Engineering](courses/technical-skills/introduction-to-industrial-engineering/README.md), the broad entry point, then pick a category.

See [ROADMAP.md](ROADMAP.md) for a checklist of what is built and what is still open in each category, and [VISION.md](VISION.md) for where the site is going: a role advisor that turns a target position into a training plan grounded in the official standard for the role and in what the market asks for.

[![Roadmap graph](public/roadmap.svg)](public/roadmap.svg)

**Interactive site:** <https://theiehub.com/> is the hub's home page: search, where to start, the live numbers and what is here. The courses are on <https://theiehub.com/learn>:

- **Catalog:** every course by category, with search.
- **Learning path:**
  - six role-based tracks (industrial, quality and manufacturing engineer, operations research analyst, management analyst, industrial production manager), each anchored to an O*NET occupation with its BLS outlook;
  - a time-budget mode that fits courses to the hours you have.
- **Mind map:** courses, modules and prerequisites.
- **Reader:** an on-site reader for every course and module.
- **Sources page:** what each course cites.
- **Site roadmap:** where the hub is going, phase by phase, at <https://theiehub.com/roadmap>.

Progress ticks are kept in your browser only; there are no accounts and no tracking. Light and dark themes follow your system setting.

The site is generated into `public/` by `python tools/roadmap_graph.py` (standard library only). It is published on Cloudflare Pages at <https://theiehub.com/>: on each push to `main`, `python tools/build_site.py` puts the pages from `public/` and the `courses/` folder side by side in `_site/`, which is what gets served. Pushes to `dev` build a private preview at `dev.theiehub.com` (maintainer only) for checking a release before it goes out. Never edit `public/` by hand; edit the templates in `tools/` and rebuild.

Suggested order without a track: Measurement & Basic Statistics, Process Mapping and Voice of the Customer, then Charting Process Behavior, then Fundamentals of Hypothesis Testing, then Design for Six Sigma, then Root Cause Analysis. Kaizen Leader and Lean Methods Accelerator have no prerequisites and can be taken at any point. The tracks themselves are defined in [roles/tracks.md](roles/tracks.md).

### [Analytics, Data Science & AI](courses/analytics-data-science-ai/README.md)

| Course | Topic | Length | Status |
|---|---|---|---|
| [Introduction to Engineering Analytics](courses/analytics-data-science-ai/engineering-analytics/README.md) | Analytics types and process; visualization and dashboards; data models, star schema, SQL; k-means segmentation, ABC classification, logistic and tree classifiers, accuracy measures; regression case study; PCA; forecasting; Big Data technology and enterprise data models; linear-programming optimization; strategy | ~2 days | draft |
| [Advanced Engineering Analytics](courses/analytics-data-science-ai/advanced-engineering-analytics/README.md) | Business impact of data science; managing and merging multi-source data (Excel + exports); data preparation; descriptive statistics; ANOVA; regression; nonparametric tests and bootstrap; DOE; improving prediction accuracy (CV, features, leakage); dashboards | ~2 days | draft |
| [Analytics-Based Enterprise Performance Management](courses/analytics-data-science-ai/analytics-based-epm/README.md) | EPM and ERM; BI vs BA, forecasting vs predictive analytics; ABC/M and chargebacks; strategy maps, balanced scorecards, KPIs vs PIs; customer profitability, cost-to-serve, CLV; unit costing, cost of quality, value-stream costing; driver-based budgets, rolling forecasts, risk-adjusted Monte Carlo, outsourcing; intangible-asset ROI; adoption barriers | 1 day (+ exercises) | draft |
| [Efficient AI](courses/analytics-data-science-ai/efficient-ai/README.md) | AI foundations (ML, GenAI, rules); problem-first thinking; cross-functional use cases; AI with Lean Six Sigma (PICK chart, DMAIC pilots); risks, limitations, misconceptions (GenAI pilot evaluation); data readiness audit; from ideas to a phased roadmap with business case | ~4 h | draft |
| [Human-Centered AI](courses/analytics-data-science-ai/human-centered-ai/README.md) | Human-centered design foundations; qualitative insight gathering (simulated interviews); from insights to themes; opportunity framing (How might we); bridge to design sprints and rapid prototyping (assumption maps, Wizard of Oz) | ~2 h | draft |
| [Data Analytics for Business Results](courses/analytics-data-science-ai/data-analytics-for-business-results/README.md) | Analytics types, lifecycle, MAD dashboards, 12 data-quality dimensions, EDA, Apriori, A/B tests, regression, ML (churn, RFM), storytelling, decision models, biases | 8 h (4 × 2 h) | draft |
### [Ergonomics & Safety](courses/ergonomics-safety/README.md)

_No courses yet._

### [Healthcare Process Improvement](courses/healthcare-process-improvement/README.md)

_No courses yet._

### [Leadership & Project Management](courses/leadership-project-management/README.md)

_No courses yet._

### [Lean & Six Sigma](courses/lean-six-sigma/README.md)

| Course | Topic | Length | Status |
|---|---|---|---|
| [Measurement & Basic Statistics](courses/lean-six-sigma/measurement-and-basic-statistics/README.md) | Data types, accuracy vs precision, Pareto charts, histograms, center, spread, the normal distribution | ~6 h | draft |
| [Process Mapping](courses/lean-six-sigma/process-mapping/README.md) | SIPOC, flow charts, swim lanes, value-added flow charts, spaghetti diagrams, VSM, VOC, affinity diagrams, CTQ trees, VOC as specifications | ~6 h | draft |
| [Voice of the Customer](courses/lean-six-sigma/voice-of-the-customer/README.md) | Customers and segments, Kano, surveys and margin of error, affinity and CTQ trees, operational definitions, VOC as specifications, cause-and-effect matrix | ~7 h | draft |
| [Lean Methods Accelerator](courses/lean-six-sigma/lean-methods-accelerator/README.md) | Standalone Lean toolkit: COPQ, VSM, takt, balancing, heijunka, benchmarking, flow and cells, SMED, TOC, pull (kanban, CONWIP), 5S, visual management, TPM, standard work | ~18 h | draft |
| [Charting Process Behavior](courses/lean-six-sigma/charting-process-behavior/README.md) | Statistical Process Control: run charts, XmR, X̄–R, attribute charts, capability | ~12 h + capstone | draft |
| [Fundamentals of Hypothesis Testing](courses/lean-six-sigma/fundamentals-of-hypothesis-testing/README.md) | Hypotheses, errors, power, CIs; t, ANOVA, proportion, chi-square, variance and nonparametric tests | ~14 h + capstone | draft |
| [Design for Six Sigma](courses/lean-six-sigma/design-for-six-sigma/README.md) | DCDOV: VOC, QFD, Pugh, FMEA, error-proofing, scorecards, DOE, tolerance stack-up, flow simulation, line balancing, reliability | ~45 h incl. capstone | draft |
| [Root Cause Analysis & Problem Solving](courses/lean-six-sigma/root-cause-analysis/README.md) | Problem statements, Pareto, process maps, fishbone, 5-Why, root cause trees, stratification, regression, logistic regression, corrective actions | ~14 h | draft |
| [Kaizen Leader](courses/lean-six-sigma/kaizen-leader/README.md) | Planning and leading kaizen events: charter, VSM, takt, TOC, flow, balancing, kanban, SMED, 5S, TPM, standard work, A3; includes a one-day team-member track | ~22 h | draft |
### [Logistics & Supply Chain](courses/logistics-supply-chain/README.md)

_No courses yet._

### [Quality & Operational Excellence](courses/quality-operational-excellence/README.md)

| Course | Topic | Length | Status |
|---|---|---|---|
| [Statistical Quality Control](courses/quality-operational-excellence/statistical-quality-control/README.md) | Descriptive statistics; common vs special cause; X̄–R, I–MR, p, c and short-run charts; Cp/Cpk; acceptance sampling: risks, OC curves, AOQ/AOQL, ASN, ATI, ANSI/ASQ Z1.4 use | ~3 days | draft |
| [Cost of Quality](courses/quality-operational-excellence/cost-of-quality/README.md) | CoQ models (PAF, process cost, activity-based); prevention, appraisal, internal and external failure; hidden costs and quality loss; cost assessments; cost drivers; project selection and savings; CoQ reports; Excel tracker | ~2 days | draft |
| [Quality Engineering Essentials](courses/quality-operational-excellence/quality-engineering-essentials/README.md) | DMAIC quality toolkit: charter, 8 wastes, basic statistics, distribution ID, data cleansing, gauge R&R and attribute MSA, baseline/DPMO, SPC with transformations and stage variables, capability, root cause (fishbone, 5-Why, stratification, regression), FMEA, reliability, error-proofing, pilots, change management, control plans, 5S, standard work | ~39 h | draft |
### [Technical Skills](courses/technical-skills/README.md)

| Course | Topic | Length | Status |
|---|---|---|---|
| [Introduction to Industrial Engineering](courses/technical-skills/introduction-to-industrial-engineering/README.md) | What IEs do; methods and motion study; time study, work sampling and standards; ergonomics; layout; job analysis, evaluation and pay; Lean, Six Sigma, RCA; basic statistics | ~3 days | draft |
| [Applied Statistics](courses/technical-skills/applied-statistics/README.md) | Data collection systems; descriptive statistics; hypergeometric, binomial, Poisson, normal, exponential, t, chi-square, F; CIs and tests; non-normal data; correlation; linear and multiple regression | ~2 days | draft |
| [Design of Experiments](courses/technical-skills/design-of-experiments/README.md) | Completely randomized, randomized block and Latin square designs; two-factor ANOVA and interaction; balanced vs unbalanced; replication and power; 2^k full and fractional factorials; operating levels with cost | ~2 days | draft |
| [Financial Management for Engineers](courses/technical-skills/financial-management-for-engineers/README.md) | Business organization; balance sheet, income statement, cash flow; ratios and dashboards; budgets and variances; time value of money; sources and cost of capital; ROI, NPV, IRR; lease vs buy; sensitivity and Monte Carlo; break-even; valuation and M&A | ~2 days | draft |
| [Technical Communications](courses/technical-skills/technical-communications/README.md) | Presenting quantitative work to managers: common errors, audience analysis, purpose and one-sentence message, answer-first structure, listening and Q&A, data visualization, process-improvement tools for presentations, quality presentations, capstone | 9 × 2 h | draft |
| [Reliability Engineering Excellence](courses/technical-skills/reliability-engineering-excellence/README.md) | Reliability role and program; risk and criticality; design for reliability, RBD, reliability growth; MTBF/MTTR/availability; RCM and TPM; Pareto, exponential, normal and Weibull (with suspensions); LCC and optimum reliability cost; RCA, FRACAS, FMECA; PM optimization; five PdM technologies | ~5 days | draft |
| [Process Modeling and Simulation](courses/technical-skills/process-modeling-and-simulation/README.md) | Discrete-event process models: build to think, validation, design exploration, resilience testing, operating procedures, model-based FMEA, business case, teaching Lean | ~7 h | draft |
### [Work Design & Work Measurement](courses/work-design-work-measurement/README.md)

| Course | Topic | Length | Status |
|---|---|---|---|
| [Work Measurement](courses/work-design-work-measurement/work-measurement/README.md) | Need for and impact of standards; standard practice; documentation and charting; methods analysis and work design; defining work; time study, elemental analysis, rating, allowances, computations; labor reporting; job analysis; work sampling; standard data and PMTS; learning curves and staffing | ~2 days | draft |
| [Standard Data Systems](courses/work-design-work-measurement/standard-data-systems/README.md) | Microscopic vs macroscopic data; advantages and disadvantages; element structure and data sheets; correlation and regression (Excel LINEST/ToolPak); developing models with dummies, transformations and VIF; evaluating with residuals, intervals and hold-out validation; quoting, capacity and maintenance | ~2 days | draft |
| [Staffing Models & Human Capital Management](courses/work-design-work-measurement/staffing-models/README.md) | Staffing models in the HCM framework; terminology; seven data types; work measurement for staffing; available hours and relief factors; workload, coverage, queueing (Erlang C), ratio and benchmark models; forecasting; supply, attrition and hiring plans; development phases, back-testing and sensitivity; budgets and executive summaries | ~2 days | draft |
| [Predetermined Time Standards (MODAPTS Topics)](courses/work-design-work-measurement/predetermined-time-standards/README.md) | Follows the MODAPTS practitioner outline item by item: PMTS basics, acronym, code symbol, history, modular concept, movement classes and rules, get vs put, conscious control, GET/PUT elements, auxiliary activities, practice analyses with an original teaching code card (not the official card), method and ergonomic improvement | ~3 days | draft |
| [Facilities and Workplace Design](courses/work-design-work-measurement/facilities-and-workplace-design/README.md) | Facilities strategy and levels of design; layout planning and project plan; P-Q, inventory, usage, flow and processes; planning units, affinities, space constraints, configuration diagrams; material flow and layout exchange; cellular and workstation layouts; process charting, time estimates, cell capacity, people and machines; ergonomics, motion economy; infrastructure, scheduling, containers, balancing, supervision, rewards; cell configurations and layout procedures | ~2 days | draft |
| [Detailed Motion Time Analysis (MTM-1 Topics)](courses/work-design-work-measurement/detailed-motion-time-analysis/README.md) | Methods analysis and two-handed charts; reach, move, turn, apply pressure, grasp, position, release, disengage, eye and body motions; simultaneous motions; writing analyses; SIMO-based improvement; developing standards; 11 labs. Original teaching data card (not MTM data) | ~10 days with labs | draft |
### [Operations Research & Decision Analysis](courses/operations-research-decision-analysis/README.md)

| Course | Topic | Length | Status |
|---|---|---|---|
| [Engineering Decision Making & Risk Management](courses/operations-research-decision-analysis/engineering-decision-making/README.md) | Decision contexts, objectives, measurement scales; AHP, MAUT, swing weighting; group decisions (Borda, Kemeny-Young, majority judgement); aleatory vs epistemic uncertainty, eliciting probabilities; stochastic dominance, decision trees, risk aversion, expected utility; zero-sum and mixed-motive games; incremental and contingency processes, search, secretary problem; EVPI, EVII; risk treatment, potential problem analysis, warnings, ROC curves, risk communication; learning from failures, sensitivity analysis | ~3 days | draft |
### [Microlearning Refreshers](courses/microlearning-refreshers/README.md)

_No courses yet._

## Role profiles

[roles/](roles/README.md) holds the evidence for the role advisor in [VISION.md](VISION.md):

- **O*NET profiles:** occupation profiles for eight codes around industrial engineering, vendored from the official O*NET database files. Each has rated tasks, knowledge, skills and technology. `python tools/onet_refresh.py` rebuilds them.
- **Course-to-role maps:** written by `/map-course <slug>` in Claude Code. They show which parts of a role each course teaches, with quoted evidence. Every row stays `proposed` until a person confirms it. Quality Engineering Essentials is the first course mapped.
- **Learning-path tracks:** [roles/tracks.md](roles/tracks.md) defines the tracks the site's learning path shows.

O*NET data is used under CC BY 4.0 (U.S. Department of Labor, ETA); the project is not affiliated with or endorsed by USDOL/ETA or BLS.

## Adding a course

1. Pick the category folder under `courses/` that fits, and create `courses/<category>/<course-name>/` (lowercase, hyphenated).
2. Include `README.md` (objectives + syllabus), `modules/`, and `solutions/`, `data/`, `tools/` as needed.
3. Follow the module structure in [CONTRIBUTING.md](CONTRIBUTING.md), then add a row to the category README and to the table above.

## Status, review and legal

Every course is written with AI assistance and is marked `draft` in the tables above until a reviewer has completed [REVIEW.md](REVIEW.md); it then reads `verified (Name, YYYY-MM-DD)`. The review board (`/review-course <slug>` in Claude Code) does the checking and writes its report to [reviews/](reviews/README.md); a person answers its questions and signs off. The site shows the same status on each course. The project is not affiliated with IISE: only the public catalog's course titles and topic lists were used, as a coverage map. See [NOTICE.md](NOTICE.md), and the site's [Privacy Policy](https://theiehub.com/privacy.html), [Terms of Use](https://theiehub.com/terms.html) and [Sources](https://theiehub.com/sources.html) pages (sources in `tools/legal/`). Courses cite their references by ID from `reference/sources.md`; an entry reads verified only after a reviewer checks it.

## License

Content: CC BY 4.0. Code: MIT. See [LICENSE](LICENSE).
