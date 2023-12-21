-- User Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    password_hash_method VARCHAR(50),
    role VARCHAR(100)
);

-- Recipe Table
CREATE TABLE recipes (
    recipe_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    prep_time INT,
    difficulty VARCHAR(50),
    main_image TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Food Table
CREATE TABLE foods (
    food_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(255),
    calories DECIMAL,
    proteins DECIMAL,
    carbohydrates DECIMAL,
    fats DECIMAL,
    unit_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (unit_id) REFERENCES units(unit_id)
);

-- Portion Table
CREATE TABLE portions (
    portion_id SERIAL PRIMARY KEY,
    food_id INT NOT NULL,
    size DECIMAL NOT NULL,
    unit_id INT NOT NULL,
    FOREIGN KEY (food_id) REFERENCES foods(food_id),
    FOREIGN KEY (unit_id) REFERENCES units(unit_id)
);

-- Unit Table
CREATE TABLE units (
    unit_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- RecipeFood Table
CREATE TABLE recipe_foods (
    recipe_id INT,
    food_id INT,
    portion_id INT,
    quantity DECIMAL,
    unit_id INT,
    PRIMARY KEY (recipe_id, food_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY (food_id) REFERENCES foods(food_id),
    FOREIGN KEY (portion_id) REFERENCES portions(portion_id),
    FOREIGN KEY (unit_id) REFERENCES units(unit_id)
);

-- Step Table
CREATE TABLE steps (
    step_id SERIAL PRIMARY KEY,
    recipe_id INT NOT NULL,
    step_number INT NOT NULL,
    description TEXT,
    step_image TEXT,
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
    proteins DECIMAL,
    carbohydrates DECIMAL,
    fats DECIMAL,
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
