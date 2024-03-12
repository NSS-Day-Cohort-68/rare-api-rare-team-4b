DELETE FROM Tags;
DROP TABLE IF EXISTS Tags;
--* TABLE CREATION *--
CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);
CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);
CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);
CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
);
CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);
CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);
CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);
CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);
CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);
CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);
--* TABLE POPULATION *--
INSERT INTO Categories ('label')
VALUES ('News');
INSERT INTO Tags ('label')
VALUES ('JavaScript');
INSERT INTO Reactions ('label', 'image_url')
VALUES ('happy', 'https://pngtree.com/so/happy');
--* DISPLAY ALL *--
SELECT *
FROM Users;
SELECT *
FROM DemotionQueue;
SELECT *
FROM Subscriptions;
SELECT *
FROM Posts;
SELECT *
FROM Comments;
SELECT *
FROM Reactions;
SELECT *
FROM PostReactions;
SELECT *
FROM Tags;
SELECT *
FROM PostTags;
SELECT *
FROM Categories;
--? TEST DATA ?--
-- test users
INSERT INTO Users (
    first_name,
    last_name,
    email,
    bio,
    username,
    password,
    profile_image_url,
    created_on,
    active
  )
VALUES (
    'John',
    'Doe',
    'john@example.com',
    'Software Developer',
    'johndoe',
    'password123',
    NULL,
    '2023-04-01',
    1
  );
INSERT INTO Users (
    first_name,
    last_name,
    email,
    bio,
    username,
    password,
    profile_image_url,
    created_on,
    active
  )
VALUES (
    'Jane',
    'Doe',
    'jane@example.com',
    'Data Scientist',
    'janedoe',
    'password456',
    NULL,
    '2023-04-02',
    1
  );
INSERT INTO Users (
    first_name,
    last_name,
    email,
    bio,
    username,
    password,
    profile_image_url,
    created_on,
    active
  )
VALUES (
    'Alice',
    'Smith',
    'alice@example.com',
    'Product Manager',
    'alice',
    'password789',
    NULL,
    '2023-04-03',
    1
  );
-- test comments
INSERT INTO Comments (post_id, author_id, content)
VALUES (1, 1, "I love cats!");
-- test posts
INSERT INTO Posts (
    user_id,
    category_id,
    title,
    publication_date,
    image_url,
    content,
    approved
  )
VALUES (
    1,
    1,
    'First Example Post',
    '2023-04-01 00:00:00',
    'https://jooinn.com/images/beauty-of-nature-24.jpg',
    'Lorem ipsum dolor sit amet consectetur adipiscing elit neque commodo porttitor, iaculis hac nam sagittis auctor duis maecenas in fames, rutrum elementum erat semper torquent varius vel faucibus pharetra. Metus mattis facilisis ridiculus scelerisque lobortis at nisl mollis proin, taciti eleifend tempus cubilia integer justo dui felis convallis, viverra nec habitasse volutpat imperdiet feugiat cursus nulla. Libero magnis est habitant lacinia curae sollicitudin eu enim, leo quis curabitur gravida vulputate dignissim quisque netus platea, hendrerit lacus tortor venenatis dapibus nunc non. Nostra a vivamus ad malesuada parturient conubia mi porta, ligula diam ultrices ac ullamcorper arcu lectus etiam mauris, phasellus potenti magna dictum turpis senectus nascetur. Id odio fringilla suscipit aptent himenaeos, rhoncus laoreet nibh morbi, accumsan bibendum tristique cras.',
    1
  );
INSERT INTO Posts (
    user_id,
    category_id,
    title,
    publication_date,
    image_url,
    content,
    approved
  )
VALUES (
    2,
    1,
    'Second Example Post',
    '2023-04-02 00:00:00',
    null,
    'Lorem ipsum dolor sit amet consectetur adipiscing elit nam maecenas iaculis arcu, phasellus mauris dapibus vehicula nisl mollis porta parturient dis. Semper congue donec sollicitudin pellentesque nulla vitae vestibulum nibh consequat vulputate, mattis posuere sodales tortor ac vel ullamcorper lobortis cras nullam ante, pretium feugiat dignissim inceptos hendrerit magna primis luctus a. Quis bibendum cursus molestie et neque vivamus felis auctor convallis, eget habitasse sapien torquent dui porttitor turpis conubia augue interdum, ornare ultrices venenatis ridiculus mus diam malesuada odio. Aenean eu praesent magnis montes nunc lacus pulvinar eleifend netus aliquet, proin class quisque aptent penatibus fusce duis blandit velit, ultricies suscipit sociis morbi litora tellus dictumst massa non. Tristique id habitant varius sem tempor scelerisque, gravida curae curabitur facilisi.',
    1
  );
INSERT INTO Posts (
    user_id,
    category_id,
    title,
    publication_date,
    image_url,
    content,
    approved
  )
VALUES (
    3,
    1,
    'Third Example Post',
    '2023-04-03 00:00:00',
    'https://www.pixelstalk.net/wp-content/uploads/2016/07/Wallpapers-pexels-photo.jpg',
    'Lorem ipsum dolor sit amet consectetur adipiscing elit leo, et inceptos eget mus cum rutrum potenti, praesent libero tortor morbi condimentum tempor ullamcorper. Placerat semper facilisi netus nascetur tellus sapien habitasse magna natoque, sodales odio arcu velit hac elementum porttitor mattis magnis, mi gravida viverra quis per mollis nullam luctus. Faucibus massa erat posuere quisque varius ornare lobortis nisi, nunc vivamus penatibus sollicitudin sociosqu pellentesque ligula felis, dapibus conubia purus justo torquent egestas convallis. Imperdiet nibh nostra integer molestie feugiat duis diam accumsan phasellus ante class, auctor ad rhoncus nam bibendum orci donec facilisis urna pulvinar. Eleifend dis fermentum parturient pretium vestibulum augue euismod nec, consequat vulputate habitant eu curae suscipit vitae venenatis, eros risus at sagittis ridiculus congue himenaeos.',
    1
  );
INSERT INTO `Tags`
VALUES (null, "Python")
INSERT INTO `Tags`
VALUES (null, "C#")
INSERT INTO `Tags`
VALUES (null, "Django")
INSERT INTO `Tags`
VALUES (null, "Computer Failure")
INSERT INTO Users (
    first_name,
    last_name,
    email,
    bio,
    username,
    password,
    profile_image_url,
    created_on,
    active
  )
VALUES (
    'John',
    'Doe',
    'john.doe@example.com',
    'Software Developer',
    'johndoe',
    'password123',
    'https://example.com/johndoe.jpg',
    '2023-04-01',
    1
  );
INSERT INTO Users (
    first_name,
    last_name,
    email,
    bio,
    username,
    password,
    profile_image_url,
    created_on,
    active
  )
VALUES (
    'Jane',
    'Doe',
    'jane.doe@example.com',
    'Data Scientist',
    'janedoe',
    'password456',
    'https://example.com/janedoe.jpg',
    '2023-04-02',
    1
  );
INSERT INTO Users (
    first_name,
    last_name,
    email,
    bio,
    username,
    password,
    profile_image_url,
    created_on,
    active
  )
VALUES (
    'Alice',
    'Smith',
    'alice.smith@example.com',
    'Product Manager',
    'alicesmith',
    'password789',
    'https://example.com/alicesmith.jpg',
    '2023-04-03',
    1
  );