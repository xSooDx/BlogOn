
CREATE TABLE 'categories' (
  'name' varchar(30) NOT NULL,
  'parent' varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE 'comments' (
  'commentid' int(11) NOT NULL,
  'postid' int(11) NOT NULL,
  'email' varchar(50) NOT NULL,
  'name' varchar(50) NOT NULL,
  'comment' varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE 'pages' (
  'pageid' int(11) NOT NULL,
  'title' varchar(60) NOT NULL,
  'content' text NOT NULL,
  'description' varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE 'posts' (
  'postid' int(11) NOT NULL,
  'userid' int(11) NOT NULL,
  'title' varchar(60) NOT NULL,
  'content' text NOT NULL,
  'description' varchar(250) DEFAULT NULL,
  'creation_date' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  'modified_date' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  'tags' varchar(250) DEFAULT NULL,
  'type' int(3) NOT NULL DEFAULT '0',
  'pulblished' tinyint(1) NOT NULL DEFAULT '0',
  'img' varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE 'post_category' (
  'postid' int(11) NOT NULL,
  'category' varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE 'settings' (
  'setting' varchar(60) NOT NULL,
  'value' varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE 'users' (
  'userid' int(11) NOT NULL,
  'username' varchar(50) NOT NULL,
  'email' varchar(50) NOT NULL,
  'passwordhash' varchar(100) NOT NULL,
  'token' varchar(64) NOT NULL,
  'join_date' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  'last_login' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  'settings' varchar(32500) DEFAULT NULL,
  'rank' int(3) NOT NULL DEFAULT '-1'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE 'categories'
  ADD PRIMARY KEY ('name'),
  ADD UNIQUE KEY 'name' ('name'),
  ADD KEY 'parent' ('parent');

ALTER TABLE 'comments'
  ADD PRIMARY KEY ('commentid'),
  ADD KEY 'postid' ('postid');

ALTER TABLE 'pages'
  ADD PRIMARY KEY ('pageid'),
  ADD UNIQUE KEY 'title' ('title');

ALTER TABLE 'posts'
  ADD PRIMARY KEY ('postid'),
  ADD KEY 'uid' ('userid');

ALTER TABLE 'post_category'
  ADD PRIMARY KEY ('category','postid'),
  ADD KEY 'postid' ('postid');

ALTER TABLE 'settings'
  ADD PRIMARY KEY ('setting');

ALTER TABLE 'users'
  ADD PRIMARY KEY ('userid'),
  ADD UNIQUE KEY 'username' ('username'),
  ADD UNIQUE KEY 'email' ('email');

ALTER TABLE 'comments'
  MODIFY 'commentid' int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE 'pages'
  MODIFY 'pageid' int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE 'posts'
  MODIFY 'postid' int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

ALTER TABLE 'users'
  MODIFY 'userid' int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

ALTER TABLE 'categories'
  ADD CONSTRAINT 'categories_ibfk_1' FOREIGN KEY ('parent') REFERENCES 'categories' ('name');

ALTER TABLE 'comments'
  ADD CONSTRAINT 'comments_ibfk_1' FOREIGN KEY ('postid') REFERENCES 'posts' ('postid');

ALTER TABLE 'posts'
  ADD CONSTRAINT 'post_author' FOREIGN KEY ('userid') REFERENCES 'users' ('userid');

ALTER TABLE 'post_category'
  ADD CONSTRAINT 'post_category_ibfk_1' FOREIGN KEY ('postid') REFERENCES 'posts' ('postid'),
  ADD CONSTRAINT 'post_category_ibfk_2' FOREIGN KEY ('category') REFERENCES 'categories' ('name');
