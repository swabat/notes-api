def test_create_note(client):
    response = client.post(
        "/notes/",
        json={
            "title": "Test note",
            "content": "Test content"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test note"
    assert data["content"] == "Test content"
    assert data["is_archived"] is False

def test_create_note_with_category(client):
    category_response = client.post(
        "/categories/",
        json={"name": "Work"}
    )
    category_id = category_response.json()["id"]

    response = client.post(
        "/notes/",
        json={
            "title": "Work note",
            "content": "Important",
            "category_id": category_id
        }
    )

    assert response.status_code == 201
    assert response.json()["category_id"] == category_id


def test_create_note_with_invalid_category(client):
    response = client.post(
        "/notes/",
        json={
            "title": "Invalid note",
            "category_id": 9999
        }
    )

    assert response.status_code == 404


def test_filter_notes_by_category(client):
    category = client.post(
        "/categories/",
        json={"name": "Work"}
    ).json()

    client.post(
        "/notes/",
        json={"title": "Work note", "category_id": category["id"]}
    )

    client.post(
        "/notes/",
        json={"title": "Personal note"}
    )

    response = client.get(
        f"/notes/?category_id={category['id']}"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Work note"


def test_search_notes(client):
    client.post(
        "/notes/",
        json={"title": "Python learning"}
    )

    client.post(
        "/notes/",
        json={"title": "Shopping list"}
    )

    response = client.get("/notes/?search=python")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Python learning"


def test_archive_note(client):
    note = client.post(
        "/notes/",
        json={"title": "Archive me"}
    ).json()

    response = client.patch(f"/notes/{note['id']}/archive")

    assert response.status_code == 200
    assert response.json()["is_archived"] is True


def test_filter_archived_notes(client):
    note = client.post(
        "/notes/",
        json={"title": "Archived note"}
    ).json()

    client.patch(f"/notes/{note['id']}/archive")

    response = client.get("/notes/?is_archived=true")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Archived note"   


def test_update_note(client):
    note = client.post(
        "/notes/",
        json={"title": "Old title"}
    ).json()

    response = client.patch(
        f"/notes/{note['id']}",
        json={"title": "New title"}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New title"


def test_delete_note(client):
    note = client.post(
        "/notes/",
        json={"title": "Delete me"}
    ).json()

    response = client.delete(f"/notes/{note['id']}")

    assert response.status_code == 204

    response = client.get(f"/notes/{note['id']}")
    assert response.status_code == 404


def test_create_note_without_title(client):
    response = client.post(
        "/notes/",
        json={"content": "No title"}
    )

    assert response.status_code == 422


def test_create_note_with_empty_title(client):
    response = client.post(
        "/notes/",
        json={"title": ""}
    )

    assert response.status_code == 422


def test_pagination(client):
    for i in range(5):
        client.post(
            "/notes/",
            json={"title": f"Note {i}"}
        )

    response = client.get("/notes/?skip=1&limit=2")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_invalid_pagination(client):
    response = client.get("/notes/?limit=0")

    assert response.status_code == 422


def test_update_note_with_invalid_category(client):
    note = client.post(
        "/notes/",
        json={"title": "Test note"}
    ).json()

    response = client.patch(
        f"/notes/{note['id']}",
        json={"category_id": 9999}
    )

    assert response.status_code == 404

