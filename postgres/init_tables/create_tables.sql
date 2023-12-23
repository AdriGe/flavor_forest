-- User Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    is_admin BOOLEAN
);

CREATE TABLE refresh_tokens (
    id SERIAL PRIMARY KEY,
    jti VARCHAR(255) NOT NULL,
    user_id INTEGER NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- Unit Table
CREATE TABLE units (
    unit_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Recipe Table
CREATE TABLE recipes (
    recipe_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    total_time INT,
    prep_time INT,
    difficulty VARCHAR(50),
    image_url TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Food Table
CREATE TABLE foods (
    food_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(255),
    calories DECIMAL,
    fats DECIMAL,
    saturated_fats DECIMAL,
    carbohydrates DECIMAL,
    sugars DECIMAL,
    fibers DECIMAL,
    proteins DECIMAL,
    sodium DECIMAL,
    unit_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (unit_id) REFERENCES units(unit_id)
);

-- Portion Table
CREATE TABLE portions (
    food_id INT NOT NULL,
    portion_id INT NOT NULL,
    name VARCHAR(255),
    size DECIMAL NOT NULL,
    PRIMARY KEY(food_id, portion_id),
    FOREIGN KEY (food_id) REFERENCES foods(food_id)
);



-- RecipeFood Table
CREATE TABLE recipe_foods (
    recipe_id INT,
    food_id INT,
    quantity DECIMAL,
    portion_id INT,
    unit_id INT,
    PRIMARY KEY (recipe_id, food_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY (food_id) REFERENCES foods(food_id),
    FOREIGN KEY (food_id, portion_id) REFERENCES portions(food_id, portion_id),
    FOREIGN KEY (unit_id) REFERENCES units(unit_id)
);

-- Step Table
CREATE TABLE steps (
    recipe_id INT NOT NULL,
    step_number INT NOT NULL,
    description TEXT[],
    image_url TEXT,
    PRIMARY KEY(recipe_id, step_number),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
);

-- Utensil Table
CREATE TABLE utensils (
    utensil_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- RecipeUtensil Table
CREATE TABLE recipe_utensils (
    recipe_id INT,
    utensil_id INT,
    PRIMARY KEY (recipe_id, utensil_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY (utensil_id) REFERENCES utensils(utensil_id)
);

-- NutritionalValueRecipe Table
CREATE TABLE nutritional_values_recipes (
    recipe_id INT PRIMARY KEY,
    calories DECIMAL,
    fats DECIMAL,
    saturated_fats DECIMAL,
    carbohydrates DECIMAL,
    sugars DECIMAL,
    fibers DECIMAL,
    proteins DECIMAL,
    sodium DECIMAL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
);

-- Tag Table
CREATE TABLE tags (
    tag_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- RecipeTag Table
CREATE TABLE recipe_tags (
    recipe_id INT,
    tag_id INT,
    PRIMARY KEY (recipe_id, tag_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);
