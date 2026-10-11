#!/usr/bin/env python3
"""Run one candidate deterministic control in temporary fixtures.

No original-arm reproduction and no model qualification is performed here.
A zero exit means assertions passed, including expected rejection cases.
"""
import argparse
import io
import json
import sys
import unittest

CONTROLS = {
 'C2-active-time': ['test_state_controls.StateControls.test_c2_approval_and_paused_idle_excluded_active_usage_monotonic'],
 'C5-observed-writes': ['test_state_controls.StateControls.test_c5_own_run_ledger_excluded_from_output_snapshot',
                       'test_state_controls.StateControls.test_c5_legitimate_parallel_writer_changes_are_separated',
                       'test_state_controls.StateControls.test_c5_observed_declared_write_hashes_complete',
                       'test_state_controls.StateControls.test_c5_missing_or_forged_writeset_evidence_rejected',
                       'test_state_controls.StateControls.test_c5_undeclared_write_or_deletion_rejected'],
 'C8-successor-history': ['test_state_controls.StateControls.test_c8_new_approved_successor_preserves_exhausted_history'],
 'C9-terminal-receipt': ['test_engine_lifecycle.LifecycleControls.test_c9_stop_preserves_terminal_verdict_receipts'],
 'C12-peer-discovery': ['test_state_controls.StateControls.test_c12_target_peer_autoprobe_before_state_creation'],
 'C14-required-criterion': ['test_review_controls.ReviewControls.test_c14_required_quality_failure_vetoes_majority',
                            'test_engine_lifecycle.LifecycleControls.test_c14_required_failure_full_finalizer_not_dissent',
                            'test_engine_lifecycle.LifecycleControls.test_finalizer_dissent_state_handoff_report_preserved'],
 'N1': ['test_state_controls.StateControls.test_n1_frozen_question_change_detected',
        'test_planning_controls.PlanningControls.test_n1_reader_question_mutation_rejected',
        'test_review_controls.ReviewControls.test_contract_hash_covers_question_set',
        'test_inspection_controls.InspectionControls.test_n1_reader_questions_cannot_be_substituted'],
 'N2': ['test_review_controls.ReviewControls.test_n2_false_plan_hash_never_passes',
        'test_engine_lifecycle.LifecycleControls.test_n2_hash_false_full_lifecycle_cannot_verify'],
 'N3': ['test_engine_lifecycle.LifecycleControls.test_n3_round_replay_is_idempotent_not_second_win',
        'test_state_controls.StateControls.test_launch_replay_does_not_spend_or_relaunch'],
 'N4': ['test_planning_controls.PlanningControls.test_n4_duplicate_and_out_of_order_waves'],
 'N5': ['test_state_controls.StateControls.test_n5_counters_cannot_decrease'],
 'N6': ['test_planning_controls.PlanningControls.test_n6_parallel_overlap_and_aliases',
        'test_planning_controls.PlanningControls.test_n6_symlink_escape_and_protected_bar',
        'test_state_controls.StateControls.test_n6_parallel_nested_write_overlap_refused'],
 'N7': ['test_state_controls.StateControls.test_n7_exhaustion_never_certifies',
        'test_review_controls.ReviewControls.test_n7_capped_or_unready_eligibility_cannot_verify',
        'test_planning_controls.PlanningControls.test_n7_capped_work_is_not_ready_or_integrated'],
 'N8': ['test_planning_controls.PlanningControls.test_n8_diamond_readiness',
        'test_planning_controls.PlanningControls.test_n8_stale_predecessor_blocks_dependents',
        'test_engine_lifecycle.LifecycleControls.test_project_dependency_dispatch_acceptance_integration_final'],
 'D4-brief': ['test_inspection_controls.InspectionControls.test_brief_completeness_and_external_bar_controls',
              'test_inspection_controls.InspectionControls.test_cli_brief_success_and_failure'],
 'D4-blind': ['test_review_controls.ReviewControls.test_cli_blind_packet_is_neutral_and_overwrite_refused',
              'test_engine_lifecycle.LifecycleControls.test_snapshot_changed_between_dispatch_and_record_rejected'],
 'D4-target-identity': ['test_engine_lifecycle.LifecycleControls.test_cli_verification_target_substitution_rejected',
                        'test_engine_lifecycle.LifecycleControls.test_cli_multiapproved_targets_partial_coverage_rejected',
                        'test_engine_lifecycle.LifecycleControls.test_verification_only_symlink_alias_resolves_to_frozen_identity'],
 'D4-no-gap': ['test_engine_lifecycle.LifecycleControls.test_no_material_gap_pass_and_blind_win_accepted',
               'test_engine_lifecycle.LifecycleControls.test_no_gap_failing_or_losing_verdict_refused'],
 'D4-review-capacity': ['test_engine_lifecycle.LifecycleControls.test_repair_builder_refused_when_its_review_cannot_fit',
                        'test_engine_lifecycle.LifecycleControls.test_repair_builder_allowed_when_review_capacity_remains'],
 'D4-round-ownership': ['test_engine_lifecycle.LifecycleControls.test_cli_round_artifact_outside_approved_scope_rejected',
                        'test_engine_lifecycle.LifecycleControls.test_cli_round_cross_workstream_output_rejected'],
 'D4-smoother': ['test_engine_lifecycle.LifecycleControls.test_smoother_verification_only_forbidden',
                 'test_engine_lifecycle.LifecycleControls.test_smoother_artifact_resets_wins_and_excluded_from_self_grade',
                 'test_engine_lifecycle.LifecycleControls.test_smoother_project_invalidates_dependents_and_integration'],
 'D4-rubric': ['test_engine_lifecycle.LifecycleControls.test_nonblind_rubric_real_evidence_without_fake_pairing',
               'test_engine_lifecycle.LifecycleControls.test_nonblind_claimed_pass_below_frozen_threshold_refused'],
 'D4-consensus': ['test_engine_lifecycle.LifecycleControls.test_finalizer_dissent_state_handoff_report_preserved',
                  'test_review_controls.ReviewControls.test_consensus_table',
                  'test_review_controls.ReviewControls.test_partial_panel_duplicate_session_and_builder_refused',
                  'test_review_controls.ReviewControls.test_four_independent_votes_cover_three_perspectives',
                  'test_review_controls.ReviewControls.test_context_contamination_and_missing_perspectives',
                  'test_engine_lifecycle.LifecycleControls.test_happy_artifact_rounds_panel_report_and_replay'],
 'D4-lock': ['test_state_controls.StateControls.test_lock_serializes_subprocess_writers',
             'test_state_controls.StateControls.test_recovery_preserves_reservation_accounting_and_disk_resume'],
 'D4-handoff': ['test_state_controls.StateControls.test_handoff_and_report_derive_from_state'],
 'D4-approval': ['test_state_controls.StateControls.test_approval_required_before_launch'],
 'D4-knowledge': ['test_engine_lifecycle.LifecycleControls.test_knowledge_reader_claims_two_plus_two_final_negative_exports',
                  'test_inspection_controls.InspectionControls.test_contradicted_and_unsupported_both_survive',
                  'test_inspection_controls.InspectionControls.test_false_quote_hash_or_missing_source_refused',
                  'test_inspection_controls.InspectionControls.test_reader_guess_is_gap'],
 'D5-peer': ['test_state_controls.StateControls.test_d5_peer_absent_active_both_named_before_state',
             'test_state_controls.StateControls.test_d5_peer_terminal_read_from_run_log_not_manifest'],
 'D5-advisor': ['test_advisor_controls.AdvisorControls'],
 'D7-precheck': ['test_state_controls.StateControls.test_d7_degraded_recorded_and_unsupported_refused'],
 'D7-drift': ['test_state_controls.StateControls.test_d7_capability_drift_blocks_before_dispatch'],
}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('control',choices=sorted(CONTROLS))
    a=p.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromNames(CONTROLS[a.control])
    log=io.StringIO();result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    sys.stderr.write(log.getvalue())
    print(json.dumps({'control':a.control,'passed':result.wasSuccessful(),'tests_run':result.testsRun,
        'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
        'fixtures':'Synthetic temporary files and explicit synthetic host attestations; no model proof',
        'limitation':'Candidate regression only. Original reproductions and independent host benchmark remain separate.'},sort_keys=True))
    return 0 if result.wasSuccessful() and not result.skipped else 1
if __name__=='__main__':sys.exit(main())
