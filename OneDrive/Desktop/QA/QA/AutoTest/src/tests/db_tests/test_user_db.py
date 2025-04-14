import dummy_data


def test_insert_user_api_then_check_db(api_client, db_client, dummy_data):
    #1.테스트용 유저 데이터
    user= dummy_data.user()

    #2. API 호출 (회원가입)
    res = api_client.post("users/register", json=user)
    assert res.status.code == 201 #API 정상확인

    query = f"SELCET * FROM users WHERE email = '{user['email']}';"
    result = db_client.select(query)

    assert len(result) == 1 #DB에 해당 데이터 1건 있어야 함
    assert result[0]["username"] == ["username"] # username값 검증

    delete_query = f"DELETE FROM users WHERE email='{user['email']}';"
    db_client.execute(delete_query)





