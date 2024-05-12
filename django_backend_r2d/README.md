# Helpful Commands
1. Accessing Db Shell
    * ``docker exec -it [CONTAINER_NAME_OR_ID] psql -U [YOUR_POSTGRES_USERNAME] -d requirements_to_design_db``
2. Retrieving container information
    * ``docker ps``
3. Generating new django secret key
    * ``python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'``