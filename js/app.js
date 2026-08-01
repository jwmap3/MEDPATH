// MEDPATH — field protocol decision engine
// Flow: Chief Complaint -> Demographic -> Vitals/Weight -> (Branch select) -> Protocol steps

const state = {
  protocols: null,
  drugs: null,
  drugById: {},
  topics: {},        // topicKey -> {adult: protocolId|null, pediatric: protocolId|null, label}
  chosenTopicKey: null,
  chosenDemographic: null,
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

  // Build topic map for demographic pairing (e.g. Seizure / Pediatric Seizure)
  state.protocols.forEach(p => {
    const key = p.title.replace(/^Pediatric\s+/i, '').trim().toLowerCase();
    if(!state.topics[key]) state.topics[key] = {adult:null, pediatric:null, label: p.title.replace(/^Pediatric\s+/i,'').trim()};
    state.topics[key][p.demographic] = p.id;
  });
}

function protocolById(id){ return state.protocols.find(p => p.id === id); }

// ---------- Router ----------
function render(){
  window.scrollTo(0,0);
  if(state.step === 'home') return renderHome();
  if(state.step === 'cc') return renderChiefComplaint();
  if(state.step === 'demographic') return renderDemographic();
  if(state.step === 'vitals') return renderVitals();
  if(state.step === 'branch') return renderBranchSelect();
  if(state.step === 'protocol') return renderProtocolView();
  if(state.step === 'browseAll') return renderBrowseAll();
  if(state.step === 'drugRef') return renderDrugRef();
}

function goHome(){
  Object.assign(state, {
    step:'home', chosenTopicKey:null, chosenDemographic:null,
    chosenProtocolId:null, chosenBranchId:null, vitals:null
  });
  render();
}

document.getElementById('brandHome').addEventListener('click', goHome);

// ---------- Home ----------
function renderHome(){
  const tpl = document.getElementById('tpl-home').content.cloneNode(true);
  app.innerHTML = '';
  app.appendChild(tpl);
  document.getElementById('newPatientBtn').addEventListener('click', () => {
    state.step = 'cc'; render();
  });
  document.getElementById('browseAllBtn').addEventListener('click', () => {
    state.step = 'browseAll'; render();
  });
  document.getElementById('drugRefBtn').addEventListener('click', () => {
    state.step = 'drugRef'; render();
  });
  document.getElementById('metaNote').textContent =
    `${state.protocols.length} protocols · ${state.drugs.length} drug references loaded · works offline`;
}

// ---------- Step 1: Chief Complaint ----------
function renderChiefComplaint(){
  const tpl = document.getElementById('tpl-chief-complaint').content.cloneNode(true);
  app.innerHTML = '';
  app.appendChild(tpl);
  const backBtn = document.createElement('button');
  backBtn.className = 'back-btn'; backBtn.textContent = '← Home';
  backBtn.addEventListener('click', goHome);
  app.prepend(backBtn);

  const input = document.getElementById('ccSearch');
  const results = document.getElementById('ccResults');

  function search(q){
    q = q.trim().toLowerCase();
    const seen = new Set();
    const matches = [];
    for(const key in state.topics){
      const topic = state.topics[key];
      const anyProto = protocolById(topic.adult) || protocolById(topic.pediatric);
      const tagPool = [
        topic.label.toLowerCase(),
        ...(protocolById(topic.adult)?.chief_complaint_tags || []),
        ...(protocolById(topic.pediatric)?.chief_complaint_tags || [])
      ];
      const isMatch = q === '' ? false : tagPool.some(t => t.includes(q));
      if(isMatch && !seen.has(key)){
        seen.add(key);
        matches.push(topic);
      }
    }
    return matches.sort((a,b) => a.label.localeCompare(b.label));
  }

  function renderResults(list){
    results.innerHTML = '';
    if(input.value.trim() === ''){
      results.innerHTML = '<p class="cc-empty">Start typing a complaint (e.g. "chest pain", "seizure", "allergic reaction", "cardiac arrest")…</p>';
      return;
    }
    if(list.length === 0){
      results.innerHTML = '<p class="cc-empty">No converted protocol matches yet. This app currently covers a priority MVP set — the full protocol book is added in batches.</p>';
      return;
    }
    list.forEach(topic => {
      const btn = document.createElement('button');
      btn.className = 'cc-item';
      const avail = [];
      if(topic.adult) avail.push('Adult');
      if(topic.pediatric) avail.push('Pediatric');
      btn.innerHTML = `<span>${topic.label}</span><span class="tag">${avail.join(' + ')}</span>`;
      btn.addEventListener('click', () => {
        state.chosenTopicKey = Object.keys(state.topics).find(k => state.topics[k] === topic);
        goToDemographicOrSkip();
      });
      results.appendChild(btn);
    });
  }

  input.addEventListener('input', () => renderResults(search(input.value)));
  renderResults([]);
  input.focus();
}

