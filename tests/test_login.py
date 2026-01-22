def test_login_page_renders(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"Login" in resp.data or b"\xd8\xaa\xd8\xb3\xd8\xac\xd9\8a\xd9\84" in resp.data
