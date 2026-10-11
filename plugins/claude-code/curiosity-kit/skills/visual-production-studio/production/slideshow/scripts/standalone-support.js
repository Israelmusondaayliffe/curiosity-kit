/* Local, framework-neutral support for the documented bare-player harness.
 * These helpers do not implement or replace HyperFrames' player/controller.
 */
(function (global) {
  'use strict';
  const PREFIX = 'hf-slideshow:presenter-notes:v1:';
  function isMedia(el) {
    const RealmMedia = el && el.ownerDocument && el.ownerDocument.defaultView && el.ownerDocument.defaultView.HTMLMediaElement;
    return Boolean(RealmMedia && el instanceof RealmMedia);
  }
  function muteMedia(doc, muted, detached = []) {
    for (const el of [...doc.querySelectorAll('audio,video'), ...detached]) {
      if (isMedia(el)) el.muted = Boolean(muted);
    }
  }
  function stopSlideMedia(doc, oldPosition, newPosition) {
    if (oldPosition && newPosition && oldPosition.sequenceId === newPosition.sequenceId &&
        oldPosition.slideIndex === newPosition.slideIndex) return false;
    // Call this on the composition document, never the top-level deck audio.
    for (const el of doc.querySelectorAll('audio,video')) if (isMedia(el)) el.pause();
    return true;
  }
  function notesDeckKey(el) {
    const explicit = el.getAttribute('notes-storage-key');
    if (explicit && explicit.trim()) return explicit.trim();
    const src = el.querySelector('hyperframes-player')?.getAttribute('src') || '';
    let resolved = src; try { resolved = new URL(src, location.href).href; } catch (_) {}
    return `${location.origin}${location.pathname}|${document.title}|${resolved}`;
  }
  function notesStorageKey(el, position, slide) {
    return PREFIX + JSON.stringify([notesDeckKey(el), position.sequenceId, position.slideIndex, slide.sceneId || '']);
  }
  function readNotes(el, position, slide) {
    try { const value = localStorage.getItem(notesStorageKey(el, position, slide)); return value === null ? slide.notes || '' : value; }
    catch (_) { return slide.notes || ''; }
  }
  function saveNotes(el, position, slide, value) {
    try { localStorage.setItem(notesStorageKey(el, position, slide), String(value)); return true; }
    catch (_) { return false; }
  }
  function bridgeGuard(event, sourceWindow, origin, channel, acceptedTypes) {
    if (!sourceWindow || typeof origin !== 'string' || origin === 'null' || !/^https?:\/\//.test(origin)) return false;
    if (event.source !== sourceWindow || event.origin !== origin) return false;
    const msg=event.data;
    return Boolean(msg && typeof msg === 'object' && !Array.isArray(msg) &&
      typeof channel === 'string' && channel.length > 0 && msg.channel === channel && acceptedTypes.includes(msg.type));
  }
  function postToParent(payload, origin, channel) {
    if (origin === 'null' || !/^https?:\/\//.test(origin) || !channel) throw new Error('Use an exact HTTP(S) parent origin and deck channel');
    parent.postMessage({...payload, channel}, origin);
  }
  function sceneVisibility(el, active) {
    el.style.opacity=active?'1':'0';el.style.visibility=active?'visible':'hidden';el.style.pointerEvents=active?'auto':'none';
  }
  function fragmentVisibility(el, time, threshold) {
    if (![time,threshold].every(Number.isFinite)) throw new TypeError('Fragment times must be finite');
    sceneVisibility(el,time>=threshold);
  }
  global.HFStandaloneSupport=Object.freeze({isMedia,muteMedia,stopSlideMedia,notesDeckKey,notesStorageKey,readNotes,saveNotes,bridgeGuard,postToParent,sceneVisibility,fragmentVisibility});
})(window);