function goToDemographicOrSkip(){
  const topic = state.topics[state.chosenTopicKey];
  const hasAdult = !!topic.adult, hasPed = !!topic.pediatric;
  if(hasAdult && hasPed){
    state.step = 'demographic'; render();
  } else {
    state.chosenDemographic = hasAdult ? 'adult' : 'pediatric';
    state.chosenProtocolId = hasAdult ? topic.adult : topic.pediatric;
    state.step = 'vitals'; render();
  }
}

// ---------- Step 2: Demographic ----------
function renderDemographic(){
  const tpl = document.getElementById('tpl-demographic').content.cloneNode(true);
  app.innerHTML = '';
  app.appendChild(tpl);
  const backBtn = document.createElement('button');
  backBtn.className = 'back-btn'; backBtn.textContent = '← Chief Complaint';
  backBtn.addEventListener('click', () => { state.step='cc'; render(); });
  app.prepend(backBtn);

  const topic = state.topics[state.chosenTopicKey];
  app.querySelector('.protocol-context').textContent = `Complaint: ${topic.label}`;

  app.querySelectorAll('.choice-btn').forEach(btn => {
    const demo = btn.dataset.demo;
    const available = demo === 'adult' ? !!topic.adult : !!topic.pediatric;
    if(!available){ btn.disabled = true; btn.style.opacity = 0.35; }
    btn.addEventListener('click', () => {
      if(!available) return;
      state.chosenDemographic = demo;
      state.chosenProtocolId = demo === 'adult' ? topic.adult : topic.pediatric;
      state.step = 'vitals'; render();
    });
  });
}

// ---------- Step 3: Vitals & Weight ----------
function renderVitals(){
  const tpl = document.getElementById('tpl-vitals').content.cloneNode(true);
  app.innerHTML = '';
  app.appendChild(tpl);
  const proto = protocolById(state.chosenProtocolId);
  const backBtn = document.createElement('button');
  backBtn.className = 'back-btn'; backBtn.textContent = '← Back';
  backBtn.addEventListener('click', () => {
    const topic = state.topics[state.chosenTopicKey];
    state.step = (topic.adult && topic.pediatric) ? 'demographic' : 'cc';
    render();
  });
  app.prepend(backBtn);

  const title = document.createElement('h2');
  title.className = 'step-title';
  title.innerHTML = `<span class="step-num">✓</span> ${proto.title}`;
  app.querySelector('.screen').prepend(title);

  document.getElementById('lbHint').textContent = '';
  const weightInput = document.querySelector('input[name="weight"]');
  weightInput.addEventListener('input', () => {
    const kg = parseFloat(weightInput.value);
    document.getElementById('lbHint').textContent = kg ? `≈ ${(kg*2.20462).toFixed(1)} lb` : '';
  });

  document.getElementById('vitalsForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    state.vitals = Object.fromEntries(fd.entries());
    const branches = proto.branches;
    if(branches.length > 1){
      state.step = 'branch';
    } else {
      state.chosenBranchId = branches[0].id;
      state.step = 'protocol';
    }
    render();
  });
}

function vitalsSummaryHTML(){
  if(!state.vitals) return '';
  const v = state.vitals;
  const items = [];
  if(v.weight) items.push(`${v.weight} kg`);
  if(v.hr) items.push(`HR ${v.hr}`);
  if(v.sbp || v.dbp) items.push(`BP ${v.sbp||'?'}/${v.dbp||'?'}`);
  if(v.rr) items.push(`RR ${v.rr}`);
  if(v.spo2) items.push(`SpO2 ${v.spo2}%`);
  if(v.temp) items.push(`Temp ${v.temp}°F`);
  if(v.glucose) items.push(`Glu ${v.glucose}`);
  if(v.gcs) items.push(`GCS/LOC ${v.gcs}`);
  return items.map(i => `<span>${i}</span>`).join('');
}

// crude vital-based suggestion heuristics (advisory badge only — never auto-selects)
function suggestBranch(proto){
  const v = state.vitals || {};
  const sbp = parseFloat(v.sbp), spo2 = parseFloat(v.spo2), hr = parseFloat(v.hr);
  let best = null;
  for(const b of proto.branches){
    const label = b.id + ' ' + b.label.toLowerCase();
    let score = 0;
    if(/arrest|crashing/.test(label) && (v.gcs && /unresp|0|apneic/i.test(v.gcs))) score += 3;
    if(/shock|impending/.test(label) && sbp && sbp < 90) score += 2;
    if(/hypotension/.test(label) && sbp && sbp < 90) score += 2;
    if(/respiratory|stridor|wheeze/.test(label) && spo2 && spo2 < 92) score += 2;
    if(/hives|only/.test(label) && spo2 && spo2 >= 95) score += 1;
    if(score > 0 && (!best || score > best.score)) best = {id: b.id, score};
  }
  return best ? best.id : null;
}

