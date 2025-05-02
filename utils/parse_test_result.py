import xml.etree.ElementTree as ET





def parse_test_result(xml_path="report.xml"):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        suite = root.find("testsuite")
        if suite is None:
            print("❌ <testsuite> 태그를 찾을 수 없습니다.")
            return 0, 0, 0, 0

        total = int(suite.attrib.get("tests", "0"))
        failures = int(suite.attrib.get("failures", "0"))
        errors = int(suite.attrib.get("errors", "0"))
        skipped = int(suite.attrib.get("skipped", "0"))

        passed = total - failures - errors - skipped

        return passed, failures, errors, skipped

    except Exception as e:
        print(f"❌ 테스트 결과 파싱 실패: {e}")
        return 0, 0, 0, 0

def get_failed_test_names(xml_path="report.xml"):

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        suite = root.find("testsuite")
        if suite in None:
            return []

        failed_tests = []
        for testcase in suite.findall("testcase"):
            if testcase.find("failure") is not None or testcase.find("error") is not None:
                name = testcase.attrib.get("name", "unknown")
                failed_tests.append(name)

        return failed_tests

    except Exception as e:
        print(f"❌ 실패한 테스트 이름 파싱 실패: {e}")
        return []









