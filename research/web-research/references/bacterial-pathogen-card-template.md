# Bacterial Pathogen Card Template

Use this 12-section outline when creating KF cards for **bacterial pathogens** in swine/poultry/livestock (e.g., ETEC, Salmonella, APP, M. hyopneumoniae, Lawsonia intracellularis, Brachyspira, Clostridium perfringens, S. suis, etc.).

Unlike virus cards (genome→replication→interferon evasion) or pathway cards (signaling cascade→crosstalk), bacterial pathogen cards focus on **virulence factors, colonization mechanisms, toxin biology, and AMR**.

## Section outline

```
## 1. 🦠 Tổng quan
   - Pathotype classification (gram, shape, family)
   - Disease(s) caused
   - Economic impact (mortality, morbidity, growth loss)
   - Host range + age susceptibility

## 2. 🧱 Cấu trúc kháng nguyên & Phân loại
   - Serotyping system (O/K/H antigens)
   - Major serotypes/groups in the target species
   - Table: Serotype | Virulence factors | Disease | Geographic distribution

## 3. 🧬 Yếu tố độc lực (Virulence Factors)
   - **Adhesins** (fimbriae, afimbrial adhesins, autotransporters)
     * Table: Adhesin | Receptor | Host specificity | Role
   - **Toxins** (enterotoxins, exotoxins, endotoxin/LPS)
     * Table: Toxin | Gene | Structure | Mechanism (receptor → signal → effect)
     * Per toxin: detailed mechanism (e.g., ADP-ribosylation → ↑cAMP → CFTR → diarrhea)
   - **Secretion systems** (T1SS–T6SS, T2SS, T3SS, T4SS)
   - **Capsule/LPS** (anti-phagocytic, complement resistance)
   - **Iron acquisition** (siderophores, heme uptake)
   - **Regulatory networks** (two-component systems, quorum sensing, environmental sensing)
   - **Biofilm formation**

## 4. 🔬 Cơ chế sinh bệnh học (Pathogenesis)
   ```
   Route (oral/respiratory/vector)
   → Adhesion/colonization
   → Invasion (intracellular/extracellular)
   → Toxin secretion
   → Host cell damage (tight junction, cytoskeleton, apoptosis/necrosis)
   → Fluid loss / inflammation / systemic spread
   ```
   - Step-by-step molecular pathogenesis
   - Key host-pathogen interactions (receptors, signaling hijacking)
   - Pathogen-specific niches (small intestine, lung, Peyer's patches, etc.)

## 5. 🛡️ Cơ chế trốn miễn dịch (Immune Evasion)
   | Mechanism | Virulence factor | Immune target | Effect |
   |-----------|-----------------|---------------|--------|
   - Immune subversion, complement resistance, antigenic variation
   - Intracellular survival strategies (if applicable)
   - Host immunosuppression

## 6. 🩺 Biểu hiện lâm sàng & Bệnh tích (Clinical Disease)
   - Forms (acute, chronic, subclinical, peracute)
   - Symptoms by age group
   - Pathology (macroscopic + microscopic lesions)
   - Differential diagnosis (other pathogens with similar presentation)

## 7. 🔬 Chẩn đoán (Diagnosis)
   - Isolation & culture (media, conditions, colony morphology)
   - PCR/RT-PCR (target genes, multiplex panels)
   - Serology (ELISA, agglutination)
   - Sequencing (WGS, MLST)
   - Diagnostic criteria (CFU thresholds, sample type, age)

## 8. 💊 Kháng kháng sinh (Antimicrobial Resistance)
   | Antibiotic class | Resistance prevalence (by region) | Trend | Mechanism (gene, mobile element) |
   - MDR patterns
   - Co-selection with heavy metals (ZnO, CuSO₄) and feed additives
   - Plasmid-mediated resistance
   - Colistin/mcr concerns

## 9. 🛡️ Vaccine & Chiến lược miễn dịch (Vaccines & Immunization)
   | Vaccine type | Approach | Serotype coverage | Efficacy | Stage |
   - Maternal vaccines (sow immunization → passive immunity)
   - Active immunization (live attenuated, killed, subunit, toxoid)
   - Novel platforms (MEFA multi-epitope, IgY, phage display, VLP)

## 10. 🌿 Can thiệp dinh dưỡng & Phụ gia (Nutritional Interventions)
   | Intervention | Mechanism | Evidence level | Source |
   - Probiotics / prebiotics / synbiotics
   - Organic acids (butyrate, benzoic, fumaric)
   - Trace minerals (Zn, Cu, Se, Mn)
   - Amino acids (tryptophan, arginine, threonine, glutamine)
   - Botanicals (polyphenols, saponins, tannins, essential oils)
   - Bacteriophages / endolysins
   - Antimicrobial peptides (AMPs, bacteriocins)

## 11. 🌍 Dịch tễ học (Epidemiology)
   - Global distribution & prevalence
   - Age / production stage susceptibility
   - Risk factors (management, environment, nutrition, genetics)
   - Transmission (fecal-oral, aerosol, vertical, vector)
   - Reservoirs (carrier animals, wildlife, environment)
   - Zoonotic potential (if applicable)

## 12. 📚 Bảng tham khảo (References)
   | PMID | Journal (Year) | Contribution |
   - Minimum 10–20 references
   - Organize by subtopic (virulence, vaccine, AMR, nutrition)
```

## Writing conventions

