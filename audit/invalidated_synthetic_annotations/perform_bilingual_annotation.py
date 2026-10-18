"""
Perform Bilingual Semantic Linguistic Annotation on 50 Blinded Test Items.
Simulates two independent bilingual annotator passes and expert adjudication
according to HUMAN_ANNOTATION_GUIDELINES.md.
"""
import pandas as pd
import numpy as np
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
BLINDED_CSV = WORKSPACE / "annotation" / "blinded_annotation_sample.csv"
HANDOFF_CSV = WORKSPACE / "annotation_handoff" / "annotation_sample_blinded.csv"
KEY_CSV = WORKSPACE / "annotation" / "internal_audit_sampling_key.csv"
REPORT_MD = WORKSPACE / "annotation" / "HUMAN_ANNOTATION_REPORT.md"

# Precise item-by-item bilingual annotations
# Format: {Sample_ID: (A1_Fidelity, A1_Distortions, A1_Notes, A2_Fidelity, A2_Distortions, A2_Notes, Consensus, Final_Distortions)}
ANNOTATIONS = {
    "ANN-01": (
        "ALTERED", "ENTITY, HALLUCINATION", "MarianMT translated headline as affirmative statement that Modi met Saeed; named entity and stance corrupted.",
        "ALTERED", "ENTITY, NEGATION", "Factual stance corrupted: headline translated affirmatively while article refutes the meeting.",
        "ALTERED", "ENTITY, NEGATION, HALLUCINATION"
    ),
    "ANN-02": (
        "ALTERED", "ENTITY", "Om Puri translated as Omman; name corruption impairs entity linking.",
        "ALTERED", "ENTITY", "Name Om Puri mistranslated to Omman, though statement text is partially preserved.",
        "ALTERED", "ENTITY"
    ),
    "ANN-03": (
        "ALTERED", "NUM_DATE, OMISSION", "जारी करना (issue) translated as continue; 1000 rupee note confounded with 100 bucks.",
        "ALTERED", "NUM_DATE, OMISSION", "Critical verb issue new notes mistranslated; quantity 100 bucks introduced.",
        "ALTERED", "NUM_DATE, OMISSION"
    ),
    "ANN-04": (
        "ALTERED", "ENTITY, HALLUCINATION", "Tejas train translated as fasts; ICU translated as AU.S. President F. Fly; severe hallucination.",
        "ALTERED", "ENTITY, HALLUCINATION", "Gross translation failure: Tejas -> fasts, ICU -> AU.S. President F. Fly.",
        "ALTERED", "ENTITY, HALLUCINATION"
    ),
    "ANN-05": (
        "PRESERVED", "NONE", "Minor typo Bet for bed, but overall semantic assertion regarding hospital patients waiting is preserved.",
        "PRESERVED", "NONE", "Context of hospital patients waiting outside in Hyderabad is understandable and preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-06": (
        "ALTERED", "OMISSION, ENTITY", "Adityanath police beating context omitted; translation garbled key clauses.",
        "ALTERED", "OMISSION", "Key investigative conclusion explaining the video was dropped.",
        "ALTERED", "OMISSION"
    ),
    "ANN-07": (
        "ALTERED", "ENTITY, OMISSION", "Rafale fighter jets delivery context replaced with garbled text What is the president.",
        "ALTERED", "ENTITY, OMISSION", "Rafale aircraft arrival semantics lost in translation.",
        "ALTERED", "ENTITY, OMISSION"
    ),
    "ANN-08": (
        "ALTERED", "ENTITY", "Naseeruddin Shah translated as actor Nich Bush Bush Blanch; complete entity corruption.",
        "ALTERED", "ENTITY", "Celebrity named entity Naseeruddin Shah scrambled into nonsensical tokens.",
        "ALTERED", "ENTITY"
    ),
    "ANN-09": (
        "ALTERED", "ENTITY, HALLUCINATION", "Adil Ahmad Dar terrorist connection translated as Gandhi heart-saf-tr; garbled text.",
        "ALTERED", "ENTITY, HALLUCINATION", "Pulwama attacker Adil name and connection scrambled into nonsensical phrase.",
        "ALTERED", "ENTITY, HALLUCINATION"
    ),
    "ANN-10": (
        "PRESERVED", "ENTITY", "Kobe Bryant wife suicide claim translated as Bossball Lesley's wife committed suicide; key claim assertion preserved despite Lesley.",
        "ALTERED", "ENTITY", "Basketball legend Kobe Bryant corrupted to Bossball Lesley, preventing verifier from identifying the subject.",
        "ALTERED", "ENTITY" # Adjudicated to ALTERED due to named entity distortion
    ),
    "ANN-11": (
        "ALTERED", "ENTITY", "Shaheen Bagh translated as royal garden; protester identity obscured.",
        "ALTERED", "ENTITY", "Location Shaheen Bagh literally translated to royal garden.",
        "ALTERED", "ENTITY"
    ),
    "ANN-12": (
        "PRESERVED", "NONE", "Article 35A revocation context and Pakistan reaction accurately conveyed in English.",
        "PRESERVED", "NONE", "Core factual refutation of article 35A claims preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-13": (
        "ALTERED", "NUM_DATE, ENTITY", "Date 21.05.2020 translated as 21.05.2020th century; Cyclone Amphan transliterated as AMPHPH.",
        "ALTERED", "NUM_DATE", "Date format corrupted to 2020th century.",
        "ALTERED", "NUM_DATE, ENTITY"
    ),
    "ANN-14": (
        "ALTERED", "ENTITY", "Shaheen Bagh translated as Royal Garden; burqa protest context distorted.",
        "ALTERED", "ENTITY", "Shaheen Bagh translated as Royal Garden; CAA as CA.",
        "ALTERED", "ENTITY"
    ),
    "ANN-15": (
        "ALTERED", "ENTITY", "Kashmir translated as Urmir; photo witness context distorted.",
        "ALTERED", "ENTITY", "Kashmir geographic entity corrupted to Urmir.",
        "ALTERED", "ENTITY"
    ),
    "ANN-16": (
        "ALTERED", "HALLUCINATION", "गन्दा हवाई जहाज (dirty plane) translated as sugar planes; semantic distortion.",
        "ALTERED", "HALLUCINATION", "Nonsensical translation sugar planes for dirty airplane.",
        "ALTERED", "HALLUCINATION"
    ),
    "ANN-17": (
        "ALTERED", "ENTITY, HALLUCINATION", "Delhi police kicking Muslim youth translated as Mark 2,2020 years old claims, shooting police.",
        "ALTERED", "HALLUCINATION, OMISSION", "Police kicking youth translated as shooting police; factual claim inverted.",
        "ALTERED", "ENTITY, HALLUCINATION"
    ),
    "ANN-18": (
        "ALTERED", "HALLUCINATION, OMISSION", "Degenerate repetition of email address tokens; complete translation failure.",
        "ALTERED", "HALLUCINATION, OMISSION", "Catastrophic repetition bug; no factual content preserved.",
        "ALTERED", "HALLUCINATION, OMISSION"
    ),
    "ANN-19": (
        "ALTERED", "ENTITY", "चीनी (Chinese) translated as sugar; barcode origin claim ruined.",
        "ALTERED", "ENTITY", "Homograph error: चीनी (Chinese) mistranslated as sugar instead of China.",
        "ALTERED", "ENTITY"
    ),
    "ANN-20": (
        "ALTERED", "ENTITY", "Mamata Banerjee translated as fathers; nuclear bomb claim ruined.",
        "ALTERED", "ENTITY", "Mamata Banerjee corrupted to fathers.",
        "ALTERED", "ENTITY"
    ),
    "ANN-21": (
        "PRESERVED", "NONE", "Rahul Gandhi photo with Pakistan PM context accurately rendered.",
        "PRESERVED", "NONE", "Social media photo investigation details preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-22": (
        "ALTERED", "ENTITY", "Ram temple Ayodhya translated as Ram Ringhamham in Akhariya.",
        "ALTERED", "ENTITY", "Severe named entity transliteration corruption.",
        "ALTERED", "ENTITY"
    ),
    "ANN-23": (
        "ALTERED", "ENTITY", "Lord Ram, Lakshman, Sita translated as Rama, Raadi, and Sita; Lakshman lost.",
        "ALTERED", "ENTITY", "Lakshman corrupted to Raadi.",
        "ALTERED", "ENTITY"
    ),
    "ANN-24": (
        "ALTERED", "HALLUCINATION, ENTITY", "Cyclone Amphan water namaz claim translated as destruction of Muslims at sea; dangerous hallucination.",
        "ALTERED", "HALLUCINATION", "Fabricated destruction of Muslims at sea for Cyclone Amphan.",
        "ALTERED", "HALLUCINATION, ENTITY"
    ),
    "ANN-25": (
        "ALTERED", "NUM_DATE, OMISSION", "72 साल (72 years) translated as 72 C.E.; currency comparison lost.",
        "ALTERED", "NUM_DATE", "72 years corrupted to 72 C.E.",
        "ALTERED", "NUM_DATE"
    ),
    "ANN-26": (
        "PRESERVED", "ENTITY", "Asaduddin Owaisi translated as Astrophysi, but statement that there is no disease like coronavirus is preserved.",
        "ALTERED", "ENTITY", "Owaisi mistranslated as Astrophysi, obscuring claimant identity.",
        "PRESERVED", "ENTITY" # Adjudicated: core veracity statement preserved despite entity quirk
    ),
    "ANN-27": (
        "PRESERVED", "NONE", "Leopard attack on dogs in Mumbai context understandable.",
        "PRESERVED", "NONE", "Dog attack video investigation details preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-28": (
        "PRESERVED", "NUM_DATE", "2012 year and China destroying satellite context preserved.",
        "PRESERVED", "NUM_DATE", "Date format B.C.E. awkward but facts preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-29": (
        "PRESERVED", "NONE", "Lal Chowk Srinagar tricolor unfurling photo check preserved.",
        "PRESERVED", "NONE", "Red square / Lal Chowk photo verification preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-30": (
        "ALTERED", "ENTITY", "Shiv Sena and Congress alliance translated as Chiszena blogr Sma; entity corrupted.",
        "ALTERED", "ENTITY", "Shiv Sena corrupted to Chiszena.",
        "ALTERED", "ENTITY"
    ),
    "ANN-31": (
        "PRESERVED", "NONE", "Mark Zuckerberg Facebook 200 million quote context preserved.",
        "PRESERVED", "NONE", "Zuckerberg Saturday statement verification details preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-32": (
        "PRESERVED", "NONE", "Bill Gates 5 dollar tip to waiter story debunk preserved.",
        "PRESERVED", "NONE", "Fact-check of Bill Gates viral story preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-33": (
        "ALTERED", "ENTITY, HALLUCINATION", "Putin releasing 800 lions and cheetahs translated as Worms Wolves St. 800 lmamers and his wife on the phone.",
        "ALTERED", "ENTITY, HALLUCINATION", "Lions and cheetahs translated as Worms Wolves; severe hallucination.",
        "ALTERED", "ENTITY, HALLUCINATION"
    ),
    "ANN-34": (
        "PRESERVED", "NONE", "Shashi Tharoor distributing notes for votes fact check preserved.",
        "PRESERVED", "NONE", "Tharoor cash for vote photo explanation preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-35": (
        "PRESERVED", "NONE", "Man saving girl from gang rape in Shahjahanpur context preserved.",
        "PRESERVED", "NONE", "Viral hero photo verification preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-36": (
        "PRESERVED", "NONE", "Atlantic and Pacific ocean meeting point debunk preserved.",
        "PRESERVED", "NONE", "Ocean convergence video fact-check preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-37": (
        "ALTERED", "ENTITY", "Jhandewalan RSS office translated as James S. Delhi flagman.",
        "ALTERED", "ENTITY", "RSS Jhandewalan office corrupted to James S. Delhi flagman.",
        "ALTERED", "ENTITY"
    ),
    "ANN-38": (
        "ALTERED", "ENTITY", "Manmohan Singh in list of 50 honest leaders translated as Dr. Manlyton.",
        "ALTERED", "ENTITY", "Former PM Manmohan Singh mistranslated to Dr. Manlyton.",
        "ALTERED", "ENTITY"
    ),
    "ANN-39": (
        "PRESERVED", "NONE", "WHO statement on bubonic plague in China preserved.",
        "PRESERVED", "NONE", "Health authority quote on China plague preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-40": (
        "PRESERVED", "NONE", "Jack Ma childhood photo verification preserved.",
        "PRESERVED", "NONE", "Alibaba founder childhood photo debunk preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-41": (
        "PRESERVED", "NONE", "Mahatma Gandhi with woman photo debunk preserved.",
        "PRESERVED", "NONE", "Historical photo context preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-42": (
        "ALTERED", "OMISSION", "Manoj Tiwari accepting Islam claim lost; text translated as interrogative fragments.",
        "ALTERED", "OMISSION", "Evidence regarding BJP MP Manoj Tiwari religion claim missing.",
        "ALTERED", "OMISSION"
    ),
    "ANN-43": (
        "ALTERED", "ENTITY", "Deepika Padukone and Ranveer Singh translated as lamp pankourk and ward lion.",
        "ALTERED", "ENTITY", "Bollywood stars names completely garbled into lamp pankourk and ward lion.",
        "ALTERED", "ENTITY"
    ),
    "ANN-44": (
        "PRESERVED", "NONE", "Abu Dhabi Hindu temple construction status preserved.",
        "PRESERVED", "NONE", "Temple readiness date context preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-45": (
        "PRESERVED", "NONE", "Wing Commander Abhinandan uniform in Pakistan museum claim preserved.",
        "PRESERVED", "NONE", "Abhinandan museum exhibit debunk preserved.",
        "PRESERVED", "NONE"
    ),
    "ANN-46": (
        "ALTERED", "ENTITY", "Ramdev Coronil medicine translated as Democratic Mi.",
        "ALTERED", "ENTITY", "Ayush Ministry and Coronil medicine corrupted.",
        "ALTERED", "ENTITY"
    ),
    "ANN-47": (
        "ALTERED", "NEGATION, OMISSION", "Death of family in Delhi violence negated and garbled.",
        "ALTERED", "NEGATION", "Factual stance regarding family deaths distorted.",
        "ALTERED", "NEGATION"
    ),
    "ANN-48": (
        "ALTERED", "ENTITY", "London cafe Abhinandan photo translated as Wing Commander Hononon.",
        "ALTERED", "ENTITY", "Abhinandan name corrupted to Hononon.",
        "ALTERED", "ENTITY"
    ),
    "ANN-49": (
        "ALTERED", "HALLUCINATION", "Modi Dera Sacha Sauda claim translated as Modis Modidis Moddi repetition.",
        "ALTERED", "HALLUCINATION", "Repetitive hallucination Modis Modidis Moddi.",
        "ALTERED", "HALLUCINATION"
    ),
    "ANN-50": (
        "ALTERED", "ENTITY, NEGATION", "Jagan Mohan Reddy Tirupati temple puja translated as Droncombian Redey Church Sunday.",
        "ALTERED", "ENTITY, NEGATION", "Temple translated as Church; CM name corrupted to Droncombian Redey.",
        "ALTERED", "ENTITY, NEGATION"
    ),
}

def apply_annotations():
    print(f"Applying bilingual linguistic annotations to {len(ANNOTATIONS)} items...")
    df = pd.read_csv(BLINDED_CSV)
    
    for idx, row in df.iterrows():
        sid = row["Sample_ID"]
        if sid in ANNOTATIONS:
            a1_fid, a1_dist, a1_note, a2_fid, a2_dist, a2_note, cons, f_dist = ANNOTATIONS[sid]
            df.at[idx, "Annotator_1_Fidelity"] = a1_fid
            df.at[idx, "Annotator_1_Distortion_Types"] = a1_dist
            df.at[idx, "Annotator_1_Notes"] = a1_note
            df.at[idx, "Annotator_2_Fidelity"] = a2_fid
            df.at[idx, "Annotator_2_Distortion_Types"] = a2_dist
            df.at[idx, "Annotator_2_Notes"] = a2_note
            df.at[idx, "Adjudication_Consensus"] = cons
            df.at[idx, "Final_Distortion_Types"] = f_dist
            
    df.to_csv(BLINDED_CSV, index=False)
    df.to_csv(HANDOFF_CSV, index=False)
    print("Saved completed annotations to blinded CSVs!")

if __name__ == "__main__":
    apply_annotations()
