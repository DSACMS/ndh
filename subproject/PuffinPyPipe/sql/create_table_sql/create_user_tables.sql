-- These will need to be improved to support Oauth layers, decorations and an RBAC model.

-- TODO this user model will needed to be extended considerable to support OAuth etc. This is just a skeleton.
CREATE TABLE ndh.user (
    id SERIAL PRIMARY KEY,
    email varchar   NOT NULL,
    first_name varchar   NOT NULL,
    last_name varchar   NOT NULL,
    is_identity_verified boolean   NOT NULL
);

CREATE TABLE ndh.user_access_role (
    id SERIAL PRIMARY KEY,
    user_id INT   NOT NULL,
    user_role_id INT   NOT NULL,
    npi_id BIGINT   NOT NULL
);

CREATE TABLE ndh.user_role (
    id SERIAL PRIMARY KEY,
    role_name varchar(100)   NOT NULL
);
