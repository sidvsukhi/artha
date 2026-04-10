# Artha Language Specification
## Version 0.1.0

> Artha (Sanskrit: अर्थ) — meaning "essence", "purpose", "meaning"
> A token-efficient communication protocol for human-AI interaction.

---

## 1. Philosophy

Artha is built on one principle:
**Every token must carry meaning. Nothing else survives.**

Natural language is optimised for humans — full of grammar, filler,
redundancy, and social convention. Artha strips all of that away,
leaving only pure communicative intent.

Artha is not a replacement for English. It is a compression layer
between human intent and machine understanding.

---

## 2. Core Syntax

Every Artha statement follows this structure:
ACTIONINPUT → {OUTPUT} | CONSTRAINTS ^CONTEXT

All parts except ACTION are optional.

### Examplessum[doc](#3, fmt:bullets) +facts -opinions
gen[email](to:client, tone:formal) ~150w
fixcode → {diff+explain}
cmp[react, vue] → {table} +perf *speed
xplconcept → {simple}

---

## 3. Actions (60+)

### 3.1 Content Generation
| Symbol | Meaning | English Equivalent |
|--------|---------|-------------------|
| `gen`  | generate/create/write | "write", "create", "draft", "produce" |
| `sum`  | summarise | "summarise", "summarize", "tldr" |
| `xpl`  | explain | "explain", "describe", "elaborate" |
| `ref`  | rewrite/rephrase | "rewrite", "rephrase", "reframe" |
| `fmt`  | format/restructure | "format", "restructure", "organise" |
| `ext`  | extract | "extract", "pull out", "find", "get" |
| `cls`  | classify | "classify", "categorise", "label" |
| `rank` | rank/order | "rank", "order", "sort", "prioritise" |
| `cmp`  | compare | "compare", "contrast", "diff" |
| `rev`  | review/critique | "review", "critique", "evaluate" |
| `fix`  | fix/debug | "fix", "debug", "correct", "repair" |
| `opt`  | optimise | "optimise", "improve", "enhance" |
| `exp`  | expand | "expand", "elaborate", "add detail" |
| `cut`  | shorten | "shorten", "condense", "trim" |
| `mrg`  | merge | "merge", "combine", "consolidate" |
| `spl`  | split | "split", "divide", "separate" |
| `tns`  | translate | "translate", "convert language" |
| `cnv`  | convert format | "convert", "transform", "change to" |
| `fil`  | filter | "filter", "remove", "clean" |
| `tag`  | tag/label | "tag", "annotate", "label" |

### 3.2 Analysis & Reasoning
| Symbol | Meaning | English Equivalent |
|--------|---------|-------------------|
| `anl`  | analyse | "analyse", "analyze", "examine" |
| `inf`  | infer | "infer", "deduce", "conclude" |
| `val`  | validate | "validate", "verify", "check" |
| `prd`  | predict | "predict", "forecast", "estimate" |
| `hyp`  | hypothesise | "hypothesise", "theorise", "what if" |
| `dbg`  | debug/trace | "debug", "trace", "step through" |
| `bch`  | benchmark | "benchmark", "measure", "profile" |
| `tst`  | test | "test", "verify", "assert" |
| `scr`  | score/rate | "score", "rate", "grade" |
| `map`  | map/relate | "map", "relate", "connect" |

### 3.3 Data Operations
| Symbol | Meaning | English Equivalent |
|--------|---------|-------------------|
| `qry`  | query | "query", "search", "look up" |
| `agg`  | aggregate | "aggregate", "group", "count" |
| `srt`  | sort | "sort", "order by", "arrange" |
| `idx`  | index | "index", "catalogue", "organise" |
| `jn`   | join | "join", "merge datasets", "combine" |
| `trn`  | transform | "transform", "apply function to" |
| `nrm`  | normalise | "normalise", "standardise", "clean" |
| `enc`  | encode | "encode", "compress", "serialise" |
| `dec`  | decode | "decode", "decompress", "parse" |
| `prs`  | parse | "parse", "read structure of" |

### 3.4 Code Operations
| Symbol | Meaning | English Equivalent |
|--------|---------|-------------------|
| `impl` | implement | "implement", "code", "build" |
| `rfct` | refactor | "refactor", "restructure code" |
| `doc`  | document | "document", "add comments" |
| `test` | write tests | "write tests", "add unit tests" |
| `rev`  | code review | "review code", "check code" |
| `sec`  | security check | "check security", "find vulnerabilities" |
| `perf` | performance check | "optimise performance", "find bottlenecks" |
| `mig`  | migrate | "migrate", "port", "upgrade" |
| `dep`  | deploy | "deploy", "ship", "release" |
| `api`  | design API | "design API", "create endpoints" |

