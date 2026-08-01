// MEDPATH — field protocol decision engine
// Flow: Adult/Pediatric -> Chief Complaint -> Vitals/Weight -> (Branch select) -> Protocol steps

const GCS_OPTIONS = {
  e: [[4,'Spontaneous'],[3,'To voice'],[2,'To pain'],[1,'None']],
  v: [[5,'Oriented'],[4,'Confused'],[3,'Inappropriate words'],[2,'Incomprehensible sounds'],[1,'None']],
  m: [[6,'Obeys commands'],[5,'Localizes pain'],[4,'Withdraws from pain'],[3,'Abnormal flexion'],[2,'Abnormal extension'],[1,'None']]
};

const state = {
  protocols: null,
  drugs: null,
  drugById: {},
  topics: {},        // topicKey -> {adult: protocolId|null, pediatric: protocolId|null, label}
  chosenDemographic: null,
  chosenTopicKey: null,
  chosenProtocolId: null,
  chosenBranchId: null,
  vitals: null,
};

const app = document.getElementById('app');

// ---------- Data loading ----------
async function loadData(){
  const [protoRes, drugRes] = await Promise.all([
    fetch('data/protocols.json'),
    fetch('data/drugs.json')
  ]);
  state.protocols = (await protoRes.json()).protocols;
  const drugData = await drugRes.json();
  state.drugs = drugData.drugs;
  state.drugs.forEach(d => state.drugById[d.id] = d);

  state.protocols.forEach(p => {
    const key = p.title.replace(/^Pediatric\s+/i, '').trim().toLowerCase();
    if(!state.topics[key]) state.topics[key] = {adult:null, pediatric:null, label: p.title.replace(/^Pediatric\s+/i,'').trim()};
    state.topics[key][p.demographic] = p.id;
  });
}

function protocolById(id){ return state.protocols.find(p => p.id === id); }

// Group protocol sections into friendly, related categories for the complaint grid
const CATEGORY_MAP = {
  'Cardiovascular': 'Heart',
  'Respiratory': 'Breathing',
  'Neurological': 'Neuro',
  'General Medical': 'General',
  'Gastrointestinal': 'Stomach & GI',
  'Toxicology': 'Overdose & Poisoning',
  'Trauma': 'Trauma',
  'OB/GYN': 'OB / Childbirth',
  'Environmental': 'Environmental',
};
function categoryFor(protocol){
  const bare = (protocol.section || '').replace(/^(Adult|Pediatric)\s*/i, '').trim();
  return CATEGORY_MAP[bare] || bare || 'General';
}

// ---------- Router ----------
// The app keeps a real browser history entry per screen so the phone's
// hardware/gesture back button steps back through MEDPATH's own screens
// instead of leaving the app.
let isRestoringHistory = false;
let historyBooted = false;

function snapshotState(){
  return {
    step: state.step,
    chosenDemographic: state.chosenDemographic,
    chosenTopicKey: state.chosenTopicKey,
    chosenProtocolId: state.chosenProtocolId,
    chosenBranchId: state.chosenBranchId,
    vitals: state.vitals,
  };
}

function pushHistory(){
  if(isRestoringHistory) return;
  if(!historyBooted){
    historyBooted = true;
    history.replaceState(snapshotState(), '');
    return;
  }
  history.pushState(snapshotState(), '');
}

function dispatch(){
  if(state.step === 'home') return renderHome();
  if(state.step === 'demographic') return renderDemographic();
  if(state.step === 'ccList') return renderCcList();
  if(state.step === 'branch') return renderBranchSelect();
  if(state.step === 'protocol') return renderProtocolView();
  if(state.step === 'browseAll') return renderBrowseAll();
  if(state.step === 'drugRef') return renderDrugRef();
  if(state.step === 'arrest') return renderArrest();
}

// Start a fresh patient run: clears any vitals/weight collected during a
// previous chief complaint so nothing bleeds over between patients, then
// jumps straight to the branch picker (if the protocol has more than one
// clinical presentation) or straight to the protocol steps.
function beginProtocolRun(protocolId){
  state.chosenProtocolId = protocolId;
  state.vitals = {};
  const proto = protocolById(protocolId);
  if(proto.branches.length > 1){
    state.step = 'branch';
  } else {
    state.chosenBranchId = proto.branches[0].id;
    state.step = 'protocol';
  }
}

function render(){
  window.scrollTo(0,0);
  dispatch();
  pushHistory();
  refreshArrestFab();
}

// Small floating button that appears on any screen while an arrest
// operation is running in the background, so it's one tap to get back to it.
function refreshArrestFab(){
  const fab = document.getElementById('arrestFab');
  if(!fab) return;
  const show = typeof arrestState !== 'undefined' && arrestState.active && state.step !== 'arrest';
  fab.classList.toggle('hidden', !show);
  fab.onclick = () => { state.step = 'arrest'; render(); };
}

window.addEventListener('popstate', (e) => {
  if(!e.state) return;
  isRestoringHistory = true;
  Object.assign(state, e.state);
  render();
  isRestoringHistory = false;
});

function goHome(){
  Object.assign(state, {
    step:'home', chosenDemographic:null, chosenTopicKey:null,
    chosenProtocolId:null, chosenBranchId:null, vitals:null
  });
  render();
}

document.getElementById('brandHome').addEventListener('click', goHome);

function addBackBtn(onClick){
  const backBtn = document.createElement('button');
  backBtn.className = 'back-btn';
  backBtn.innerHTML = '←';
  backBtn.setAttribute('aria-label', 'Back');
  backBtn.addEventListener('click', onClick);
  app.prepend(backBtn);
}

// ---------- Home ----------
function renderHome(){
  const tpl = document.getElementById('tpl-home').content.cloneNode(true);
  app.innerHTML = '';
  app.appendChild(tpl);
  document.getElementById('newPatientBtn').addEventListener('click', () => {
    state.step = 'demographic'; render();
  });
  document.getElementById('browseAllBtn').addEventListener('click', () => {
    state.step = 'browseAll'; render();
  });
  document.getElementById('drugRefBtn').addEventListener('click', () => {
    state.step = 'drugRef'; render();
  });
  document.getElementById('runArrestBtn').addEventListener('click', () => {
    state.step = 'arrest'; render();
  });
  document.getElementById('metaNote').textContent =
    `${state.protocols.length} protocols · ${state.drugs.length} drug references loaded · works offline`;
}

// ---------- Step 1: Demographic ----------
function renderDemographic(){
  const tpl = document.getElementById('tpl-demographic').content.cloneNode(true);
  app.innerHTML = '';
  app.appendChild(tpl);
  addBackBtn(goHome);

  app.querySelectorAll('.choice-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      state.chosenDemographic = btn.dataset.demo;
      state.step = 'ccList'; render();
    });
  });
}

