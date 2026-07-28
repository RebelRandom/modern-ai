def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_delete_missing_note_returns_404(client):
    r = client.delete("/notes/999999")
    assert r.status_code == 404


def test_create_note_rejects_blank_fields(client):
    r = client.post("/notes/", json={"title": "  ", "content": "content"})
    assert r.status_code == 422

    r = client.post("/notes/", json={"title": "Title", "content": ""})
    assert r.status_code == 422


def test_patch_note_rejects_blank_title(client):
    r = client.post("/notes/", json={"title": "Title", "content": "Content"})
    note_id = r.json()["id"]

    r = client.patch(f"/notes/{note_id}", json={"title": "   "})
    assert r.status_code == 422


def test_list_notes_rejects_invalid_sort_field(client):
    r = client.get("/notes/", params={"sort": "not_a_field"})
    assert r.status_code == 400


def test_list_notes_rejects_invalid_pagination(client):
    r = client.get("/notes/", params={"skip": -1})
    assert r.status_code == 422

    r = client.get("/notes/", params={"limit": 0})
    assert r.status_code == 422


def test_list_notes_limit_boundary_values(client):
    r = client.get("/notes/", params={"limit": 200})
    assert r.status_code == 200

    r = client.get("/notes/", params={"limit": 201})
    assert r.status_code == 422


def test_list_notes_pagination_slices_in_id_order(client):
    ids = [
        client.post("/notes/", json={"title": f"Note {i}", "content": "c"}).json()["id"]
        for i in range(5)
    ]

    r = client.get("/notes/", params={"sort": "id", "skip": 0, "limit": 2})
    assert [n["id"] for n in r.json()] == ids[0:2]

    r = client.get("/notes/", params={"sort": "id", "skip": 2, "limit": 2})
    assert [n["id"] for n in r.json()] == ids[2:4]

    r = client.get("/notes/", params={"sort": "id", "skip": 4, "limit": 2})
    assert [n["id"] for n in r.json()] == ids[4:5]


def test_list_notes_pagination_beyond_total_returns_empty(client):
    client.post("/notes/", json={"title": "Only one", "content": "c"})

    r = client.get("/notes/", params={"skip": 1000, "limit": 10})
    assert r.status_code == 200
    assert r.json() == []


def test_list_notes_sort_ascending_and_descending_by_id(client):
    ids = [
        client.post("/notes/", json={"title": f"Sort {i}", "content": "c"}).json()["id"]
        for i in range(3)
    ]

    r = client.get("/notes/", params={"sort": "id"})
    assert [n["id"] for n in r.json()] == sorted(ids)

    r = client.get("/notes/", params={"sort": "-id"})
    assert [n["id"] for n in r.json()] == sorted(ids, reverse=True)


def test_list_notes_sort_by_title(client):
    client.post("/notes/", json={"title": "Zebra", "content": "c"})
    client.post("/notes/", json={"title": "Apple", "content": "c"})

    r = client.get("/notes/", params={"sort": "title", "limit": 200})
    titles = [n["title"] for n in r.json()]
    assert titles.index("Apple") < titles.index("Zebra")

    r = client.get("/notes/", params={"sort": "-title", "limit": 200})
    titles = [n["title"] for n in r.json()]
    assert titles.index("Zebra") < titles.index("Apple")


def test_list_notes_default_sort_is_created_at_desc(client):
    first = client.post("/notes/", json={"title": "First", "content": "c"}).json()
    second = client.post("/notes/", json={"title": "Second", "content": "c"}).json()

    r = client.get("/notes/", params={"limit": 200})
    ids = [n["id"] for n in r.json()]
    assert ids.index(second["id"]) < ids.index(first["id"])


def test_list_notes_search_combined_with_pagination_and_sort(client):
    ids = [
        client.post("/notes/", json={"title": f"Match {i}", "content": "Hello"}).json()["id"]
        for i in range(3)
    ]
    client.post("/notes/", json={"title": "No match", "content": "Something else"})

    r = client.get(
        "/notes/", params={"q": "Hello", "sort": "id", "skip": 1, "limit": 1}
    )
    assert r.status_code == 200
    assert [n["id"] for n in r.json()] == ids[1:2]


