import re


def extract_code(filename):
    """
    Extract an 11-digit code from the filename.

    Args:
        filename: The name of the file to process

    Returns:
        The extracted 11-digit code if found, None otherwise
    """
    filename = filename  # Note: This line is redundant and could be removed
    match = re.search(r'(\d{11})', filename)  # Search for 11 consecutive digits
    return match.group(1) if match else None  # Return the matched digits or None


def match_reg_part_files(registration_files, participant_files):
    """
    Match registration files with corresponding participant files based on common code.

    Args:
        registration_files: List of registration file objects
        participant_files: List of participant file objects

    Returns:
        Dictionary containing:
        - 'matched_pairs': List of tuples with matched (registration_file, participant_file)
        - 'missing_files': List of filenames that don't have a matching counterpart
    """
    # Create safe lists even if None is passed
    reg_files = registration_files if registration_files else []
    part_files = participant_files if participant_files else []
    all_files = reg_files + part_files

    # Create dictionaries mapping codes to file objects
    reg_dict = {}
    part_dict = {}

    # Map registration files by their code
    for file in reg_files:
        reg_dict[extract_code(file.name)] = file

    # Map participant files by their code
    for file in part_files:
        part_dict[extract_code(file.name)] = file

    # Find codes that exist in both registration and participant files
    common_codes = set(reg_dict.keys() & part_dict.keys())

    # Identify files without a matching counterpart
    missing_files = []
    for file in all_files:
        if extract_code(file.name) not in common_codes:
            missing_files.append(file.name)

    # Create pairs of matching registration and participant files
    matched_pairs = []
    for code in common_codes:
        matched_pairs.append((reg_dict[code], part_dict[code]))

    return {"matched_pairs": matched_pairs, "missing_files": missing_files}