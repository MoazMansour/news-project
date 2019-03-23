-- Create a ranked_views view table that ranks articles by number of views

create or replace view ranked_views as
select substring(path,position('e/' IN path)+2) as slug,
       count(*) as views
    from log
    where status = '200 OK'
    and path != '/'
    group by slug
    order by views desc;

-- Create a author_views view table that holds the
-- number of views per author id

create or replace view author_views as
select author, sum(views) as sum
    from articles as a, ranked_views as v
    where a.slug = v.slug
    group by author
    order by sum desc;

-- Create a total_req view table that holds
-- the total number of requests per day

create or replace view total_req as
select cast(time as date) as date, count(*) as total_req
    from log
    group by date;

-- Create a error_req view table that holds
-- the failed number of requests per day

create or replace view error_req as
select cast(time as date) as date, count(*) as error_req
    from log
    where status != '200 OK'
    group by date;