// ---------- Step 2: Chief Complaint grid ----------
function renderCcList(){
  const tpl = document.getElementById('tpl-cc-list').content.cloneNode(true);
  app.innerHTML = '';
  app.appendChild(tpl);
  addBackBtn(() => { state.step = 'demographic'; render(); });

  const input = document.getElementById('ccSearch');
  const grid = document.getElementById('ccGrid');
  const demo = state.chosenDemographic;

  function topicsForDemo(){
    return Object.keys(state.topics)
      .map(k => ({key:k, ...state.topics[k]}))
      .filter(t => t[demo])
      .sort((a,b) => a.label.localeCompare(b.label));
  }

  function makeBox(t){
    const box = document.createElement('button');
    box.className = 'cc-box';
    box.textContent = t.label;
    box.addEventListener('click', () => {
      state.chosenTopicKey = t.key;
      beginProtocolRun(t[demo]);
      render();
    });
    return box;
  }

  function draw(q){
    q = q.trim().toLowerCase();
    let list = topicsForDemo();
    if(q){
      list = list.filter(t => {
        const p = protocolById(t[demo]);
        const pool = [t.label.toLowerCase(), ...(p.chief_complaint_tags||[])];
        return pool.some(x => x.includes(q));
      });
    }
    grid.innerHTML = '';
    if(list.length === 0){
      grid.innerHTML = '<p class="cc-empty">No converted protocol matches yet for this demographic.</p>';
      return;
    }
    if(q){
      // flat results while actively searching
      const flat = document.createElement('div');
      flat.className = 'cc-grid';
      list.forEach(t => flat.appendChild(makeBox(t)));
      grid.appendChild(flat);
      return;
    }
    // grouped by related category when browsing
    const groups = {};
    list.forEach(t => {
      const cat = categoryFor(protocolById(t[demo]));
      (groups[cat] = groups[cat] || []).push(t);
    });
    Object.keys(groups).sort().forEach(cat => {
      const section = document.createElement('div');
      section.className = 'cc-category';
      const title = document.createElement('p');
      title.className = 'cc-category-title';
      title.textContent = cat;
      const catGrid = document.createElement('div');
      catGrid.className = 'cc-grid';
      groups[cat].forEach(t => catGrid.appendChild(makeBox(t)));
      section.appendChild(title);
      section.appendChild(catGrid);
      grid.appendChild(section);
    });
  }

  input.addEventListener('input', () => draw(input.value));
  draw('');
}

function vitalsSummaryHTML(){
  if(!state.vitals) return '';
  const v = state.vitals;
  const items = [];
  if(v.weightLb) items.push(`${Math.round(v.weightLb*10)/10} lb (${parseFloat(v.weight).toFixed(1)} kg)`);
  if(v.hr) items.push(`HR ${v.hr}`);
  if(v.sbp || v.dbp) items.push(`BP ${v.sbp||'?'}/${v.dbp||'?'}`);
  if(v.rr) items.push(`RR ${v.rr}`);
  if(v.spo2) items.push(`SpO2 ${v.spo2}%`);
  if(v.temp) items.push(`Temp ${v.temp}°F`);
  if(v.glucose) items.push(`Glu ${v.glucose}`);
  if(v.gcs) items.push(`GCS ${v.gcs}`);
  return items.map(i => `<span>${i}</span>`).join('');
}

// ---------- Step 3: Branch select ----------
function renderBranchSelect(){
  const tpl = document.getElementById('tpl-branch-select').content.cloneNode(true);
  app.innerHTML = '';
  app.appendChild(tpl);
  const proto = protocolById(state.chosenProtocolId);
  addBackBtn(() => { state.step = 'ccList'; render(); });

  app.querySelector('.protocol-context').textContent = proto.title;

  const list = document.getElementById('branchList');
  proto.branches.forEach(b => {
    const btn = document.createElement('button');
    btn.className = 'branch-item';
    btn.textContent = b.label;
    btn.addEventListener('click', () => {
      state.chosenBranchId = b.id;
      state.step = 'protocol'; render();
    });
    list.appendChild(btn);
  });
}

// ---------- Inline vitals/dosing widgets (live inside protocol steps) ----------
// No separate vitals screen — a step that needs the patient's weight for a
// per-kg dose, or that explicitly calls for a specific vital, gets a small
// inline control right in that step's card. Anything entered anywhere is
// shared globally for the rest of the run (typing weight once fills in
// every per-kg dose on the page) and shows up in the sticky summary.

function stepNeedsWeight(text){
  return /\d+(?:\.\d+)?\s*(?:-\s*\d+(?:\.\d+)?\s*)?(mg|mcg|gm|mEq|mL)\/kg/i.test(text);
}

// Best-effort keyword detection for an explicit vital-sign instruction in a
// step, same spirit as the dose-calculator regex — works on any protocol
// text without per-step tagging. "where appropriate" per the source text,
// not exhaustive.
function detectVitalNeeds(text){
  const needs = [];
  if(/\bGCS\b|Glasgow\s+Coma/i.test(text)) needs.push('gcs');
  if(/blood\s+glucose|\bBGL\b|glucose\s+level/i.test(text)) needs.push('glucose');
  if(/blood\s+pressure|\bSBP\b|\bDBP\b/i.test(text)) needs.push('bp');
  if(/heart\s+rate/i.test(text)) needs.push('hr');
  if(/respiratory\s+rate/i.test(text)) needs.push('rr');
  if(/SpO2|oxygen\s+saturation|pulse\s+ox(imetry)?/i.test(text)) needs.push('spo2');
  if(/\btemperature\b/i.test(text)) needs.push('temp');
  if(needs.length === 0 && /\bvital\s*signs\b/i.test(text)) needs.push('all');
  return needs;
}

let activeWeightWidgets = [];
let activeDoseDisplays = [];
let activeStickyEls = [];

function kgToDisplayVal(kg, unit){
  if(kg == null || isNaN(kg)) return '';
  const v = unit === 'kg' ? kg : kg * 2.20462;
  return String(Math.round(v * 10) / 10);
}

function refreshAfterVitalChange(){
  activeWeightWidgets.forEach(w => w.refresh());
  activeDoseDisplays.forEach(d => {
    const dose = computeDose(d.text, state.vitals.weight);
    d.el.textContent = dose || '';
    d.el.classList.toggle('hidden', !dose);
  });
  const html = vitalsSummaryHTML();
  activeStickyEls.forEach(el => {
    el.innerHTML = html;
    el.classList.toggle('hidden', !html);
  });
}

function createWeightWidget(){
  const wrap = document.createElement('div');
  wrap.className = 'inline-vital inline-weight';
  wrap.innerHTML = `
    <span class="inline-vital-label">Weight</span>
    <div class="weight-toggle-row">
      <input type="number" step="0.1" min="0" class="text-input inline-weight-input" placeholder="e.g. 180">
      <div class="unit-toggle">
        <button type="button" class="unit-btn active" data-unit="lb">lb</button>
        <button type="button" class="unit-btn" data-unit="kg">kg</button>
      </div>
    </div>`;
  const input = wrap.querySelector('.inline-weight-input');
  const unitBtns = [...wrap.querySelectorAll('.unit-btn')];
  let unit = 'lb';

  function refresh(){
    if(document.activeElement === input) return; // don't clobber active typing
    input.value = kgToDisplayVal(state.vitals.weight, unit);
  }
  unitBtns.forEach(b => b.addEventListener('click', () => {
    unit = b.dataset.unit;
    unitBtns.forEach(x => x.classList.toggle('active', x === b));
    input.value = kgToDisplayVal(state.vitals.weight, unit);
  }));
  input.addEventListener('input', () => {
    const val = parseFloat(input.value);
    if(!isNaN(val) && val > 0){
      const kg = unit === 'kg' ? val : val / 2.20462;
      state.vitals.weight = kg;
      state.vitals.weightLb = unit === 'lb' ? val : kg * 2.20462;
    } else {
      state.vitals.weight = null;
      state.vitals.weightLb = null;
    }
    refreshAfterVitalChange();
  });

  wrap.refresh = refresh;
  refresh();
  activeWeightWidgets.push(wrap);
  return wrap;
}

