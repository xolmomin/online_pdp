import json

data = [
  {
    "model": "users.course",
    "pk": "4b9aea7b-0c53-4799-afa7-0143fe7451b2",
    "fields": {
      "updated_at": "2025-10-18T06:36:31.194Z",
      "created_at": "2025-09-15T04:26:25.702Z",
      "name": "DevOps",
      "level": "intermediate",
      "full_description": "<p>DevOps</p>",
      "short_description": "<p>DevOps</p>",
      "has_certificate": False,
      "has_support": False,
      "practice_count": 45,
      "valid_days": 30,
      "price": 990000,
      "rating": 0,
      "video_count": 0,
      "total_video_duration": 0,
      "cover_image": "cover_image_courses/2025/10/18/devops.webp",
      "category": "de2bceea-fe92-4e9b-b0c9-b201ed20d254",
      "teachers": "77963b82-5f2d-49b9-aafb-6969c66fc6e6"
    }
  },
  {
    "model": "users.course",
    "pk": "64e713dd-a73d-419f-9653-1ecc4855f99c",
    "fields": {
      "updated_at": "2025-10-18T06:38:24.609Z",
      "created_at": "2025-09-15T04:26:25.702Z",
      "name": "Django Template based",
      "level": "intermediate",
      "full_description": "<p>Django Template based</p>",
      "short_description": "<p>Django Template based</p>",
      "has_certificate": False,
      "has_support": False,
      "practice_count": 45,
      "valid_days": 30,
      "price": 790000,
      "rating": 0,
      "video_count": 0,
      "total_video_duration": 0,
      "cover_image": "cover_image_courses/2025/10/18/Django-Template.webp",
      "category": "de2bceea-fe92-4e9b-b0c9-b201ed20d254",
      "teachers": "77963b82-5f2d-49b9-aafb-6969c66fc6e6"
    }
  },
  {
    "model": "users.course",
    "pk": "7395593f-cc13-4a56-901e-12bc5bdd9069",
    "fields": {
      "updated_at": "2025-10-18T06:40:31.897Z",
      "created_at": "2025-09-15T04:26:25.702Z",
      "name": "Data Structure and Algorithm",
      "level": "intermediate",
      "full_description": "<p>Data Structure and Algorithm</p>",
      "short_description": "<p>Data Structure and Algorithm</p>",
      "has_certificate": False,
      "has_support": False,
      "practice_count": 45,
      "valid_days": 30,
      "price": 990000,
      "rating": 0,
      "video_count": 0,
      "total_video_duration": 0,
      "cover_image": "cover_image_courses/2025/10/18/data-structure.webp",
      "category": "de2bceea-fe92-4e9b-b0c9-b201ed20d254",
      "teachers": "77963b82-5f2d-49b9-aafb-6969c66fc6e6"
    }
  },
  {
    "model": "users.course",
    "pk": "7bbed029-3154-418a-b054-bdc5a2a40cc8",
    "fields": {
      "updated_at": "2025-10-18T06:33:44.076Z",
      "created_at": "2025-09-15T04:26:25.702Z",
      "name": "FastAPI",
      "level": "intermediate",
      "full_description": "<p>FastAPI</p>",
      "short_description": "<p>FastAPI</p>",
      "has_certificate": False,
      "has_support": False,
      "practice_count": 45,
      "valid_days": 30,
      "price": 990000,
      "rating": 0,
      "video_count": 0,
      "total_video_duration": 0,
      "cover_image": "cover_image_courses/2025/10/18/fastapi.webp",
      "category": "de2bceea-fe92-4e9b-b0c9-b201ed20d254",
      "teachers": "77963b82-5f2d-49b9-aafb-6969c66fc6e6"
    }
  },
  {
    "model": "users.course",
    "pk": "8f498748-ee38-48a1-95b1-cb2a4c38591f",
    "fields": {
      "updated_at": "2025-10-18T06:34:45.248Z",
      "created_at": "2025-09-15T04:26:25.702Z",
      "name": "Django Rest Framework",
      "level": "intermediate",
      "full_description": "<p>Django Rest Framework</p>",
      "short_description": "<p>Django Rest Framework</p>",
      "has_certificate": False,
      "has_support": False,
      "practice_count": 45,
      "valid_days": 30,
      "price": 990000,
      "rating": 0,
      "video_count": 0,
      "total_video_duration": 0,
      "cover_image": "cover_image_courses/2025/10/18/drf.webp",
      "category": "de2bceea-fe92-4e9b-b0c9-b201ed20d254",
      "teachers": "77963b82-5f2d-49b9-aafb-6969c66fc6e6"
    }
  },
  {
    "model": "users.course",
    "pk": "aaee2b54-d626-44f9-a1f1-3acb4b6b4dd1",
    "fields": {
      "updated_at": "2025-10-18T06:31:02.914Z",
      "created_at": "2025-09-15T04:26:25.702Z",
      "name": "Python Basic",
      "level": "intermediate",
      "full_description": "<p>Modul 1</p>",
      "short_description": "<p>Modul 1</p>",
      "has_certificate": False,
      "has_support": False,
      "practice_count": 45,
      "valid_days": 30,
      "price": 590000,
      "rating": 0,
      "video_count": 0,
      "total_video_duration": 0,
      "cover_image": "cover_image_courses/2025/10/18/basic-python.webp",
      "category": "de2bceea-fe92-4e9b-b0c9-b201ed20d254",
      "teachers": "77963b82-5f2d-49b9-aafb-6969c66fc6e6"
    }
  },
  {
    "model": "users.course",
    "pk": "c6255d66-ca14-4e50-8c9e-d0d11bc950cc",
    "fields": {
      "updated_at": "2025-10-18T06:29:21.482Z",
      "created_at": "2025-09-15T04:26:25.702Z",
      "name": "Python Advanced Practice with async and aiogram",
      "level": "intermediate",
      "full_description": "<p>Python Advanced Practice with async and aiogram</p>",
      "short_description": "<p>Python Advanced Practice with async and aiogram</p>",
      "has_certificate": False,
      "has_support": False,
      "practice_count": 45,
      "valid_days": 30,
      "price": 790000,
      "rating": 0,
      "video_count": 0,
      "total_video_duration": 0,
      "cover_image": "cover_image_courses/2025/10/18/aiogram.webp",
      "category": "de2bceea-fe92-4e9b-b0c9-b201ed20d254",
      "teachers": "77963b82-5f2d-49b9-aafb-6969c66fc6e6"
    }
  },
  {
    "model": "users.course",
    "pk": "c9864158-0e19-49ca-b181-fadf9f567686",
    "fields": {
      "updated_at": "2025-10-18T06:39:19.035Z",
      "created_at": "2025-09-15T04:26:25.702Z",
      "name": "Python Advanced",
      "level": "intermediate",
      "full_description": "<p>OOP kirish, Class &amp; Object</p>",
      "short_description": "<p>OOP kirish, Class &amp; Object</p>",
      "has_certificate": False,
      "has_support": False,
      "practice_count": 45,
      "valid_days": 30,
      "price": 690000,
      "rating": 0,
      "video_count": 0,
      "total_video_duration": 0,
      "cover_image": "cover_image_courses/2025/10/18/python.webp",
      "category": "de2bceea-fe92-4e9b-b0c9-b201ed20d254",
      "teachers": "77963b82-5f2d-49b9-aafb-6969c66fc6e6"
    }
  },
  {
    "model": "users.course",
    "pk": "d97bb06c-aa14-44b2-87b3-7ce4cfba36d4",
    "fields": {
      "updated_at": "2025-10-18T06:41:59.407Z",
      "created_at": "2025-09-15T04:26:25.702Z",
      "name": "Telegram Bot (aiogram)",
      "level": "intermediate",
      "full_description": "<p>Telegram Bot (aiogram)</p>",
      "short_description": "<p>Telegram Bot (aiogram)</p>",
      "has_certificate": False,
      "has_support": False,
      "practice_count": 45,
      "valid_days": 30,
      "price": 790000,
      "rating": 0,
      "video_count": 0,
      "total_video_duration": 0,
      "cover_image": "cover_image_courses/2025/10/18/telegram-bot.webp",
      "category": "de2bceea-fe92-4e9b-b0c9-b201ed20d254",
      "teachers": "77963b82-5f2d-49b9-aafb-6969c66fc6e6"
    }
  },
  {
    "model": "users.category",
    "pk": "de2bceea-fe92-4e9b-b0c9-b201ed20d254",
    "fields": {
      "updated_at": "2025-10-16T05:24:36.933Z",
      "created_at": "2025-10-16T05:24:36.933Z",
      "name": "Pythonga kirish"
    }
  }
]


output = []

for section in data:
    section_id = section["id"]  # parent section ID

    for part in section.get("parts", []):
        lesson = {
            "model": "users.lesson",
            "pk": part["id"],
            "fields": {
                "updated_at": "2025-09-15T06:17:07.324Z",
                "created_at": "2025-09-15T06:17:07.324Z",
                "order_number": part.get("ord"),
                "name": part.get("title"),
                "status": "unpublished",
                "access_type": "private",
                "video_duration": 0,
                "section": section_id,
                "video_link": part.get("mediaUrl"),
                "video": "videos/2025/09/15/example_video_vMb6u3o.mp4"
            }
        }
        output.append(lesson)

with open("lesson_fixture.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
