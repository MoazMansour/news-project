###############################################################################
# NAME:      newsreport.py
# AUTHOR:    Moaz Mansour
# E-MAIL:	 moaz.mansour@gmail.com
# DATE:      03/20/2019
# LANG:		 Python 3.7
#
# This python program runs an analytics report on a news database
# part of udacity Full Stack Nano degree
#
# VERSION HISTORY:
# 1.0    03/20/2019		Initial Version
###############################################################################

##############################################################
# ---------------- News Report Analytics tool ----------------
##############################################################

import psycopg2
import textwrap
import datetime


def create_views():
    db = psycopg2.connect("dbname = news")
    c = db.cursor()
    # Create a ranked_views view table that ranks articles by number of views
    # and turns the path col into a slug col
    c.execute('''
        create or replace view ranked_views as
        select substring(path,position('e/' IN path)+2) as slug,
               count(*) as views
            from log
            where status = '200 OK'
            and path != '/'
            group by slug
            order by views desc;
            ''')
    # Create a author_views view table that holds the
    #  number of views per author id
    c.execute('''
        create or replace view author_views as
        select author, sum(views) as sum
            from articles as a, ranked_views as v
            where a.slug = v.slug
            group by author
            order by sum desc;
            ''')
    # Create a total_req view table that holds
    # the total number of requests per day
    c.execute('''
        create or replace view total_req as
        select cast(time as date) as date, count(*) as total_req
            from log
            group by date;
            ''')
    # Create a error_req view table that holds
    # the failed number of requests per day
    c.execute('''
        create or replace view error_req as
        select cast(time as date) as date, count(*) as error_req
            from log
            where status != '200 OK'
            group by date;
            ''')
    db.commit()
    db.close()


def most_popular():
    db = psycopg2.connect("dbname = news")
    c = db.cursor()
    c.execute('''
        select a.title, v.views
            from ranked_views as v JOIN articles as a
            on a.slug = v.slug
            limit 3
            ''')
    results = c.fetchall()
    db.close()
    return results


def pop_author():
    db = psycopg2.connect("dbname = news")
    c = db.cursor()
    c.execute('''
        select a.name, cast(v.sum as bigint)
            from author_views as v JOIN authors as a
            on v.author = a.id
            ''')
    results = c.fetchall()
    db.close()
    return results


def error_per():
    db = psycopg2.connect("dbname = news")
    c = db.cursor()
    c.execute('''
        select date, percent
            from (
                select t.date,
                cast((cast (error_req as float)
                / cast (total_req as float))
                * 100 as decimal(2,1)) as percent
                    from error_req as e JOIN total_req as t
                    on t.date = e.date) AS err
            where percent > 1;
            ''')
    results = c.fetchall()
    db.close()
    return results


def write_report(
            mostPop, popAuth,
            errPer):
    f = open("report.txt", "w+")
    # Add header to the report
    header = '''
                News Analytics Report
                --------------------------\n
                1. Most popular three articles of all time:\n
            '''
    f.write(textwrap.dedent(header))
    # Add the most popular list
    for article in mostPop:
        f.write('- "{0}" -- {1} views \n'.format(article[0], article[1]))
    # Add a divider for the popular authors
    auth_divider = '''
                --------------------------\n
                2. Most popular article authors of all time:\n
            '''
    f.write(textwrap.dedent(auth_divider))
    # Add a list of the authors
    for author in popAuth:
        f.write('- {0} -- {1} views \n'.format(author[0], author[1]))
    # Add a divider for the error report
    err_divider = '''
                --------------------------\n
                3. Days when more than 1% of requests lead to errors:\n
            '''
    f.write(textwrap.dedent(err_divider))
    # Add a list of the error days
    for day in errPer:
        f.write('- {0} -- {1}% errors \n'.format(
                day[0].strftime("%B %d, %Y"), day[1]))
    f.close()


create_views()
write_report(
        most_popular(), pop_author(),
        error_per())
