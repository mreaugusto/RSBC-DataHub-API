
def test_unauthorized_user_cannot_reach_search_endpoints(as_guest):
    resp = as_guest.get("/v1/search/123",
                        query_string={"noticeNo": "222"},
                        json={},
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 401


def test_authorized_user_can_search_for_a_prohibition_by_notice_number(as_guest, auth_header):
    resp = as_guest.get("/v1/search/123",
                        query_string={"noticeNo": "222"},
                        follow_redirects=True,
                        headers=auth_header,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "impoundmentId" in resp.json
    assert "prohibitionId" in resp.json