function createNumericVitalWidget(key, label, placeholder){
  const wrap = document.createElement('div');
  wrap.className = 'inline-vital';
  wrap.innerHTML = `<span class="inline-vital-label">${label}</span>
    <input type="number" class="text-input inline-vital-input" placeholder="${placeholder}">`;
  const input = wrap.querySelector('.inline-vital-input');
  if(state.vitals[key]) input.value = state.vitals[key];
  input.addEventListener('input', () => {
    state.vitals[key] = input.value ? input.value : null;
    refreshAfterVitalChange();
  });
  return wrap;
}

function createBpWidget(){
  const wrap = document.createElement('div');
  wrap.className = 'inline-vital';
  wrap.innerHTML = `<span class="inline-vital-label">Blood Pressure</span>
    <div class="bp-box">
      <input type="number" class="bp-input inline-sbp" placeholder="120" aria-label="Systolic">
      <span class="bp-slash">/</span>
      <input type="number" class="bp-input inline-dbp" placeholder="80" aria-label="Diastolic">
    </div>`;
  const sbp = wrap.querySelector('.inline-sbp');
  const dbp = wrap.querySelector('.inline-dbp');
  if(state.vitals.sbp) sbp.value = state.vitals.sbp;
  if(state.vitals.dbp) dbp.value = state.vitals.dbp;
  sbp.addEventListener('input', () => { state.vitals.sbp = sbp.value || null; refreshAfterVitalChange(); });
  dbp.addEventListener('input', () => { state.vitals.dbp = dbp.value || null; refreshAfterVitalChange(); });
  return wrap;
}

function createGcsWidget(){
  const wrap = document.createElement('div');
  wrap.className = 'inline-vital inline-gcs';
  const boxText = state.vitals.gcs ? `GCS ${state.vitals.gcs}` : 'Tap to score GCS';
  wrap.innerHTML = `
    <button type="button" class="gcs-box inline-gcs-box"><span class="inline-gcs-box-text">${boxText}</span></button>
    <div class="gcs-panel hidden inline-gcs-panel">
      <div class="gcs-group"><p class="gcs-group-title">Eye Opening</p><div class="gcs-options inline-gcs-e"></div></div>
      <div class="gcs-group"><p class="gcs-group-title">Verbal Response</p><div class="gcs-options inline-gcs-v"></div></div>
      <div class="gcs-group"><p class="gcs-group-title">Motor Response</p><div class="gcs-options inline-gcs-m"></div></div>
      <button type="button" class="ghost-btn inline-gcs-close">Close</button>
    </div>`;
  const box = wrap.querySelector('.inline-gcs-box');
  const boxTextEl = wrap.querySelector('.inline-gcs-box-text');
  const panel = wrap.querySelector('.inline-gcs-panel');
  const sel = {e:null, v:null, m:null};

  function buildOpts(container, cat){
    GCS_OPTIONS[cat].forEach(([val, label]) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'gcs-opt-btn';
      btn.textContent = `${val} – ${label}`;
      btn.addEventListener('click', () => {
        sel[cat] = val;
        container.querySelectorAll('.gcs-opt-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        checkComplete();
      });
      container.appendChild(btn);
    });
  }
  buildOpts(wrap.querySelector('.inline-gcs-e'), 'e');
  buildOpts(wrap.querySelector('.inline-gcs-v'), 'v');
  buildOpts(wrap.querySelector('.inline-gcs-m'), 'm');

  function checkComplete(){
    if(sel.e && sel.v && sel.m){
      const total = sel.e + sel.v + sel.m;
      state.vitals.gcs = `${total} (E${sel.e} V${sel.v} M${sel.m})`;
      boxTextEl.textContent = `GCS ${state.vitals.gcs}`;
      panel.classList.add('hidden');
      refreshAfterVitalChange();
    }
  }
  box.addEventListener('click', () => panel.classList.toggle('hidden'));
  wrap.querySelector('.inline-gcs-close').addEventListener('click', () => panel.classList.add('hidden'));
  return wrap;
}

function createVitalWidget(key){
  if(key === 'gcs') return createGcsWidget();
  if(key === 'bp') return createBpWidget();
  if(key === 'hr') return createNumericVitalWidget('hr', 'Heart Rate (bpm)', 'e.g. 88');
  if(key === 'rr') return createNumericVitalWidget('rr', 'Respiratory Rate', 'e.g. 16');
  if(key === 'spo2') return createNumericVitalWidget('spo2', 'Oxygen Saturation (SpO2 %)', 'e.g. 97');
  if(key === 'temp') return createNumericVitalWidget('temp', 'Temperature (°F)', 'e.g. 98.6');
  if(key === 'glucose') return createNumericVitalWidget('glucose', 'Blood Glucose', 'e.g. 110');
  return null;
}

