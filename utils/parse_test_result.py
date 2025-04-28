import xml.etree.ElementTree as ET

def parse_test_result(xml_path="report.xml"):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        total = int(root.attrib.get("tests", 0))
        failures = int(root.attrib.get("failure", 0))
        errors = int(root.attrib.get("error", 0))
        skipped = int(root.attrib.get("skipped", 0))

        passed = total - failures- errors - skipped

        return passed, failures, errors, skipped
    except Exception as e:
        print(f"❌ 테스트 결과 파싱 실패: {e}")
        return 0, 0, 0, 0
