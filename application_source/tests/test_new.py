from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import pytest
from httpx import AsyncClient
from app.main import app
from app.database import get_session,Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
TEST_DATABASE_URL="postgresql+asyncpg://postgres:Paridhi#9@localhost/test_db"
engine = create_async_engine(TEST_DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    async with async_session() as session:
        yield session

app.dependency_overrides[get_session] = override_get_db



async def setup():
    async with engine.begin() as conn:
        print("setup called")
        await conn.run_sync(Base.metadata.create_all)

async def teardown():
    async with engine.begin() as conn:
         print("teardown called")
         await conn.run_sync(Base.metadata.drop_all)

async def get_access_token():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/login",
                               data={
                                   "username": "testuser",
                                   "password": "test"
                               }
                               )

        access_token = response.json().get('access_token')
        return access_token


@pytest.mark.asyncio
async def test_create_user():
    await setup()
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/create_user",json={"username":"testuser","email":"email","password":"test"})
        assert response.status_code == 201
    await teardown()

@pytest.mark.asyncio
async def test_post_books_endpoint():
    await setup()
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/create_user",
                          json={"username": "testuser", "email": "email", "password": "test"})
        access_token =await get_access_token()
        response = await client.post("/books",json={
                                      "title": "test_book_title",
                                      "author": "test_author",
                                      "genre": "test_genre",
                                      "year_published": "2024-08-05",
                                      "summary": "test_summary"
                    },
                               headers={
                                   "Authorization": "Bearer " + access_token
                               })

        assert response.status_code == 201
        assert response.json().get('title')=="test_book_title"
    await teardown()

@pytest.mark.asyncio
async def test_get_books_endpoint():
    await setup()
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/create_user",
                          json={"username": "testuser", "email": "email", "password": "test"})
        access_token = await get_access_token()
        print("printing",access_token)
        response = await client.get("/books",headers={
                               "Authorization": "Bearer " + access_token
                           })
        assert response.status_code == 200
        assert response.json()==[]
    await teardown()

@pytest.mark.asyncio
async def test_get_book_for_id_endpoint():
    await setup()
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/create_user",
                          json={"username": "testuser", "email": "email", "password": "test"})
        access_token = await get_access_token()
        await client.post("/books", json={
                                        "title": "test_book_title",
                                        "author": "test_author",
                                        "genre": "test_genre",
                                        "year_published": "2024-08-05",
                                        "summary": "test_summary"
                                    },
                                     headers={
                                         "Authorization": "Bearer " + access_token
                                     })

        response = await client.get("/books/{id}?book_id=1",headers={
                                   "Authorization": "Bearer " + access_token
                               })

        assert response.status_code == 200
        book=response.json()
        if book['title']=="test_book_title":
            assert book['author']=="test_author"
            assert book['genre']=="test_genre"
            assert book['year_published']=="2024-08-05"
            assert book['summary']=="test_summary"
    await teardown()

@pytest.mark.asyncio
async def test_update_book_for_id_endpoint():
    await setup()
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/create_user",
                          json={"username": "testuser", "email": "email", "password": "test"})
        access_token = await get_access_token()
        await client.post("/books", json={
            "title": "test_book_title",
            "author": "test_author",
            "genre": "test_genre",
            "year_published": "2024-08-05",
            "summary": "test_summary"
        },
                          headers={
                              "Authorization": "Bearer " + access_token
                          })

        response =await client.put("/books/{id}?book_id=1",
                              json={
                                  "title": "test_book_title_updated2",
                                  "author": "test_author_updated",
                                  "genre": "test_genre",
                                  "year_published": "2024-08-05",
                                  "summary": "test_summary"
                              },
                              headers={
                                           "Authorization": "Bearer " + access_token
                                       })
        print(response.json())

        assert response.status_code == 200
        book=response.json()
        assert book['title']=="test_book_title_updated2"
        assert book['author'] == "test_author_updated"
        assert book['genre'] == "test_genre"
        assert book['year_published'] == "2024-08-05"
        assert book['summary'] == "test_summary"
    await teardown()

@pytest.mark.asyncio
async def test_delete_book_for_id_endpoint():
    await setup()
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/create_user",
                          json={"username": "testuser", "email": "email", "password": "test"})
        access_token = await get_access_token()
        await client.post("/books", json={
            "title": "test_book_title",
            "author": "test_author",
            "genre": "test_genre",
            "year_published": "2024-08-05",
            "summary": "test_summary"
        },
                          headers={
                              "Authorization": "Bearer " + access_token
                          })
        response =await client.delete("/books/{id}?book_id=1",
                              headers={
                                  "Authorization": "Bearer " + access_token
                              })

        assert response.json().get('message')=="Book deleted"
    await teardown()

@pytest.mark.asyncio
async def test_post_review_endpoint():
    await setup()
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/create_user",
                          json={"username": "testuser", "email": "email", "password": "test"})
        access_token = await get_access_token()
        await client.post("/books", json={
            "title": "test_book_title",
            "author": "test_author",
            "genre": "test_genre",
            "year_published": "2024-08-05",
            "summary": "test_summary"
        },
                          headers={
                              "Authorization": "Bearer " + access_token
                          })
        response = await client.post("/books/{id}/reviews?book_id=1",
                               json={

                                       "user_id": 1,
                                       "review_text": "test_review",
                                       "rating": 4

                               },
                               headers={
                                   "Authorization": "Bearer " + access_token
                               })

        assert response.status_code == 201
        assert response.json().get('review_text') == "test_review"
    await teardown()


@pytest.mark.asyncio
async def test_get_review_endpoint():
    await setup()
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/create_user",
                          json={"username": "testuser", "email": "email", "password": "test"})
        access_token = await get_access_token()
        await client.post("/books", json={
            "title": "test_book_title",
            "author": "test_author",
            "genre": "test_genre",
            "year_published": "2024-08-05",
            "summary": "test_summary"
        },
                          headers={
                              "Authorization": "Bearer " + access_token
                          })
        await client.post("/books/{id}/reviews?book_id=1",
                                     json={

                                         "user_id": 1,
                                         "review_text": "test_review",
                                         "rating": 4

                                     },
                                     headers={
                                         "Authorization": "Bearer " + access_token
                                     })

        response =await client.get("/books/{id}/reviews?book_id=1",
                               headers={
                                   "Authorization": "Bearer " + access_token
                               })

        for review in response.json():
            if review['review_text']=="test_review":
                assert review['user_id'] == 1
                assert review['rating'] ==4

    await teardown()

























