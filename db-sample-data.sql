PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Ingredient" (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO Ingredient VALUES(1,'Canned tomatoes');
INSERT INTO Ingredient VALUES(2,'Cumin powder');
INSERT INTO Ingredient VALUES(3,'Ribeye');
INSERT INTO Ingredient VALUES(4,'Salt');
INSERT INTO Ingredient VALUES(5,'Pepper');
CREATE TABLE IF NOT EXISTS "User" (
	id INTEGER NOT NULL, 
	email VARCHAR(35) NOT NULL, 
	name VARCHAR(25) NOT NULL, 
	password VARCHAR(64) NOT NULL, 
	joined_on DATE NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	UNIQUE (name)
);
INSERT INTO User VALUES(1,'testuser1@gmail.com','TestUser1','tu3passwordhash','2000-06-23');
INSERT INTO User VALUES(2,'TU2@gmail.com','TestUser2','tu2passwordhash','1992-10-05');
INSERT INTO User VALUES(3,'TestUser3@gmail.com','TestUser3','tu3passwordhash','2021-01-20');
CREATE TABLE IF NOT EXISTS "Recipe" (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	prep_time_minutes INTEGER, 
	cook_time_minutes INTEGER, 
	submitted_on DATE NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	FOREIGN KEY(user_id) REFERENCES "User" (id)
);
INSERT INTO Recipe VALUES(1,'Test Recipe 1',10,25,'2021-01-20',1);
INSERT INTO Recipe VALUES(2,'Test Recipe 2',25,50,'2021-01-21',2);
CREATE TABLE IF NOT EXISTS "Comment" (
	id INTEGER NOT NULL, 
	content VARCHAR NOT NULL, 
	submitted_on DATETIME NOT NULL, 
	recipe_id INTEGER, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(recipe_id) REFERENCES "Recipe" (id), 
	FOREIGN KEY(user_id) REFERENCES "User" (id)
);
INSERT INTO Comment VALUES(1,'This is gross','2021-01-20 12:00:00.000000',1,2);
INSERT INTO Comment VALUES(2,'That''s just, like, your opinion, man','2021-01-21 16:15:00.000000',1,1);
INSERT INTO Comment VALUES(3,'Simmer dean','2021-01-22 05:30:00.000000',1,3);
INSERT INTO Comment VALUES(4,'Now this is a meal','2021-01-24 04:30:00.000000',2,2);
INSERT INTO Comment VALUES(5,'He might have you beat @user1','2021-01-24 08:45:00.000000',2,3);
INSERT INTO Comment VALUES(6,'Okay, this IS better','2021-01-24 19:10:00.000000',2,1);
CREATE TABLE IF NOT EXISTS "RecipeIngredient" (
	recipe_id INTEGER NOT NULL, 
	ingredient_id INTEGER NOT NULL, 
	amount FLOAT NOT NULL, 
	units VARCHAR, 
	PRIMARY KEY (recipe_id, ingredient_id), 
	FOREIGN KEY(recipe_id) REFERENCES "Recipe" (id), 
	FOREIGN KEY(ingredient_id) REFERENCES "Ingredient" (id)
);
INSERT INTO RecipeIngredient VALUES(1,1,1.0,'can');
INSERT INTO RecipeIngredient VALUES(1,2,2.0,'Tbsp');
INSERT INTO RecipeIngredient VALUES(2,3,13.999999999999999999,'oz');
INSERT INTO RecipeIngredient VALUES(2,4,1.0,'Tsp');
INSERT INTO RecipeIngredient VALUES(2,5,1.5,'Tsp');
CREATE TABLE IF NOT EXISTS "RecipeStep" (
	id INTEGER NOT NULL, 
	number INTEGER NOT NULL, 
	content VARCHAR NOT NULL, 
	recipe_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(recipe_id) REFERENCES "Recipe" (id)
);
INSERT INTO RecipeStep VALUES(1,1,'Take out the ingredients',1);
INSERT INTO RecipeStep VALUES(2,2,'Cook the ingredients',1);
INSERT INTO RecipeStep VALUES(3,3,'Eat the meal',1);
INSERT INTO RecipeStep VALUES(4,1,'Thaw meat',2);
INSERT INTO RecipeStep VALUES(5,2,'Season meat',2);
INSERT INTO RecipeStep VALUES(6,3,'Cook meat',2);
INSERT INTO RecipeStep VALUES(7,4,'Let sit for 5 minutes, then serve',2);
COMMIT;
