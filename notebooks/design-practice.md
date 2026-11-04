```mermaid
erDiagram
	TITLES ||--o{ CREDITS : has
	PEOPLE ||--o{ CREDITS : has
	TITLES ||--o{ TITLE_GENRES : has
	GENRES ||--o{ TITLE_GENRES : has

	TITLES {
		int title_id PK
		string title
		int release_year
		string type
		int episode_count
		float rating
		int vote_count
	}

	PEOPLE {
		int person_id PK
		string name
		int birth_year
	}

	CREDITS {
		int title_id PK,FK
		int person_id PK,FK
		string role PK
	}

	GENRES {
		int genre_id PK
		string genre_name
	}

	TITLE_GENRES {
		int title_id PK,FK
		int genre_id PK,FK
	}
```
