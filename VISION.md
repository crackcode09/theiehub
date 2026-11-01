# Vision: from a course catalog to a role advisor

Recorded 2026-10-27. The public version of this page is the site's [roadmap](https://theiehub.com/roadmap.html).

## Why The IE Hub exists

Industrial engineering makes work safer, faster and less wasteful, and the world needs more of it: it is projected to be among the fastest-growing engineering occupations through 2034 ([BLS](https://www.bls.gov/ooh/architecture-and-engineering/industrial-engineers.htm)). Yet the way people learn it has not kept up. Good material is scattered: much of it sits behind paywalls, in journals or in software sales pitches, and what is free is usually one course or one topic, often frozen years ago. Methods only turn into skill through practice on real problems, and there are few places to get that practice. And plants are losing the people who know how the work really runs, often before anyone has written it down.

The IE Hub is an open answer: the whole field mapped, the methods taught for free, practised on data anyone can rerun, each course checked in public by a named reviewer before it is marked verified, and improved by the people who use it.

**Why open source.** Knowledge that improves how work gets done should be free to read, check and build on. Every course, dataset and line of code here can be inspected, corrected, reused and extended, even commercially (content CC BY 4.0, code MIT; see [LICENSE](LICENSE)). Being open is also how it stays honest: mistakes are visible, and anyone can fix them.

## The end goal

A person comes to the site and names a position close to industrial engineering that they want to work in, for example *continuous improvement engineer*. The site answers, for that position and for the way the market defines it today:

- **what to train**: the knowledge and skills the role actually requires, mapped to the courses here;
- **how to train it**: an ordered plan through those courses, with the time it takes and the prerequisites it assumes;
- **where to focus**: the points that matter most given the ground reality of the role now, including the expectation that engineers in these roles use AI in their work.

Two kinds of evidence anchor the advice, so it is not opinion:

1. **The official standard for the position**: the government occupational description of the role (tasks, knowledge, skills, abilities, tools) such as the O*NET or Bureau of Labor Statistics profile.
2. **The market signal**: what employers currently ask for in postings for the role, so the advice reflects demand rather than a syllabus.

The IISE course catalog gives the map of the discipline; the courses here are the training; the two evidence sources turn that into advice for a named role.

## Stages

| Stage | What exists when it is done | Status |
|---|---|---|
| 1. Catalog | Original courses grouped by the IISE catalog categories; roadmap of coverage; site with catalog, learning path, mind map and reader | done (32 courses, 33 of 102 topics) |
| 2. Trust | Every course verified by a person through the review board (`REVIEW.md`, `/review-course`); status shown on every page; privacy, terms and originality notice | in progress (board built, 0 of 32 verified) |
| 3. Role profiles | A profile per target position: the official standard's tasks, knowledge and skills, plus the market's current asks, each mapped to the courses and modules that teach it | next; O*NET and BLS sources received, postings signal still to find |
| 4. Advisor | The user picks a role (and optionally what they already know); the site produces a training plan, the focus points, and the gaps the catalog cannot yet cover, which feed back into the course roadmap | after 3 |
| 5. Keeping it current | The market signal is refreshed on a schedule and role profiles show what changed, so the advice ages well | after 4 |

## Using O*NET (the official standard)

First source, given 2026-10-27: the O*NET profile for Industrial Engineers, [17-2112.00](https://www.onetonline.org/link/summary/17-2112.00). O*NET publishes, for every occupation, rated lists of tasks, knowledge, skills, abilities, work activities and technology skills (each with an importance score and "in demand" flags derived from job postings), plus education levels and the BLS wage and growth figures. The data is reusable under CC BY 4.0 with attribution and is available as a bulk database download and a web API, so it is read by a script, not copied by hand.

How it is used, stage 3:

1. **Role profile.** A target position is mapped to an O*NET occupation or a weighted blend. "Continuous improvement engineer" is not an O*NET title; it maps to Industrial Engineers with parts of Management Analysts (13-1111) and Industrial Production Managers (11-3051). Related O*NET codes: 17-2112.01 Human Factors Engineers and Ergonomists, 17-2112.02 Validation Engineers, 17-2112.03 Manufacturing Engineers, 15-2031 Operations Research Analysts, 13-1081 Logisticians.
2. **Mapping.** A table in the repo (`roles/`) links each O*NET element to the modules that teach it, for example "Analyze statistical data to set quality and reliability objectives" to Statistical Quality Control, Charting Process Behavior and Fundamentals of Hypothesis Testing; "SQL (in demand)" to the data-model module of Introduction to Engineering Analytics. The mapping is editorial work, reviewed like a course.
3. **Role page.** Three outputs: what the standard says, ranked by importance; where it is taught here, as an ordered training plan with hours and prerequisites; and the gaps, the high-importance elements with no module, which feed the course roadmap as the next things to build.
4. **Focus points.** O*NET's technology list for Industrial Engineers carries no AI tools yet; the standard lags the role. The market signal (second source, to come) sharpens and overrides it, and the role page shows both columns with the date of each.
5. **Currency.** O*NET releases quarterly; a script diffs each release against the stored profile and flags changed elements.

Attribution to carry wherever the data appears: "This page includes information from the O*NET Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA), used under the CC BY 4.0 license. O*NET is a trademark of USDOL/ETA. The IE Hub is not affiliated with or endorsed by USDOL/ETA."

## Using the BLS Occupational Outlook Handbook (the outlook)

Second source, given 2026-10-27: the BLS Occupational Outlook Handbook entry for [Industrial Engineers](https://www.bls.gov/ooh/architecture-and-engineering/industrial-engineers.htm). Where O*NET describes the work in detail, the Handbook describes the role's place in the economy: median pay and the pay range, entry education, licences (PE after the FE and PE exams), the "important qualities", the largest employing industries, the 2025 to 2035 outlook (12 percent growth, about 23,100 openings a year) and what drives it (cost reduction, production optimisation, supply chain and logistics, automation). BLS content is U.S. government work and may be reused; cite it as the source.

How it is used:

1. **The "why" column of a role page.** Outlook, pay range, employers and drivers, so a learner sees what the role is worth and where the demand is, with the BLS release date.
2. **Entry and advancement.** Education, the PE path and the management path, which decide what a training plan should start from and end at.
3. **Demand drivers as focus points.** The Handbook names what pulls demand (automation, supply chain, cost); those become headline focus points that the O*NET elements and the courses are grouped under.
4. **Specialties.** The Handbook's named specialties (human factors, manufacturing, validation) line up with the O*NET sub-codes and become the first set of role profiles beside "industrial engineer".

What is still missing is a **postings-based market signal**: what employers list in current job ads for the role, including AI and data tooling. Neither O*NET nor the Handbook carries that at the granularity needed. Candidate sources: a job-postings dataset or API (for example Lightcast open skills data, or a periodic sample of public postings), summarised into the role page's "market asks" column with its date.

## Principles that do not change

- Original content only; the IISE catalog is a map, not a source.
- A course is `draft` until a named person verifies it.
- Advice cites its evidence: every focus point points at the standard or the market data it comes from.
- Free, open, no accounts, no tracking.
