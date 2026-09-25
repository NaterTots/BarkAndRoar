"""Behavioral Web-export checks. Requires a running HTTP server or live Pages URL.

python tests/browser_check.py http://127.0.0.1:8765/ [chromium|webkit]
Audio analysis observes the engine's real output graph; it is not a listening test.
"""
import json
import math
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765/'
BROWSER = sys.argv[2] if len(sys.argv) > 2 else 'chromium'
OUT = Path('test-results') / ('live' if URL.startswith('https:') else 'local') / BROWSER
OUT.mkdir(parents=True, exist_ok=True)
AUDIO_PROBE = r"""
(() => {
  window.audioProbe = {contexts: [], peak: 0, nodes: 0};
  const Native = window.AudioContext || window.webkitAudioContext;
  if (!Native || typeof AudioNode === 'undefined') return;
  const connect = AudioNode.prototype.connect;
  const analysers = new WeakMap();
  AudioNode.prototype.connect = function(destination, ...rest) {
    if (destination instanceof AudioDestinationNode) {
      let analyser = analysers.get(this.context);
      if (!analyser) {
        analyser = this.context.createAnalyser();
        analyser.fftSize = 2048;
        analysers.set(this.context, analyser);
        connect.call(analyser, destination);
        window.audioProbe.contexts.push(this.context);
        const samples = new Float32Array(2048);
        setInterval(() => {
          analyser.getFloatTimeDomainData(samples);
          let peak = 0;
          for (const sample of samples) peak = Math.max(peak, Math.abs(sample));
          window.audioProbe.peak = Math.max(window.audioProbe.peak, peak);
        }, 15);
      }
      window.audioProbe.nodes++;
      return connect.call(this, analyser, ...rest);
    }
    return connect.call(this, destination, ...rest);
  };
})();
"""

results = []
errors = []
failed_requests = []


def record(name, details=None):
    results.append({'check': name, 'result': 'pass', 'details': details})
    print('PASS', name, details or '', flush=True)


