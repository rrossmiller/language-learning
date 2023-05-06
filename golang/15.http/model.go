package main

type Response struct {
	Meta struct {
		Disclaimer  string `json:"disclaimer"`
		Terms       string `json:"terms"`
		License     string `json:"license"`
		LastUpdated string `json:"last_updated"`
		Results     struct {
			Skip  int `json:"skip"`
			Limit int `json:"limit"`
			Total int `json:"total"`
		} `json:"results"`
	} `json:"meta"`
	Results []struct {
		SplProductDataElements                               []string `json:"spl_product_data_elements"`
		RecentMajorChanges                                   []string `json:"recent_major_changes"`
		RecentMajorChangesTable                              []string `json:"recent_major_changes_table"`
		IndicationsAndUsage                                  []string `json:"indications_and_usage"`
		DosageAndAdministration                              []string `json:"dosage_and_administration"`
		DosageAndAdministrationTable                         []string `json:"dosage_and_administration_table"`
		DosageFormsAndStrengths                              []string `json:"dosage_forms_and_strengths"`
		Contraindications                                    []string `json:"contraindications"`
		WarningsAndCautions                                  []string `json:"warnings_and_cautions"`
		AdverseReactions                                     []string `json:"adverse_reactions"`
		AdverseReactionsTable                                []string `json:"adverse_reactions_table"`
		DrugInteractions                                     []string `json:"drug_interactions"`
		UseInSpecificPopulations                             []string `json:"use_in_specific_populations"`
		Pregnancy                                            []string `json:"pregnancy"`
		PediatricUse                                         []string `json:"pediatric_use"`
		GeriatricUse                                         []string `json:"geriatric_use"`
		Overdosage                                           []string `json:"overdosage"`
		Description                                          []string `json:"description"`
		ClinicalPharmacology                                 []string `json:"clinical_pharmacology"`
		MechanismOfAction                                    []string `json:"mechanism_of_action"`
		Pharmacodynamics                                     []string `json:"pharmacodynamics"`
		Pharmacokinetics                                     []string `json:"pharmacokinetics"`
		NonclinicalToxicology                                []string `json:"nonclinical_toxicology"`
		CarcinogenesisAndMutagenesisAndImpairmentOfFertility []string `json:"carcinogenesis_and_mutagenesis_and_impairment_of_fertility"`
		ClinicalStudies                                      []string `json:"clinical_studies"`
		ClinicalStudiesTable                                 []string `json:"clinical_studies_table"`
		HowSupplied                                          []string `json:"how_supplied"`
		StorageAndHandling                                   []string `json:"storage_and_handling"`
		InformationForPatients                               []string `json:"information_for_patients"`
		SplMedguide                                          []string `json:"spl_medguide"`
		SplMedguideTable                                     []string `json:"spl_medguide_table"`
		InstructionsForUse                                   []string `json:"instructions_for_use"`
		InstructionsForUseTable                              []string `json:"instructions_for_use_table"`
		PackageLabelPrincipalDisplayPanel                    []string `json:"package_label_principal_display_panel"`
		SetID                                                string   `json:"set_id"`
		ID                                                   string   `json:"id"`
		EffectiveTime                                        string   `json:"effective_time"`
		Version                                              string   `json:"version"`
		Openfda                                              struct {
			ApplicationNumber  []string `json:"application_number"`
			BrandName          []string `json:"brand_name"`
			GenericName        []string `json:"generic_name"`
			ManufacturerName   []string `json:"manufacturer_name"`
			ProductNdc         []string `json:"product_ndc"`
			ProductType        []string `json:"product_type"`
			Route              []string `json:"route"`
			SubstanceName      []string `json:"substance_name"`
			Rxcui              []string `json:"rxcui"`
			SplID              []string `json:"spl_id"`
			SplSetID           []string `json:"spl_set_id"`
			PackageNdc         []string `json:"package_ndc"`
			IsOriginalPackager []bool   `json:"is_original_packager"`
			Nui                []string `json:"nui"`
			PharmClassEpc      []string `json:"pharm_class_epc"`
			PharmClassMoa      []string `json:"pharm_class_moa"`
			Unii               []string `json:"unii"`
		} `json:"openfda"`
	} `json:"results"`
}
