# FRAAND

[![Built with Django Bootstrap Template](https://img.shields.io/badge/Built%20with-Django%20Bootstrap%20Template-blueviolet.svg)](https://github.com/griceturrble/django-bootstrap-template/)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Free Rent (it's called 'sharing') Application Among Neighbours [Decentrilized] platform.
Is a stuff sharing platform (aka social network).


## Planned Features

- [ ] profile
    - [ ] photo?
    - [ ] prefered contacts (email, Telegram alias, etc.)
    - [ ] list of items with a search bar
    - [ ] [FUTURE] activity feed
    - [ ] [FUTURE] reputation points
- [ ] item
    - [x] name
    - [x] description
    - [ ] categories/tags
    - [ ] carousel of images (or URLs field)
    - [ ] rent-to (link to a profile)
    - [ ] public/accessible by link/hidden
        - [ ] probably, make custom groups (e.g., for BDSM-only members)
- [ ] deal
    - [ ] due to
    - [ ] item(s)
    - [ ] from profile(s)
    - [ ] to profile(s)
    - [ ] `change_due_date_to(new_date)`
    - [ ] state
        - [ ] communicating
        - [ ] on-going
        - [ ] success
        - [ ] failed (the item is not returned in time)
- [ ] [FUTURE] chat
- [ ] [FUTURE] map
- [ ] [FUTURE] organizations/gropus/clubs



## License

This project uses the GPLv3 license. Please see the [LICENSE](LICENSE) for details.


## Installation

1. Install [PDM](https://github.com/pdm-project/pdm) dependencies.

   ```bash
   pdm init
   ```

2. *PostgreSQL settings*: if not present already create a new `.env` file at `fraand/core/.env`. This file should be gitignored from the repo, and should contain credentials for connecting to the PostgreSQL database:

   - `POSTGRES_NAME`: database name
   - `POSTGRES_USER`: username
   - `POSTGRES_PASSWORD`: password
   - `POSTGRES_HOST`: host serving the database
   - `POSTGRES_PORT`: port

3. Migrate models to the database:

   ```bash
   python fraand/manage.py migrate
   ```

4. Create a superuser:

   ```bash
   python fraand/manage.py createsuperuser
   ```

5. Run the development server:

   ```bash
   python fraand/manage.py runserver
   ```

6. Open http://localhost:8000 to view the running site.