// ---------- Step 4: Branch select ----------
function renderBranchSelect(){
  const tpl = document.getElementById('tpl-branch-select').content.cloneNode(true);
  app.innerHTML = '';
  app.appendChild(tpl);
  const proto = protocolById(state.chosenProtocolId);
  const backBtn = document.createElement('button');
  backBtn.className = 'back-btn'; backBtn.textContent = '← Vitals';
  backBtn.addEventListener('click', () => { state.step='vitals'; render(); });
  app.prepend(backBtn);

  app.querySelector('.protocol-context').textContent = proto.title;
  document.getElementById('vitalsSummary').innerHTML = vitalsSummaryHTML();

  const suggested = suggestBranch(proto);
  const list = document.getElementById('branchList');
  proto.branches.forEach(b => {
    const btn = document.createElement('button');
    btn.className = 'branch-item';
    btn.innerHTML = `${b.label}` + (b.id === suggested ? ' <span class="tag" style="background:#fbe9e3;color:#8a3f2c;">Suggested by vitals</span>' : '');
    btn.addEventListener('click', () => {
      state.chosenBranchId = b.id;
      state.step = 'protocol'; render();
    });
    list.appendChild(btn);
  });
  const note = document.createElement('p');
  note.className = 'meta-note';
  note.textContent = 'Vital-based suggestion is advisory only — use clinical judgment to pick the matching presentation.';
  list.after(note);
}

// ---------- Dose calculation from step text ----------
function computeDose(text, weightKg){
  if(!weightKg || isNaN(weightKg)) return null;
  const w = parseFloat(weightKg);

  // range per kg: "0.02 - 0.05 mg/kg" or "0.02-0.05 mg/kg"
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

  // max dose cap
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
  return `≈ ${doseStr} for ${w} kg${capped ? ' (capped at protocol maximum)' : ''}`;
}

// ---------- Step 5: Protocol view ----------
function renderProtocolView(){
  const tpl = document.getElementById('tpl-protocol-view').content.cloneNode(true);
  app.innerHTML = '';
  app.appendChild(tpl);
  const proto = protocolById(state.chosenProtocolId);
  const branch = proto.branches.find(b => b.id === state.chosenBranchId);

  const backBtn = document.createElement('button');
  backBtn.className = 'back-btn';
  backBtn.textContent = proto.branches.length > 1 ? '← Change presentation' : '← Vitals';
  backBtn.addEventListener('click', () => {
    state.step = proto.branches.length > 1 ? 'branch' : 'vitals';
    render();
  });
  app.prepend(backBtn);

  document.getElementById('protoTitle').textContent = proto.title;
  document.getElementById('protoBranchLabel').textContent =
    (proto.branches.length > 1 ? branch.label : '') ;
  document.getElementById('vitalsSummarySticky').innerHTML = vitalsSummaryHTML();

  // Universal / Pediatric Universal Care precede reminder
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

  const list = document.getElementById('stepsList');
  branch.steps.forEach((step, i) => {
    const li = document.createElement('li');
    li.className = 'step-item' + (step.drug_id ? ' has-drug' : '') + (step.goto_protocol ? ' goto' : '');
    const bullet = document.createElement('div');
    bullet.className = 'step-bullet';
    bullet.textContent = i+1;
    const body = document.createElement('div');
    body.style.flex = '1';
    const textDiv = document.createElement('div');
    textDiv.className = 'step-text';
    textDiv.textContent = step.text;
    body.appendChild(textDiv);

    const dose = computeDose(step.text, state.vitals && state.vitals.weight);
    if(dose){
      const doseDiv = document.createElement('div');
      doseDiv.className = 'step-dose-calc';
      doseDiv.textContent = dose;
      body.appendChild(doseDiv);
    }

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
  const backBtn = document.createElement('button');
  backBtn.className = 'back-btn'; backBtn.textContent = '← Home';
  backBtn.addEventListener('click', goHome);
  app.appendChild(backBtn);

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
        state.chosenProtocolId = p.id;
        state.chosenDemographic = p.demographic;
        state.chosenTopicKey = Object.keys(state.topics).find(k =>
          state.topics[k].adult === p.id || state.topics[k].pediatric === p.id);
        state.step = 'vitals'; render();
      });
      secDiv.appendChild(btn);
    });
    app.appendChild(secDiv);
  });
}

// ---------- Drug reference browse ----------
function renderDrugRef(){
  app.innerHTML = '';
  const backBtn = document.createElement('button');
  backBtn.className = 'back-btn'; backBtn.textContent = '← Home';
  backBtn.addEventListener('click', goHome);
  app.appendChild(backBtn);

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
