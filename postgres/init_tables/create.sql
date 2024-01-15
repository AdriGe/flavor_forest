-- User Table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    is_admin BOOLEAN
);

CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    jti VARCHAR(255) NOT NULL,
    user_id UUID NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- Unit Table
CREATE TABLE units (
    unit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL
);

-- Recipe Table
CREATE TABLE recipes (
    recipe_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID DEFAULT NULL,
    name VARCHAR(255) NOT NULL,
    headline VARCHAR(255),
    description TEXT,
    total_time INT,
    prep_time INT,
    difficulty INT,
    utensils VARCHAR(255)[],
    image_url TEXT,
    favorites_count INT,
    kcal INT,
    fat FLOAT,
    saturated_fat FLOAT,
    carbohydrate FLOAT,
    sugars FLOAT,
    protein FLOAT,
    fiber FLOAT,
    sodium FLOAT,
    steps TEXT[],
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Food Table
CREATE TABLE foods (
    food_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(255),
    kcal DECIMAL,
    fat DECIMAL,
    saturated_fat DECIMAL,
    carbohydrate DECIMAL,
    sugars DECIMAL,
    fiber DECIMAL,
    protein DECIMAL,
    sodium DECIMAL,
    unit_id UUID NOT NULL,
    image_url TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (unit_id) REFERENCES units(unit_id)
);

-- Portion Table
CREATE TABLE portions (
    portion_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    food_id UUID NOT NULL,
    name VARCHAR(255),
    size FLOAT NOT NULL,
    FOREIGN KEY (food_id) REFERENCES foods(food_id)
);



-- RecipeFood Table
CREATE TABLE recipe_foods (
    recipe_id UUID,
    food_id UUID,
    quantity FLOAT,
    portion_id UUID,
    PRIMARY KEY (recipe_id, food_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY (food_id) REFERENCES foods(food_id),
    FOREIGN KEY (portion_id) REFERENCES portions(portion_id)
);


CREATE TYPE tag_category_enum AS ENUM ('Durée de préparation', 'Type de cuisine', 'Régime alimentaire', 'Saison');

-- Tag Table
CREATE TABLE tags (
    tag_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category tag_category_enum,
    name VARCHAR(100) NOT NULL
);

-- RecipeTag Table
CREATE TABLE recipe_tags (
    recipe_id UUID,
    tag_id UUID,
    PRIMARY KEY (recipe_id, tag_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

INSERT INTO users (user_id, username, email, hashed_password, is_admin)
VALUES (1, 'Foor Bar', 'food@bar.com', 'hashed_password', true);

-- Insert units used in the recipe
INSERT INTO units (unit_id, name)
VALUES 
    (1, 'gramme'), 
    (2, 'ml'),
    (3, 'cl'),
    (4, 'litre')
; -- Add more as needed