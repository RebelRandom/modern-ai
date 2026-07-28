def test_create_list_and_delete_tag(client):
    r = client.post("/tags/", json={"name": "Work"})
    assert r.status_code == 201, r.text
    tag = r.json()
    assert tag["name"] == "Work"

    r = client.get("/tags/")
    assert r.status_code == 200
    assert any(t["name"] == "Work" for t in r.json())

    r = client.post("/tags/", json={"name": "Work"})
    assert r.status_code == 409

    r = client.delete(f"/tags/{tag['id']}")
    assert r.status_code == 204

    r = client.get("/tags/")
    assert all(t["id"] != tag["id"] for t in r.json())


def test_create_tag_rejects_blank_name(client):
    r = client.post("/tags/", json={"name": "   "})
    assert r.status_code == 422


def test_delete_missing_tag_returns_404(client):
    r = client.delete("/tags/999999")
    assert r.status_code == 404


def test_attach_and_detach_tag_from_note(client):
    note = client.post("/notes/", json={"title": "Note", "content": "Content"}).json()
    tag = client.post("/tags/", json={"name": "Personal"}).json()

    r = client.post(f"/notes/{note['id']}/tags/{tag['id']}")
    assert r.status_code == 201, r.text
    data = r.json()
    assert [t["name"] for t in data["tags"]] == ["Personal"]

    # Attaching the same tag again is idempotent.
    r = client.post(f"/notes/{note['id']}/tags/{tag['id']}")
    assert r.status_code == 201
    assert [t["name"] for t in r.json()["tags"]] == ["Personal"]

    r = client.get(f"/notes/{note['id']}")
    assert [t["name"] for t in r.json()["tags"]] == ["Personal"]

    r = client.delete(f"/notes/{note['id']}/tags/{tag['id']}")
    assert r.status_code == 200
    assert r.json()["tags"] == []


def test_attach_tag_missing_note_or_tag_returns_404(client):
    tag = client.post("/tags/", json={"name": "SoloTag"}).json()
    r = client.post(f"/notes/999999/tags/{tag['id']}")
    assert r.status_code == 404

    note = client.post("/notes/", json={"title": "N", "content": "C"}).json()
    r = client.post(f"/notes/{note['id']}/tags/999999")
    assert r.status_code == 404
