import json

# Transcribed from Toledo Fire & Rescue Bureau of EMS Patient Care Protocols (Responsoft, reviewed 04/22/2026)
# Each protocol = the standing-order flowchart broken into clinical branches (verbatim steps) +
# the companion "Medical Reference" page (history/signs/differential/pearls).
# NOTE: MVP set - highest-acuity adult + core pediatric protocols. Remainder of the 259-entry
# book to be converted in later passes (see manifest.json / raw/ for source text).

PROTOCOLS = [

{
  "id": "universal_patient_care", "title": "Universal Patient Care", "demographic": "adult",
  "section": "Adult", "source_pages": [14,15], "chief_complaint_tags": [],
  "always_first": True,
  "reference": {"pearls": [
    "Any patient contact that does not result in transport requires documentation and disposition.",
    "Minimum required vital signs on every patient include BP, Pulse, Respiratory rate, Pulse oximetry, and Pain severity.",
    "Pulse oximetry, glucose measurement, and temperature documentation is dependent on complaint.",
    "Timing of transport based on patient's clinical condition."
  ]},
  "branches": [{"id": "default", "label": "Every patient", "steps": [
    {"text": "Scene Safety & BSI (body substance isolation)."},
    {"text": "Bring all necessary equipment to patient's side; demonstrate professionalism and courtesy."},
    {"text": "PPE - consider airborne or droplet precautions."},
    {"text": "Initial assessment. BLS: consider Spinal Motion Restriction (SMR)."},
    {"text": "Pulse oximetry, supplemental oxygen, vital signs, temperature and blood glucose as indicated."},
    {"text": "Consider cardiac monitor / 12-lead ECG."},
    {"text": "Proceed to the appropriate protocol based on chief complaint."},
    {"text": "If patient doesn't fit a protocol, contact OLMC (Online Medical Control)."}
  ]}]
},
{
  "id": "pediatric_universal_care", "title": "Pediatric Universal Care", "demographic": "pediatric",
  "section": "Pediatric", "source_pages": [129,130], "chief_complaint_tags": [],
  "always_first": True,
  "reference": {"pearls": [
    "For the purposes of this protocol, a pediatric patient is < 16 years old.",
    "Any patient contact that does not result in transport requires documentation and disposition.",
    "Required vital signs on every patient include BP, pulse, RR, pain/severity.",
    "Pulse oximetry, glucose measurement, and temperature documentation is dependent on complaint.",
    "Timing of transport based on patient's clinical condition."
  ]},
  "branches": [{"id": "default", "label": "Every pediatric patient", "steps": [
    {"text": "Scene safety; bring all necessary equipment to patient's side; demonstrate professionalism and courtesy."},
    {"text": "PPE - consider airborne or droplet precautions."},
    {"text": "Initial assessment. BLS: consider Spinal Motion Restriction."},
    {"text": "Consider pulse oximetry, capnography, supplemental oxygen, pediatric vital signs, temperature and blood glucose as indicated."},
    {"text": "Consider cardiac monitor / 12-lead ECG."},
    {"text": "Proceed to the appropriate protocol based on chief complaint (e.g. Pediatric Cardiac Arrest -> Pediatric Pulseless Arrest)."},
    {"text": "If patient doesn't fit a protocol, contact OLMC."}
  ]}]
},

{
  "id": "asystole", "title": "Asystole (Includes POCUS)", "demographic": "adult",
  "section": "Adult Cardiovascular / Cardiac Arrest", "source_pages": [24,25],
  "chief_complaint_tags": ["cardiac arrest", "asystole", "no pulse", "unresponsive not breathing", "flatline"],
  "precedes": ["universal_patient_care"],
  "reference": {
    "history": ["Past medical history", "Medications", "Events", "End stage renal failure", "Estimated downtime", "Hypothermia?", "Overdose?", "DNR?"],
    "signs_symptoms": ["Pulseless", "Apneic", "No electrical activity on ECG", "No auscultated heart tones"],
    "differential": ["5 H's: Hypovolemia, Hypoxia, Hydrogen ion (acidosis), Hypo/Hyperkalemia, Hypothermia/Hyperthermia",
                     "5 T's: Tension pneumothorax, Tamponade, Toxins (beta/calcium blockers, digoxin, antidepressants, cocaine), Thrombosis (PE), Thrombosis (coronary)",
                     "Other: Trauma, electrical shock, pacemaker failure"],
    "pearls": ["Always confirm asystole in more than one lead.", "Always address correctable causes."]
  },
  "branches": [{"id": "default", "label": "Confirmed asystole", "steps": [
    {"text": "Immediate uninterrupted CPR."},
    {"text": "First airway: Supraglottic Airway (SGA) with EtCO2. If this fails, intubate through SGA or move to intubation with Video Laryngoscopy. Attach ResQPOD."},
    {"text": "Adult IV/IO access."},
    {"text": "Epinephrine 1 mg/10 mL - 1 mg IVP, IO. Repeat every 10 minutes. Maximum total 4 mg.", "drug_id": "epi_1_10"},
    {"text": "Identify / correct causes of asystole (H's and T's) - check Blood Glucose Analysis."},
    {"text": "If available, POCUS (linear probe) may be used during pulse checks to assess for cardiac activity at the Common Carotid Artery (CCA). Limit time off chest < 10 seconds."},
    {"text": "POCUS-assisted TOR guidelines: standard cardiac arrest care completed + asystole on monitor + absent CCA pulsation + persistently low EtCO2."},
    {"text": "Persistent asystole after 30 minutes of high-quality CPR with BLS and ALS interventions -> move to Termination of Resuscitation (TOR) guideline."},
    {"text": "AT ANY TIME ROSC achieved -> go to Post ROSC Care protocol.", "goto_protocol": "post_rosc_care"}
  ]}]
},
{
  "id": "pea", "title": "Pulseless Electrical Activity (PEA)", "demographic": "adult",
  "section": "Adult Cardiovascular / Cardiac Arrest", "source_pages": [26,27],
  "chief_complaint_tags": ["cardiac arrest", "pea", "pulseless electrical activity"],
  "precedes": ["universal_patient_care"],
  "reference": {
    "history": ["Past medical history", "Medications", "Events", "End stage renal failure", "Estimated downtime", "Hypothermia?", "Overdose?", "DNR?"],
    "signs_symptoms": ["Pulseless", "Apneic", "No auscultated heart tones"],
    "differential": ["Hypovolemia (trauma, AAA, other)", "Hypoxia", "Potassium (hypo/hyperkalemia)", "Overdose (TCAs, digoxin, beta blockers, calcium channel blockers)", "Acidosis", "Hypothermia", "Cardiac tamponade", "Massive MI", "Hyperkalemia"],
    "pearls": ["Always address correctable causes.", "Routine use of Sodium Bicarbonate, Dextrose, Naloxone and Calcium is NOT indicated unless a clinical scenario exists (e.g. blood sugar < 60; known IVDA; missed/on dialysis)."]
  },
  "branches": [{"id": "default", "label": "Confirmed PEA", "steps": [
    {"text": "Immediate uninterrupted CPR. Adult Airway & Adult IV/IO protocols."},
    {"text": "Epinephrine 1 mg/10 mL - 1 mg IVP, IO. Repeat every 10 minutes. Maximum total 4 mg.", "drug_id": "epi_1_10"},
    {"text": "Consider H's and T's causes. Routine use of the following is NOT indicated unless clinical info suggests hypoglycemia, opiate overdose, or hyperkalemia:"},
    {"text": "Hypoglycemia suspected: Dextrose 10% (D10) - 5 gm IV Infusion (50 mL). Withdraw 50 mL from 250 mL NS bag, add 1 amp D50 = D10. Give 50 mL (5g) increments until normal mentation. Maximum total 25 gm (250 mL).", "drug_id": "dextrose_10"},
    {"text": "Opiate overdose suspected: Naloxone (Narcan) 2-4 mg IVP, IO.", "drug_id": "naloxone"},
    {"text": "Hyperkalemia arrest: Calcium Chloride 1 gm IVP, IO.", "drug_id": "calcium_chloride"},
    {"text": "TCA / hyperkalemia / renal failure: Sodium Bicarbonate (1 mEq/mL) 1 mEq/kg IVP, IO.", "drug_id": "sodium_bicarbonate"},
    {"text": "Beta blocker overdose suspected: Glucagon 1 mg IVP.", "drug_id": "glucagon"},
    {"text": "Suspected tension pneumothorax: Needle Chest Decompression."},
    {"text": "POCUS (if available): assess CCA during pulse checks, limit time off chest < 10 sec. Pseudo-PEA criteria: organized ECG + rising EtCO2 + visible CCA pulsation. If pseudo-PEA present: fluid resuscitate, begin Epinephrine infusion, treat reversible causes, pause CPR."},
    {"text": "Criteria to discontinue: cease efforts per department guideline."},
    {"text": "AT ANY TIME ROSC achieved -> go to Post ROSC Care protocol.", "goto_protocol": "post_rosc_care"}
  ]}]
},
{
  "id": "vfib_pulseless_vtach", "title": "V-Fib/Pulseless V-Tach", "demographic": "adult",
  "section": "Adult Cardiovascular / Cardiac Arrest", "source_pages": [28,29],
  "chief_complaint_tags": ["cardiac arrest", "v-fib", "vfib", "ventricular fibrillation", "pulseless v-tach", "vtach"],
  "precedes": ["universal_patient_care"],
  "reference": {
    "history": ["Past medical history", "Medications", "Events", "End stage renal failure", "Estimated downtime", "Hypothermia?", "Overdose?", "DNR?"],
    "signs_symptoms": ["Pulseless", "Apneic", "No auscultated heart tones"],
    "differential": ["Medical or trauma", "Hypoxia", "Potassium (hypo/hyperkalemia)", "Overdose", "Acidosis", "Hypothermia", "Device error - check leads", "Death"],
    "pearls": ["Reassess airway frequently.", "Suspected HYPERKALEMIC arrest: give Calcium Chloride and Sodium Bicarbonate.", "Torsades de Pointes: 2 grams Magnesium Sulfate.", "Uninterrupted high-quality CPR and early defibrillation are key.", "ALS crew discretion on advanced airway (SGA vs VL ETT).", "Persistent VF/pulseless VT (>3 shocks): consider adjusting pad placement to Anterior/Posterior if not previously used."]
  },
  "branches": [{"id": "default", "label": "Confirmed VF / Pulseless VT", "steps": [
    {"text": "Defibrillation sequence: immediately defibrillate VF/Pulseless VT at 200, 300, 360 Joules. Immediately resume CPR."},
    {"text": "Reassess rhythm and repeat every 2 minutes. Charge defibrillator at 1:45 in the 2-minute cycle. At 2 minutes: pulse check, med admin, defibrillate. Dump charge if rhythm becomes non-shockable."},
    {"text": "CPR: immediate uninterrupted manual or automated CPR; use metronome and feedback device if available."},
    {"text": "Adult Airway protocol; begin ventilation 10/min."},
    {"text": "Epinephrine 1 mg/10 mL - 1 mg IVP, IO. Repeat every 10 minutes. Maximum total 4 mg.", "drug_id": "epi_1_10"},
    {"text": "Amiodarone (Cordarone) 300 mg IVP, IO. After 3-5 minutes, Amiodarone 150 mg IVP, IO.", "drug_id": "amiodarone"},
    {"text": "Torsades de Pointes: Magnesium Sulfate 2 gm IVP.", "drug_id": "magnesium_sulfate"},
    {"text": "Suspected hyperkalemia: Calcium Chloride 1 gm IVP, IO AND Sodium Bicarbonate 50 mEq IVP, IO.", "drug_id": "calcium_chloride"},
    {"text": "Persistent VF/pulseless VT after 3 shocks: adjust pad placement to Anterior/Posterior if not previously used. Consider new pads following multiple defibrillations with original set."},
    {"text": "Dual Sequential Defibrillation (DSD) - indications: refractory VF/pVT after 3 standard shocks. Procedure: bring 2nd defibrillator, apply 2nd set of patches (one set ant/post, other ant/lat), one paramedic operates both monitors, charge both to max joules, call 'CLEAR', push button on monitor #1 then immediately monitor #2 (not simultaneously), resume standard care. Subsequent VF/pVT: use DSD again at same (maximal) energy."},
    {"text": "TOR (Termination of Resuscitation) criteria met? -> follow TOR guideline."},
    {"text": "AT ANY TIME ROSC achieved -> go to Post ROSC Care protocol.", "goto_protocol": "post_rosc_care"}
  ]}]
},

{
  "id": "chest_pain_acs", "title": "Chest Pain (Suspected ACS)", "demographic": "adult",
  "section": "Adult Cardiovascular", "source_pages": [32,33],
  "chief_complaint_tags": ["chest pain", "acs", "heart attack", "mi", "cardiac chest pain"],
  "precedes": ["universal_patient_care"],
  "reference": {
    "history": ["Age", "Medications", "Erectile dysfunction meds?", "Past medical history", "Diabetes", "Allergies", "Onset", "Palliation/provocation", "Quality", "Region/radiation/referred", "Severity", "Time (duration)"],
    "signs_symptoms": ["Chest pain", "Location (substernal, epigastric, arm, jaw, neck, shoulder)", "Radiation of pain", "Pale, diaphoresis", "Shortness of breath", "Nausea, vomiting, dizziness"],
    "differential": ["Trauma vs medical", "Acute coronary syndrome vs MI", "Pericarditis", "PE - Asthma/COPD", "Pneumothorax", "Aortic dissection", "GE reflux, hiatal hernia", "Esophageal spasm", "Chest wall pain", "Pleural pain", "Overdose (cocaine)"],
    "pearls": ["Avoid NTG in patients who used erectile dysfunction meds (Viagra, Levitra, Cialis) in the past 24 hours.", "If patient has STEMI, establish a 2nd IV.", "Monitor for hypotension after NTG administration.", "Diabetic, geriatric, and female patients often have atypical symptoms."]
  },
  "branches": [{"id": "default", "label": "Suspected ACS", "steps": [
    {"text": "Oxygen to maintain SpO2 > 94%.", "drug_id": "oxygen"},
    {"text": "Aspirin 324 mg PO, unless allergy to ASA.", "drug_id": "aspirin"},
    {"text": "12-Lead ECG (EMT may set up and transmit)."},
    {"text": "Adult IV/IO protocol - prefer 2 saline locks. Avoid saline infusions in STEMI unless hypotensive (delays cath lab transit)."},
    {"text": "If Paramedic interprets 12-lead as STEMI: transmit 12-lead ECG, contact dispatch to pre-alert closest STEMI receiving facility, declare STEMI alert on transport."},
    {"text": "Inferior MI? Do right-sided ECG (V4R). Use caution with nitroglycerin in Inferior MI (+V4R) WITHOUT adequate fluid resuscitation."},
    {"text": "Hypotension? Normal Saline 0.9% 1 L Fluid Bolus and re-evaluate.", "drug_id": "normal_saline"},
    {"text": "Nitroglycerin 0.4 mg SL (spray or tablet) every 5 minutes if SBP > 90.", "drug_id": "nitroglycerin"},
    {"text": "Continued pain: Fentanyl (Sublimaze) 25-50 mcg IVP, up to 100 mcg.", "drug_id": "fentanyl"},
    {"text": "May repeat Nitroglycerin 0.4 mg SL every 5 minutes if SBP > 90.", "drug_id": "nitroglycerin"},
    {"text": "Hypotension / arrhythmia develops -> treat per that protocol."},
    {"text": "Nausea/vomiting: consider Ondansetron (Zofran) 4 mg IVP, IM.", "drug_id": "ondansetron"}
  ]}]
},

{
  "id": "hypotension_shock_non_trauma", "title": "Hypotension/Shock Non-Trauma", "demographic": "adult",
  "section": "Adult Cardiovascular", "source_pages": [36,37],
  "chief_complaint_tags": ["hypotension", "shock", "low blood pressure", "sepsis", "septic shock"],
  "precedes": ["universal_patient_care"],
  "reference": {
    "history": ["Blood loss: GI, AAA, ectopic, vaginal", "Fluid loss - vomiting, diarrhea, fever", "Infection", "Cardiac: ischemia (MI, CHF)", "Medications", "Allergic reaction", "Pregnancy", "Poor PO intake history"],
    "signs_symptoms": ["Restless, confused", "Weakness, dizziness", "Weak, rapid pulse", "Pale, cool, clammy skin", "Delayed capillary refill", "Hypotension", "Coffee-ground emesis", "Tarry stools"],
    "differential": ["Shock: hypovolemic, cardiogenic, septic, neurogenic, anaphylactic", "Ectopic pregnancy", "Dysrhythmias", "PE", "Tension pneumothorax", "Medications/OD", "Vasovagal", "Physiologic"],
    "pearls": ["Hypotension = SBP < 90 mmHg.", "Consider orthostatic vitals on non-trauma patients with suspected blood/fluid loss.", "Vasopressors should be given through a large-bore antecubital site.", "Use extreme caution with peripheral-line vasopressors; stop and notify receiving facility if any sign of infiltration."]
  },
  "branches": [
    {"id": "trauma", "label": "Trauma etiology", "steps": [{"text": "Treat per the appropriate trauma protocol instead of this one."}]},
    {"id": "cardiac", "label": "Cardiac etiology", "steps": [
      {"text": "No rales present: Normal Saline 0.9% 500 mL Fluid Bolus.", "drug_id": "normal_saline"},
      {"text": "Treat per the appropriate cardiac protocol."}
    ]},
    {"id": "symptomatic_non_cardiac_non_trauma", "label": "Symptomatic, non-cardiac, non-trauma", "steps": [
      {"text": "Universal Patient Care, Adult IV/IO protocol."},
      {"text": "Normal Saline 0.9% - 20 mL/kg Fluid Bolus.", "drug_id": "normal_saline"},
      {"text": "SEPTIC SHOCK consideration: assure aggressive crystalloid given before vasopressors - Normal Saline 30 mL/kg Fluid Bolus. See Fever/Suspected Sepsis protocol.", "drug_id": "normal_saline", "goto_protocol": "fever_suspected_sepsis"},
      {"text": "Pressor needed (paramedic discretion)? Epinephrine Push Dose 10-20 mcg IVP, IO. Dilution: discard 9 mL of Epi 1:10,000 (0.1 mg/mL), draw up 9 mL NS to make Epi 1:100,000 (10 mcg/mL). Give 1-2 mL every 3 minutes until BP/HR goals achieved. LABEL syringe.", "drug_id": "epi_push_dose"},
      {"text": "If pressor needed beyond push-dose: Epinephrine Drip 1 mg mixed into 1,000 mL NS (60 gtt set). Infuse until HR > 60 and MAP > 65 mmHg. LABEL the bag.", "drug_id": "epi_drip"}
    ]},
    {"id": "no_trauma_stable", "label": "Not trauma, otherwise stable", "steps": [{"text": "Observe and reassess."}]}
  ]
},

{
  "id": "altered_mental_status", "title": "Altered Mental Status", "demographic": "adult",
  "section": "Adult Neurological", "source_pages": [73,74],
  "chief_complaint_tags": ["altered mental status", "ams", "confusion", "unresponsive", "decreased loc", "altered loc"],
  "precedes": ["universal_patient_care"],
  "reference": {
    "history": ["Known diabetic, medic alert tag", "Drugs, drug paraphernalia", "Report of illicit drug use or ingestion", "Past medical history", "Medications", "History of trauma"],
    "signs_symptoms": ["Decreased mental status", "Change in baseline mental status", "Bizarre behavior", "Hypoglycemia (cool, diaphoretic skin)", "Hyperglycemia (warm, dry skin, fruity breath)", "Kussmaul respirations, dehydration"],
    "differential": ["Head trauma", "CNS (CVA, tumor, seizure, infection)", "Infection", "Thyroid", "Shock (septic, metabolic, traumatic)", "Diabetes (hyper/hypoglycemia)", "Toxicologic", "Acidosis/Alkalosis", "Environmental exposure", "Pulmonary", "Electrolyte abnormality", "Psychiatric"],
    "pearls": ["Safer to assume hypoglycemia than hyperglycemia if in doubt; recheck blood sugar after D10/glucagon.", "Do not let alcohol confuse the clinical picture.", "Do not give oral glucose if patient cannot protect airway.", "Consider patient restraints.", "Omit thiamine if no signs of malnutrition or alcoholism."]
  },
  "branches": [{"id": "default", "label": "Altered mental status", "steps": [
    {"text": "Consider Spinal Motion Restriction (SMR)."},
    {"text": "Adult IV/IO protocol; Blood Glucose Analysis; 12-lead ECG."},
    {"text": "If signs of shock: Normal Saline 0.9% 20 mL/kg Fluid Bolus.", "drug_id": "normal_saline"},
    {"text": "Glucose abnormal? -> go to Hypoglycemia/Hyperglycemia protocol.", "goto_protocol": "hypoglycemia_hyperglycemia"},
    {"text": "Hypotensive/shock? -> go to Hypotension/Shock Non-Trauma protocol.", "goto_protocol": "hypotension_shock_non_trauma"},
    {"text": "Suspected overdose/toxic exposure? -> go to that protocol.", "goto_protocol": "overdose_toxic_exposure"},
    {"text": "Fever/suspected sepsis? -> go to that protocol.", "goto_protocol": "fever_suspected_sepsis"},
    {"text": "Arrhythmia present? -> go to specific protocol: Bradycardia-Unstable or Tachycardia w/Pulse (SVT, A-Fib/A-Flutter, VT)."}
  ]}]
},

{
  "id": "seizure", "title": "Seizure", "demographic": "adult",
  "section": "Adult Neurological", "source_pages": [78,79],
  "chief_complaint_tags": ["seizure", "convulsion", "status epilepticus"],
  "precedes": ["universal_patient_care"],
  "reference": {
    "history": ["Reported/witnessed seizure", "Previous seizure history", "Medical alert tag", "History of trauma", "History of diabetes", "History of pregnancy"],
    "signs_symptoms": ["Decreased mental status", "Sleepiness", "Incontinence", "Observed seizure activity", "Evidence of trauma", "Unconsciousness"],
    "differential": ["CNS trauma", "Tumor", "Metabolic, hepatic, renal failure", "Hypoxia", "Electrolyte abnormality", "Drugs, meds, noncompliance", "Infection/fever", "Alcohol withdrawal", "Eclampsia", "Stroke", "Hyperthermia", "Hypoglycemia"],
    "pearls": ["Status Epilepticus: >2 successive seizures without a period of consciousness/recovery.", "Grand mal: generalized - LOC, incontinence, tongue trauma.", "Focal seizures (petit mal): only part of the body, no LOC.", "Jacksonian seizures: focal seizures that become generalized.", "Be prepared for airway problems and continued seizures.", "Assess for occult trauma and substance abuse.", "Be prepared to assist ventilation if midazolam is used.", "Seizures in pregnant patients: follow Obstetrical Emergency.", "Thiamine may be omitted if patient does not appear malnourished."]
  },
  "branches": [{"id": "actively_seizing", "label": "Actively seizing", "steps": [
    {"text": "Spinal Motion Restriction (SMR); check Blood Glucose Analysis."},
    {"text": "No IV/IO access - Age < 65: Midazolam (Versed) 10 mg IM. Age > 65: Midazolam 5 mg IM.", "drug_id": "midazolam"},
    {"text": "IV/IO present: Midazolam (Versed) 2-5 mg IVP, IO.", "drug_id": "midazolam"},
    {"text": "Still seizing? Repeat Midazolam (Versed) 2-5 mg IVP, IO.", "drug_id": "midazolam"},
    {"text": "Recurrent/refractory seizure: Ketamine (Ketalar) (50 mg/mL) 1 mg/kg IVP, IO. Maximum dose 100 mg. Full monitoring mandatory including EtCO2. Consider intubation with Video Laryngoscopy.", "drug_id": "ketamine"},
    {"text": "Adult IV/IO protocol."}
  ]},
  {"id": "postictal", "label": "Postictal (seizure has stopped)", "steps": [
    {"text": "Blood Glucose Analysis."},
    {"text": "Glucose < 60 mg/dL -> go to Hypoglycemia protocol.", "goto_protocol": "hypoglycemia_hyperglycemia"}
  ]}]
},

{
  "id": "suspected_stroke", "title": "Suspected Stroke", "demographic": "adult",
  "section": "Adult Neurological", "source_pages": [80,81],
  "chief_complaint_tags": ["stroke", "cva", "facial droop", "slurred speech", "weakness one side"],
  "precedes": ["universal_patient_care"],
  "reference": {
    "history": ["Previous CVA, TIA", "Previous cardiac/vascular surgery", "Diabetes, HTN, CAD", "AFib", "Medications (blood thinners)", "Trauma?"],
    "signs_symptoms": ["Altered mental status", "Weakness/paralysis", "Blindness or sensory loss", "Aphasia/dysarthria", "Syncope", "Vertigo/dizziness", "Vomiting", "Headache", "Seizures", "Respiratory pattern change", "Hyper/Hypotension"],
    "differential": ["See Altered Mental Status", "TIA", "Seizure", "Hypoglycemia", "CVA", "Tumor", "Trauma"],
    "pearls": ["Optimize scene/transport time if symptom onset < 24 hours.", "Onset = last witnessed time patient was symptom-free.", "Monitor for airway problems (swallowing, vomiting).", "Always assess for hypoglycemia.", "Document RACE score and 12-lead ECG.", "Interventional stroke centers = transport to closest appropriate Comprehensive Stroke Center."]
  },
  "branches": [{"id": "default", "label": "Suspected stroke", "steps": [
    {"text": "Blood Glucose Analysis."},
    {"text": "BEFAST exam / RACE Scoring Tool. If positive and symptoms < 24 hours: determine 'Last Known Well' time; bring patient ID to hospital for quick registration."},
    {"text": "Adult IV/IO protocol; 12-Lead ECG."},
    {"text": "Pediatric patient with suspected stroke? Transport to Pediatric Hospital (SVMMC or ProMedica Toledo Hospital ED)."},
    {"text": "Calculate RACE Scoring Tool. Score >= 5: declare 'RACE Alert', transport to closest Comprehensive Stroke or Thrombectomy-capable Center."},
    {"text": "Score < 5: declare 'Stroke Alert', transport to closest Primary Stroke Center."},
    {"text": "Primary Stroke Centers: Mercy St. Charles, Mercy St. Vincent, ProMedica Flower, ProMedica Bay Park, ProMedica Toledo Hospital, University of Toledo Medical Center."},
    {"text": "Comprehensive Stroke Centers: Mercy St. Vincent, ProMedica Toledo Hospital. Thrombectomy-Capable: University of Toledo Medical Center."}
  ]}]
},

{
  "id": "respiratory_distress", "title": "Respiratory Distress", "demographic": "adult",
  "section": "Adult Respiratory", "source_pages": [100,101],
  "chief_complaint_tags": ["respiratory distress", "shortness of breath", "sob", "difficulty breathing", "wheezing", "asthma", "copd"],
  "precedes": ["universal_patient_care"],
  "reference": {
    "history": ["Asthma", "COPD", "CHF", "Home treatment (oxygen/nebulizer)", "Meds (theophylline, steroids, inhalers)", "Toxic exposure", "Smoke inhalation"],
    "signs_symptoms": ["SOB", "Pursed lip breathing", "Decreased ability to speak", "Increased respiratory rate and effort", "Wheezing, rhonchi, rales, stridor", "Accessory muscle use", "Fever, cough, tachycardia"],
    "differential": ["Asthma", "Anaphylaxis", "Aspiration", "COPD", "Pneumonia/pleural effusion", "Pneumothorax", "Cardiac (MI/CHF)", "PE", "Tamponade", "Hyperventilation", "Inhaled toxin"],
    "pearls": ["ALWAYS give Epinephrine 1 mg/1 mL IM (never IV); 1 mg/10 mL may be given only as directed in the flowchart.", "Monitor pulse ox continuously.", "CPAP indicated in hypertensive pulmonary edema and COPD exacerbation with impending respiratory arrest.", "Contact OLMC before epinephrine in patients > 50 years old, cardiac history, or HR > 150 - perform 12-lead ECG on these patients.", "Record/monitor ETCO2 for respiratory distress patients."]
  },
  "branches": [
    {"id": "rales_chf", "label": "Rales / CHF picture", "steps": [
      {"text": "Follow Acute Pulmonary Edema protocol with immediate consideration of CPAP.", "goto_protocol": "acute_pulmonary_edema"},
      {"text": "Contact OLMC if patient does not meet criteria for Epinephrine."}
    ]},
    {"id": "wheezes", "label": "Wheezes", "steps": [
      {"text": "Adult IV/IO protocol. Consider CPAP for severe COPD."},
      {"text": "Albuterol (Proventil) 2.5 mg NEB.", "drug_id": "albuterol"},
      {"text": "Albuterol 2.5 mg NEB mixed with Ipratropium (Atrovent) 0.5 mg NEB. May repeat x1.", "drug_id": "albuterol"},
      {"text": "Consider Methylprednisolone (Solu-Medrol) 125 mg IVP.", "drug_id": "methylprednisolone"},
      {"text": "Consider Magnesium Sulfate 2 gm IV Infusion, mixed in 50 mL D5W, run wide open with 60 gtt set, delivered over 10-20 minutes.", "drug_id": "magnesium_sulfate"},
      {"text": "Consider Epinephrine 1 mg/1 mL 0.5 mg IM. May repeat x1.", "drug_id": "epi_1_1"}
    ]},
    {"id": "stridor", "label": "Stridor", "steps": [
      {"text": "Adult IV/IO protocol. Nebulized Saline 3 mL."},
      {"text": "If no improvement: Epinephrine 1 mg/1 mL 0.3-0.5 mg NEB mixed with 3 mL NS.", "drug_id": "epi_1_1"},
      {"text": "Methylprednisolone (Solu-Medrol) 125 mg IVP.", "drug_id": "methylprednisolone"},
      {"text": "AEMT: Epinephrine 1 mg/1 mL 0.3-0.5 mg IM.", "drug_id": "epi_1_1"},
      {"text": "Adult Airway protocol as needed. For severe cases: Epinephrine 1 mg/10 mL (0.1 mcg/mL... i.e. 1:10,000) 1 mcg/kg IVP - each 1 mL = 100 mcg; typical adult dose ~100 mcg.", "drug_id": "epi_1_10"}
    ]},
    {"id": "respiratory_insufficiency", "label": "Respiratory insufficiency / CPAP intolerance", "steps": [
      {"text": "Position of comfort. CPAP settings range 5-10 cmH2O."},
      {"text": "Anxiety/intolerance to CPAP, if SBP > 100 and not tolerating mask: Ketamine (Ketalar) (100 mg/mL) 0.5 mg/kg IN, IM, OR Ketamine 25 mg IVP, IO mixed with 50 mL NS over 10 minutes.", "drug_id": "ketamine"},
      {"text": "Additional sedation needed: Midazolam (Versed) 2-5 mg IVP, maximum 5 mg, OR Midazolam 2 mg IN if needed.", "drug_id": "midazolam"}
    ]}
  ]
},

{
  "id": "overdose_toxic_exposure", "title": "Overdose/Toxic Exposure", "demographic": "adult",
  "section": "Adult Toxicology", "source_pages": [108,109],
  "chief_complaint_tags": ["overdose", "od", "toxic exposure", "poisoning", "ingestion"],
  "precedes": ["universal_patient_care"],
  "reference": {
    "history": ["Ingestion or suspected ingestion of toxic substance", "Substance, quantity, route", "Time of ingestion", "Reason (suicidal, accidental, criminal)", "Available medications in home", "Past medical history, medications"],
    "signs_symptoms": ["Mental status changes", "Hypotension/hypertension", "Decreased respiratory rate", "Tachycardia, dysrhythmias", "Seizures"],
    "differential": ["TCAs", "Acetaminophen", "Depressants", "Stimulants", "Anticholinergic", "Cardiac medications", "Solvents, alcohols, cleaning agents", "Insecticides (organophosphates)"],
    "pearls": ["Do not rely on patient's history of ingestion in a suicide attempt.", "Bring bottles to the ED.", "Depressants: decreased HR/BP/temp/respirations, non-specific pupils.", "Stimulants: increased HR/BP/temp, dilated pupils, seizures.", "Anticholinergic: increased HR/temp, dilated pupils, mental status change.", "Insecticides: increased/decreased HR, increased secretions, N/V/D, pinpoint pupils.", "Consider restraints per policy.", "ALS units may transport patients who received activated charcoal."]
  },
  "branches": [
    {"id": "respiratory_depression", "label": "Respiratory depression (suspected opioid)", "steps": [
      {"text": "EMT: Naloxone (Narcan) 2-4 mg IN.", "drug_id": "naloxone"},
      {"text": "AEMT/Paramedic: Naloxone (Narcan) 2-4 mg IN, IVP, IO, IM to reverse respiratory depression. May repeat x2.", "drug_id": "naloxone"},
      {"text": "Refusal of care? Follow Refusal Procedure."}
    ]},
    {"id": "carbon_monoxide", "label": "Carbon monoxide exposure", "steps": [
      {"text": "Use co-oximetry (SpCO) to screen: headache, dizziness, weakness, confusion, LOC."},
      {"text": "Treatment thresholds: COHb > 5% in non-smokers, > 10% in smokers."},
      {"text": "Treatment: 100% Oxygen by NRB.", "drug_id": "oxygen"},
      {"text": "Hyperbaric facility consideration: COHb > 25-30%, neurological impairment, cardiac involvement, or pregnancy."}
    ]},
    {"id": "beta_calcium_blocker", "label": "Beta / Calcium channel blocker overdose", "steps": [
      {"text": "Beta blocker OD: Glucagon 1 mg IVP, IN, IM.", "drug_id": "glucagon"},
      {"text": "Calcium channel blocker OD: Calcium Chloride 1 gm Slow IVP.", "drug_id": "calcium_chloride"}
    ]},
    {"id": "cyanide", "label": "Cyanide exposure", "steps": [
      {"text": "Adult > 70 kg (154 lbs) with suspected cyanide poisoning: Cyanokit (Hydroxocobalamin) 5 gm IV Infusion. Add 200 mL NS to upright vial via transfer spike to fill line, invert 60 sec, use vented tubing + filter line, infuse over 15 minutes.", "drug_id": "cyanokit"}
    ]},
    {"id": "tricyclic", "label": "Tricyclic (TCA) ingestion", "steps": [
      {"text": "12-Lead ECG."},
      {"text": "Sodium Bicarbonate (1 mEq/mL) 1-2 mEq/kg IVP for hypotension, seizures, ventricular dysrhythmias, or mental status changes.", "drug_id": "sodium_bicarbonate"},
      {"text": "Otherwise treat per the appropriate protocol for the presenting symptom."}
    ]}
  ]
},

{
  "id": "allergic_reaction", "title": "Allergic Reaction", "demographic": "adult",
  "section": "Adult Respiratory", "source_pages": [96,97],
  "chief_complaint_tags": ["allergic reaction", "anaphylaxis", "hives", "allergy"],
  "precedes": ["universal_patient_care"],
  "reference": {
    "history": ["Onset/location", "Insect sting or bite", "Food allergy/exposure", "Medication allergy/exposure", "New clothing, soap", "Past history", "Medication history"],
    "signs_symptoms": ["Itching/hives", "Coughing/wheezing/respiratory distress", "Chest or throat tightening", "Difficulty swallowing", "Hypotension/shock", "Edema"],
    "differential": ["Urticaria", "Anaphylaxis", "Shock", "Angioedema", "Aspiration", "Vasovagal", "Asthma/COPD", "CHF"],
    "pearls": ["Epinephrine may precipitate cardiac ischemia - use caution in patients > 50 years old; perform ECG.", "Shorter onset = more severe reaction."]
  },
  "branches": [
    {"id": "hives_only", "label": "Hives / Rash only - no respiratory component", "steps": [
      {"text": "IV / cardiac monitor."},
      {"text": "Diphenhydramine (Benadryl) 50 mg IVP, IM.", "drug_id": "diphenhydramine"},
      {"text": "Reassess. If hypotension develops -> Hypotension protocol. If arrhythmia -> Arrhythmia protocol. If respiratory distress develops -> Respiratory Distress protocol.", "goto_protocol": "hypotension_shock_non_trauma"}
    ]},
    {"id": "respiratory_not_arrest", "label": "Respiratory distress - not in arrest/shock", "steps": [
      {"text": "IV / cardiac monitor."},
      {"text": "EMT-Anaphylaxis only: Epinephrine 1 mg/1 mL 0.3 mg Auto-Injector, may repeat x1.", "drug_id": "epi_1_1"},
      {"text": "Epinephrine 1 mg/1 mL 0.5 mg IM. May repeat x1 in 5 minutes. If more than 2 IM doses needed, go to IV.", "drug_id": "epi_1_1"},
      {"text": "Paramedic only: Diphenhydramine (Benadryl) 50 mg IVP, IM.", "drug_id": "diphenhydramine"},
      {"text": "Paramedic only: Methylprednisolone (Solu-Medrol) 125 mg IVP, IM.", "drug_id": "methylprednisolone"}
    ]},
    {"id": "impending_arrest_shock", "label": "Impending arrest / shock", "steps": [
      {"text": "Adult IV/IO, cardiac monitor."},
      {"text": "Epinephrine 1 mg/1 mL 0.5 mg IM (Paramedic only). May repeat x1 in 5 minutes. If more than 2 IM doses needed, go to IV.", "drug_id": "epi_1_1"},
      {"text": "Epinephrine 1:10,000 (Epinephrine 1 mg/10 mL) 0.1 mg IVP (100 mcg). Give every minute until symptoms improve. NOTE: this is NOT the same as Push Dose Epinephrine.", "drug_id": "epi_1_10"},
      {"text": "No improvement, paramedic discretion, requires large-bore IV (18 or 16 gauge preferred): Epinephrine Push Dose 10-20 mcg IVP, IO. Dilution: discard 9 mL Epi 1:10,000, draw 9 mL NS to make 1:100,000 (10 mcg/mL). Give 1-2 mL every 3 minutes until BP/HR goals met. LABEL syringe.", "drug_id": "epi_push_dose"},
      {"text": "Still refractory: Epinephrine Drip 1 mg mixed into 1,000 mL NS (60 gtt set). Infuse until HR > 60 and MAP > 65 mmHg. LABEL the bag.", "drug_id": "epi_drip"}
    ]},
    {"id": "crashing_anaphylaxis", "label": "Crashing anaphylaxis (unconscious, requiring assisted ventilations, apneic, or arrested)", "steps": [
      {"text": "Give Epinephrine as above."},
      {"text": "Intubate - first best attempt, no SGA, needs ETT."}
    ]}
  ]
},

{
  "id": "pediatric_altered_mental_status", "title": "Pediatric Altered Mental Status", "demographic": "pediatric",
  "section": "Pediatric Neurological", "source_pages": [152,153],
  "chief_complaint_tags": ["altered mental status", "ams", "confusion", "unresponsive", "altered loc"],
  "precedes": ["pediatric_universal_care"],
  "reference": {
    "history": ["Known diabetic, medic alert tag", "Drugs, drug paraphernalia", "Report of illicit drug use or ingestion", "Past medical history", "Medications", "History of trauma"],
    "signs_symptoms": ["Decreased mental status", "Change in baseline mental status", "Bizarre behavior", "Hypoglycemia (cool, diaphoretic skin)", "Hyperglycemia (warm, dry skin, fruity breath)", "Kussmaul respirations, dehydration"],
    "differential": ["Head trauma", "CNS (CVA, tumor, seizure, infection)", "Infection", "Thyroid", "Shock (septic, metabolic, traumatic)", "Diabetes (hyper/hypoglycemia)", "Toxicologic", "Acidosis/Alkalosis", "Environmental exposure", "Pulmonary", "Electrolyte abnormality", "Psychiatric"],
    "pearls": ["Be aware of AMS as a sign of environmental toxin or Haz-Mat exposure.", "Safer to assume hypoglycemia than hyperglycemia if in doubt.", "Low glucose < 60, normal 60-120, high > 250."]
  },
  "branches": [{"id": "default", "label": "Pediatric altered mental status", "steps": [
    {"text": "Consider Spinal Motion Restriction."},
    {"text": "Pediatric Universal Care, Pediatric IV/IO, Blood Glucose."},
    {"text": "If signs of shock: Normal Saline 0.9% 20 mL/kg Fluid Bolus.", "drug_id": "normal_saline"},
    {"text": "Glucose abnormal? -> go to Pediatric Hypoglycemia/Hyperglycemia protocol.", "goto_protocol": "pediatric_hypoglycemia_hyperglycemia"},
    {"text": "Shock present? -> go to Pediatric Hypotension/Sepsis/Shock Non-Trauma protocol."},
    {"text": "Suspected overdose/toxic/cyanide exposure? -> go to that protocol.", "goto_protocol": "pediatric_overdose_toxic_exposure"},
    {"text": "Fever/suspected sepsis? -> go to that protocol."},
    {"text": "Arrhythmia? -> go to specific protocol: Pediatric Bradycardia or Pediatric Tachycardia w/Pulse."}
  ]}]
},

{
  "id": "pediatric_seizure", "title": "Pediatric Seizure", "demographic": "pediatric",
  "section": "Pediatric Neurological", "source_pages": [154,155],
  "chief_complaint_tags": ["seizure", "convulsion", "febrile seizure"],
  "precedes": ["pediatric_universal_care"],
  "reference": {
    "history": ["Fever", "Previous seizure history", "Reported seizure activity", "History of recent head trauma", "Congenital abnormality"],
    "signs_symptoms": ["Observed seizure activity", "Altered mental status", "Hot, dry skin or elevated body temperature"],
    "differential": ["Fever", "Infection", "Head trauma", "Medication/toxin", "Hypoxia/respiratory failure", "Hypoglycemia", "Metabolic abnormality/acidosis", "Tumor"],
    "pearls": ["Status Epilepticus: >2 successive seizures without a period of consciousness/recovery.", "Be prepared to assist ventilation if Versed is used.", "Immobilize the spine if trauma suspected.", "In an infant, a seizure may be the only evidence of a closed head injury."]
  },
  "branches": [{"id": "active_seizure", "label": "Active seizure", "steps": [
    {"text": "Pediatric Airway protocol as needed."},
    {"text": "Pediatric IV/IO; Blood Glucose."},
    {"text": "Glucose < 60 mg/dL -> go to Pediatric Hypoglycemia/Hyperglycemia protocol.", "goto_protocol": "pediatric_hypoglycemia_hyperglycemia"},
    {"text": "Midazolam (Versed) (5 mg/mL) 0.2 mg/kg IN, IM, IVP, IO. May repeat x1. Maximum dosing 5 mg.", "drug_id": "midazolam"},
    {"text": "Continued seizure activity after 2 doses of midazolam: Ketamine (Ketalar) (50 mg/mL) 1 mg/kg IVP, IO. Maximum 100 mg. Be prepared to assist ventilations / place SGA.", "drug_id": "ketamine"},
    {"text": "Fever present? Begin cooling measures."}
  ]}]
},

{
  "id": "pediatric_respiratory_distress", "title": "Pediatric Respiratory Distress", "demographic": "pediatric",
  "section": "Pediatric Respiratory", "source_pages": [163,164],
  "chief_complaint_tags": ["respiratory distress", "shortness of breath", "wheezing", "croup", "bronchiolitis", "difficulty breathing"],
  "precedes": ["pediatric_universal_care"],
  "reference": {
    "history": ["Asthma", "Home treatment (oxygen/nebulizer)", "Meds (theophylline, steroids, inhalers)", "Toxic exposure", "Smoke inhalation"],
    "signs_symptoms": ["SOB", "Pursed lip breathing", "Decreased ability to speak", "Increased respiratory rate and effort", "Wheezing, rhonchi, rales, stridor", "Accessory muscle use", "Fever, cough, tachycardia"],
    "differential": ["Asthma", "Anaphylaxis", "Aspiration", "Pneumonia", "Pneumothorax", "Cardiac", "PE", "Tamponade", "Hyperventilation", "Inhaled toxin"],
    "pearls": ["Pulse oximetry should be monitored continuously.", "Do not force a child into a position - allow position of comfort.", "Bronchiolitis (viral, typically infants) may not respond to albuterol.", "Croup (<2 yrs, viral) - fever, gradual onset, no drooling.", "Epiglottitis (>2 yrs, bacterial) - fever, rapid onset, possible stridor, common drooling."]
  },
  "branches": [
    {"id": "wheezes_under1_or_first", "label": "Wheezes, age < 1 year or 1st wheeze", "steps": [
      {"text": "Albuterol (Proventil) 2.5 mg NEB. May repeat x1. Monitor and transport.", "drug_id": "albuterol"},
      {"text": "For severe cases, consider Epinephrine 1 mg/mL 0.01 mg/kg IM. Maximum 0.5 mg (0.5 mL).", "drug_id": "epi_1_1"}
    ]},
    {"id": "wheezes_over1_or_history", "label": "Wheezes, age > 1 year or history of wheeze", "steps": [
      {"text": "Assessment: alertness, skin color/tone, work of breathing, accessory muscle use, nasal flaring, grunting, fever, cough."},
      {"text": "Supplemental oxygen/respiratory support via nasal cannula, NRB, or CPAP with RAM cannula."},
      {"text": "Albuterol (Proventil) 2.5 mg NEB mixed with Ipratropium (Atrovent) 0.5 mg NEB. May repeat x1.", "drug_id": "albuterol"},
      {"text": "Methylprednisolone (Solu-Medrol) (62.5 mg/mL) 2 mg/kg IVP, IM. Maximum 125 mg (2 mL).", "drug_id": "methylprednisolone"},
      {"text": "For severe cases, consider Epinephrine 1 mg/mL 0.01 mg/kg IM. Maximum 0.5 mg (0.5 mL).", "drug_id": "epi_1_1"},
      {"text": "No improvement, consider Pediatric IV if SpO2 < 92%."}
    ]},
    {"id": "stridor", "label": "Stridor", "steps": [
      {"text": "Nebulized Saline 3 mL."},
      {"text": "Epinephrine 1 mg/1 mL 0.5 mg NEB (0.5 mL mixed in 3 mL NS, nebulized).", "drug_id": "epi_1_1"}
    ]}
  ]
},

{
  "id": "pediatric_allergic_reaction", "title": "Pediatric Allergic Reaction", "demographic": "pediatric",
  "section": "Pediatric Respiratory", "source_pages": [161,162],
  "chief_complaint_tags": ["allergic reaction", "anaphylaxis", "hives", "allergy"],
  "precedes": ["pediatric_universal_care"],
  "reference": {
    "history": ["Onset/location", "Insect sting or bite", "Food allergy/exposure", "Medication allergy/exposure", "New clothing, soap", "Past history", "Medication history"],
    "signs_symptoms": ["Itching/hives", "Coughing/wheezing/respiratory distress", "Chest or throat tightening", "Difficulty swallowing", "Hypotension/shock", "Edema"],
    "differential": ["Urticaria", "Anaphylaxis", "Shock", "Angioedema", "Aspiration", "Vasovagal", "Asthma/COPD", "CHF"],
    "pearls": ["Any patient with respiratory symptoms or extensive reaction should receive epinephrine and IV/IM Benadryl.", "Shorter onset = more severe reaction."]
  },
  "branches": [
    {"id": "hives_only", "label": "Hives/Rash only - no respiratory component", "steps": [
      {"text": "Pediatric IV; cardiac monitor."},
      {"text": "Diphenhydramine (Benadryl) (50 mg/mL) 1 mg/kg IVP, IM. Maximum 25 mg (0.5 mL).", "drug_id": "diphenhydramine"},
      {"text": "Reassess."}
    ]},
    {"id": "respiratory_not_arrest", "label": "Respiratory distress - not in arrest/shock", "steps": [
      {"text": "Pediatric IV; cardiac monitor."},
      {"text": "Epinephrine 1 mg/mL 0.01 mg/kg IM. Maximum 0.5 mg (0.5 mL). EMT permitted to administer if patient in anaphylaxis.", "drug_id": "epi_1_1"},
      {"text": "Diphenhydramine (Benadryl) (50 mg/mL) 1 mg/kg IVP, IM. Maximum 25 mg (0.5 mL).", "drug_id": "diphenhydramine"},
      {"text": "Methylprednisolone (Solu-Medrol) (62.5 mg/mL) 2 mg/kg IVP, IM. Maximum 125 mg (2 mL).", "drug_id": "methylprednisolone"}
    ]},
    {"id": "impending_arrest_shock", "label": "Impending arrest / shock (anaphylaxis)", "steps": [
      {"text": "Epi-Pen: may assist patient with their own Epi-Pen."},
      {"text": "Epinephrine Push Dose 10-20 mcg IVP, IO. Dilution: discard 9 mL Epi 1:10,000 (0.1 mg/mL), draw 9 mL NS to make Epi 1:100,000 (10 mcg/mL). Give 1-2 mL every 3 minutes until BP/HR goals met. LABEL syringe.", "drug_id": "epi_push_dose"}
    ]}
  ]
},

]

meta = {
  "source": "Toledo Fire & Rescue Department, Bureau of EMS - Patient Care Protocols",
  "source_review_date": "2026-04-22",
  "extracted_from": "Patient Care Protocols - Responsoft 4-22-2026.pdf",
  "status": "MVP subset - 18 of 259 source entries converted. Remainder pending (see /data/manifest.json).",
  "disclaimer": "Reference tool only. Verify against the current official protocol book before clinical use. Not a substitute for medical direction, training, or clinical judgment."
}

out = {"meta": meta, "protocols": PROTOCOLS}
with open('/sessions/festive-determined-bohr/mnt/outputs/protocols/protocols.json', 'w') as f:
    json.dump(out, f, indent=2)
print("wrote", len(PROTOCOLS), "protocols")
