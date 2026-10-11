/** Pure frame-coordinate recipes. Not a React compiler or renderer adapter. */
function finite(value, name) {
  if (typeof value !== 'number' || !Number.isFinite(value)) throw new TypeError(`${name} must be finite`);
  return value;
}
export function mapFrame(globalFrame, operations = []) {
  let frame = finite(globalFrame, 'globalFrame');
  for (const op of operations) {
    if (op.kind === 'sequence') frame -= finite(op.from, 'sequence.from');
    else if (op.kind === 'freeze') {
      if (op.active !== undefined && typeof op.active !== 'boolean') throw new TypeError('freeze.active must be boolean');
      if (op.active !== false) frame = finite(op.frame, 'freeze.frame');
    } else if (op.kind === 'loop') {
      const duration = finite(op.duration, 'loop.duration');
      if (!Number.isInteger(duration) || duration <= 0) throw new RangeError('loop.duration must be a positive integer');
      frame = ((frame % duration) + duration) % duration;
    } else throw new TypeError(`Unknown clock transform: ${op.kind}`);
  }
  return frame;
}
export function finiteIterations(start, end, duration) {
  finite(start,'start');finite(end,'end');finite(duration,'duration');
  if (![start,end,duration].every(Number.isInteger) || start < 0 || end <= start || duration <= 0) {
    throw new RangeError('Finite integer window and positive duration required');
  }
  const count = Math.ceil((end-start)/duration);
  if (count > 100000) throw new RangeError('Expand fewer than 100001 iterations or use an explicit modulo adapter');
  return Array.from({length:count}, (_,i)=>({start:start+i*duration,end:Math.min(end,start+(i+1)*duration)}));
}
export function cubicCounter(sceneFrame, target, durationFrames=45) {
  finite(sceneFrame,'sceneFrame');finite(target,'target');finite(durationFrames,'durationFrames');
  if (durationFrames<=0) throw new RangeError('durationFrames must be positive');
  const t=Math.max(0,Math.min(1,sceneFrame/durationFrames));
  return Math.round(target*(1-(1-t)**3));
}
