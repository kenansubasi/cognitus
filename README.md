# Cognitus


## Installation

We use docker to run the project.

[Download Docker](https://www.docker.com/community-edition)

Docker can't help for some devices. If the project does not work with Docker, Docker Toolbox will help you.

[Download Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_windows/#step-2-install-docker-toolbox)


## How to Run?

To build the project:
```
docker-compose -p cognitus -f docker/docker-compose.yml -f docker/docker-compose.dev.yml build
```

To run the project:
```
docker-compose -p cognitus -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up -d
```

To restart the project:
```
docker-compose -p cognitus -f docker/docker-compose.yml -f docker/docker-compose.dev.yml restart
```

To stop the project:
```
docker-compose -p cognitus -f docker/docker-compose.yml -f docker/docker-compose.dev.yml stop
```

To see logs:
```
docker-compose -p cognitus -f docker/docker-compose.yml -f docker/docker-compose.dev.yml logs -f --tail 50
```

To status docker containers:
```
docker-compose -p cognitus -f docker/docker-compose.yml -f docker/docker-compose.dev.yml ps
```

To run tests:
```
docker exec -i -t cognitus_web_1 /bin/bash
coverage run manage.py test --noinput && coverage html --skip-covered
```

To load init data:
```
docker exec -i -t cognitus_web_1 /bin/bash
python manage.py initdb
```


## Technologies

This is a list of mostly used awesome technologies and libraries that are used in cognitus Project:

- [Python](https://www.python.org/): Python is an interpreted high-level programming language for general-purpose programming.

- [Django](https://www.djangoproject.com/): Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.

- [PostgreSQL](https://www.postgresql.org/): PostgreSQL is a powerful, open source object-relational database system that has strong reputation for reliability, feature robustness, and performance.

- [Django Rest Framework](https://www.django-rest-framework.org/): Django REST framework is a powerful and flexible toolkit for building Web APIs.


## Maintainers

* **Kenan Subaşı**  - *kenansubasiceng@gmail.com*
