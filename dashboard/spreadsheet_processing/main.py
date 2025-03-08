import re

def extract_code(filename):
    filename = filename
    match = re.search(r'(\d{11})', filename)
    return match.group(1) if match else None


def match_registration_participant_files(registration_files, participant_files):
    reg_files = registration_files if registration_files else []
    part_files = participant_files if participant_files else []
    all_files = reg_files + part_files
    reg_dict = {}
    part_dict = {}

    for file in reg_files:
        reg_dict[extract_code(file.name)] = file

    for file in part_files:
        part_dict[extract_code(file.name)] = file

    common_codes = set(reg_dict.keys() & part_dict.keys())
    missing_files = []
    for file in all_files:
        if extract_code(file.name) not in common_codes:
            missing_files.append(file.name)

    matched_pairs = []

    for code in common_codes:
        matched_pairs.append((reg_dict[code], part_dict[code]))


    return {"matched_pairs": matched_pairs, "missing_files": missing_files}


