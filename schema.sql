drop table if exists emotions;
create table emotions (
  emotion_id integer primary key autoincrement,
  description text not null,
  dimention_0 REAL not null,
  dimention_1 REAL not null,
  dimention_2 REAL not null
);

drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  word text not null,
  emotion_id INTEGER,
  power REAL not NULL,
  FOREIGN KEY(emotion_id) REFERENCES emotions(emotion_id)
);