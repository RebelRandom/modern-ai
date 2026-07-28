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


def test_list_action_items_limit_boundary_values(client):
    r = client.get("/action-items/", params={"limit": 200})
    assert r.status_code == 200

    r = client.get("/action-items/", params={"limit": 201})
    assert r.status_code == 422


def test_list_action_items_pagination_slices_in_id_order(client):
    ids = [
        client.post("/action-items/", json={"description": f"Item {i}"}).json()["id"]
        for i in range(5)
    ]

    r = client.get("/action-items/", params={"sort": "id", "skip": 0, "limit": 2})
    assert [it["id"] for it in r.json()] == ids[0:2]

    r = client.get("/action-items/", params={"sort": "id", "skip": 2, "limit": 2})
    assert [it["id"] for it in r.json()] == ids[2:4]

    r = client.get("/action-items/", params={"sort": "id", "skip": 4, "limit": 2})
    assert [it["id"] for it in r.json()] == ids[4:5]


def test_list_action_items_pagination_beyond_total_returns_empty(client):
    client.post("/action-items/", json={"description": "Only one"})

    r = client.get("/action-items/", params={"skip": 1000, "limit": 10})
    assert r.status_code == 200
    assert r.json() == []


def test_list_action_items_sort_ascending_and_descending_by_id(client):
    ids = [
        client.post("/action-items/", json={"description": f"Sort {i}"}).json()["id"]
        for i in range(3)
    ]

    r = client.get("/action-items/", params={"sort": "id"})
    assert [it["id"] for it in r.json()] == sorted(ids)

    r = client.get("/action-items/", params={"sort": "-id"})
    assert [it["id"] for it in r.json()] == sorted(ids, reverse=True)


def test_list_action_items_sort_by_completed(client):
    open_item = client.post("/action-items/", json={"description": "Open"}).json()
    done_item = client.post("/action-items/", json={"description": "Done"}).json()
    client.put(f"/action-items/{done_item['id']}/complete")

    r = client.get("/action-items/", params={"sort": "completed", "limit": 200})
    items = r.json()
    completed_values = [it["completed"] for it in items]
    assert completed_values == sorted(completed_values)

    ids = [it["id"] for it in items]
    assert ids.index(open_item["id"]) < ids.index(done_item["id"])


def test_list_action_items_default_sort_is_created_at_desc(client):
    first = client.post("/action-items/", json={"description": "First"}).json()
    second = client.post("/action-items/", json={"description": "Second"}).json()

    r = client.get("/action-items/", params={"limit": 200})
    ids = [it["id"] for it in r.json()]
    assert ids.index(second["id"]) < ids.index(first["id"])


def test_list_action_items_completed_filter_combined_with_pagination(client):
    for i in range(3):
        client.post("/action-items/", json={"description": f"Open {i}"})

    ids_done = []
    for i in range(3):
        item = client.post("/action-items/", json={"description": f"Done {i}"}).json()
        client.put(f"/action-items/{item['id']}/complete")
        ids_done.append(item["id"])

    r = client.get(
        "/action-items/", params={"completed": True, "sort": "id", "skip": 1, "limit": 1}
    )
    assert r.status_code == 200
    items = r.json()
    assert [it["id"] for it in items] == ids_done[1:2]
    assert all(it["completed"] for it in items)


