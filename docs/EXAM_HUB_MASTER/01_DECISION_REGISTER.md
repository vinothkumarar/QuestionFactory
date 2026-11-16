# Decision Register

| ID | Area | Decision | Status |
|---|---|---|---|
| D-001 | Product | Exam Hub, AIR-X and Pragatipath are related but distinct product capabilities | Confirmed history |
| D-002 | Scope | College entrance preparation: JEE Main, JEE Advanced, NEET and BITSAT; exclude banking, SSC, UPSC and railways | Confirmed |
| D-003 | Architecture | Student platform and Question Factory OS remain separate systems | Confirmed |
| D-004 | Factory | AMA v1.0 is the governing high-level v3.0 target | Confirmed |
| D-005 | Integration | Factory produces approved CSV for manual Supabase upload; no direct factory DB integration | Confirmed history; verify live operations |
| D-006 | Curriculum | Subject → Unit → Chapter → Subtopic | Confirmed |
| D-007 | Discovery | AI discovers concepts/QPs/archetypes; do not hardcode an exhaustive archetype catalogue | Confirmed |
| D-008 | Planning | Operator defines scope; planner should calculate production workload | Confirmed target; current CLI still accepts questions-per-batch |
| D-009 | Validation | R01–R20 plus DE/AR and technical/coverage validation | Confirmed target; current service container registers R01–R03 only |
| D-010 | Repair | Repaired questions restart validation at R01 | Confirmed target; current orchestrator has one repair/revalidation pass |
| D-011 | Export | Export only after quality and coverage gates pass | Confirmed target; coverage gate not verified |
| D-012 | Engineering | Preserve completed modules; complete-file replacements only for approved fixes | Confirmed |
| D-013 | Quality | Compileall and mypy are required verification gates | Confirmed; current run not performed |
| D-014 | Workflow | Run internal R03 audit and repair/rebuild automatically without per-issue approval | Confirmed |
| D-015 | CSV | Simplified CSV; retain subject_id and remove unnecessary empty fields | Confirmed target; current code still exports 29 columns |
| D-016 | Repository baseline | Audit main at 2a253dc; keep recovery-test separate | Verified |
| D-017 | Blueprint | Do not combine conflicting R01–R12 namespaces | Required reconciliation |
| D-018 | Distractors | Current repo prompt defines DE-01 DR01–DR10 and DE-02 quality rules | Provisional working source |
| D-019 | Archetypes | AR17–AR20 are archetype patterns, not validator rules | Confirmed |
| D-020 | Curriculum | Supabase remains source of truth; repo CSVs are snapshots; in-memory sample is not full curriculum | Confirmed target; implementation gap |
| D-021 | U1 assets | Preserve legacy QPC/QP/archetype files and migrate IDs deliberately | Required |
| D-022 | Coverage | 100% coverage/saturation gate must block export until complete | Confirmed target; not verified |
| D-023 | Branch | Do not merge recovery-test without reviewing raw-response logging and code divergence | Required |
| D-024 | Test evidence | No current CI status or test run was obtained during audit | Not verified |

## Blueprint conflict

Engine/prompts/master/05_blueprint_rules.md defines R01 Concept First through R12 Production Readiness. Blueprint/01_RULES.md defines R01 Continuity through R12 Saturation Monitoring. These are different rule namespaces using the same IDs. A versioned Blueprint v1.5 source file was not found in the audited repository. See 11_DECISION_RECONCILIATION_ADDENDUM.md.