// ---------- Dose calculation from step text ----------
function computeDose(text, weightKg){
  if(!weightKg || isNaN(weightKg)) return null;
  const w = parseFloat(weightKg);

  let m = text.match(/(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(mg|mcg|gm|mEq|mL)\/kg/i);
  let low, high, unit;
  if(m){
    low = parseFloat(m[1]) * w;
    high = parseFloat(m[2]) * w;
    unit = m[3];
  } else {
    m = text.match(/(\d+(?:\.\d+)?)\s*(mg|mcg|gm|mEq|mL)\/kg/i);
    if(m){
      low = high = parseFloat(m[1]) * w;
      unit = m[2];
    }
  }
  if(low === undefined) return null;

  const maxMatch = text.match(/[Mm]aximum(?:\s+(?:single|total)?\s*dose)?\s*[:]?\s*(\d+(?:\.\d+)?)\s*(mg|mcg|gm|mEq|mL)/);
  let capped = false;
  if(maxMatch){
    const maxVal = parseFloat(maxMatch[1]);
    const maxUnit = maxMatch[2];
    if(maxUnit.toLowerCase() === unit.toLowerCase()){
      if(high > maxVal){ high = maxVal; capped = true; }
      if(low > maxVal){ low = maxVal; capped = true; }
    }
  }

  const fmt = n => {
    if(n >= 100) return Math.round(n).toString();
    if(n >= 10) return n.toFixed(1);
    return n.toFixed(2).replace(/0$/,'').replace(/\.$/,'');
  };
  const doseStr = (Math.abs(low-high) < 0.001) ? `${fmt(low)} ${unit}` : `${fmt(low)}–${fmt(high)} ${unit}`;
  return `≈ ${doseStr} for ${w.toFixed(1)} kg${capped ? ' (capped at protocol maximum)' : ''}`;
}

// ---------- Step 4: Protocol view ----------
function renderProtocolView(){
  const tpl = document.getElementById('tpl-protocol-view').content.cloneNode(true);
  app.innerHTML = '';
  app.appendChild(tpl);
  const proto = protocolById(state.chosenProtocolId);
  const branch = proto.branches.find(b => b.id === state.chosenBranchId);
  if(!state.vitals) state.vitals = {};

  activeWeightWidgets = [];
  activeDoseDisplays = [];
  activeStickyEls = [];

  addBackBtn(() => {
    state.step = proto.branches.length > 1 ? 'branch' : 'ccList';
    render();
  });

  document.getElementById('protoTitle').textContent = proto.title;
  document.getElementById('protoBranchLabel').textContent =
    (proto.branches.length > 1 ? branch.label : '') ;
  const stickyEl = document.getElementById('vitalsSummarySticky');
  const stickyHtml = vitalsSummaryHTML();
  stickyEl.innerHTML = stickyHtml;
  stickyEl.classList.toggle('hidden', !stickyHtml);
  activeStickyEls.push(stickyEl);

  if(proto.precedes && proto.precedes.length){
    const pre = protocolById(proto.precedes[0]);
    if(pre){
      const wrap = document.createElement('div');
      wrap.className = 'ref-panel';
      wrap.innerHTML = `<button class="ghost-btn" id="toggleUPC">Show ${pre.title} checklist (do first)</button><div id="upcSteps" class="hidden" style="margin-top:10px;"></div>`;
      document.querySelector('.screen-protocol').insertBefore(wrap, document.getElementById('vitalsSummarySticky').nextSibling);
      wrap.querySelector('#toggleUPC').addEventListener('click', () => {
        const div = wrap.querySelector('#upcSteps');
        div.classList.toggle('hidden');
        if(!div.dataset.loaded){
          div.dataset.loaded = '1';
          const ul = document.createElement('ul');
          pre.branches[0].steps.forEach(s => {
            const li = document.createElement('li'); li.textContent = s.text; ul.appendChild(li);
          });
          div.appendChild(ul);
        }
      });
    }
  }

  const progress = document.createElement('div');
  progress.className = 'steps-progress';
  document.querySelector('.screen-protocol').insertBefore(progress, document.getElementById('stepsList'));
  let doneCount = 0;
  function updateProgress(){
    progress.textContent = `${doneCount} of ${branch.steps.length} steps done — tap a circle as you complete it`;
  }
  updateProgress();

  const list = document.getElementById('stepsList');
  branch.steps.forEach((step, i) => {
    const li = document.createElement('li');
    li.className = 'step-item' + (step.drug_id ? ' has-drug' : '') + (step.goto_protocol ? ' goto' : '');
    const bullet = document.createElement('button');
    bullet.type = 'button';
    bullet.className = 'step-check';
    bullet.setAttribute('aria-pressed', 'false');
    bullet.setAttribute('aria-label', `Mark step ${i+1} done`);
    bullet.textContent = i+1;
    bullet.addEventListener('click', () => {
      const isDone = bullet.getAttribute('aria-pressed') === 'true';
      bullet.setAttribute('aria-pressed', String(!isDone));
      bullet.textContent = isDone ? (i+1) : '✓';
      li.classList.toggle('done', !isDone);
      doneCount += isDone ? -1 : 1;
      updateProgress();
    });
    const body = document.createElement('div');
    body.style.flex = '1';
    const textDiv = document.createElement('div');
    textDiv.className = 'step-text';
    textDiv.textContent = step.text;
    body.appendChild(textDiv);

    if(stepNeedsWeight(step.text)){
      body.appendChild(createWeightWidget());
      const doseDiv = document.createElement('div');
      doseDiv.className = 'step-dose-calc hidden';
      body.appendChild(doseDiv);
      const dose = computeDose(step.text, state.vitals.weight);
      if(dose){ doseDiv.textContent = dose; doseDiv.classList.remove('hidden'); }
      activeDoseDisplays.push({el: doseDiv, text: step.text});
    }

    detectVitalNeeds(step.text).forEach(key => {
      if(key === 'all'){
        ['hr','bp','rr','spo2','temp','glucose','gcs'].forEach(k => {
          const w = createVitalWidget(k);
          if(w) body.appendChild(w);
        });
      } else {
        const w = createVitalWidget(key);
        if(w) body.appendChild(w);
      }
    });

    if(step.drug_id && state.drugById[step.drug_id]){
      const drugBtn = document.createElement('button');
      drugBtn.className = 'step-drug-link';
      drugBtn.textContent = `View ${state.drugById[step.drug_id].name} reference →`;
      drugBtn.addEventListener('click', () => showDrugModal(step.drug_id));
      body.appendChild(drugBtn);
    }
    if(step.goto_protocol){
      const target = protocolById(step.goto_protocol);
      const gotoBtn = document.createElement('button');
      gotoBtn.className = 'step-drug-link';
      gotoBtn.textContent = target ? `Jump to ${target.title} →` : 'Referenced protocol not yet added';
      gotoBtn.disabled = !target;
      gotoBtn.addEventListener('click', () => {
        if(!target) return;
        // Continuing the same patient run — keep whatever vitals/weight
        // have already been entered rather than clearing them.
        state.chosenProtocolId = target.id;
        state.chosenTopicKey = Object.keys(state.topics).find(k =>
          state.topics[k].adult === target.id || state.topics[k].pediatric === target.id);
        state.chosenBranchId = target.branches[0].id;
        state.step = target.branches.length > 1 ? 'branch' : 'protocol';
        render();
      });
      body.appendChild(gotoBtn);
    }

    li.appendChild(bullet); li.appendChild(body);
    list.appendChild(li);
  });

  const refBtn = document.getElementById('showRefBtn');
  const refPanel = document.getElementById('refPanel');
  refBtn.addEventListener('click', () => {
    refPanel.classList.toggle('hidden');
    if(!refPanel.dataset.loaded){
      refPanel.dataset.loaded = '1';
      const r = proto.reference || {};
      const section = (title, arr) => arr && arr.length ?
        `<div><h4>${title}</h4><ul>${arr.map(x=>`<li>${x}</li>`).join('')}</ul></div>` : '';
      refPanel.innerHTML =
        section('History', r.history) +
        section('Signs & Symptoms', r.signs_symptoms) +
        section('Differential', r.differential) +
        section('Pearls', r.pearls);
    }
  });

  const reportBtn = document.createElement('button');
  reportBtn.type = 'button';
  reportBtn.className = 'ghost-btn';
  reportBtn.textContent = 'Download run report (.txt) for documentation';
  reportBtn.style.alignSelf = 'flex-start';
  reportBtn.addEventListener('click', () => {
    downloadTextFile(buildProtocolReportText(proto, branch), `medpath-run-report-${dateStamp(new Date())}.txt`);
  });
  document.querySelector('.screen-protocol').appendChild(reportBtn);
}

// Plain-text run summary for a completed/in-progress protocol run. MEDPATH
// has no direct API integration with any ePCR software (including ESO) —
// no personal/independent app can push data straight into ESO's fields.
// This produces a clean, timestamped report meant to be copy/pasted into
// your ePCR's narrative or relevant fields instead.
function buildProtocolReportText(proto, branch){
  const now = new Date();
  const lines = [];
  lines.push('MEDPATH — Run Report');
  lines.push(`Generated: ${now.toLocaleString()}`);
  lines.push(`Demographic: ${state.chosenDemographic || '—'}`);
  lines.push(`Chief complaint / protocol: ${proto.title}${branch.label ? ' — ' + branch.label : ''}`);
  lines.push('');
  lines.push('Vitals:');
  const v = state.vitals || {};
  if(v.weightLb) lines.push(`  Weight: ${v.weightLb} lb (${parseFloat(v.weight).toFixed(1)} kg)`);
  if(v.hr) lines.push(`  HR: ${v.hr}`);
  if(v.sbp || v.dbp) lines.push(`  BP: ${v.sbp || '?'}/${v.dbp || '?'}`);
  if(v.rr) lines.push(`  RR: ${v.rr}`);
  if(v.spo2) lines.push(`  SpO2: ${v.spo2}%`);
  if(v.temp) lines.push(`  Temp: ${v.temp}°F`);
  if(v.glucose) lines.push(`  Glucose: ${v.glucose}`);
  if(v.gcs) lines.push(`  GCS: ${v.gcs}`);
  lines.push('');
  lines.push('Steps:');
  document.querySelectorAll('#stepsList .step-item').forEach((li, i) => {
    const done = li.classList.contains('done');
    const text = li.querySelector('.step-text').textContent;
    lines.push(`  [${done ? 'x' : ' '}] ${i + 1}. ${text}`);
  });
  lines.push('');
  lines.push('Copy/paste the relevant lines into your ePCR (e.g. ESO) narrative or times fields — MEDPATH has no direct integration with ePCR software. Verify every entry before submitting documentation.');
  return lines.join('\n');
}

function dateStamp(d){
  const p = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}`;
}

function downloadTextFile(text, filename){
  const blob = new Blob([text], {type: 'text/plain'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// ---------- Drug modal ----------
function showDrugModal(drugId){
  const d = state.drugById[drugId];
  if(!d) return;
  const backdrop = document.createElement('div');
  backdrop.className = 'modal-backdrop';
  const card = document.createElement('div');
  card.className = 'drug-card';
  const section = (title, arr) => arr && arr.length ?
    `<h4>${title}</h4><ul>${arr.map(x=>`<li>${x}</li>`).join('')}</ul>` : '';
  const doseBlock = (title, arr) => {
    if(!arr || !arr.length) return `<h4>${title}</h4><p style="font-size:0.85rem;color:var(--sumi-soft);">${d.pediatric_note && title.includes('Pediatric') ? d.pediatric_note : 'None listed'}</p>`;
    return `<h4>${title}</h4>` + arr.map(ind => `
      <div style="margin-bottom:8px;">
        <strong style="font-size:0.85rem;">${ind.indication}</strong>
        <ul>${ind.steps.map(s=>`<li>${s.text}</li>`).join('')}</ul>
      </div>`).join('');
  };
  card.innerHTML = `
    <button class="close-btn">✕</button>
    <h3>${d.name}</h3>
    <div class="cert">${(d.certification||[]).join(' · ')}${d.onset ? ' · Onset: '+d.onset : ''}${d.peak_effect ? ' · Peak: '+d.peak_effect : ''}${d.half_life ? ' · Half-life: '+d.half_life : ''}</div>
    ${doseBlock('Adult Dosing', d.adult_dosing)}
    ${doseBlock('Pediatric Dosing', d.pediatric_dosing)}
    ${section('Contraindications', d.contraindications)}
    ${section('Adverse Reactions', d.adverse_reactions)}
    ${section('Precautions', d.precautions)}
    ${section('Medical Considerations', d.medical_considerations)}
    ${d.mechanism_of_action ? `<h4>Mechanism</h4><p style="font-size:0.88rem;">${d.mechanism_of_action}</p>` : ''}
  `;
  backdrop.appendChild(card);
  document.body.appendChild(backdrop);
  const close = () => document.body.removeChild(backdrop);
  card.querySelector('.close-btn').addEventListener('click', close);
  backdrop.addEventListener('click', (e) => { if(e.target === backdrop) close(); });
}

// ---------- Browse all ----------
function renderBrowseAll(){
  app.innerHTML = '';
  addBackBtn(goHome);

  const h = document.createElement('h2'); h.className='step-title'; h.textContent = 'All Converted Protocols';
  app.appendChild(h);

  const bySection = {};
  state.protocols.forEach(p => {
    const sec = p.section || 'Other';
    (bySection[sec] = bySection[sec] || []).push(p);
  });
  Object.keys(bySection).sort().forEach(sec => {
    const secDiv = document.createElement('div'); secDiv.className = 'browse-section';
    secDiv.innerHTML = `<h3>${sec}</h3>`;
    bySection[sec].forEach(p => {
      const btn = document.createElement('button');
      btn.className = 'cc-item';
      btn.innerHTML = `<span>${p.title}</span><span class="tag">${p.demographic}</span>`;
      btn.addEventListener('click', () => {
        state.chosenDemographic = p.demographic;
        state.chosenTopicKey = Object.keys(state.topics).find(k =>
          state.topics[k].adult === p.id || state.topics[k].pediatric === p.id);
        beginProtocolRun(p.id);
        render();
      });
      secDiv.appendChild(btn);
    });
    app.appendChild(secDiv);
  });
}

// ---------- Drug reference browse ----------
function renderDrugRef(){
  app.innerHTML = '';
  addBackBtn(goHome);

  const h = document.createElement('h2'); h.className='step-title'; h.textContent = 'Drug Reference';
  app.appendChild(h);

  const input = document.createElement('input');
  input.className = 'text-input'; input.placeholder = 'Search medications…';
  app.appendChild(input);

  const list = document.createElement('div'); list.className = 'cc-results';
  app.appendChild(list);

  function renderList(q){
    list.innerHTML = '';
    const items = state.drugs.filter(d => d.name.toLowerCase().includes(q.toLowerCase()));
    items.forEach(d => {
      const btn = document.createElement('button');
      btn.className = 'cc-item';
      btn.innerHTML = `<span>${d.name}</span>`;
      btn.addEventListener('click', () => showDrugModal(d.id));
      list.appendChild(btn);
    });
  }
  input.addEventListener('input', () => renderList(input.value));
  renderList('');
}

// ---------- Run An Arrest ----------
// Timestamped timer/documentation tool, modeled on apps like CPR Recorder.
// Timing is drawn straight from TFD's own Asystole / PEA / V-Fib-Pulseless
// V-Tach protocols: Epinephrine 1 mg repeated every 10 minutes (max 4 mg
// total), rhythm reassessment + med admin + defib every 2 minutes, charge
// the defibrillator at the 1:45 mark of that 2-minute cycle, Amiodarone
// 300 mg first dose then 150 mg after 3-5 minutes if still in refractory
// VF/pulseless VT.
const arrestState = {
  active: false,
  ended: false,
  startTime: null,
  endTime: null,
  log: [],            // {time: Date, label: string}
  cprRunning: false,
  cprSegStart: null,
  cprAccumMs: 0,
  cprCycles: 0,
  lastEpiTime: null,
  epiCount: 0,
  lastRhythmTime: null,
  rhythmCheckCount: 0,
  shockCount: 0,
  amiodaroneCount: 0,
  rhythmAlerted: false,
  chargedAlerted: false,
  epiAlerted: false,
};

function ordinal(n){
  const s = ['th','st','nd','rd'], v = n % 100;
  return n + (s[(v - 20) % 10] || s[v] || s[0]);
}
let arrestTickTimer = null;

const ARREST_MEDS = [
  {label:'Epinephrine 1 mg IVP/IO', note:'repeat q10min, max 4 mg total'},
  {label:'Amiodarone 300 mg IVP/IO', note:'1st dose, refractory VF/pVT'},
  {label:'Amiodarone 150 mg IVP/IO', note:'2nd dose, after 3–5 min'},
  {label:'Calcium Chloride 1 g IVP/IO', note:'suspected hyperkalemia'},
  {label:'Sodium Bicarbonate', note:'50 mEq (PEA: 1 mEq/kg) IVP/IO'},
  {label:'Magnesium Sulfate 2 g IVP', note:'torsades de pointes'},
  {label:'Naloxone 2–4 mg IVP/IO', note:'PEA, suspected opioid'},
  {label:'Dextrose 10% (D10) 5 g IV', note:'PEA, suspected hypoglycemia'},
  {label:'Glucagon 1 mg IVP', note:'suspected beta blocker OD'},
];
const ARREST_RHYTHMS = ['V-Fib','Pulseless V-Tach','PEA','Asystole','Organized rhythm / possible ROSC','Torsades de Pointes'];
const ARREST_AIRWAY = ['BVM ventilation','Supraglottic Airway (SGA) placed','Intubated (ETT via VL)','EtCO2 attached','ResQPOD attached','POCUS performed'];
const ARREST_IVIO = ['IV — Right AC','IV — Left AC','IO — Tibial','IO — Humeral','Right EJ','Left EJ'];
const ARREST_SHOCK_J = ['200 J','300 J','360 J'];

function fmtClock(d){
  return d.toLocaleTimeString([], {hour:'numeric', minute:'2-digit', second:'2-digit'});
}
function fmtElapsedShort(ms){
  const s = Math.max(0, Math.floor(ms/1000));
  const m = Math.floor(s/60), r = s%60;
  return `${String(m).padStart(2,'0')}:${String(r).padStart(2,'0')}`;
}
function fmtElapsedLong(ms){
  const s = Math.max(0, Math.floor(ms/1000));
  const h = Math.floor(s/3600), m = Math.floor((s%3600)/60), r = s%60;
  return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(r).padStart(2,'0')}`;
}
function vibrate(pattern){
  if('vibrate' in navigator){ try{ navigator.vibrate(pattern); }catch(e){} }
  // Note: iOS Safari/PWAs do not support the Vibration API — the on-screen
  // alert banner is the reliable cross-platform cue; vibration is a bonus
  // on Android.
}
function logArrestEvent(label){
  arrestState.log.push({time: new Date(), label});
}

