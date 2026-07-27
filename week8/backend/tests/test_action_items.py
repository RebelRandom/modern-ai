def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"

    r = client.get(f"/action-items/{item['id']}")
    assert r.status_code == 200
    assert r.json()["description"] == "Updated"

    r = client.delete(f"/action-items/{item['id']}")
    assert r.status_code == 204

    r = client.get(f"/action-items/{item['id']}")
    assert r.status_code == 404


def test_get_missing_action_item_returns_404(client):
    r = client.get("/action-items/999999")
    assert r.status_code == 404


def test_delete_missing_action_item_returns_404(client):
    r = client.delete("/action-items/999999")
    assert r.status_code == 404


def test_create_action_item_rejects_blank_description(client):
    r = client.post("/action-items/", json={"description": "   "})
    assert r.status_code == 422


def test_list_action_items_rejects_invalid_sort_field(client):
    r = client.get("/action-items/", params={"sort": "not_a_field"})
    assert r.status_code == 400


def test_list_action_items_rejects_invalid_pagination(client):
    r = client.get("/action-items/", params={"skip": -1})
    assert r.status_code == 422

    r = client.get("/action-items/", params={"limit": 0})
    assert r.status_code == 422


