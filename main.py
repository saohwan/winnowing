from winnowing import Winnowing


def calculate_similarity(a_content, b_content):
    """
    :Author SangWanLee
    :Description: 소스코드 winnowing 알고리즘을 사용한 유사도 측정 테스트 함수
    :param a_content:
    :param b_content:
    :return:
    """
    winnower = Winnowing()

    # WFP 문자열을 파싱하여 (라인 번호, 해시 값) 의 쌍으로 이루어진 집합(set)을 생성.
    a_wfp = winnower.wfp_for_contents('a.py', False, a_content.encode('utf-8'))
    b_wfp = winnower.wfp_for_contents('b.py', False, b_content.encode('utf-8'))

    print(a_wfp)
    print(b_wfp)

    def parse_wfp(wfp_str):
        winnow_set = set()
        lines = wfp_str.strip().split('\n')
        for line in lines:
            items = line.split(',')
            for item in items:
                if '=' in item:
                    line_number, hash_value = item.split('=')
                    try:
                        line_number = int(line_number)
                        # hash_value = int(hash_value)
                        winnow_set.add((line_number, hash_value))
                    except ValueError:
                        pass
        return winnow_set

    a_winnow = parse_wfp(a_wfp)
    b_winnow = parse_wfp(b_wfp)
    # intersection = a_winnow.intersection(b_winnow)

    # simillarity = a_winnow.intersection(b_winnow)

    matching_line_numbers = len(
        a_winnow.intersection(b_winnow))  # a_winnow 와 b_winnow 의 교집합을 matching_line_numbers 에 반환
    print(f"matching line numbers: {matching_line_numbers}")
    total_line_numbers = max(len(a_winnow), len(b_winnow))
    print(f"total_line_numbers: {total_line_numbers}")

    similarity_percentage = (matching_line_numbers / total_line_numbers) * 100

    return similarity_percentage, a_winnow.intersection(b_winnow)


with open('a.py', 'r', encoding='utf-8') as a_file:
    a_content = a_file.read()

with open('b.py', 'r', encoding='utf-8') as b_file:
    b_content = b_file.read()

similarity, matched_items = calculate_similarity(a_content, b_content)

print(f'소스코드 파일 a.py와 b.py의 일치율: {similarity:.2f}%')

print('일치하는 항목들:')
for line_number, hash_value in matched_items:
    print(f'라인 {line_number}: 해시 값 {hash_value}')
