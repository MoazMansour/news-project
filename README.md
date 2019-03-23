# FSND Project1: News Analytics Report

AUTHOR: Moaz Mansour

This project is build using python 3.7 in integration with PostgreSQL
as part of Udacity's Full stack development nanodegree

The purpose of this code is to analyze a news sql database to answer
3 main questions
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

The program was created to answer the 3 main questions all included
in one python code file which takes advantage if
1. Python PostgreSQL DB-API
2. SQL views
3. Different types of SQL table joins
4. SQL table aggregations
5. SQL subselect

## Logic and Functions: ##

The program mainly run on 5 main functions

__1. create_views:__

        * For accessibility and scalability reason this functions was
          included in the code to make views creation in the database easier.
        * It is also easier for the instructors to only run the
          python code to get the results.
        * In other words it is safe to share and consistent

__2.write_report:__

        * The code output comes in the form of a text file.
        * This function takes care of this job by calling the three
          other functions to run the required analytics and getting
          their results

__3.most_popular:__

        * This function takes care of answering the first question
          "What are the most popular three articles of all time?"
        * It does that by joining articles original table with the
          ranked_views special view.
        * The view counts the number of views per article and
          extracts the article slug from the path record in the log table.
        * Both tables then join on the slug to display the article name
          and number of views

__4.pop_author:__

        * This function takes care of answering the second question
          "Who are the most popular article authors of all time?"
        * It does that by joining the author table to newly created
          author_views view.
        * The author_views view takes advantage of the ranked_views view
          as it joins it with the articles table the same way the
          most_popular function work but this time to get the author id
          instead of the article title
        * The author table and the author view then join on the author id to
          display the author name with the total number of views per author

__5.error_per:__

        * This function takes care of answering the last question
          "On which days did more than 1% of requests lead to errors?"
        * It does that by applying the percentage condition through
          a subselect from a select table that calculates the percentage
          of error per day
        * The percentage table noted as err is a result of joining two
          newly created views
          * error_req: which aggregates the number of unsuccessful
            requests by day from the log table
          * total_req: which counts the total number of requests per
            day from the log table

## Special modules usage ##

Cast was used with some sql views and select statements as follows:

__1.ranked_views view:__ 
       
       Substring was used here to extract the slug part from the path record

__2.total_req view:__ 
       
       The aggregation was needed on day level. Hence, cast was used to convert datetime record types to date

__3.error_req view:__ 
       
       Cast was used for the same purpose as total_req

__4.pop_author fn:__ 
       
       Cast was used to convert the sum aggregation to int instead of long for python 2.7 compatibility

__5.error_per fn:__ 
       
       Cast was used to convert int count values to float to enable division and getting percentage
       
__6.write_report:__ 
       
       Textwrap was used to eliminate extra tabs from the output to the text file strftim was used from the datetime module
       for the formatting target as well

## Appendix ##
Attached below the SQL view code used if needed

`       -- ranked_views view     
        create or replace view ranked_views as
        select substring(path,position('e/' IN path)+2) as slug,
               count(*) as views
            from log
            where status = '200 OK'
            and path != '/'
            group by slug
            order by views desc;

       -- author_view view
       create or replace view author_views as
       select author, sum(views) as sum
            from articles as a, ranked_views as v
            where a.slug = v.slug
            group by author
            order by sum desc;
            
      -- total_req view      
       create or replace view total_req as
       select cast(time as date) as date, count(*) as total_req
            from log
            group by date;

        -- error_req view
       create or replace view error_req as
       select cast(time as date) as date, count(*) as error_req
            from log
            where status != '200 OK'
            group by date;
