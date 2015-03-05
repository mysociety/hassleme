--
-- schema.sql:
-- Hassle schema.
--
-- Copyright (c) 2005 Chris Lightfoot. All rights reserved.
-- Email: chris@ex-parrot.com; WWW: http://www.ex-parrot.com/~chris/
--

create table secret (
    id integer not null default(0) check(id = 0),
    secret text not null
);

create table hassle (
    id serial not null primary key,
    frequency integer not null,
    what text not null,
    whencreated timestamp not null default(current_timestamp),
    public boolean not null default(false),
    ipaddr text -- IP address of client creating hassle
);

create table recipient (
    id serial not null primary key,
    hassle_id integer not null references hassle(id),
    email text not null,
    confirmed boolean not null default(false),
    deleted boolean not null default(false)
);

create table hassle_sent (
    hassle_id integer not null references hassle(id),
    recipient_id integer not null references recipient(id),
    whensent timestamp not null default(current_timestamp)
);

create table no_send_list (
    email text not null
);

create table tc (
    id serial not null primary key,
    email text not null,
    action text not null,
    created timestamp not null default(current_timestamp)
);
