import xml.etree.ElementTree as ET



def parse_test_result(xml_path="report.xml"):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        suite = root if root.tag == "testsuite" else root.find("testsuite")
        if suite is None:
            print("❌ <testsuite> 태그를 찾을 수 없습니다.")
            return 0, 0, 0, 0

        total = int(suite.attrib.get("tests", "0"))
        failures = int(suite.attrib.get("failures", "0"))
        broken = int(suite.attrib.get("broken", "0"))
        skipped = int(suite.attrib.get("skipped", "0"))

        passed = total - failures - broken - skipped

        return passed, failures, broken, skipped

    except Exception as e:
        print(f"❌ 테스트 결과 파싱 실패: {e}")
        return 0, 0, 0, 0

def get_failed_test_names(xml_path="report.xml"):

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        suite = root if root.tag == "testsuite" else root.find("testsuite")
        if suite in None:
            return []

        failed_tests = []
        for testcase in suite.findall("testcase"):
            if testcase.find("failure") is not None or testcase.find("broken") is not None:
                name = testcase.attrib.get("name", "unknown")
                failed_tests.append(name)

        return failed_tests

    except Exception as e:
        print(f"❌ 실패한 테스트 이름 파싱 실패: {e}")
        return []