function renderArrest(){
  const tpl = document.getElementById('tpl-arrest').content.cloneNode(true);
  app.innerHTML = '';
  app.appendChild(tpl);
  if(!state.vitals) state.vitals = {};
  addBackBtn(() => {
    if(arrestState.active){
      if(!confirm('An operation is still running. Go back without ending it? The timer keeps running in the background and you can return to it from the home screen.')) return;
    }
    goHome();
  });

  const pre = document.getElementById('arrestPre');
  const live = document.getElementById('arrestLive');
  const summary = document.getElementById('arrestSummary');

  if(arrestState.ended){
    pre.classList.add('hidden'); live.classList.add('hidden'); summary.classList.remove('hidden');
    renderArrestSummary();
    return;
  }
  if(!arrestState.active){
    pre.classList.remove('hidden'); live.classList.add('hidden'); summary.classList.add('hidden');
    document.getElementById('startOpBtn').addEventListener('click', startArrestOperation);
    return;
  }

  pre.classList.add('hidden'); live.classList.remove('hidden'); summary.classList.add('hidden');
  document.getElementById('arrestStartedLabel').textContent = `Started ${fmtClock(arrestState.startTime)}`;

  document.getElementById('cprToggleBtn').addEventListener('click', toggleCpr);
  document.getElementById('epiLogBtn').addEventListener('click', () => { logEpiDose(); redrawArrestLog(); });
  document.getElementById('endOpBtn').addEventListener('click', endArrestOperation);
  app.querySelectorAll('.event-btn').forEach(btn => {
    btn.addEventListener('click', () => openEventModal(btn.dataset.evt));
  });
  wireSizingPanel();
  renderArrestProtocolLinks('arrestProtocolLinksLive');

  refreshCprButton();
  redrawArrestLog();
  tickArrest();
  if(arrestTickTimer) clearInterval(arrestTickTimer);
  arrestTickTimer = setInterval(tickArrest, 1000);
}

