#!/usr/bin/env node
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { readFileSync } from 'node:fs';
import { loadPlan } from './lib/music-plan.mjs';

const HELP = `Usage: node validate-plan.mjs [options]

Validate a music storyboard against its canonical audio map and recipe catalog.

Options:
  --hyperframes <directory>  Project directory (default: current directory)
  --storyboard <file>        Storyboard (default: <project>/STORYBOARD.md)
  --audiomap <file>          Audio map (default: <project>/audiomap.json)
  --templates <directory>   Template catalog (default: this method's templates)
  --help, -h                Show this help without reading project files

Exit codes: 0 for help or a valid plan; 1 for invalid arguments or validation failure.
`;

function parseArgs(args) {
  const options = {};
  const valueFlags = new Set(['--hyperframes', '--storyboard', '--audiomap', '--templates']);
  for (let i = 0; i < args.length; i++) {
    const flag = args[i];
    if (flag === '--help' || flag === '-h') {
      options.help = true;
      continue;
    }
    if (!valueFlags.has(flag)) throw new Error(`Unknown argument: ${flag}`);
    if (Object.hasOwn(options, flag)) throw new Error(`Repeated option: ${flag}`);
    const value = args[++i];
    if (!value || value.startsWith('-')) throw new Error(`Missing value for ${flag}`);
    options[flag] = value;
  }
  return options;
}

try {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    process.stdout.write(HELP);
  } else {
    const root = resolve(options['--hyperframes'] ?? '.');
    const own = dirname(fileURLToPath(import.meta.url));
    const primitives = JSON.parse(
      readFileSync(join(own, '../references/implementation-manifest.json'), 'utf8'),
    ).primitives.map((item) => item.id);
    const { plan } = loadPlan(
      resolve(options['--storyboard'] ?? join(root, 'STORYBOARD.md')),
      resolve(options['--audiomap'] ?? join(root, 'audiomap.json')),
      {
        project: root,
        templates: resolve(options['--templates'] ?? join(own, '../references/templates')),
        primitives,
      },
    );
    console.log(JSON.stringify({
      status: 'PASS',
      frames: plan.frames.length,
      groups: plan.frames.reduce((count, frame) => count + frame.groups.length, 0),
      duration: plan.duration,
      canvas: plan.canvas,
    }));
  }
} catch (error) {
  console.error(JSON.stringify({ status: 'FAIL', error: error.message }));
  process.exitCode = 1;
}
