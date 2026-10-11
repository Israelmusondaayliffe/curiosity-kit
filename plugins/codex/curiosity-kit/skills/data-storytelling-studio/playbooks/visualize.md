# Make and audit meaningful exhibits

Inputs: actual checked values or supplied visual, the intended claim, metric definitions, audience and source. Output: a useful exhibit with caption/source/accessible explanation, or a specific audit verdict and repair. Read supplied images through an actual image-capable tool when possible; text extraction cannot establish the visual's encoding or legibility.

## Choose an encoding for the question

- Compare categories: aligned bars or dots with direct labels. Bars need a zero baseline because length encodes magnitude; a narrower dot-plot domain must be explicit and justified.
- Follow time: line chart with true time spacing, chronological order and gaps shown as missing. Do not interpolate absent observations into fact.
- Examine a relationship: scatterplot with actual paired observations. Association and a fitted line do not establish causality.
- Show a distribution: histogram, boxplot or interval display appropriate to the supplied analysis. Define bins and interval meaning; do not invent raw observations from a mean.
- Show composition: a common-baseline stacked view or simple labeled shares when the components use the same whole. Shares need a known denominator; overlapping groups cannot be treated as a partition.
- Compare multiple groups: small multiples or a deliberately limited set of directly labeled series with consistent scales. Check whether aggregation hides an important segment reversal.
- Show exact values or weak visual differences: a clear table may be the best exhibit. Use no chart when it adds no comprehension.

Choose native spreadsheet/chart tools when adequate. The bundled [chart CLI](../references/tools.md#local-dot-plot) renders categorical dots and optional supplied intervals from checked CSV columns. It preserves row order and does not calculate findings. Other encodings need an available plotting/artifact tool. Do not use generative image output as a precise quantitative chart.

## Construct the exhibit

Write its proposed takeaway before styling. Identify the exact source rows/cells, metric, unit, population, time window, denominator and comparison. Use the supplied precision, not cosmetic extra decimals. If derived display quantities are necessary, document their formula and authority; don't silently recompute the analysis.

Give the exhibit one clear job. Title it with a supported message; label axes and units, endpoints or meaningful dates, series and material exclusions. Place a material caveat with the exhibit. Include exact source location/version and an accessible text summary or adjacent data table. Do not rely on color alone; use labels, shapes or patterns. Use restrained color for the relevant comparison, with legible contrast and type at the real export size.

Keep comparable panels on comparable axes. If a scale differs, show it unmistakably and explain why. Avoid dual axes or pictorial area encodings when a simpler aligned view answers the question. A log scale is a substantive transformation and must be labeled. Do not rank unknown values with zero, connect across missing periods or hide an excluded group without disclosure. Respect supplied privacy/suppression rules; do not expose individual records in a chart or its embedded metadata.

## Audit all seven dimensions

For each material exhibit, record actual observations and a verdict:

1. Claim scope: do title and caption match measured population, period and metric?
2. Denominator/baseline: is the whole or comparison base known and visible where needed?
3. Encoding: do position, length, area, scale, order and aggregation preserve the relationship?
4. Comparability: are definitions, samples and windows comparable, or is the difference stated?
5. Uncertainty: are missing data, sample limits, supplied intervals and observational limits visible when material?
6. Accessibility: can the reader distinguish and read content without color alone, including the export?
7. Action fit: does the exhibit answer the reader's question without implying an unsupported choice?

Pass means no material issue changes interpretation. Revise means evidence can support the message but display/copy/accessibility needs repair. Block the affected claim when evidence is absent, contradictory, incomparable or materially weaker than it. A causal headline over observational data cannot pass because the chart's numbers are correct.

## Repair and inspect

Separate analysis problems from encoding, copy and accessibility problems. Do not alter source rows to force a pass. Fix the smallest affected part, then rerender and inspect the actual final visual. Compare point/bar values against the selected source, read annotations at intended size, check clipping and the non-color route, and open exported files. A parse success cannot establish these observations.

Return the corrected exhibit and its meaningful caveat, or the exact blocked source/claim and requested analytical resolution. Preserve unaffected elements. When image viewing is unavailable, state visual inspection unverified and complete only the checks actually possible.