function startArrestOperation(){
  Object.assign(arrestState, {
    active:true, ended:false, startTime:new Date(), endTime:null, log:[],
    cprRunning:false, cprSegStart:null, cprAccumMs:0, cprCycles:0,
    lastEpiTime:null, epiCount:0, lastRhythmTime:new Date(), rhythmCheckCount:0, shockCount:0,
    amiodaroneCount:0, rhythmAlerted:false, chargedAlerted:false, epiAlerted:false,
  });
  logArrestEvent('Operation started');
  vibrate(200);
  render();
}

function toggleCpr(){
  if(arrestState.cprRunning){
    arrestState.cprAccumMs += Date.now() - arrestState.cprSegStart;
    arrestState.cprRunning = false;
    logArrestEvent('CPR paused');
  } else {
    arrestState.cprSegStart = Date.now();
    arrestState.cprRunning = true;
    arrestState.cprCycles += 1;
    logArrestEvent('CPR started' + (arrestState.cprCycles > 1 ? ` (cycle ${arrestState.cprCycles})` : ''));
  }
  refreshCprButton();
  redrawArrestLog();
}
function refreshCprButton(){
  const btn = document.getElementById('cprToggleBtn');
  if(!btn) return;
  btn.textContent = arrestState.cprRunning ? '⏸' : '▶';
  btn.classList.toggle('active', arrestState.cprRunning);
}

function logEpiDose(){
  arrestState.epiCount += 1;
  arrestState.lastEpiTime = new Date();
  arrestState.epiAlerted = false;
  logArrestEvent(`Epinephrine 1 mg IVP/IO — dose #${arrestState.epiCount}${arrestState.epiCount >= 4 ? ' (max total 4 mg reached)' : ''}`);
  vibrate(100);
}

function resetRhythmCycle(){
  arrestState.lastRhythmTime = new Date();
  arrestState.rhythmCheckCount += 1;
  arrestState.rhythmAlerted = false;
  arrestState.chargedAlerted = false;
}