with sync_playwright() as p:
    browser = getattr(p, BROWSER).launch(headless=True)
    context = browser.new_context(viewport={'width': 1024, 'height': 768}, has_touch=True)
    context.add_init_script(AUDIO_PROBE)
    page = context.new_page()
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    page.on('response', lambda r: failed_requests.append([r.url, r.status]) if r.status >= 400 else None)
    page.goto(URL + ('&' if '?' in URL else '?') + 'qa=1')
    if not page.evaluate("!!(window.AudioContext || window.webkitAudioContext)"):
        report = {'url': URL, 'browser': BROWSER, 'version': browser.version, 'result': 'unavailable', 'reason': 'This browser build exposes neither AudioContext nor webkitAudioContext. It cannot validate required audio.', 'console_errors': errors}
        (OUT / 'results.json').write_text(json.dumps(report, indent=2), encoding='utf8')
        page.screenshot(path=str(OUT / 'unavailable.png'))
        print('UNAVAILABLE', report['reason'], flush=True)
        browser.close()
        raise SystemExit(2)
    page.wait_for_function('window.barkReady === true && window.barkState', timeout=90000)
    page.screenshot(path=str(OUT / 'play.png'))

    def state():
        page.wait_for_timeout(130)
        return page.evaluate('window.barkState')

    def expect(expression):
        page.wait_for_function(expression, timeout=5000)

    assert state()['playing'] is False
    assert page.evaluate('window.audioProbe.peak') == 0
    page.touchscreen.tap(512, 384)
    expect('window.barkState.playing')
    assert [a['activations'] for a in state()['animals']] == [0, 0]
    record('Fresh load silent; play gesture enters toy without an animal activation')

    for i, x in enumerate([240, 780]):
        page.evaluate('window.audioProbe.peak = 0')
        page.touchscreen.tap(x, 380)
        expect(f'window.barkState.animals[{i}].audio')
        expect('window.audioProbe.peak > 0.001')
        sample = state()
        assert sample['animals'][i]['activations'] == 1
        record(f'First animal tap {i}: exactly one activation and nonzero audio output', page.evaluate('({peak:audioProbe.peak, states:audioProbe.contexts.map(c=>c.state)})'))
        page.wait_for_timeout(1400)

    # Mouse shares the coordinator and remains captured across the divider.
    page.mouse.move(12, 12)
    page.mouse.down()
    expect('window.barkState.animals[0].held')
    page.mouse.move(1000, 700, steps=5)
    s = state()
    assert s['animals'][0]['held'] and not s['animals'][1]['held']
    assert 0 < math.hypot(*s['animals'][0]['offset']) <= 52
    page.mouse.up()
    expect('window.barkState.owners === 0 && Math.abs(window.barkState.animals[0].offset[0]) < 1')
    record('Panel edge mouse press, clamped cross-divider drag, outside-panel release')

    before = [a['activations'] for a in state()['animals']]
    for x, y in [(4,4),(508,4),(4,764),(508,764),(516,4),(1020,4),(516,764),(1020,764)]:
        page.touchscreen.tap(x,y)
    assert [a['activations'] for a in state()['animals']] == [n+4 for n in before]
    record('All eight panel corners activate their correct animal once')
    page.wait_for_timeout(1400)

    if BROWSER == 'chromium':
        cdp = context.new_cdp_session(page)

        def touch(kind, points):
            cdp.send('Input.dispatchTouchEvent', {'type': kind, 'touchPoints': [
                {'id': n, 'x': x, 'y': y, 'radiusX': 4, 'radiusY': 4, 'force': 1}
                for n, x, y in points]})

        touch('touchStart', [(1, 250, 380), (2, 780, 380)])
        expect('window.barkState.owners === 2 && window.barkState.animals.every(a=>a.held && a.audio)')
        before = [a['activations'] for a in state()['animals']]
        touch('touchStart', [(1, 250, 380), (2, 780, 380), (3, 50, 50)])
        s = state()
        assert s['owners'] == 2
        assert [a['activations'] for a in s['animals']] == before
        touch('touchMove', [(1, 900, 380), (2, 100, 380), (3, 50, 50)])
        s = state()
        assert s['animals'][0]['offset'][0] > 0 and s['animals'][1]['offset'][0] < 0
        touch('touchEnd', [])
        expect('window.barkState.owners === 0')
        record('Two simultaneous touch/audio reactions; third finger ignored; independent cross-divider capture')
        touch('touchStart', [(1, 250, 380)])
        touch('touchCancel', [])
        expect('window.barkState.owners === 0 && window.barkState.animals.every(a=>!a.held)')
        if not state()['playing']:
            page.touchscreen.tap(512, 384)
        record('Browser touch cancellation clears ownership')

    page.wait_for_timeout(1400)
    before = state()['animals'][1]
    for _ in range(12):
        page.touchscreen.tap(900, 700)
        page.wait_for_timeout(12)
    after = state()['animals'][1]
    assert after['activations'] - before['activations'] == 12
    assert after['sound_starts'] - before['sound_starts'] < 12
    assert all(a['players'] == 1 for a in state()['animals'])
    page.wait_for_timeout(1500)
    assert not any(a['audio'] for a in state()['animals'])
    record('Rapid taps animate each time with one player per animal and no queued audio')

    # Resize while held must clear stale input and update coordinate mapping.
    page.mouse.move(250, 380)
    page.mouse.down()
    page.mouse.move(340, 420)
    page.set_viewport_size({'width': 768, 'height': 1024})
    expect('window.barkState.owners === 0')
    page.mouse.up()
    page.wait_for_timeout(500)
    before = [a['activations'] for a in state()['animals']]
    page.touchscreen.tap(750, 12)
    page.touchscreen.tap(12, 1000)
    after = [a['activations'] for a in state()['animals']]
    assert after == [n+1 for n in before]
    record('Rotation during drag resets ownership; portrait top/bottom edge hit targets align')
    page.wait_for_timeout(1400)
    for width, height in [(768, 1024), (1024, 768), (1180, 820), (820, 1180)]:
        page.set_viewport_size({'width': width, 'height': height})
        page.wait_for_timeout(350)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth && document.documentElement.scrollHeight <= innerHeight')
        page.screenshot(path=str(OUT / f'{width}x{height}.png'))
    record('Four portrait/landscape viewport screenshots; no required page scrolling')

    page.touchscreen.tap(300, 300)
    page.evaluate("window.dispatchEvent(new Event('blur'))")
    expect('!window.barkState.playing && window.barkState.owners === 0 && window.barkState.animals.every(a=>!a.audio)')
    page.touchscreen.tap(400, 590)
    page.evaluate('window.audioProbe.peak = 0')
    page.touchscreen.tap(300, 300)
    expect('window.barkState.animals[0].audio && window.audioProbe.peak > 0.001')
    record('Simulated focus loss stops audio and gates play; next gestures restore nonzero audio')

    # Headless tabs stay visible, so explicitly simulate the visibility lifecycle.
    page.evaluate("Object.defineProperty(document, 'hidden', {get:()=>true, configurable:true}); document.dispatchEvent(new Event('visibilitychange')); delete document.hidden;")
    expect('!window.barkState.playing && window.barkState.animals.every(a=>!a.audio)')
    page.touchscreen.tap(400,590)
    page.evaluate('window.audioProbe.peak = 0')
    page.touchscreen.tap(300,300)
    expect('window.audioProbe.peak > 0.001')
    record('Simulated hidden-document lifecycle gates play; return gestures restore audio')
    assert not errors, errors
    assert not failed_requests, failed_requests
    record('No JavaScript/application console errors or HTTP asset failures')
    for resource in ['index.js', 'index.wasm']:
        failure_page = context.new_page()
        failure_page.route('**/' + resource, lambda route: route.abort())
        failure_page.goto(URL)
        failure_page.wait_for_function("document.getElementById('notice').textContent.includes('could not wake up')", timeout=30000)
        assert failure_page.locator('#status').is_visible()
        failure_page.close()
        record(f'Parent-readable error when {resource} download fails')
    report = {'url': URL, 'browser': BROWSER, 'version': browser.version, 'checks': results, 'errors': errors, 'failed_requests': failed_requests, 'limitations': 'Emulation only. Human listening, actual Safari toolbar/lock and 15–30 minute iPad stability remain pending.'}
    (OUT / 'results.json').write_text(json.dumps(report, indent=2), encoding='utf8')
    browser.close()
