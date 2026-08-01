import json

# Source: Toledo Fire & Rescue Bureau of EMS - Patient Care Protocols (Responsoft), reviewed 04/22/2026
# Transcribed verbatim from pages 180-232. dose "text" fields are verbatim from source.
# value/unit/per_kg/max_mg fields are structured helpers for the app's calculator ONLY -
# the app must always display the verbatim text alongside any computed number.

DRUGS = [
{
  "id": "adenosine", "name": "Adenosine (Adenocard)", "source_pages": [180,181],
  "certification": ["Paramedic"],
  "special_notes": "Will not convert atrial fib, atrial flutter, or VT to NSR.",
  "onset": None, "half_life": "< 10 seconds",
  "adult_dosing": [
    {"indication": "Tachycardia w/Pulse (SVT, A-Fib/A-Flutter, VT)", "steps": [
      {"text": "6 mg Rapid IVP"},
      {"text": "12 mg Rapid IVP (if first dose ineffective)"}
    ]}
  ],
  "pediatric_dosing": [
    {"indication": "Pediatric Tachycardia w/Pulse", "steps": [
      {"text": "0.1 mg/kg (3 mg/mL) Rapid IVP, IO. Maximum 6 mg", "per_kg": 0.1, "unit": "mg", "concentration": "3 mg/mL", "route": "IVP, IO", "max_mg": 6},
      {"text": "0.2 mg/kg (3 mg/mL) Rapid IVP, IO. Maximum 12 mg", "per_kg": 0.2, "unit": "mg", "concentration": "3 mg/mL", "route": "IVP, IO", "max_mg": 12},
      {"text": "0.3 mg/kg (3 mg/mL) Rapid IVP, IO. Maximum 12 mg", "per_kg": 0.3, "unit": "mg", "concentration": "3 mg/mL", "route": "IVP, IO", "max_mg": 12}
    ]}
  ],
  "contraindications": ["2nd & 3rd degree AV Block", "Sick Sinus Syndrome", "Symptomatic bradycardia unless patient has a functioning artificial pacemaker"],
  "adverse_reactions": ["Facial flushing, headache, sweating, palpitations, chest pain, hypotension", "Shortness of breath, chest pressure, hyperventilation, head pressure", "Lightheadedness, dizziness, tingling in arms, numbness, apprehension, blurred vision", "Nausea, metallic taste, tightness in throat, pressure in groin"],
  "precautions": ["May be rarely associated with ventricular fibrillation.", "Effects antagonized by methylxanthines (caffeine, theophylline) - larger doses may be needed or adenosine may not work.", "New rhythms may occur at conversion; usually self-resolve."],
  "medical_considerations": ["Adult dose: flush with 20 mL NS after each dose", "Pediatric dose: flush with 5 mL NS after each dose", "IV at antecubital site preferred"],
  "mechanism_of_action": "Antiarrhythmic"
},
{
  "id": "albuterol", "name": "Albuterol (Proventil)", "source_pages": [182],
  "certification": ["EMT", "AEMT", "Paramedic"],
  "special_notes": None, "onset": "Improvement within 5 minutes", "peak_effect": "2 hours",
  "adult_dosing": [{"indication": "Respiratory Distress", "steps": [{"text": "2.5 mg NEB", "unit": "mg", "route": "NEB"}]}],
  "pediatric_dosing": [{"indication": "Pediatric Respiratory Distress", "steps": [{"text": "2.5 mg NEB", "unit": "mg", "route": "NEB"}]}],
  "contraindications": ["Hypersensitivity", "Use caution with tachydysrhythmias and cardiovascular disorders"],
  "adverse_reactions": ["Tachycardia, hypertension", "Tremors, dizziness, nervousness, headache, insomnia", "Pharyngitis, nasal congestion", "Nausea, dyspepsia", "Bronchospasm, cough, bronchitis, wheezing"],
  "precautions": ["Use caution in cardiovascular disorders, coronary insufficiency, cardiac arrhythmias, hypertension, convulsive disorders, hyperthyroidism, or diabetes mellitus."],
  "medical_considerations": ["Use of mouth piece is most effective route if patient is cooperative"],
  "mechanism_of_action": "Bronchodilator"
},
{
  "id": "amiodarone", "name": "Amiodarone (Cordarone)", "source_pages": [183,184],
  "certification": ["Paramedic"],
  "special_notes": None, "onset": "Immediate",
  "adult_dosing": [
    {"indication": "V-Fib/Pulseless V-Tach", "steps": [
      {"text": "300 mg IVP, IO"},
      {"text": "After 3-5 minutes: 150 mg IVP, IO"}
    ]},
    {"indication": "Tachycardia w/Pulse (SVT, A-Fib/A-Flutter, VT)", "steps": [
      {"text": "150 mg IV Infusion over 10 minutes. Mix 150 mg amiodarone in 250 mL D5W, infuse over 10 min with 10 gtt set at 4 drops/sec = 250 drops/min."}
    ]}
  ],
  "pediatric_dosing": [
    {"indication": "Pediatric Pulseless Arrest", "steps": [{"text": "5 mg/kg (50 mg/mL) IVP, IO. Maximum 300 mg", "per_kg": 5, "unit": "mg", "concentration": "50 mg/mL", "route": "IVP, IO", "max_mg": 300}]},
    {"indication": "Pediatric Tachycardia w/Pulse", "steps": [{"text": "5 mg/kg (50 mg/mL) IV Infusion over 10 min. Mix 150 mg in 250 mL D5W, infuse over 10 min w/ 10 gtt set at 4 drops/sec = 250 drops/min. Maximum 150 mg", "per_kg": 5, "unit": "mg", "concentration": "50 mg/mL", "route": "IV Infusion", "max_mg": 150}]}
  ],
  "contraindications": ["N/A"],
  "adverse_reactions": ["Fever", "Hypotension, asystole/cardiac arrest/EMD, cardiogenic shock, CHF, bradycardia, ventricular tachycardia, A-V block", "Nausea"],
  "precautions": ["May worsen existing arrhythmias or precipitate new arrhythmia.", "2% reported respiratory distress syndrome (ARDS).", "May cause vasodilation and hypotension.", "Do not use with irregular tachyarrhythmias or Torsades."],
  "medical_considerations": ["Use large needle when drawing into syringe, draw slowly to prevent foaming."],
  "mechanism_of_action": "Antiarrhythmic"
},
{
  "id": "aspirin", "name": "Aspirin", "source_pages": [185],
  "certification": ["EMT", "AEMT", "Paramedic"],
  "special_notes": None, "onset": None, "peak_effect": "15 minutes to 2 hours",
  "adult_dosing": [{"indication": "Chest Pain (Suspected ACS)", "steps": [{"text": "324 mg PO", "unit": "mg", "route": "PO"}]}],
  "pediatric_dosing": [],
  "pediatric_note": "No pediatric doses for this medication.",
  "contraindications": ["Ulcers", "GI disorders", "Other bleeding disorders", "Allergy/hypersensitivity", "Renal failure"],
  "adverse_reactions": ["GI bleeding", "Nausea", "Vomiting", "Bronchospasm"],
  "precautions": ["Use cautiously in asthma, pregnancy.", "A one-time dose is safe if patient is on coumadin."],
  "medical_considerations": ["None"],
  "mechanism_of_action": "Blood modifier / Platelet aggregation inhibitor"
},
{
  "id": "atropine", "name": "Atropine", "source_pages": [186,187],
  "certification": ["Paramedic"],
  "special_notes": None, "onset": "2-5 minutes", "peak_effect": "10-30 minutes",
  "adult_dosing": [{"indication": "Bradycardia-Unstable", "steps": [{"text": "1 mg IVP, IO. May repeat every 3-5 minutes. Maximum total 3 mg", "unit": "mg", "route": "IVP, IO", "max_mg": 3}]}],
  "pediatric_dosing": [
    {"indication": "Pediatric Bradycardia", "steps": [{"text": "0.02-0.05 mg/kg (0.1 mg/mL) IVP, IO. May repeat x1. Maximum single dose 0.5 mg, maximum total dose 1 mg", "per_kg_range": [0.02,0.05], "unit": "mg", "concentration": "0.1 mg/mL", "route": "IVP, IO", "max_single_mg": 0.5, "max_mg": 1}]},
    {"indication": "Pediatric Overdose/Toxic Exposure/Cyanide Exposure", "steps": [{"text": "0.02-0.05 mg/kg (0.1 mg/mL) IVP, IO every 10-20 minutes until secretions dry. Maximum 1 mg (10 mL)", "per_kg_range": [0.02,0.05], "unit": "mg", "concentration": "0.1 mg/mL", "route": "IVP, IO", "max_mg": 1}]}
  ],
  "contraindications": ["Hypersensitivity", "Glaucoma"],
  "adverse_reactions": ["Palpitations, bradycardia (low doses), tachycardia (higher doses)", "Headache, flushing, nervousness, drowsiness, weakness, dizziness, fever; elderly may exhibit confusion/excitement, restlessness, tremor", "Nausea, vomiting, heartburn"],
  "precautions": ["May produce drowsiness, dizziness, blurred vision.", "Use cautiously with asthma/allergies.", "Use caution in CAD, CHF, arrhythmias, tachycardia, HTN, infants, small children, debilitated patients with chronic lung disease."],
  "medical_considerations": ["Use caution in patients with asthma, allergies, CAD, CHF, HTN, infants, small children, and persons with Down syndrome."],
  "mechanism_of_action": "Anticholinergic; increases heart rate"
},
{
  "id": "calcium_chloride", "name": "Calcium Chloride", "source_pages": [188],
  "certification": ["Paramedic"],
  "special_notes": None, "onset": "Immediate",
  "adult_dosing": [
    {"indication": "Pulseless Electrical Activity (PEA) / V-Fib/Pulseless V-Tach", "steps": [{"text": "1 gm IVP, IO", "unit": "gm", "route": "IVP, IO"}]},
    {"indication": "Overdose/Toxic Exposure", "steps": [{"text": "1 gm Slow IVP", "unit": "gm", "route": "Slow IVP"}]}
  ],
  "pediatric_dosing": [{"indication": "Pediatric Overdose/Toxic Exposure/Cyanide Exposure", "steps": [{"text": "20 mg/kg (100 mg/mL) Slow IVP. Maximum 1,000 mg (1 gram)", "per_kg": 20, "unit": "mg", "concentration": "100 mg/mL", "route": "Slow IVP", "max_mg": 1000}]}],
  "contraindications": ["Patients at risk of existing digitalis toxicity"],
  "adverse_reactions": ["Rapid injection may cause tingling, calcium taste, or heat wave.", "Peripheral vasodilation, local burning, or moderate fall in BP.", "If infiltration occurs, discontinue IV at that site immediately."],
  "precautions": ["Inject slowly through a small needle into a large vein to minimize venous irritation."],
  "medical_considerations": ["Irritating to veins; must not be injected into tissue - severe necrosis/sloughing may occur."],
  "mechanism_of_action": "Treats hyperkalemia; calcium channel blocker antagonist"
},
{
  "id": "cyanokit", "name": "Cyanokit (Hydroxocobalamin)", "source_pages": [189],
  "certification": ["Paramedic"],
  "special_notes": None, "onset": "Immediate", "half_life": "26-31 hours",
  "adult_dosing": [{"indication": "Overdose/Toxic Exposure / Burns - Adult >70 kg (154 lbs) with suspected cyanide poisoning", "steps": [{"text": "5 gm IV Infusion. Add 200 mL NS to upright vial via transfer spike to fill line, invert vial 60 sec, use vented tubing + filter line, infuse over 15 minutes.", "unit": "gm", "route": "IV Infusion"}]}],
  "pediatric_dosing": [{"indication": "Pediatric Overdose/Toxic Exposure/Cyanide Exposure", "steps": [{"text": "70 mg/kg (25 mg/mL) IVP, IO over 15 minutes. Same reconstitution as adult. Maximum 5,000 mg (5 gm)", "per_kg": 70, "unit": "mg", "concentration": "25 mg/mL", "route": "IVP, IO", "max_mg": 5000}]}],
  "contraindications": ["Pregnancy - consult medical control", "Allergies to hydroxocobalamin or cyanocobalamin B-12"],
  "adverse_reactions": [">5%: transient chromaturia (abnormal urine coloration), erythema, rash, increased blood pressure, nausea, headache, injection site reactions."],
  "precautions": ["Known anaphylactic reactions to hydroxocobalamin or cyanocobalamin"],
  "medical_considerations": ["None"],
  "mechanism_of_action": "Binds with cyanide ions"
},
{
  "id": "dextrose_10", "name": "Dextrose 10% (D10)", "source_pages": [190,191],
  "certification": ["AEMT", "Paramedic"],
  "special_notes": None, "onset": "1-2 minutes",
  "adult_dosing": [{"indication": "Pulseless Electrical Activity (PEA) / Hypoglycemia/Hyperglycemia", "steps": [{"text": "5 gm (50 mL) IV Infusion. Withdraw 50 mL from 250 mL NS bag, add 1 amp D50 to bag = D10. Give 50 mL (5 g) increments until patient regains normal mentation. Maximum total 25 gm (250 mL)", "unit": "gm", "route": "IV Infusion", "max_mg": 25000}]}],
  "pediatric_dosing": [{"indication": "Pediatric Hypoglycemia/Hyperglycemia", "steps": [{"text": "0.1 gm/kg (0.1 gm/mL) IV Infusion (50 mL prep, same as adult). Give until normal mentation. Maximum 25 gm (250 mL)", "per_kg": 0.1, "unit": "gm", "concentration": "0.1 gm/mL", "route": "IV Infusion", "max_mg": 25000}]}],
  "contraindications": ["Sub Q & IM injections", "Intracerebral bleeding", "Hemorrhagic CVA", "Cerebral edema", "Delirium tremens if patient dehydrated"],
  "adverse_reactions": ["Febrile response", "Infection at injection site", "Tissue necrosis", "Venous thrombosis or phlebitis", "Extravasation", "Hypovolemia/dehydration", "Mental confusion or unconsciousness", "May cause allergic reactions in corn-sensitive persons", "Rapid infusion may cause generalized flush"],
  "precautions": ["Inject slowly to avoid extravasation.", "If thrombosis occurs, stop injection."],
  "medical_considerations": ["Do not use Dextrose if IV site is questionable.", "Perform blood glucose analysis prior to administration and 5-15 minutes after."],
  "mechanism_of_action": "Natural sugar"
},
{
  "id": "diltiazem", "name": "Diltiazem (Cardizem)", "source_pages": [192,193],
  "certification": ["Paramedic"],
  "special_notes": None, "peak_effect": "2-3 hours",
  "adult_dosing": [{"indication": "Tachycardia w/Pulse (SVT, A-Fib/A-Flutter, VT)", "steps": [{"text": "10 mg Slow IVP. May repeat x1. Do not use in suspected WPW.", "unit": "mg", "route": "Slow IVP"}]}],
  "pediatric_dosing": [], "pediatric_note": "No pediatric doses for this medication.",
  "contraindications": ["Hypersensitivity", "Sick sinus syndrome, 2nd/3rd degree blocks (except with functioning ventricular pacemaker)", "Severe hypotension or cardiogenic shock", "WPW or short PR syndrome", "Wide complex tachycardia, acute MI, CHF"],
  "adverse_reactions": ["Hypotension", "Itching/burning at injection site", "Vasodilation (flushing)", "Asystole, A-V block, chest pain, CHF, syncope, V-fib, V-tach, ectopy", "Dizziness, headache", "Nausea, vomiting", "Edema"],
  "precautions": ["Consider 5 mg in caution situations.", "Use caution with BP < 110.", "If BP remains > 110 and HR remains > 110, may give other half of initial loading bolus in 5 minutes."],
  "medical_considerations": ["Do not mix with other drugs.", "Flush tubing after use.", "Response usually within 3 minutes; rarely converts A-fib/flutter to NSR but decreases HR; lasts 1-3 hours."],
  "mechanism_of_action": "Calcium channel blocker; decreases heart rate; slows ventricular rate in rapid A-fib/flutter"
},
{
  "id": "diphenhydramine", "name": "Diphenhydramine (Benadryl)", "source_pages": [194,195],
  "certification": ["AEMT", "Paramedic"],
  "special_notes": None, "onset": "< 15 minutes", "peak_effect": "1-4 hours",
  "adult_dosing": [
    {"indication": "Dystonic Reaction", "steps": [{"text": "50 mg IVP, IO, IM", "unit": "mg", "route": "IVP, IO, IM"}]},
    {"indication": "Allergic Reaction", "steps": [{"text": "50 mg IVP, IM", "unit": "mg", "route": "IVP, IM"}]}
  ],
  "pediatric_dosing": [{"indication": "Pediatric Allergic Reaction", "steps": [{"text": "1 mg/kg (50 mg/mL) IVP, IM. Maximum 25 mg (0.5 mL)", "per_kg": 1, "unit": "mg", "concentration": "50 mg/mL", "route": "IVP, IM", "max_mg": 25}]}],
  "contraindications": ["Hypersensitivity", "Newborns", "Lactating females"],
  "adverse_reactions": ["Hypotension, headache, palpitations, tachycardia, extrasystoles", "Sedation, sleepiness, dizziness, fatigue, confusion, restlessness, excitation, nervousness, tremor, irritability, blurred vision, vertigo, tinnitus, convulsions", "Nausea, vomiting, diarrhea", "Thickening of bronchial secretions, chest tightness/wheezing, nasal stuffiness"],
  "precautions": ["Atropine-like action - caution with bronchial asthma, increased intraocular pressure, cardiovascular disease/hypertension.", "Caution with lower respiratory disease including asthma, and pregnant patients.", "Caution in elderly - may cause dizziness, extreme calm, hypotension."],
  "medical_considerations": ["Should be given following Epinephrine 1 mg/1 mL in cases involving the respiratory system (stridor, wheezing, retractions)."],
  "mechanism_of_action": "Antihistamine"
},
{
  "id": "epi_1_1", "name": "Epinephrine 1 mg/1 mL", "source_pages": [196,197],
  "certification": ["EMT - IM Anaphylaxis Only", "AEMT - IM Only", "Paramedic"],
  "special_notes": None, "onset": "5-10 minutes IM",
  "adult_dosing": [
    {"indication": "Allergic Reaction", "steps": [
      {"text": "0.3 mg Auto-Injector", "unit": "mg", "route": "IM (auto-injector)"},
      {"text": "0.5 mg IM. May repeat x1 in 5 minutes. If more than 2 IM doses needed, go to IV.", "unit": "mg", "route": "IM"}
    ]},
    {"indication": "Respiratory Distress", "steps": [
      {"text": "0.3-0.5 mg IM", "unit": "mg", "route": "IM"},
      {"text": "Consider 0.5 mg IM, may repeat x1", "unit": "mg", "route": "IM"}
    ]}
  ],
  "pediatric_dosing": [{"indication": "Pediatric Respiratory Distress", "steps": [{"text": "0.5 mg NEB (0.5 mL mixed in 3 mL NS, nebulized)", "unit": "mg", "route": "NEB"}]}],
  "contraindications": ["None in Cardiac Arrest", "Known hypersensitivity", "Do not give to patients who have repeatedly used an aerosol bronchodilator within the past 4 hours"],
  "adverse_reactions": ["Palpitations", "Arrhythmias", "Hypertension", "Pulmonary edema", "Dyspnea", "Nervousness"],
  "precautions": ["Hypertensive crisis possible if patient stabilized on antidepressants.", "Do not mix with other drugs.", "Very light sensitive - do not use discolored solutions or those with precipitate.", "Massage site after injection to counteract vasoconstriction.", "Use caution with previous Epi-Pen usage."],
  "medical_considerations": ["Always transport after treatment due to rebound effect.", "Use caution in males over 35 or those with history of HTN, thyroid disease, or angina."],
  "mechanism_of_action": "Sympathomimetic; cardiac stimulant"
},
{
  "id": "epi_1_10", "name": "Epinephrine 1 mg/10 mL", "source_pages": [198,199],
  "certification": ["Paramedic"],
  "special_notes": None, "onset": "< 5 minutes",
  "adult_dosing": [
    {"indication": "Asystole / PEA / V-Fib/Pulseless V-Tach", "steps": [{"text": "1 mg IVP, IO. Repeat every 10 minutes. Maximum total 4 mg", "unit": "mg", "route": "IVP, IO", "max_mg": 4}]},
    {"indication": "Allergic Reaction", "steps": [{"text": "Epinephrine 1:10,000 - 0.1 mg IVP (100 mcg). Give every minute until symptoms improve. NOTE: this is NOT the same as Push Dose Epinephrine.", "unit": "mg", "route": "IVP"}]},
    {"indication": "Respiratory Distress", "steps": [{"text": "1 mcg/kg IVP (1 mg/10 mL = 1:10,000, each mL = 100 mcg). Typical adult dose ~100 mcg.", "per_kg": 0.001, "unit": "mg", "concentration": "0.1 mg/mL (1:10,000)", "route": "IVP"}]}
  ],
  "pediatric_dosing": [
    {"indication": "Newly Born", "steps": [{"text": "0.01-0.03 mg/kg (0.1 mg/mL) IVP, IO", "per_kg_range": [0.01,0.03], "unit": "mg", "concentration": "0.1 mg/mL", "route": "IVP, IO"}]},
    {"indication": "Pediatric Bradycardia", "steps": [{"text": "0.01 mg/kg (0.1 mg/mL) IVP, IO. Repeat every 5 minutes. Maximum 1 mg/dose (10 mL)", "per_kg": 0.01, "unit": "mg", "concentration": "0.1 mg/mL", "route": "IVP, IO", "max_mg": 1}]},
    {"indication": "Pediatric Pulseless Arrest", "steps": [{"text": "0.01 mg/kg (0.1 mg/mL) IVP, IO. Repeat every 5 minutes. Maximum 1 mg/dose (10 mL)", "per_kg": 0.01, "unit": "mg", "concentration": "0.1 mg/mL", "route": "IVP, IO", "max_mg": 1}]}
  ],
  "contraindications": ["None in Cardiac Arrest", "Known hypersensitivity", "Do not give to patients who have repeatedly used an aerosol bronchodilator within the past 4 hours"],
  "adverse_reactions": ["Palpitations", "Arrhythmias", "Hypertension", "Pulmonary edema", "Dyspnea", "Nervousness"],
  "precautions": ["Hypertensive crisis possible if stabilized on antidepressants.", "Do not mix with other drugs.", "Very light sensitive.", "Massage site after injection.", "Use caution with previous Epi-Pen usage."],
  "medical_considerations": ["None"],
  "mechanism_of_action": "Sympathomimetic; cardiac stimulant"
},
{
  "id": "epi_drip", "name": "Epinephrine Drip", "source_pages": [200],
  "certification": ["Paramedic"],
  "special_notes": None, "onset": "Immediate",
  "adult_dosing": [{"indication": "Bradycardia-Unstable / Hypotension-Shock Non-Trauma / Post ROSC Care / Fever-Suspected Sepsis / Allergic Reaction", "steps": [{"text": "1 mg IV Drip. Mix 1 mg Epinephrine into 1,000 mL NS (60 gtt set). Infuse until HR > 60 and MAP > 65 mmHg. LABEL the bag.", "unit": "mg", "route": "IV Drip"}]}],
  "pediatric_dosing": [], "pediatric_note": "No pediatric doses for this medication.",
  "contraindications": ["Known hypersensitivity", "Do not give to patients who have repeatedly used an aerosol bronchodilator within the past 4 hours"],
  "adverse_reactions": ["Chest pain, palpitations, arrhythmias, hypertension", "Pulmonary edema, dyspnea", "Nausea and vomiting", "Nervousness, tremor", "Diaphoresis"],
  "precautions": ["Hypertensive crisis possible if stabilized on antidepressants; do not mix with other drugs.", "Very light sensitive.", "Massage site after injection.", "Use caution with previous Epi-Pen usage."],
  "medical_considerations": ["Protect from light exposure.", "Do not use if discolored or contains precipitate."],
  "mechanism_of_action": "Sympathomimetic; cardiac stimulant"
},
{
  "id": "epi_push_dose", "name": "Epinephrine Push Dose", "source_pages": [201,202],
  "certification": ["Paramedic"],
  "special_notes": "Epinephrine 1:10,000, 0.9% Sodium Chloride flush syringe", "onset": "Immediate",
  "adult_dosing": [{"indication": "Hypotension/Shock Non-Trauma / Fever-Suspected Sepsis / Allergic Reaction", "steps": [{"text": "10-20 mcg IVP, IO. Dilution: discard 9 mL of Epi 1:10,000 (0.1 mg/mL), draw up 9 mL NS to create Epi 1:100,000 (yields 10 mcg/mL). Give 1-2 mL every 3 minutes until BP/HR goals met. LABEL syringe.", "unit": "mcg", "route": "IVP, IO"}]}],
  "pediatric_dosing": [{"indication": "Pediatric Hypotension/Sepsis/Shock Non-Trauma / Pediatric Allergic Reaction", "steps": [{"text": "10-20 mcg IVP, IO. Same dilution/administration as adult.", "unit": "mcg", "route": "IVP, IO"}]}],
  "contraindications": ["Known hypersensitivity", "Glaucoma"],
  "adverse_reactions": ["Anxiety", "Headache", "Fear and palpitations", "Repeated injections can cause necrosis at injection sites"],
  "precautions": ["Quantities > 50 mcg/min can potentially cause end-organ damage."],
  "medical_considerations": ["Push dose is a short-term bridge to IV drip, not for prolonged use. Notify receiving facility of push dose epi use ASAP."],
  "mechanism_of_action": "Sympathomimetic; cardiac stimulant"
},
{
  "id": "fentanyl", "name": "Fentanyl (Sublimaze)", "source_pages": [203,204],
  "certification": ["AEMT", "Paramedic"],
  "special_notes": None, "onset": "Almost immediate", "peak_effect": "Maximal analgesic/respiratory effect may take several minutes",
  "adult_dosing": [
    {"indication": "Chest Pain (Suspected ACS)", "steps": [{"text": "25-50 mcg IVP, up to 100 mcg", "unit": "mcg", "route": "IVP"}]},
    {"indication": "Post ROSC Care", "steps": [{"text": "50-100 mcg IVP, IO", "unit": "mcg", "route": "IVP, IO"}]},
    {"indication": "Pain Control", "steps": [{"text": "50-100 mcg IVP, IN, IM. May repeat 50-100 mcg x1. Maximum 200 mcg", "unit": "mcg", "route": "IVP, IN, IM", "max_mg": 0.2}]}
  ],
  "pediatric_dosing": [{"indication": "Pediatric Pain Control", "steps": [{"text": "0.5-1 mcg/kg (50 mcg/mL) IVP, IN. Maximum single dose 25 mcg", "per_kg_range": [0.5,1], "unit": "mcg", "concentration": "50 mcg/mL", "route": "IVP, IN", "max_single_mg": 0.025}]}],
  "contraindications": ["Known intolerance to drug"],
  "adverse_reactions": ["Respiratory depression, apnea, laryngospasm", "Bradycardia, hypertension, hypotension", "Dizziness, blurred vision", "Nausea & vomiting", "Rigidity, diaphoresis"],
  "precautions": ["Caution with head injuries and elevated ICP.", "Caution with bradycardia, COPD, decreased respiratory reserve, or patients using narcotics.", "Reduce dose in elderly/debilitated patients and in HTN.", "High doses (>2-3 mcg/kg) can cause 'stiff chest' - treat with IV succinylcholine and intubation."],
  "medical_considerations": ["Use caution in elderly/debilitated patients or those with limited pulmonary reserve."],
  "mechanism_of_action": "Narcotic analgesic"
},
{
  "id": "glucagon", "name": "Glucagon", "source_pages": [205,206],
  "certification": ["EMT - IM & IN Only", "AEMT", "Paramedic"],
  "special_notes": None, "onset": "Should respond within 15 minutes",
  "adult_dosing": [
    {"indication": "Pulseless Electrical Activity (PEA)", "steps": [{"text": "1 mg IVP", "unit": "mg", "route": "IVP"}]},
    {"indication": "Hypoglycemia/Hyperglycemia", "steps": [{"text": "1 mg IM, IN", "unit": "mg", "route": "IM, IN"}]},
    {"indication": "Overdose/Toxic Exposure", "steps": [{"text": "1 mg IVP, IN, IM", "unit": "mg", "route": "IVP, IN, IM"}]}
  ],
  "pediatric_dosing": [
    {"indication": "Pediatric Hypoglycemia/Hyperglycemia", "steps": [{"text": "0.025 mg/kg (1 mg/mL) IM, IN. Maximum 1 mg (1 mL)", "per_kg": 0.025, "unit": "mg", "concentration": "1 mg/mL", "route": "IM, IN", "max_mg": 1}]},
    {"indication": "Pediatric Overdose/Toxic Exposure/Cyanide Exposure", "steps": [{"text": "0.025 mg/kg (1 mg/mL) IVP. Maximum 1 mg (1 mL)", "per_kg": 0.025, "unit": "mg", "concentration": "1 mg/mL", "route": "IVP", "max_mg": 1}]}
  ],
  "contraindications": ["Hypersensitivity", "Hyperglycemia", "Allergies to beef or porcine proteins", "Insulinoma", "Adrenal gland tumor"],
  "adverse_reactions": ["Nausea", "Vomiting"],
  "precautions": ["Of little help in adrenal insufficiency.", "Follow with supplemental carbohydrates."],
  "medical_considerations": ["Do not mix with saline."],
  "mechanism_of_action": "Anti-hypoglycemic"
},
{
  "id": "ipratropium", "name": "Ipratropium (Atrovent)", "source_pages": [207,208],
  "certification": ["EMT", "AEMT", "Paramedic"],
  "special_notes": None, "peak_effect": "1.5-2 hours",
  "adult_dosing": [{"indication": "Respiratory Distress", "steps": [{"text": "0.5 mg NEB", "unit": "mg", "route": "NEB"}]}],
  "pediatric_dosing": [{"indication": "Pediatric Respiratory Distress", "steps": [{"text": "0.5 mg NEB", "unit": "mg", "route": "NEB"}]}],
  "contraindications": ["Allergy to soy or peanut products", "Glaucoma", "Suspected hypersensitivity to Ipratropium Bromide, Atropine, or derivatives", "Caution in OB patients"],
  "adverse_reactions": ["Dry mouth", "Headache", "Cough", "Nausea", "Vomiting", "Dizziness", "Nervousness", "Palpitations", "Glaucoma patients may have pain or blurred vision if eye contact"],
  "precautions": ["May worsen bronchoconstriction (hypotonicity/additives) - give beta-agonists first or in combination.", "Caution with narrow angle glaucoma, prostatic hyperplasia, or bladder-neck obstruction."],
  "medical_considerations": ["None"],
  "mechanism_of_action": "Bronchodilator"
},
{
  "id": "ketamine", "name": "Ketamine (Ketalar)", "source_pages": [209,210],
  "certification": ["AEMT", "Paramedic"],
  "special_notes": None, "onset": "IV 30 sec-2 min; IM 3-4 min",
  "adult_dosing": [
    {"indication": "Cardiac Arrest", "steps": [{"text": "100 mg IVP, IO. May repeat x1", "unit": "mg", "route": "IVP, IO"}]},
    {"indication": "Bradycardia-Unstable", "steps": [
      {"text": "0.2 mg/kg (50 mg/mL) IVP, IO. Maximum single dose 25 mg. May repeat x1 in 10 min to total max 50 mg.", "per_kg": 0.2, "unit": "mg", "concentration": "50 mg/mL", "route": "IVP, IO", "max_single_mg": 25, "max_mg": 50},
      {"text": "0.5 mg/kg (100 mg/mL) IN, IM. May repeat x1 in 10 min. Maximum single dose 25 mg, total max 50 mg.", "per_kg": 0.5, "unit": "mg", "concentration": "100 mg/mL", "route": "IN, IM", "max_single_mg": 25, "max_mg": 50}
    ]},
    {"indication": "Post ROSC Care", "steps": [{"text": "50-100 mg IVP, IO. May repeat 50-100 mg x1. Maximum 200 mg", "unit": "mg", "route": "IVP, IO", "max_mg": 200}]},
    {"indication": "Tachycardia w/Pulse (SVT, A-Fib/A-Flutter, VT)", "steps": [
      {"text": "0.2 mg/kg (50 mg/mL) IVP, IO. May repeat x1. Maximum 25 mg", "per_kg": 0.2, "unit": "mg", "concentration": "50 mg/mL", "route": "IVP, IO", "max_mg": 25},
      {"text": "0.5 mg/kg (100 mg/mL) IN", "per_kg": 0.5, "unit": "mg", "concentration": "100 mg/mL", "route": "IN"}
    ]},
    {"indication": "Pain Control", "steps": [
      {"text": "25 mg IV Infusion, mixed in 50 mL D5 over 10 minutes", "unit": "mg", "route": "IV Infusion"},
      {"text": "0.5 mg/kg (100 mg/mL) IN, IM. May repeat x1 in 10 min. Maximum single dose 25 mg, total max 50 mg", "per_kg": 0.5, "unit": "mg", "concentration": "100 mg/mL", "route": "IN, IM", "max_single_mg": 25, "max_mg": 50}
    ]},
    {"indication": "Behavioral Emergency / Sedation", "steps": [{"text": "4 mg/kg (100 mg/mL) IM. Maximum 400 mg", "per_kg": 4, "unit": "mg", "concentration": "100 mg/mL", "route": "IM", "max_mg": 400}]},
    {"indication": "Seizure", "steps": [{"text": "1 mg/kg (50 mg/mL) IVP, IO. Maximum dose 100 mg", "per_kg": 1, "unit": "mg", "concentration": "50 mg/mL", "route": "IVP, IO", "max_mg": 100}]},
    {"indication": "Acute Pulmonary Edema / Respiratory Distress", "steps": [
      {"text": "0.5 mg/kg (100 mg/mL) IN, IM", "per_kg": 0.5, "unit": "mg", "concentration": "100 mg/mL", "route": "IN, IM"},
      {"text": "25 mg IVP, IO mixed with 50 mL NS over 10 minutes", "unit": "mg", "route": "IVP, IO"}
    ]}
  ],
  "pediatric_dosing": [
    {"indication": "Pediatric Pain Control", "steps": [
      {"text": "0.3 mg/kg (50 mg/mL) IV Infusion, diluted in 50 mL NS or D5W over 10-15 min", "per_kg": 0.3, "unit": "mg", "concentration": "50 mg/mL", "route": "IV Infusion"},
      {"text": "1 mg/kg (100 mg/mL) IN, divided between nares. Maximum 1 mL/nostril", "per_kg": 1, "unit": "mg", "concentration": "100 mg/mL", "route": "IN"}
    ]},
    {"indication": "Pediatric Seizure", "steps": [{"text": "1 mg/kg (50 mg/mL) IVP, IO. Maximum 100 mg", "per_kg": 1, "unit": "mg", "concentration": "50 mg/mL", "route": "IVP, IO", "max_mg": 100}]},
    {"indication": "Pediatric Head Trauma", "steps": [
      {"text": "25 mg IV Infusion, mix 25 mg in 50 mL D5W over 10 min", "unit": "mg", "route": "IV Infusion"},
      {"text": "1 mg/kg (100 mg/mL) IN, divided between nares. Maximum 1 mL/nostril", "per_kg": 1, "unit": "mg", "concentration": "100 mg/mL", "route": "IN"}
    ]}
  ],
  "note": "Dose of 0.5 mg/kg (100 mg/mL) IN, max 25 mg listed in drug reference is NOT indicated on any protocol page per source document.",
  "contraindications": ["Patients where a significant BP elevation would be a serious hazard", "Known hypersensitivity"],
  "adverse_reactions": ["BP/pulse frequently elevated; hypotension and bradycardia observed; arrhythmia possible", "Nausea/vomiting, increased salivation", "Enhanced skeletal muscle tone (tonic/clonic movements resembling seizures)", "Respiration frequently stimulated but severe depression/apnea may occur with rapid IV high doses; laryngospasm possible"],
  "precautions": ["Resuscitative equipment should be ready.", "IV dose over 1 minute - faster administration risks respiratory depression/apnea.", "Caution in chronic alcoholics and acutely intoxicated patients."],
  "medical_considerations": ["Monitor vital signs frequently. Use caution and low end of dosing in elderly/pediatric patients."],
  "mechanism_of_action": "Non-barbiturate anesthetic"
},
{
  "id": "ketorolac", "name": "Ketorolac (Toradol)", "source_pages": [211],
  "certification": ["AEMT", "Paramedic"],
  "special_notes": None, "onset": "Within 30 minutes",
  "adult_dosing": [{"indication": "Pain Control", "steps": [{"text": "30 mg IVP, IM", "unit": "mg", "route": "IVP, IM"}]}],
  "pediatric_dosing": [], "pediatric_note": "No pediatric doses for this medication.",
  "contraindications": ["Allergy to aspirin, ketorolac, or other NSAIDs", "Pregnant or breastfeeding", "Significant renal impairment, especially with volume depletion", "Previous or current GI bleeding", "Intracranial bleeding", "Coagulation defects", "High risk of bleeding"],
  "adverse_reactions": ["Bleeding", "Nausea & vomiting"],
  "precautions": ["GI irritation or hemorrhage.", "Avoid in pregnancy, renal failure, or bleeding patients (GI, intracranial, intra-abdominal/AAA)."],
  "medical_considerations": ["N/A"],
  "mechanism_of_action": "Inhibits prostaglandin synthesis via COX-1 and COX-2 inhibition"
},
{
  "id": "lidocaine", "name": "Lidocaine (Xylocaine)", "source_pages": [212,213],
  "certification": ["AEMT - IO Pain Relief Only", "Paramedic"],
  "special_notes": None, "onset": "30-90 seconds",
  "adult_dosing": [{"indication": "Adult IV/IO (pain relief for IO insertion)", "steps": [{"text": "20 mg IO", "unit": "mg", "route": "IO"}]}],
  "pediatric_dosing": [], "pediatric_note": "No pediatric doses for this medication.",
  "contraindications": ["Bradycardia", "2nd or 3rd degree heart block", "Known hypersensitivity", "Stokes-Adams syndrome, WPW"],
  "adverse_reactions": ["Drowsiness", "Vomiting", "Confusion", "Seizures", "Hypotension", "Bradycardia", "Slurred speech", "Tremors", "Restlessness", "Euphoria", "Tinnitus", "Blurred/double vision"],
  "precautions": ["Contraindicated with allergy to amide-type anesthetics (e.g. Nupercaine).", "Caution with >2nd degree heart block.", "Discontinue if signs of toxicity (dizziness, convulsions, confusion) appear.", "Caution with digitalis toxicity."],
  "medical_considerations": ["Observe closely for drug toxicity: dizziness, confusion, delirium, seizures."],
  "mechanism_of_action": "Antiarrhythmic"
},
{
  "id": "magnesium_sulfate", "name": "Magnesium Sulfate", "source_pages": [214,215],
  "certification": ["Paramedic"],
  "special_notes": None, "onset": "Immediate, lasts ~30 minutes",
  "adult_dosing": [
    {"indication": "V-Fib/Pulseless V-Tach", "steps": [{"text": "2 gm IVP", "unit": "gm", "route": "IVP"}]},
    {"indication": "Maternal Arrest", "steps": [{"text": "2 gm IVP"}, {"text": "4 gm IVP"}]},
    {"indication": "Obstetrical Emergency", "steps": [{"text": "4 gm IVP over 20 minutes", "unit": "gm", "route": "IVP"}]},
    {"indication": "Respiratory Distress", "steps": [{"text": "2 gm IV Infusion, mixed in 50 mL D5W, run wide open with 60 gtt set, delivered over 10-20 minutes", "unit": "gm", "route": "IV Infusion"}]}
  ],
  "pediatric_dosing": [], "pediatric_note": "No pediatric doses for this medication.",
  "contraindications": ["Heart block or myocardial damage", "Hypertension", "Caution with renal impairment", "Reduce dosing with concurrent narcotics/hypnotics"],
  "adverse_reactions": ["Respiratory depression", "Hypothermia", "Circulatory collapse", "Respiratory paralysis", "Hypotension", "Diaphoresis", "Facial flushing", "Sweating", "Depressed reflexes"],
  "precautions": ["Caution in renal impairment (drug cleared solely by kidneys).", "Safe dosage indicated by presence of patellar reflex and absence of respiratory depression.", "Adjust dosing when given with barbiturates/narcotics/hypnotics.", "Caution with digitalis.", "Stop infusion if hypotension, breathing difficulty, decreased DTRs, or paralysis develops."],
  "medical_considerations": ["Not compatible with Sodium Bicarbonate."],
  "mechanism_of_action": "Physiologic calcium channel blocker; blocks neuromuscular transmission"
},
{
  "id": "methylprednisolone", "name": "Methylprednisolone (Solu-Medrol)", "source_pages": [216],
  "certification": ["Paramedic"],
  "special_notes": None, "onset": "1-2 hours",
  "adult_dosing": [
    {"indication": "Allergic Reaction", "steps": [{"text": "125 mg IVP, IM", "unit": "mg", "route": "IVP, IM"}]},
    {"indication": "Respiratory Distress", "steps": [{"text": "125 mg IVP", "unit": "mg", "route": "IVP"}]}
  ],
  "pediatric_dosing": [{"indication": "Pediatric Allergic Reaction / Pediatric Respiratory Distress", "steps": [{"text": "2 mg/kg (62.5 mg/mL) IVP, IM. Maximum 125 mg (2 mL)", "per_kg": 2, "unit": "mg", "concentration": "62.5 mg/mL", "route": "IVP, IM", "max_mg": 125}]}],
  "contraindications": ["No contraindications, precautions, or side effects associated with a single emergency dose."],
  "adverse_reactions": ["CHF in susceptible patients, HTN", "Weakness", "Convulsions, headache, vertigo", "Nausea & vomiting", "Arrhythmias, hypotension", "Sweating"],
  "precautions": ["Nonspecific ulcerative colitis", "Impending perforation/abscess/other infection", "Peptic ulcer", "Renal insufficiency", "Hypertension", "Osteoporosis", "Myasthenia gravis"],
  "medical_considerations": ["N/A"],
  "mechanism_of_action": "Anti-inflammatory steroid"
},
{
  "id": "midazolam", "name": "Midazolam (Versed)", "source_pages": [217,218,219],
  "certification": ["AEMT", "Paramedic"],
  "special_notes": None, "onset": "2-5 minutes",
  "adult_dosing": [
    {"indication": "Cardiac Arrest", "steps": [{"text": "2-5 mg IVP, IO", "unit": "mg", "route": "IVP, IO"}]},
    {"indication": "Bradycardia-Unstable", "steps": [{"text": "2 mg IVP, IO, IN. Maximum dose 4 mg", "unit": "mg", "route": "IVP, IO, IN", "max_mg": 4}]},
    {"indication": "Post ROSC Care", "steps": [{"text": "2.5-5 mg IVP, IO. May repeat x1", "unit": "mg", "route": "IVP, IO"}]},
    {"indication": "Tachycardia w/Pulse (SVT, A-Fib/A-Flutter, VT)", "steps": [{"text": "2.5 mg IVP, IO, IN, IM. May repeat x1", "unit": "mg", "route": "IVP, IO, IN, IM"}]},
    {"indication": "Hyperthermia", "steps": [{"text": "2.5 mg IVP, IM, IN. May repeat x1", "unit": "mg", "route": "IVP, IM, IN"}]},
    {"indication": "Dystonic Reaction", "steps": [{"text": "2.5 mg IVP, IO, IM", "unit": "mg", "route": "IVP, IO, IM"}]},
    {"indication": "Behavioral Emergency / Sedation", "steps": [
      {"text": "Adult: 2.5 mg IVP, IO, IM, IN. May repeat x1. Maximum total dose 5 mg", "unit": "mg", "route": "IVP, IO, IM, IN", "max_mg": 5},
      {"text": "Adult age > 12: 10 mg IM", "unit": "mg", "route": "IM"},
      {"text": "Adult age > 65: 5 mg IM", "unit": "mg", "route": "IM"},
      {"text": "If IVP/IO, initial dose: 5 mg IVP, IO. Maximum 10 mg", "unit": "mg", "route": "IVP, IO", "max_mg": 10},
      {"text": "Repeat dosing: 2.5 mg IM, IVP, IO, IN every 5 minutes. Maximum 20 mg", "unit": "mg", "route": "IM, IVP, IO, IN", "max_mg": 20},
      {"text": "Older than 65 (dose not indicated on protocol pages): 1-2.5 mg IVP, IO, IM, IN, may repeat every 5 min to effect, maximum total 5 mg", "unit": "mg", "route": "IVP, IO, IM, IN", "max_mg": 5}
    ]},
    {"indication": "Seizure", "steps": [
      {"text": "Age < 65: 10 mg IM", "unit": "mg", "route": "IM"},
      {"text": "Age > 65: 5 mg IM", "unit": "mg", "route": "IM"},
      {"text": "2-5 mg IVP, IO", "unit": "mg", "route": "IVP, IO"}
    ]},
    {"indication": "Obstetrical Emergency", "steps": [{"text": "2-5 mg Slow IVP, or 10 mg IM", "unit": "mg", "route": "IVP, IM"}]},
    {"indication": "Acute Pulmonary Edema / Respiratory Distress", "steps": [
      {"text": "2-5 mg IVP. Maximum 5 mg", "unit": "mg", "route": "IVP", "max_mg": 5},
      {"text": "2 mg IN", "unit": "mg", "route": "IN"}
    ]},
    {"indication": "Head Trauma", "steps": [{"text": "2.5-5 mg IVP, for sedation if intubated", "unit": "mg", "route": "IVP"}]}
  ],
  "pediatric_dosing": [
    {"indication": "Pediatric Behavioral Emergency / Sedation", "steps": [
      {"text": "0.1 mg/kg (1 mg/mL) IVP, IO, IM, IN, may repeat to maximum. Maximum single 2.5 mg, total 5 mg", "per_kg": 0.1, "unit": "mg", "concentration": "1 mg/mL", "route": "IVP, IO, IM, IN", "max_single_mg": 2.5, "max_mg": 5},
      {"text": "0.1 mg/kg (5 mg/mL) IM, IVP, IN, repeat every 5 min. Maximum single 2.5 mg, total 10 mg", "per_kg": 0.1, "unit": "mg", "concentration": "5 mg/mL", "route": "IM, IVP, IN", "max_single_mg": 2.5, "max_mg": 10}
    ]},
    {"indication": "Pediatric Tachycardia w/Pulse", "steps": [{"text": "0.1 mg/kg (1 mg/mL) IVP, IN. Maximum 2 mg", "per_kg": 0.1, "unit": "mg", "concentration": "1 mg/mL", "route": "IVP, IN", "max_mg": 2}]},
    {"indication": "Pediatric Seizure", "steps": [{"text": "0.2 mg/kg (5 mg/mL) IN, IM, IVP, IO. May repeat x1. Maximum dosing 5 mg", "per_kg": 0.2, "unit": "mg", "concentration": "5 mg/mL", "route": "IN, IM, IVP, IO", "max_mg": 5}]},
    {"indication": "Pediatric Head Trauma", "steps": [{"text": "0.1 mg/kg (5 mg/mL) IVP. Maximum 5 mg", "per_kg": 0.1, "unit": "mg", "concentration": "5 mg/mL", "route": "IVP", "max_mg": 5}]}
  ],
  "note": "Dose of 0.1 mg/kg (5 mg/mL) IM, IN, max single 2.5mg/total 5mg listed in drug reference is NOT indicated on any protocol page per source document.",
  "contraindications": ["Hypersensitivity", "Pregnant", "Nursing mothers", "Renal failure", "Shock", "Glaucoma", "Acute alcoholic intoxication with depressed vital signs"],
  "adverse_reactions": ["Apnea", "Respiratory depression", "Hypoxia", "Decreased tidal volume", "Fluctuations in vital signs", "Dysrhythmias", "Hypotension if pushed too fast", "Euphoria", "Confusion", "Nausea", "Vomiting", "Headache", "Hiccups"],
  "precautions": ["Not recommended in pregnancy - see Magnesium Sulfate for eclampsia."],
  "medical_considerations": ["Consider reducing dose in elderly/debilitated patients - may take longer to recover.", "Monitor respiratory status."],
  "mechanism_of_action": "Sedative; amnesic; short-acting benzodiazepine CNS depressant"
},
{
  "id": "morphine", "name": "Morphine", "source_pages": [220,221],
  "certification": ["AEMT", "Paramedic"],
  "special_notes": None, "onset": "2-3 minutes",
  "adult_dosing": [{"indication": "Pain Control", "steps": [{"text": "2-6 mg IVP, IM. Maximum 10 mg", "unit": "mg", "route": "IVP, IM", "max_mg": 10}]}],
  "pediatric_dosing": [], "pediatric_note": "No pediatric doses for this medication.",
  "contraindications": ["Hypersensitivity", "Significant hypotension", "Acute abdominal conditions", "Multisystem trauma", "Head injury", "Convulsive disorders", "Hypovolemia", "Asthma", "Pregnancy"],
  "adverse_reactions": ["Major hazards: respiratory depression, circulatory depression - respiratory arrest, shock, cardiac arrest possible with overdose/rapid IV", "Tachycardia, bradycardia, palpitation, faintness, syncope, orthostatic hypotension", "Euphoria, dysphasia, weakness, headache, agitation, tremor, uncoordinated movements, hallucinations, disorientation, visual disturbances", "Allergic reactions to opiates, urticaria, anaphylaxis", "Facial sweating, local tissue irritation/pain"],
  "precautions": ["Systolic BP at least 90 mmHg (may need fluid bolus).", "Watch for respiratory depression; have Narcan ready."],
  "medical_considerations": ["Administer slowly to avoid nausea/vomiting.", "Antidote: Narcan 2 mg IVP reverses morphine effects.", "Use with caution in the elderly."],
  "mechanism_of_action": "Narcotic (opiate) agonist"
},
{
  "id": "naloxone", "name": "Naloxone (Narcan)", "source_pages": [222,223],
  "certification": ["EMT - IN or Auto-Injector Only", "AEMT", "Paramedic"],
  "special_notes": None, "onset": "2 minutes",
  "adult_dosing": [
    {"indication": "Pulseless Electrical Activity (PEA)", "steps": [{"text": "2-4 mg IVP, IO", "unit": "mg", "route": "IVP, IO"}]},
    {"indication": "Overdose/Toxic Exposure", "steps": [
      {"text": "2-4 mg IN", "unit": "mg", "route": "IN"},
      {"text": "2-4 mg IN, IVP, IO, IM", "unit": "mg", "route": "IN, IVP, IO, IM"}
    ]}
  ],
  "pediatric_dosing": [{"indication": "Pediatric Overdose/Toxic Exposure/Cyanide Exposure", "steps": [
    {"text": "0.1 mg/kg (1 mg/mL) IN. Maximum 2 mg (2 mL)", "per_kg": 0.1, "unit": "mg", "concentration": "1 mg/mL", "route": "IN", "max_mg": 2},
    {"text": "If respiratory depression: 0.1 mg/kg (1 mg/mL) IVP, IN, IM. Maximum single dose 2 mg (2 mL)", "per_kg": 0.1, "unit": "mg", "concentration": "1 mg/mL", "route": "IVP, IN, IM", "max_single_mg": 2}
  ]}],
  "contraindications": ["Known hypersensitivity"],
  "adverse_reactions": ["Increased BP", "Tachycardia", "Projectile vomiting", "Tremors", "Seizures (possibly opiate withdrawal)", "Dysrhythmias", "Cardiac arrest"],
  "precautions": ["Nausea, vomiting, sweating, tachycardia, increased BP, tremulousness, seizures, cardiac arrest possible."],
  "medical_considerations": ["Short half-life; effects last 1-4 hours - watch patient closely. Narcotic effect often outlasts antagonist. Subsequent IM dose prolongs IV effects."],
  "mechanism_of_action": "Narcotic antagonist; reverses opiate effects including respiratory depression"
},
{
  "id": "nitroglycerin", "name": "Nitroglycerin", "source_pages": [224],
  "certification": ["EMT - Pt. assist Only", "AEMT - SL Only", "Paramedic"],
  "special_notes": None, "onset": "2 minutes",
  "adult_dosing": [{"indication": "Chest Pain (Suspected ACS) / Acute Pulmonary Edema", "steps": [{"text": "0.4 mg SL (spray or tablet)", "unit": "mg", "route": "SL"}]}],
  "pediatric_dosing": [], "pediatric_note": "No pediatric doses for this medication.",
  "contraindications": ["Known hypersensitivity", "Pericardial tamponade, restrictive cardiomyopathy, constrictive pericarditis", "Do not give if Cialis taken within 48 hrs, or Levitra/Viagra within 24+ hrs"],
  "adverse_reactions": ["Headache", "Orthostatic hypotension", "Dizziness", "Weakness", "Palpitations", "Nausea & vomiting"],
  "precautions": ["Contraindicated in head trauma.", "Use caution in intoxicated patients.", "Remove any transdermal patch before defibrillation."],
  "medical_considerations": ["Check for transdermal patch prior to spray/tablet administration."],
  "mechanism_of_action": "Antianginal agent (coronary vasodilator)"
},
{
  "id": "normal_saline", "name": "Normal Saline 0.9 (NS)", "source_pages": [225,226],
  "certification": ["AEMT", "Paramedic"],
  "special_notes": None,
  "adult_dosing": [
    {"indication": "Chest Pain / Vomiting-Diarrhea / Post ROSC Care / Altered Mental Status / Epistaxis / Obstetrical Emergency", "steps": [{"text": "See specific protocol for bolus volume", "route": "IV"}]},
    {"indication": "Behavioral Emergency / Sedation", "steps": [{"text": "1 L Fluid Bolus", "unit": "L", "route": "IV"}]},
    {"indication": "Hypotension/Shock Non-Trauma", "steps": [{"text": "500 mL Fluid Bolus", "unit": "mL", "route": "IV"}, {"text": "20 mL/kg Fluid Bolus", "per_kg": 20, "unit": "mL", "route": "IV"}, {"text": "30 mL/kg Fluid Bolus", "per_kg": 30, "unit": "mL", "route": "IV"}]},
    {"indication": "Multiple Trauma", "steps": [{"text": "500 mL Fluid Bolus", "unit": "mL", "route": "IV"}]},
    {"indication": "Fever/Suspected Sepsis", "steps": [{"text": "30 mL/kg Fluid Bolus", "per_kg": 30, "unit": "mL", "route": "IV"}]},
    {"indication": "Burns", "steps": [{"text": "500 mL/hr Fluid Bolus", "unit": "mL/hr", "route": "IV"}]}
  ],
  "pediatric_dosing": [
    {"indication": "Pediatric Altered Mental Status / Pediatric Head Trauma", "steps": [{"text": "20 mL/kg Fluid Bolus", "per_kg": 20, "unit": "mL", "route": "IV"}]},
    {"indication": "Pediatric Vomiting/Diarrhea", "steps": [{"text": "10 mL/kg Fluid Bolus", "per_kg": 10, "unit": "mL", "route": "IV"}]},
    {"indication": "Pediatric Hypotension/Sepsis/Shock Non-Trauma", "steps": [{"text": "60 mL/kg Fluid Bolus. Maximum total 60 mL/kg", "per_kg": 60, "unit": "mL", "route": "IV"}]}
  ],
  "contraindications": ["None known"],
  "adverse_reactions": ["Febrile response, infection at injection site, venous thrombosis/phlebitis, extravasation, hypervolemia. Discontinue infusion if adverse reaction occurs."],
  "precautions": ["Geriatric: start at low end of dosing range - decreased hepatic/renal/cardiac function common.", "Do not administer unless solution is clear and seal intact."],
  "medical_considerations": ["N/A"],
  "mechanism_of_action": "Nonpyrogenic solution for fluid/electrolyte replacement"
},
{
  "id": "ondansetron", "name": "Ondansetron (Zofran)", "source_pages": [227],
  "certification": ["AEMT - ODT Only", "Paramedic"],
  "special_notes": None, "onset": "Rapid", "peak_effect": "15-30 minutes",
  "adult_dosing": [
    {"indication": "Chest Pain (Suspected ACS)", "steps": [{"text": "4 mg IVP, IM", "unit": "mg", "route": "IVP, IM"}]},
    {"indication": "Abdominal Pain / Vomiting/Diarrhea", "steps": [{"text": "4 mg IVP, ODT, IM. May repeat x1", "unit": "mg", "route": "IVP, ODT, IM"}]}
  ],
  "pediatric_dosing": [{"indication": "Pediatric Vomiting/Diarrhea", "steps": [
    {"text": "0.2 mg/kg (2 mg/mL) IVP. Maximum 4 mg (2 mL)", "per_kg": 0.2, "unit": "mg", "concentration": "2 mg/mL", "route": "IVP", "max_mg": 4},
    {"text": "10 kg (1 year old): 2 mg ODT", "unit": "mg", "route": "ODT"},
    {"text": "> 20 kg: 4 mg ODT", "unit": "mg", "route": "ODT"}
  ]}],
  "contraindications": ["Hypersensitivity"],
  "adverse_reactions": ["Angina, ECG alterations, hypotension, tachycardia, syncope, palpitations", "Extrapyramidal reactions, grand mal seizure, dizziness, lightheadedness", "Flushing", "Pain, redness, burning at injection site", "Hypokalemia, hiccups"],
  "precautions": ["Not a GI/intestinal motility stimulant.", "Transient ECG changes including QT prolongation."],
  "medical_considerations": ["N/A"],
  "mechanism_of_action": "Antiemetic"
},
{
  "id": "oral_glucose", "name": "Oral Glucose", "source_pages": [228],
  "certification": ["EMT", "AEMT", "Paramedic"],
  "special_notes": None, "onset": "1-2 minutes",
  "adult_dosing": [{"indication": "Hypoglycemia/Hyperglycemia", "steps": [{"text": "15 gm PO", "unit": "gm", "route": "PO"}]}],
  "pediatric_dosing": [{"indication": "Pediatric Hypoglycemia/Hyperglycemia", "steps": [{"text": "7.5-15 gm PO", "unit": "gm", "route": "PO"}]}],
  "contraindications": ["Do not give to unconscious person or someone unable to swallow"],
  "adverse_reactions": ["N/A"], "precautions": ["N/A"], "medical_considerations": ["N/A"],
  "mechanism_of_action": "Natural sugar"
},
{
  "id": "oxygen", "name": "Oxygen", "source_pages": [229],
  "certification": ["EMT", "AEMT", "Paramedic"],
  "special_notes": None, "onset": "Immediate",
  "adult_dosing": [{"indication": "General", "steps": [
    {"text": "2-6 LPM via nasal cannula", "route": "Nasal cannula"},
    {"text": "10-15 LPM via non-rebreather mask", "route": "NRB mask"},
    {"text": "10-15 LPM or greater via BVM/ET", "route": "BVM/ET"}
  ]}],
  "pediatric_dosing": [{"indication": "General", "steps": [
    {"text": "2-6 LPM via nasal cannula", "route": "Nasal cannula"},
    {"text": "10-15 LPM via non-rebreather mask", "route": "NRB mask"},
    {"text": "10-15 LPM or greater via BVM/ET", "route": "BVM/ET"},
    {"text": "Blow-by Oxygen", "route": "Blow-by"}
  ]}],
  "contraindications": ["None. May depress respirations in rare COPD patients - not a contraindication, but watch closely and assist ventilations if RR declines."],
  "adverse_reactions": ["Toxicity, depressed hypercarbic drive (respiratory depression with COPD patients)"],
  "precautions": ["N/A"], "medical_considerations": ["N/A"],
  "mechanism_of_action": "Medical gas"
},
{
  "id": "sodium_bicarbonate", "name": "Sodium Bicarbonate", "source_pages": [230],
  "certification": ["Paramedic"],
  "special_notes": None, "onset": "Immediate",
  "adult_dosing": [
    {"indication": "Pulseless Electrical Activity (PEA)", "steps": [{"text": "1 mEq/kg (1 mEq/mL) IVP, IO", "per_kg": 1, "unit": "mEq", "concentration": "1 mEq/mL", "route": "IVP, IO"}]},
    {"indication": "V-Fib/Pulseless V-Tach", "steps": [{"text": "50 mEq IVP, IO", "unit": "mEq", "route": "IVP, IO"}]},
    {"indication": "Overdose/Toxic Exposure", "steps": [{"text": "1-2 mEq/kg (1 mEq/mL) IVP", "per_kg_range": [1,2], "unit": "mEq", "concentration": "1 mEq/mL", "route": "IVP"}]}
  ],
  "pediatric_dosing": [{"indication": "Pediatric Pulseless Arrest / Pediatric Overdose-Toxic Exposure-Cyanide Exposure", "steps": [{"text": "1 mEq/kg (1 mEq/mL) IVP, IO", "per_kg": 1, "unit": "mEq", "concentration": "1 mEq/mL", "route": "IVP, IO"}]}],
  "contraindications": ["Hypertension", "Convulsions", "CHF", "Other situations where sodium administration can be dangerous"],
  "adverse_reactions": ["Hypernatremia", "Alkalosis", "Hypokalemia"],
  "precautions": ["Avoid overdosage/alkalosis - may cause vascular irritation/sloughing if extravascular.", "Avoid scalp vein use.", "Caution in CHF or other edematous/sodium-retaining states."],
  "medical_considerations": ["Flush IV tubing before and after administration.", "If potassium falls too low, heart may become irritable, especially with digitalis."],
  "mechanism_of_action": "Alkalinizing agent; antacid; electrolyte"
},
{
  "id": "txa", "name": "Tranexamic Acid (TXA)", "source_pages": [231],
  "certification": ["AEMT", "Paramedic"],
  "special_notes": None, "half_life": "3 hours",
  "adult_dosing": [
    {"indication": "Epistaxis", "steps": [{"text": "200 mg IN", "unit": "mg", "route": "IN"}]},
    {"indication": "Maternal Arrest / Multiple Trauma / Trauma Arrest", "steps": [{"text": "2 gm IVP", "unit": "gm", "route": "IVP"}]},
    {"indication": "Obstetrical Emergency", "steps": [{"text": "2 gm IVP. May repeat x1 if bleeding persists.", "unit": "gm", "route": "IVP"}]}
  ],
  "pediatric_dosing": [], "pediatric_note": "No pediatric doses for this medication.",
  "contraindications": ["More than 3 hours since injury", "Do not give to known pregnancy"],
  "adverse_reactions": ["HTN", "Increased ICP"],
  "precautions": ["Monitor for symptoms of severe allergic reaction and changes in vision."],
  "medical_considerations": ["None"],
  "mechanism_of_action": "Antifibrinolytic hemostatic"
},
{
  "id": "vecuronium", "name": "Vecuronium (Norcuron)", "source_pages": [232],
  "certification": ["Paramedic"],
  "special_notes": None, "onset": "1-3 minutes", "half_life": "60-120 minutes", "peak_effect": "4-6 minutes",
  "adult_dosing": [{"indication": "Post ROSC Care", "steps": [{"text": "10 mg IVP, IO", "unit": "mg", "route": "IVP, IO"}]}],
  "pediatric_dosing": [], "pediatric_note": "No pediatric doses for this medication.",
  "contraindications": ["Hypersensitivity to vecuronium or components", "Allergy to other neuromuscular blockers or aminosteroid compounds", "Known/suspected myasthenia gravis or other neuromuscular disorders", "Severe electrolyte imbalances", "Severe hepatic disease", "Severe renal impairment", "Severe acid-base disturbances", "Severe hypoxemia", "Severe hypotension or shock", "Severe burns or trauma", "Neuromuscular diseases with elevated serum potassium"],
  "adverse_reactions": ["Hypotension, tachycardia", "Respiratory depression, bronchospasm", "Muscle weakness, paralysis", "Nausea, vomiting", "Allergic reactions, rash/itching"],
  "precautions": ["Use with caution in hepatic/renal disease or electrolyte abnormalities."],
  "medical_considerations": ["Monitor for respiratory depression."],
  "mechanism_of_action": "Binds competitively to cholinergic receptors at the motor endplate, preventing acetylcholine binding"
},
]

meta = {
  "source": "Toledo Fire & Rescue Department, Bureau of EMS - Patient Care Protocols",
  "source_review_date": "2026-04-22",
  "extracted_from": "Patient Care Protocols - Responsoft 4-22-2026.pdf",
  "disclaimer": "Reference tool only. Verify against the current official protocol book before clinical use. Not a substitute for medical direction, training, or clinical judgment."
}

out = {"meta": meta, "drugs": DRUGS}
with open('/sessions/festive-determined-bohr/mnt/outputs/protocols/drugs.json', 'w') as f:
    json.dump(out, f, indent=2)
print("wrote", len(DRUGS), "drugs")