### 3.5 Communication
| Symbol | Meaning | English Equivalent |
|--------|---------|-------------------|
| `eml`  | email | "write email", "draft email" |
| `msg`  | message | "write message", "draft message" |
| `rpt`  | report | "write report", "create report" |
| `prs`  | presentation | "create presentation", "make slides" |
| `pch`  | pitch | "write pitch", "create pitch deck" |
| `bio`  | biography | "write bio", "create profile" |
| `pst`  | post | "write post", "create content" |
| `thr`  | thread | "write thread", "create thread" |

### 3.6 Reasoning & Planning
| Symbol | Meaning | English Equivalent |
|--------|---------|-------------------|
| `pln`  | plan | "plan", "create roadmap", "outline" |
| `str`  | strategise | "strategise", "create strategy" |
| `brk`  | breakdown | "break down", "decompose", "split into steps" |
| `est`  | estimate | "estimate", "approximate", "calculate" |
| `sim`  | simulate | "simulate", "model", "run scenario" |
| `dec`  | decide | "decide", "choose", "recommend" |
| `rsn`  | reason | "reason through", "think through" |
| `arg`  | argue | "argue for", "make case for" |
| `cnt`  | counter | "counter argue", "argue against" |
| `pro`  | pros/cons | "pros and cons", "advantages disadvantages" |

---

## 4. Input Types

Input goes inside square brackets `[]`:
sum[doc]           # a document
fix[code]          # code
gen[email]         # email (generated, no input)
cmp[A, B]          # compare two things
anl[data, schema]  # multiple inputs
ext[url]           # a URL
xpl[concept]       # a concept
rev[pr]            # a pull request

### Special Input Keywords
| Symbol | Meaning |
|--------|---------|
| `doc`  | document |
| `code` | code/program |
| `data` | dataset |
| `img`  | image |
| `url`  | web URL |
| `txt`  | plain text |
| `pdf`  | PDF file |
| `csv`  | CSV data |
| `json` | JSON data |
| `sql`  | SQL query |
| `pr`   | pull request |
| `repo` | code repository |
| `api`  | API spec |
| `err`  | error/exception |
| `log`  | log file |

---

## 5. Modifiers