function openEventModal(kind){
  const cfg = {
    rhythm: {title:'Log Rhythm', options: ARREST_RHYTHMS.map(r => ({label:r})), onPick:(label) => { logArrestEvent(`Rhythm — ${label}`); resetRhythmCycle(); }},
    shock: {title:'Log Shock', options: ARREST_SHOCK_J.map(j => ({label:j})), onPick:(label) => { arrestState.shockCount += 1; logArrestEvent(`Shock #${arrestState.shockCount} delivered (${label})`); resetRhythmCycle(); }},
    meds: {title:'Log Medication', options: ARREST_MEDS.map(m => ({label:m.label, sub:m.note})), onPick:(label) => {
        if(label.startsWith('Epinephrine')){ logEpiDose(); return; }
        if(label.startsWith('Amiodarone')) arrestState.amiodaroneCount += 1;
        logArrestEvent(label);
      }},
    airway: {title:'Log Airway', options: ARREST_AIRWAY.map(a => ({label:a})), onPick:(label) => logArrestEvent(label)},
    ivio: {title:'Log IV/IO Access', options: ARREST_IVIO.map(a => ({label:a})), onPick:(label) => logArrestEvent(`Access — ${label}`)},
    other: {title:'Log Other Event', options: [], onPick:() => {}},
  }[kind];
  if(!cfg) return;

  const backdrop = document.createElement('div');
  backdrop.className = 'modal-backdrop';
  const card = document.createElement('div');
  card.className = 'drug-card';
  card.innerHTML = `<button class="close-btn">✕</button><h3>${cfg.title}</h3><div class="quick-modal-list"></div>
    <div style="margin-top:14px; display:flex; gap:8px;">
      <input type="text" class="text-input" id="quickDetailInput" placeholder="Custom / additional detail…">
      <button type="button" class="ghost-btn" id="quickLogBtn" style="white-space:nowrap;">Log</button>
    </div>`;
  const list = card.querySelector('.quick-modal-list');
  cfg.options.forEach(opt => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'quick-pick-btn';
    b.innerHTML = opt.sub ? `${opt.label}<br><span style="font-size:0.74rem;color:var(--sumi-soft);">${opt.sub}</span>` : opt.label;
    b.addEventListener('click', () => {
      cfg.onPick(opt.label);
      document.body.removeChild(backdrop);
      redrawArrestLog();
    });
    list.appendChild(b);
  });
  backdrop.appendChild(card);
  document.body.appendChild(backdrop);
  const close = () => { if(document.body.contains(backdrop)) document.body.removeChild(backdrop); };
  card.querySelector('.close-btn').addEventListener('click', close);
  backdrop.addEventListener('click', (e) => { if(e.target === backdrop) close(); });
  card.querySelector('#quickLogBtn').addEventListener('click', () => {
    const v = card.querySelector('#quickDetailInput').value.trim();
    if(!v) return;
    logArrestEvent(kind === 'other' ? v : `${cfg.title.replace('Log ', '')} — ${v}`);
    close();
    redrawArrestLog();
  });
}

// Weight-based equipment sizing quick reference. The IO needle color/site
// guidance in TFD's Vascular Access - EZ-IO protocol is given by insertion
// site + adult/pediatric, not a numeric weight table, so the weight
// breakpoints below are the standard EZ-IO manufacturer sizing guide, shown
// here for a fast visual/color cue — verify against your service's actual
// device and Broselow reference, not verbatim TFD protocol text.
function ioSizeInfo(kg){
  if(kg == null || isNaN(kg)) return null;
  if(kg < 3) return {label: 'Under 3 kg', swatch: '#9a9a9a', detail: 'EZ-IO not typically indicated at this weight — consider alternate access.'};
  if(kg < 40) return {label: 'Pink — 15 mm', swatch: '#e85d9c', detail: 'Pediatric, roughly 3–39 kg.'};
  return {label: 'Blue — 25 mm', swatch: '#2e6db4', detail: '≥40 kg, standard sites. Yellow (45 mm) if excessive tissue over the site.'};
}
function pedsEquipmentInfo(kg){
  if(kg == null || isNaN(kg) || kg >= 40) return null;
  const ett = (kg / 10 + 2.5).toFixed(1);
  const bvm = kg < 10 ? 'Infant mask' : (kg < 30 ? 'Child mask' : 'Small adult / child mask');
  return {ett, bvm};
}

function wireSizingPanel(){
  const toggleBtn = document.getElementById('sizingToggleBtn');
  const panel = document.getElementById('sizingPanel');
  const input = document.getElementById('sizingWeightInput');
  const unitBtns = [...document.querySelectorAll('#sizingUnitToggle .unit-btn')];
  const results = document.getElementById('sizingResults');
  let unit = 'lb';

  toggleBtn.addEventListener('click', () => panel.classList.toggle('hidden'));

  function renderResults(){
    const kg = state.vitals.weight;
    const io = ioSizeInfo(kg);
    if(!io){
      results.innerHTML = '<p class="meta-note">Enter a weight to see IO needle size and, if pediatric, tube/mask sizing.</p>';
      return;
    }
    const peds = pedsEquipmentInfo(kg);
    let html = `<div class="sizing-row"><span class="sizing-swatch" style="background:${io.swatch};"></span>
      <div><strong>IO Needle: ${io.label}</strong><div class="sizing-detail">${io.detail}</div></div></div>`;
    if(peds){
      html += `<div class="sizing-row"><span class="sizing-swatch" style="background:var(--indigo);"></span>
        <div><strong>Peds ET tube: ~${peds.ett} mm (uncuffed est.)</strong><div class="sizing-detail">BVM: ${peds.bvm} — general estimate, verify against your Broselow reference.</div></div></div>`;
    }
    results.innerHTML = html;
  }
  function refreshInput(){
    if(document.activeElement === input) return;
    input.value = kgToDisplayVal(state.vitals.weight, unit);
  }
  unitBtns.forEach(b => b.addEventListener('click', () => {
    unit = b.dataset.unit;
    unitBtns.forEach(x => x.classList.toggle('active', x === b));
    refreshInput();
  }));
  input.addEventListener('input', () => {
    const val = parseFloat(input.value);
    if(!isNaN(val) && val > 0){
      const kg = unit === 'kg' ? val : val / 2.20462;
      state.vitals.weight = kg;
      state.vitals.weightLb = unit === 'lb' ? val : kg * 2.20462;
    } else {
      state.vitals.weight = null;
      state.vitals.weightLb = null;
    }
    renderResults();
    refreshAfterVitalChange();
  });
  refreshInput();
  renderResults();
}

function redrawArrestLog(){
  const list = document.getElementById('arrestLogList');
  if(!list) return;
  list.innerHTML = '';
  [...arrestState.log].reverse().forEach(entry => {
    const li = document.createElement('li');
    li.innerHTML = `<span>${entry.label}</span><span class="log-time">${fmtClock(entry.time)}</span>`;
    list.appendChild(li);
  });
}

