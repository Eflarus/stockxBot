
create table bot_user (
  telegram_id bigint primary key,
  username str default NULL,
  name str default NULL,
  last_name str default NULL,
  role int not null default 0,
  created_at timestamp default current_timestamp not null
);