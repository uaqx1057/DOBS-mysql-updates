def test_login_get_renders(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"Login" in resp.data or b"\xd8\xaa\xd8\xb3\xd8\xac\xd9\8a\xd9\84" in resp.data


def test_login_post_success(client, hr_user):
    resp = client.post(
        "/login",
        data={"username": "hr1", "password": "pass123"},
        follow_redirects=False,
    )
    assert resp.status_code in (302, 303)
    # Should redirect to HR dashboard
    assert "/hr/dashboard" in resp.headers.get("Location", "") or "dashboard_hr" in resp.headers.get("Location", "")
