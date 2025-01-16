import time

def repeat_test(test_function, repeat_count=5, delay_seconds=10, *args, **kwargs):


    for i in range(repeat_count):
        print(f"테스트 반복 실행 {i + 1}...")
        test_function(*args, **kwargs)  # 테스트 함수 실행
        if i < repeat_count - 1:
            print(f"다음 반복 까지  {delay_seconds}초 전...")
            time.sleep(delay_seconds)
    print("테스트 완료 !")