function tickArrest(){
  if(!arrestState.active) return;
  const now = Date.now();

  const elapsedEl = document.getElementById('arrestElapsed');
  if(elapsedEl) elapsedEl.textContent = fmtElapsedLong(now - arrestState.startTime.getTime());

  const cprMs = arrestState.cprAccumMs + (arrestState.cprRunning ? now - arrestState.cprSegStart : 0);
  const cprTimeEl = document.getElementById('cprTime');
  if(cprTimeEl) cprTimeEl.textContent = fmtElapsedShort(cprMs);
  const cprCountEl = document.getElementById('cprCount');
  if(cprCountEl) cprCountEl.textContent = `Cycles: ${arrestState.cprCycles}`;

  const epiMs = arrestState.lastEpiTime ? now - arrestState.lastEpiTime.getTime() : now - arrestState.startTime.getTime();
  const epiTimeEl = document.getElementById('epiTime');
  if(epiTimeEl) epiTimeEl.textContent = fmtElapsedShort(epiMs);
  const epiCountEl = document.getElementById('epiCount');
  if(epiCountEl) epiCountEl.textContent = `Doses: ${arrestState.epiCount} / max 4 — 1 mg IVP/IO ea.`;

  // Small quick-reference countdowns, always visible (not just when close to due)
  const epiDueEl = document.getElementById('arrestEpiDue');
  if(epiDueEl){
    if(arrestState.epiCount >= 4){
      epiDueEl.textContent = 'Epi: max total 4 mg given';
    } else if(arrestState.lastEpiTime){
      const remain = Math.max(0, 600000 - (now - arrestState.lastEpiTime.getTime()));
      epiDueEl.textContent = `${ordinal(arrestState.epiCount + 1)} Dose Due: ${fmtElapsedShort(remain)}`;
    } else {
      const remain = Math.max(0, 60000 - (now - arrestState.startTime.getTime()));
      epiDueEl.textContent = `${ordinal(1)} Dose Due: ${fmtElapsedShort(remain)}`;
    }
  }
  const rhythmDueEl = document.getElementById('arrestRhythmDue');
  if(rhythmDueEl){
    const remain = Math.max(0, 120000 - (now - arrestState.lastRhythmTime.getTime()));
    rhythmDueEl.textContent = `${ordinal(arrestState.rhythmCheckCount + 1)} Pulse Check Due: ${fmtElapsedShort(remain)}`;
  }

  const rhythmMs = now - arrestState.lastRhythmTime.getTime();
  const banner = document.getElementById('arrestAlertBanner');
  if(banner){
    if(rhythmMs >= 120000){
      banner.textContent = 'Rhythm / pulse check + med admin / defib due now';
      banner.classList.remove('hidden');
      if(!arrestState.rhythmAlerted){ arrestState.rhythmAlerted = true; vibrate([250,100,250,100,250]); }
    } else if(rhythmMs >= 105000){
      banner.textContent = `Charge defibrillator — rhythm check in ${Math.ceil((120000-rhythmMs)/1000)}s`;
      banner.classList.remove('hidden');
      if(!arrestState.chargedAlerted){ arrestState.chargedAlerted = true; vibrate(150); }
    } else if(arrestState.lastEpiTime && (now - arrestState.lastEpiTime.getTime()) >= 600000){
      banner.textContent = 'Epinephrine due (repeat q10min)' + (arrestState.epiCount >= 4 ? ' — max total 4 mg already given' : '');
      banner.classList.remove('hidden');
      if(!arrestState.epiAlerted){ arrestState.epiAlerted = true; vibrate([200,100,200]); }
    } else if(!arrestState.lastEpiTime && (now - arrestState.startTime.getTime()) >= 60000){
      banner.textContent = 'First Epinephrine 1 mg dose due';
      banner.classList.remove('hidden');
      if(!arrestState.epiAlerted){ arrestState.epiAlerted = true; vibrate([200,100,200]); }
    } else {
      banner.classList.add('hidden');
    }
  }
}

function endArrestOperation(){
  if(!confirm('End this operation? This stops all timers and closes out the log.')) return;
  if(arrestState.cprRunning){
    arrestState.cprAccumMs += Date.now() - arrestState.cprSegStart;
    arrestState.cprRunning = false;
  }
  arrestState.active = false;
  arrestState.ended = true;
  arrestState.endTime = new Date();
  logArrestEvent('Operation ended');
  if(arrestTickTimer){ clearInterval(arrestTickTimer); arrestTickTimer = null; }
  render();
}

function buildArrestReportText(){
  const s = arrestState;
  const lines = [];
  lines.push('MEDPATH — Arrest Run Log');
  lines.push(`Started: ${s.startTime.toLocaleString()}`);
  if(s.endTime) lines.push(`Ended:   ${s.endTime.toLocaleString()}`);
  if(s.endTime) lines.push(`Total duration: ${fmtElapsedLong(s.endTime - s.startTime)}`);
  lines.push(`CPR active time: ${fmtElapsedShort(s.cprAccumMs)}  |  CPR cycles: ${s.cprCycles}`);
  lines.push(`Epinephrine doses: ${s.epiCount}  |  Shocks delivered: ${s.shockCount}  |  Amiodarone doses: ${s.amiodaroneCount}`);
  lines.push('');
  lines.push('Time         Elapsed   Event');
  s.log.forEach(e => {
    const elapsed = fmtElapsedLong(e.time - s.startTime);
    lines.push(`${fmtClock(e.time).padEnd(12)} ${elapsed}   ${e.label}`);
  });
  lines.push('');
  lines.push('Generated by MEDPATH — verify every entry against the monitor/defibrillator record before finalizing documentation. MEDPATH has no direct integration with ePCR software (e.g. ESO); copy/paste this log into the appropriate narrative or times fields. Reference tool only, not a substitute for official documentation.');
  return lines.join('\n');
}

function renderArrestSummary(){
  const body = document.getElementById('arrestSummaryBody');
  const s = arrestState;
  body.innerHTML = `
    <table class="arrest-summary-table">
      <tr><td>Started</td><td>${s.startTime.toLocaleString()}</td></tr>
      <tr><td>Ended</td><td>${s.endTime.toLocaleString()}</td></tr>
      <tr><td>Duration</td><td>${fmtElapsedLong(s.endTime - s.startTime)}</td></tr>
      <tr><td>CPR active time</td><td>${fmtElapsedShort(s.cprAccumMs)} (${s.cprCycles} cycles)</td></tr>
      <tr><td>Epinephrine</td><td>${s.epiCount} dose(s)</td></tr>
      <tr><td>Shocks</td><td>${s.shockCount}</td></tr>
      <tr><td>Amiodarone</td><td>${s.amiodaroneCount} dose(s)</td></tr>
      <tr><td>Total events logged</td><td>${s.log.length}</td></tr>
    </table>
    <div class="run-report-box">${buildArrestReportText().replace(/</g,'&lt;')}</div>
  `;
  document.getElementById('downloadLogBtn').addEventListener('click', () => downloadTextFile(buildArrestReportText(), `medpath-arrest-log-${dateStamp(s.startTime)}.txt`));
  document.getElementById('newOpBtn').addEventListener('click', () => {
    arrestState.ended = false;
    arrestState.active = false;
    render();
  });
}

// Quick-jump list to the actual arrest protocol steps (adult, then
// pediatric) so it's fast to flip back and forth for reference between
// calls without re-navigating the whole chief-complaint flow.
const ARREST_PROTOCOL_IDS = [
  'asystole', 'pea', 'vfib_pulseless_vtach', 'maternal_arrest', 'trauma_arrest',
  'pediatric_pulseless_arrest',
];
function renderArrestProtocolLinks(containerId){
  const wrap = document.getElementById(containerId);
  if(!wrap) return;
  wrap.innerHTML = '';
  ARREST_PROTOCOL_IDS.forEach(id => {
    const proto = protocolById(id);
    if(!proto) return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'cc-item';
    btn.innerHTML = `<span>${proto.title}</span><span class="tag">${proto.demographic}</span>`;
    btn.addEventListener('click', () => {
      state.chosenDemographic = proto.demographic;
      state.chosenTopicKey = Object.keys(state.topics).find(k =>
        state.topics[k].adult === proto.id || state.topics[k].pediatric === proto.id);
      beginProtocolRun(proto.id);
      render();
    });
    wrap.appendChild(btn);
  });
}

// ---------- Boot ----------
(async function boot(){
  try{
    await loadData();
    state.step = 'home';
    render();
    document.getElementById('connStatus').classList.toggle('offline', !navigator.onLine);
    window.addEventListener('online', () => document.getElementById('connStatus').classList.remove('offline'));
    window.addEventListener('offline', () => document.getElementById('connStatus').classList.add('offline'));
  }catch(err){
    app.innerHTML = `<p style="padding:20px;color:#a33;">Failed to load protocol data: ${err.message}</p>`;
    console.error(err);
  }
})();

// ---------- PWA service worker ----------
if('serviceWorker' in navigator){
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js').catch(console.error);
  });
}
