"""
JMeter 성능 테스트 자동 실행 및 HTML 리포트 생성

pytest로 실행하면:
1. JMeter CLI로 .jmx 테스트 실행
2. .jtl 결과 파일 파싱
3. HTML 리포트 자동 생성 + 브라우저 오픈

사용법:
    pytest src/tests/performance/test_jmeter_performance.py -v
    pytest src/tests/performance/test_jmeter_performance.py -k "popular" -v
"""
import os
import csv
import subprocess
import webbrowser
import pytest
from datetime import datetime

# ===================== 경로 설정 =====================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
JMETER_BIN = r"C:\Users\jmlim\AppData\Local\Programs\JMeter\bin\jmeter.bat"
RESULT_DIR = os.path.join(CURRENT_DIR, "results")
REPORT_DIR = os.path.join(CURRENT_DIR, "reports")

# JMX 테스트 파일 경로
JMX_FILES = {
    "popular_movie_load": os.path.join(CURRENT_DIR, "popular_movie_load_test.jmx"),
    "search_performance": os.path.join(CURRENT_DIR, "search_performance_test.jmx"),
}

os.makedirs(RESULT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


def run_jmeter_test(jmx_file: str, result_file: str) -> bool:
    """JMeter CLI로 테스트 실행"""
    cmd = [
        JMETER_BIN,
        "-n",  # non-GUI 모드
        "-t", jmx_file,
        "-l", result_file,
        "-j", os.path.join(RESULT_DIR, "jmeter.log"),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return result.returncode == 0


def parse_jtl_results(jtl_file: str) -> dict:
    """JTL(CSV) 결과 파일을 파싱하여 통계 생성"""
    if not os.path.exists(jtl_file):
        return None

    samples = []
    with open(jtl_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            samples.append({
                "timestamp": int(row.get("timeStamp", 0)),
                "elapsed": int(row.get("elapsed", 0)),
                "label": row.get("label", ""),
                "responseCode": row.get("responseCode", ""),
                "success": row.get("success", "").lower() == "true",
                "bytes": int(row.get("bytes", 0)),
                "latency": int(row.get("Latency", 0)),
                "connect": int(row.get("Connect", 0)),
            })

    if not samples:
        return None

    elapsed_times = [s["elapsed"] for s in samples]
    elapsed_times.sort()
    total = len(samples)
    success_count = sum(1 for s in samples if s["success"])
    fail_count = total - success_count

    # 라벨별 통계
    labels = {}
    for s in samples:
        label = s["label"]
        if label not in labels:
            labels[label] = {"times": [], "success": 0, "fail": 0}
        labels[label]["times"].append(s["elapsed"])
        if s["success"]:
            labels[label]["success"] += 1
        else:
            labels[label]["fail"] += 1

    label_stats = []
    for label, data in labels.items():
        times = sorted(data["times"])
        count = len(times)
        label_stats.append({
            "label": label,
            "count": count,
            "avg": round(sum(times) / count, 1),
            "min": min(times),
            "max": max(times),
            "p90": times[int(count * 0.9)] if count > 1 else times[0],
            "p95": times[int(count * 0.95)] if count > 1 else times[0],
            "p99": times[int(count * 0.99)] if count > 1 else times[0],
            "success": data["success"],
            "fail": data["fail"],
            "error_rate": round((data["fail"] / count) * 100, 2),
        })

    return {
        "total_samples": total,
        "success": success_count,
        "fail": fail_count,
        "error_rate": round((fail_count / total) * 100, 2),
        "avg_response": round(sum(elapsed_times) / total, 1),
        "min_response": min(elapsed_times),
        "max_response": max(elapsed_times),
        "p90": elapsed_times[int(total * 0.9)] if total > 1 else elapsed_times[0],
        "p95": elapsed_times[int(total * 0.95)] if total > 1 else elapsed_times[0],
        "p99": elapsed_times[int(total * 0.99)] if total > 1 else elapsed_times[0],
        "throughput": round(total / ((max(s["timestamp"] for s in samples) - min(s["timestamp"] for s in samples)) / 1000), 2) if total > 1 else 0,
        "label_stats": label_stats,
    }


def generate_html_report(test_name: str, stats: dict, report_path: str):
    """HTML 리포트 생성"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 라벨별 테이블 행 생성
    label_rows = ""
    for ls in stats["label_stats"]:
        status_class = "pass" if ls["error_rate"] == 0 else "fail"
        label_rows += f"""
            <tr class="{status_class}">
                <td>{ls['label']}</td>
                <td>{ls['count']}</td>
                <td>{ls['avg']}ms</td>
                <td>{ls['min']}ms</td>
                <td>{ls['max']}ms</td>
                <td>{ls['p90']}ms</td>
                <td>{ls['p95']}ms</td>
                <td>{ls['p99']}ms</td>
                <td>{ls['error_rate']}%</td>
            </tr>"""

    overall_status = "PASS" if stats["error_rate"] < 5 else "FAIL"
    status_color = "#28a745" if overall_status == "PASS" else "#dc3545"

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>JMeter Performance Report - {test_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px;
        }}
        .header h1 {{ font-size: 24px; margin-bottom: 5px; }}
        .header p {{ opacity: 0.8; font-size: 14px; }}
        .status-badge {{
            display: inline-block; padding: 5px 15px; border-radius: 20px;
            font-weight: bold; font-size: 14px; margin-top: 10px;
            background: {status_color}; color: white;
        }}
        .cards {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px; }}
        .card {{
            background: white; padding: 20px; border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08); text-align: center;
        }}
        .card .value {{ font-size: 28px; font-weight: bold; color: #333; }}
        .card .label {{ font-size: 13px; color: #888; margin-top: 5px; }}
        table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }}
        th {{ background: #667eea; color: white; padding: 12px 15px; text-align: center; font-size: 13px; }}
        td {{ padding: 10px 15px; text-align: center; border-bottom: 1px solid #eee; font-size: 13px; }}
        tr.pass td:last-child {{ color: #28a745; font-weight: bold; }}
        tr.fail td:last-child {{ color: #dc3545; font-weight: bold; }}
        tr:hover {{ background: #f8f9fa; }}
        .section-title {{ font-size: 18px; font-weight: bold; margin: 25px 0 10px; color: #333; }}
        .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 30px; padding: 15px; }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>JMeter Performance Test Report</h1>
        <p>{test_name} | {now}</p>
        <span class="status-badge">{overall_status}</span>
    </div>

    <div class="cards">
        <div class="card">
            <div class="value">{stats['total_samples']}</div>
            <div class="label">Total Samples</div>
        </div>
        <div class="card">
            <div class="value">{stats['avg_response']}ms</div>
            <div class="label">Avg Response Time</div>
        </div>
        <div class="card">
            <div class="value">{stats['throughput']}/s</div>
            <div class="label">Throughput</div>
        </div>
        <div class="card">
            <div class="value" style="color: {status_color}">{stats['error_rate']}%</div>
            <div class="label">Error Rate</div>
        </div>
    </div>

    <div class="cards" style="grid-template-columns: repeat(5, 1fr);">
        <div class="card">
            <div class="value" style="font-size:22px;">{stats['min_response']}ms</div>
            <div class="label">Min</div>
        </div>
        <div class="card">
            <div class="value" style="font-size:22px;">{stats['max_response']}ms</div>
            <div class="label">Max</div>
        </div>
        <div class="card">
            <div class="value" style="font-size:22px;">{stats['p90']}ms</div>
            <div class="label">P90</div>
        </div>
        <div class="card">
            <div class="value" style="font-size:22px;">{stats['p95']}ms</div>
            <div class="label">P95</div>
        </div>
        <div class="card">
            <div class="value" style="font-size:22px;">{stats['p99']}ms</div>
            <div class="label">P99</div>
        </div>
    </div>

    <div class="section-title">Request Details</div>
    <table>
        <thead>
            <tr>
                <th>Label</th>
                <th>Samples</th>
                <th>Avg</th>
                <th>Min</th>
                <th>Max</th>
                <th>P90</th>
                <th>P95</th>
                <th>P99</th>
                <th>Error %</th>
            </tr>
        </thead>
        <tbody>
            {label_rows}
        </tbody>
    </table>

    <div class="footer">
        Generated by QATEST JMeter Runner | {now}
    </div>
</div>
</body>
</html>"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)


# ===================== pytest 테스트 =====================

class TestJMeterPerformance:
    """JMeter 성능 테스트를 pytest로 실행"""

    @pytest.mark.parametrize("test_name,jmx_key", [
        ("인기 영화 부하 테스트", "popular_movie_load"),
        ("검색 성능 테스트", "search_performance"),
    ])
    def test_jmeter_run(self, test_name, jmx_key):
        """JMeter 테스트 실행 → 결과 파싱 → HTML 리포트 생성"""
        jmx_file = JMX_FILES[jmx_key]
        assert os.path.exists(jmx_file), f"JMX 파일을 찾을 수 없습니다: {jmx_file}"

        # 타임스탬프로 결과 파일 구분
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = os.path.join(RESULT_DIR, f"{jmx_key}_{timestamp}.jtl")

        # 1. JMeter 실행
        print(f"\n{'='*50}")
        print(f"  JMeter 실행: {test_name}")
        print(f"  JMX: {jmx_file}")
        print(f"{'='*50}")

        success = run_jmeter_test(jmx_file, result_file)
        assert success, f"JMeter 실행 실패: {test_name}"
        assert os.path.exists(result_file), f"결과 파일이 생성되지 않았습니다: {result_file}"

        # 2. 결과 파싱
        stats = parse_jtl_results(result_file)
        assert stats is not None, "결과 파싱 실패"

        # 3. HTML 리포트 생성
        report_file = os.path.join(REPORT_DIR, f"{jmx_key}_{timestamp}.html")
        generate_html_report(test_name, stats, report_file)
        print(f"\n  HTML Report: {report_file}")

        # 4. 브라우저에서 열기
        webbrowser.open(f"file:///{report_file.replace(os.sep, '/')}")

        # 5. 결과 검증
        print(f"\n  Total: {stats['total_samples']} | Avg: {stats['avg_response']}ms | Error: {stats['error_rate']}%")
        assert stats["error_rate"] < 10, f"에러율이 10%를 초과했습니다: {stats['error_rate']}%"


def run_all_and_open():
    """직접 실행 시 모든 테스트 수행"""
    for test_name, jmx_key in [("인기 영화 부하 테스트", "popular_movie_load"), ("검색 성능 테스트", "search_performance")]:
        jmx_file = JMX_FILES[jmx_key]
        if not os.path.exists(jmx_file):
            print(f"  SKIP: {jmx_file} 없음")
            continue

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = os.path.join(RESULT_DIR, f"{jmx_key}_{timestamp}.jtl")

        print(f"\n  Running: {test_name}...")
        if run_jmeter_test(jmx_file, result_file):
            stats = parse_jtl_results(result_file)
            if stats:
                report_file = os.path.join(REPORT_DIR, f"{jmx_key}_{timestamp}.html")
                generate_html_report(test_name, stats, report_file)
                webbrowser.open(f"file:///{report_file.replace(os.sep, '/')}")
                print(f"  Report: {report_file}")


if __name__ == "__main__":
    run_all_and_open()
