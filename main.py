from classifier import classify_document
import automation

automation.initialize_output_files()

file_to_process = [
    "data/Santa Monica, CA/Santa_Monica_Draft_Zoning_Ordinance.pdf",
    "data/Santa Monica, CA/Santa_Monica_staff_report.pdf",
    "data/Santa Monica, CA/Santa_Monica_Parcels_at_300_2C_600_and_900_buffers.pdf",
    "data/Huntington Beach, CA/Huntington_Beach_Study_Session_PPT.pdf",
    "data/Huntington Beach, CA/Cannabis-Regulatory-Ordinance-DRAFT.pdf",
    "data/Huntington Beach, CA/Att_3_Cannabis_Land_Use_Policy_Presentation.pdf",
    "data/Baldwin Park, CA/Baldwin_Park_Commercial_Cannabis_Retail.APP.Final.pdf",
    "data/Baldwin Park, CA/Baldwin_Park_Cannabis_ORD_1501.pdf",
    "data/Claremont, CA/Claremont_Draft_Cannabis_Tax_Ordinance.pdf",
    "data/Claremont, CA/Claremont_CA_Consideration_of_an_Amendment_to_the_Claremont_Zoning_Code_to_Allow_Cannabis_Storefront_Retail_Business_as_a_Conditionally_Permitted_Use.pdf",
    "data/St Louis Park, MN/St._Louis_Park_Cannabis_Ordinance.pdf",
    "data/St Louis Park, MN/St._Louis_Park_Local_Reg_Application_CannabisRetailerorLowerPotencyHempRetailerApplication_2025.pdf",
    "data/Hermosa Beach, CA/Cannabis_Advisoty_Group_Workplan_-_04-12-2022.pdf",
    "data/Hermosa Beach, CA/05-24-2022_City_Council_Agenda.pdf",
    "data/Monterey, CA/17AUG_Agenda_Report.pdf",
    "data/Monterey, CA/04MAY_Agenda_Report.pdf",
    "data/Citrus Heights, CA/Citrus_Heights_Staff_Report_.pdf",
    "data/Citrus Heights, CA/Citrus_Heights_4_11_staff_report.pdf",
    "data/Redondo Beach, CA/Dec_19th_Administrative_Report_(11).pdf",
    "data/Redondo Beach, CA/Redondo_Administrative_Report_(17).pdf",
    "data/Cudahy, CA/Cudahy_memo_re_lack_of_viable_parcels_in_remaining_zone.pdf",
    "data/Cudahy, CA/Ordinance_No._730_Cannabis_Business_Accountability_Measure_FINAL.pdf",
    "data/El Segundo, CA/El_Segundo_Cannabis_Regulation_and_Public_Safety_Measure_(withdraw_and_filed_7-20-2021)_(3)_(00389039xB613E).pdf",
    "data/El Segundo, CA/05-03-2022_Agenda_Packet.pdf",
    "data/El Segundo, CA/04-19-2022_City_Council_Agenda.pdf",
    "data/Novato, CA/Novato_Staff_Report_Cannabis_Storefront_Retail_Discussion.pdf",
    "data/Visalia, CA/Visalia_Tax_Ordinance_ballot_measure.pdf",
    "data/Visalia, CA/220-7065_Visalia_Cannabis_Survey_Analysis_-_(P)_presentation.pdf",
    "data/Red Wing, MN/Chapter_6_Section_6.28_-6-14-2025_Update.pdf",
    "data/Red Wing, MN/Local_Cannabis_Retail_Registration_Application_Review_Policy_5-28-2025_(1) (1).pdf",
    "data/Red Wing, MN/Red_Wing_Ord._No._216_-_Amend_Chapt_6_2C_Adding_Sect_6.28_Cannabis.pdf",
]

for file_path in file_to_process:
    print(f"Processing file: {file_path}")
    try:
        result = classify_document(file_path)
        automation.handle_automation(result)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        automation.log_failed_file(file_path, e)

# Finalize digest and logs
automation.finalize_weekly_digest()
automation.finalize_low_priority_log()
automation.finalize_failed_files_log()
automation.finalize_all_results_log()

print("Processing completed. Outputs saved in the 'outputs' folder.")