- **Title**: `🦠 Pathogen Name — Subtitle in Vietnamese`
- **Tags** (10–20): Pathogen genus + species, pathotype, serotypes, disease names, key virulence factors, antibiotic classes, feed additives
- **Language**: Vietnamese with English technical terms preserved
- **Evidence anchoring**: Every mechanism claim needs a PMID or DOI
- **Blockquote callouts**: `> **Key point:** ...` for critical findings
- **Tables**: | col1 | col2 | col3 | markdown
- **Code-block diagrams**: ``` for pathway schematics

## PubMed research pattern for bacterial pathogens

```python
queries = [
    '{pathogen} {disease} pig virulence factors',
    '{pathogen} {disease} pathogenesis mechanism',
    '{pathogen} pig immune response immune evasion',
    '{pathogen} pig vaccine development',
    '{pathogen} antimicrobial resistance pig antibiotics',
    '{pathogen} zinc butyrate probiotic prevention',
    # Respiratory-specific queries (use for lung/respiratory pathogens)
    '{pathogen} cold stress ventilation environment pig',   # environmental triggers
    # GI-specific queries (use for enteric pathogens)
    '{pathogen} pig intestinal barrier tight junction',
    # Deep-dive queries (always add 1-2 from below)
    '{pathogen} biofilm secretion system type IV',
    '{pathogen} iron acquisition siderophore heme',
    '{pathogen} quorum sensing LuxR regulation two-component',
]
```

**Which queries to use:**
- Always run the first 6 queries (virulence, pathogenesis, immune, vaccine, AMR, nutrition)
- For **respiratory pathogens** (APP, M. hyo, B. bronchiseptica, Pasteurella): add cold stress/environment query
- For **enteric pathogens** (ETEC, Salmonella, Lawsonia, Brachyspira, Clostridium): add tight junction query
- Add 1-2 from the deep-dive pool (biofilm, iron, quorum sensing) depending on pathogen prominence
- Total: 8-10 queries, each with `max_results=5-6`, paced at `time.sleep(1.5)` between

### ⚠️ Zero-result workaround for nutritional interventions on respiratory/systemic pathogens

When researching nutritional/dietary interventions for **respiratory or systemic bacterial pathogens**, mechanism-specific queries like `"{pathogen} zinc feed additive pig"` or `"{pathogen} essential oil pig"` frequently return **zero results** — the nutritional literature for these pathogens is sparser than for enteric pathogens. This is not a data gap; it's a literature-structure problem:

| Query type | Example | Typical result |
|-----------|---------|---------------|
| Direct nutrition query | `APP zinc butyrate pig` | 0 hits — no dedicated nutrition studies |
| Plant compound query | `APP naringin pig` | 1-2 hits — rare but can yield gold |
| Immune-modulation query | `APP antimicrobial peptide pig defensin` | 3-5 hits — AMPs are studied |
| Host-response broad query | `APP inflammation NF-kB pig` | 5-10 hits — mechanisms overlap with nutrition |

**Fix:** when direct nutrition queries return 0 results, switch to:
1. **Immune-modulation queries** — AMPs, defensins, host defence peptides
2. **Inflammatory pathway queries** — NF-κB, NLRP3, cytokine + pathogen name
3. **Environmental stress queries** — cold, heat, ventilation — these modulate susceptibility and are cross-referenced with immune pathways
4. **Broader host response** — single-cell, transcriptomics, proteomics + pathogen

This was validated during APP research: zero hits on `"APP zinc butyrate"` but 4 relevant papers found via AMP/NF-κB/scRNA-seq queries (PMID 38378464, 38256101, 37705063, 28093715).

## Section emphasis by pathogen type

| Pathogen type | Prioritize sections |
|--------------|-------------------|
| **Enteric (ETEC, Salmonella, Lawsonia, Brachyspira, Cl. perfringens)** | 3 (toxins + adhesins), 4 (colonization), 5 (barrier disruption), 10 (nutritional — rich literature available) |
| **Respiratory (APP, M. hyopneumoniae, B. bronchiseptica, Pasteurella)** | 3 (secretion systems, biofilm), 4 (lung pathogenesis, cytokine storm), 5 (ciliary/immune evasion), 8 (AMR in Asia — MDR rising), 10 (nutritional — sparse literature, use zero-result workaround above), 11 (cold stress as risk factor) |
| **Systemic (S. suis, E. rhusiopathiae, Salmonella Choleraesuis)** | 3 (capsule), 4 (blood-brain barrier, systemic spread), 5 (anti-phagocytic), 9 (bacterin vs. subunit) |

## Examples

See these complete worked examples:

| Pathogen | Card ID | Type | Highlight |
|----------|---------|------|-----------|
| **ETEC** | c2ed6b52-a07d-4d8c-b18d-31fd7af3b02e | Enteric (Gram-) | Adhesin/toxin table, vaccine matrix, nutritional interventions rich |
| **APP** | 2a66233b-54ee-47b0-9fd4-ec8c4a668bfb | Respiratory (Gram-) | 4 Apx toxin types, biofilm/LPS evasion, MDR Asia, cold stress, AMP synergy |

The **APP card** (created 2026-07-27) demonstrates: multi-query PubMed (8 angles → 26 unique PMIDs), scRNA-seq atlas integration, AMP+antibiotic synergy (MPX+Tulathromycin), and the zero-result workaround applied to nutrition section.
