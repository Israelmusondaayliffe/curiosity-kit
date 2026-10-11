#!/usr/bin/env python3
"""Gauntlet local CLI. No models, network, installation, or external execution."""
import argparse
import json
import sys
import state


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = ('init', 'approve', 'launch', 'complete', 'round', 'recover', 'resume', 'pause', 'stop',
                'usage', 'integrate', 'finalize', 'precheck', 'verify', 'handoff', 'report', 'advisor-validate')
    parser.add_argument('command', choices=commands)
    parser.add_argument('--run-dir')
    parser.add_argument('--input', help='JSON input path; use - for stdin')
    parser.add_argument('--context', help='Advisor canonical context JSON')
    parser.add_argument('--packet', help='Advisor composition packet JSON')
    args = parser.parse_args(argv)
    try:
        if args.command == 'advisor-validate':
            import advisor
            if not args.context or not args.packet:
                parser.error('advisor-validate needs --context and --packet')
            result = advisor.validate_composition(state.read_json(args.packet), state.read_json(args.context))
        else:
            if args.command != 'precheck' and not args.run_dir:
                parser.error('--run-dir is required')
            if args.command in ('verify', 'handoff', 'report'):
                result = getattr(state, args.command)(args.run_dir)
            else:
                if not args.input:
                    parser.error('--input is required')
                data = state.parse_json(sys.stdin.read()) if args.input == '-' else state.read_json(args.input)
                if args.command == 'precheck':
                    result = state.precheck(data)
                else:
                    name = {'init': 'init_run', 'round': 'record_round'}.get(args.command, args.command)
                    result = getattr(state, name)(args.run_dir, data)
        print(json.dumps(result, indent=2, allow_nan=False))
        if args.command == 'finalize' and result['consensus'] not in ('verified', 'verified-with-dissent'):
            return 1
        if args.command == 'launch' and not result.get('may_launch') and not result.get('replayed'):
            return 1
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
