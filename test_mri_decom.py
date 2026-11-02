"""
Unit and integration tests for MRI Decommissioning & Helium Deal-Flow Engine
"""

import unittest
from mri_decom_scraper import (
    HeliumValuationEngine,
    CONDocketParser,
    MRI_OEM_DATABASE
)

class TestMRIDecom(unittest.TestCase):
    def test_helium_valuation_cold_vs_quenched(self):
        cold_val = HeliumValuationEngine.calculate_valuation("SIEMENS_AVANTO_15T", is_at_field_cold=True)
        quenched_val = HeliumValuationEngine.calculate_valuation("SIEMENS_AVANTO_15T", is_at_field_cold=False)

        self.assertEqual(cold_val["magnet_status"], "COLD_OPERATIONAL")
        self.assertEqual(quenched_val["magnet_status"], "WARM_QUENCHED_DISCOUNTED")
        self.assertGreater(cold_val["estimated_midpoint_resale"], quenched_val["estimated_midpoint_resale"])
        self.assertGreater(cold_val["lhe_recoverable_value"], 0.0)

    def test_con_docket_keyword_filter(self):
        mri_desc = "Notice of Intent: Replacement of MRI system in main hospital radiology suite."
        office_desc = "Renovation of hospital lobby and gift shop."

        self.assertTrue(CONDocketParser.is_mri_replacement_project(mri_desc))
        self.assertFalse(CONDocketParser.is_mri_replacement_project(office_desc))

    def test_con_record_parsing(self):
        records = [{
            "facility_name": "Metro Diagnostic Health",
            "state": "GA",
            "city": "Savannah",
            "project_description": "Replacement of existing Siemens Magnetom Avanto 1.5T MRI",
            "contact_name": "Jane Doe",
            "contact_phone": "555-0199"
        }]
        leads = CONDocketParser.parse_con_records(records)
        self.assertEqual(len(leads), 1)
        self.assertEqual(leads[0]["outgoing_model"], "Magnetom Avanto 1.5T")
        self.assertGreater(leads[0]["potential_referral_fee"], 5000.0)

if __name__ == '__main__':
    unittest.main()
