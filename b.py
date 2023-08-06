def append_source_scan(session, extract_path, project_id, oss_info):
    """
    * Source Scanner 결과를 DB에 저장하기 위한 데이터 가공.
    :param project_id:
    :param extract_path:
    :param session:
    :param oss_info:
    :return:
    """
    licenses = oss_info.get("_licenses", ["None"])
    webpage_str = get_license_text(session, licenses, "SRC")

    # 원래의 copyrights 리스트를 그대로 유지하고, 중복된 정보를 처리
    unique_copyrights = []
    copyrights = oss_info.get("_copyright")
    logging.info(
        "oss-copyrights: ",
        oss_info.get("oss_name", ""),
        " - ",
        copyrights,
        " /",
        oss_info.get("file", ""),
    )
    for copyright_text in copyrights:
        if not any(
            is_same_oss(copyright_text, other_copyright)
            for other_copyright in unique_copyrights
        ):
            unique_copyrights.append(copyright_text)

    sorted_license = sorted(licenses) if isinstance(licenses, list) else licenses
    license_str = ",".join(sorted_license)

    # obligation(notify/source/restriction) 조회
    notify, source, restriction = get_obligations(session, licenses, "SRC")

    refactory_info = {
        "project_id": project_id,
        "file": oss_info.get("file", ""),
        "license": license_str,
        "copyright": ",".join(unique_copyrights),
        "comment": oss_info.get("comment", ""),
        "ossName": oss_info.get("oss_name", ""),
        "ossVersion": oss_info.get("oss_version", ""),
        "download_location": oss_info.get("download_location", ""),
        "matched_lines": oss_info.get("matched_lines", ""),
        "fileURL": oss_info.get("fileURL", ""),
        "scanoss_reference": oss_info.get("scanoss_reference", ""),
        "from": "SRC",
        "webpage": webpage_str,
        "notify": notify,
        "source": source,
        "restriction": restriction,
        "checksum": get_sha1(os.path.join(extract_path, oss_info.get("file"))),
    }