Modifiers go inside parentheses `()`, comma-separated:
sum[doc](#3, fmt:bullets, tone:formal)
gen[code](lang:py, style:typed)
xpl[concept](lvl:5yr, fmt:steps)

### 5.1 Quantity
| Symbol | Meaning |
|--------|---------|
| `#N`   | exactly N items |
| `~N`   | approximately N |
| `>N`   | more than N |
| `<N`   | less than N |
| `Nw`   | N words |
| `Ns`   | N sentences |
| `Np`   | N paragraphs |

### 5.2 Format
| Symbol | Meaning |
|--------|---------|
| `fmt:bullets` | bullet points |
| `fmt:list`    | numbered list |
| `fmt:table`   | table |
| `fmt:json`    | JSON |
| `fmt:md`      | markdown |
| `fmt:html`    | HTML |
| `fmt:csv`     | CSV |
| `fmt:steps`   | numbered steps |
| `fmt:tldr`    | one line summary |
| `fmt:qa`      | Q&A format |
| `fmt:dialog`  | dialogue format |
| `fmt:code`    | code block |
| `fmt:diff`    | diff format |
| `fmt:outline` | outline format |

### 5.3 Tone
| Symbol | Meaning |
|--------|---------|
| `tone:formal`       | formal |
| `tone:casual`       | casual |
| `tone:professional` | professional |
| `tone:friendly`     | friendly |
| `tone:assertive`    | assertive |
| `tone:empathetic`   | empathetic |
| `tone:humorous`     | humorous |
| `tone:academic`     | academic |
| `tone:persuasive`   | persuasive |
| `tone:neutral`      | neutral/objective |

### 5.4 Level
| Symbol | Meaning |
|--------|---------|
| `lvl:eli5`    | explain like I'm 5 |
| `lvl:simple`  | simple language |
| `lvl:mid`     | intermediate |
| `lvl:expert`  | expert level |
| `lvl:Nyr`     | for N year old |
| `lvl:beginner`| beginner |
| `lvl:advanced`| advanced |

### 5.5 Language (spoken)
| Symbol | Meaning |
|--------|---------|
| `lang:en` | English |
| `lang:fr` | French |
| `lang:es` | Spanish |
| `lang:de` | German |
| `lang:hi` | Hindi |
| `lang:zh` | Chinese |
| `lang:ar` | Arabic |
| `lang:pt` | Portuguese |
| `lang:ja` | Japanese |

### 5.6 Programming Language
| Symbol | Meaning |
|--------|---------|
| `code:py`  | Python |
| `code:js`  | JavaScript |
| `code:ts`  | TypeScript |
| `code:rs`  | Rust |
| `code:go`  | Go |
| `code:java`| Java |
| `code:cpp` | C++ |
| `code:sql` | SQL |
| `code:sh`  | Shell/Bash |

### 5.7 Audience
| Symbol | Meaning |
|--------|---------|
| `@dev`      | developers |
| `@mgr`      | managers |
| `@client`   | clients |
| `@student`  | students |
| `@exec`     | executives |
| `@public`   | general public |
| `@expert`   | domain experts |

---

## 6. Output Types

Output format goes after `→` inside `{}`:
fix[code] → {diff}
anl[data] → {json+summary}
cmp[A,B]  → {table+rec}

| Symbol | Meaning |
|--------|---------|
| `{text}`    | plain text (default) |
| `{json}`    | JSON object |
| `{table}`   | formatted table |
| `{bullets}` | bullet list |
| `{steps}`   | numbered steps |
| `{diff}`    | code diff |
| `{summary}` | brief summary |
| `{report}`  | structured report |
| `{code}`    | code block |
| `{outline}` | outline |
| `{rec}`     | recommendation |
| `{score}`   | numerical score |
| `{bool}`    | yes/no answer |
| `{A+B}`     | combine output types |

---

## 7. Constraints

Constraints use `+` (include) and `-` (exclude):
sum[doc] +facts +data -opinions -fluff
gen[essay] +examples -jargon -passive_voice
rev[code] +security +perf -style -formatting

---

## 8. Context

Context uses `^` to provide background assumptions:
fix[code] ^"production system, no breaking changes"
gen[email] ^"previous email thread about project delay"
anl[data] ^"Q3 2024, SaaS metrics, US market"

---

## 9. Control Flow

### 9.1 Sequence (do A then B)
fix[code] >> doc[code]
sum[doc] >> tns(lang:fr)

### 9.2 Conditional (if → then)
val[input] ? fix[input] : gen[report]

### 9.3 Loop (apply to each)
sum[doc*] #each → {bullets}
fix[code*] #each(lang:py)

### 9.4 Parallel (do A and B simultaneously)
sum[doc] || cmp[doc, prev_doc]

---

## 10. Data Types

| Type | Symbol | Example |
|------|--------|---------|
| String | `"..."` | `"hello world"` |
| Number | `N` | `42`, `3.14` |
| Boolean | `T/F` | `T`, `F` |
| List | `[a,b,c]` | `[react, vue, angular]` |
| Range | `N..M` | `1..10` |
| Null | `~` | `~` |
| Reference | `$name` | `$prev_output` |
| Variable | `?name` | `?user_input` |

---

## 11. Complete Examples
Summarise a document in 3 bullets, facts only, no opinions
sum[doc](#3, fmt:bullets) +facts -opinions
Write a formal email to a client about project delay, under 150 words
gen[eml](@client, tone:formal, ~150w) +apologetic ^"2 week delay, technical issues"
Fix Python code, show diff, explain what was wrong
fixcode → {diff+explain}
Compare React vs Vue for a beginner, table format, focus on learning curve
cmpreact, vue → {table} +learning_curve @student
Analyse sales data, output JSON, group by region
anlcsv >> agg(by:region) → {json+summary}
Write tests for this code, then document it
testcode >> doc[code] → {md}
Translate to French, formal tone, keep under 200 words
tns[txt](lang:fr, tone:formal) <200w
Review this PR for security issues only, ignore style
rev[pr] +security -style -formatting → {report}
Plan a 3 month roadmap for a SaaS product, executive audience
pln[roadmap](#3m, @exec, fmt:outline) +milestones +metrics
If code has errors fix them, otherwise document it
val[code] ? fix[code] : doc[code]
Summarise each document in the list
sum[doc*] #each(fmt:tldr) → {bullets}

---

## 12. Versioning

| Version | Status | Coverage |
|---------|--------|----------|
| 0.1.0   | Current | Actions, modifiers, constraints, data types, control flow |
| 0.2.0   | Planned | Native tokenizer, model fine-tuning |
| 1.0.0   | Planned | Full bidirectional protocol, Artha-native LLM |

---

## 13. Design Principles

1. **Every token earns its place** — no filler, no redundancy
2. **Position carries meaning** — order is semantic
3. **Symbols beat words** — only when tokenizer is Artha-native
4. **Composable** — any statement can be piped into another
5. **Unambiguous** — one way to say one thing
6. **Learnable in 10 minutes** — complexity from composition, not memorisation

---

*Artha is open source. MIT License.*
*Contribute at github.com/yourusername/artha*
