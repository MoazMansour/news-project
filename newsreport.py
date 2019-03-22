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
################# News Report Analytics tool #################
##############################################################

import psycopg2
import textwrap

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
    # Create a author_views view table that holds the number of views per author id
    c.execute('''
        create or replace view author_views as
        select author, sum(views) as sum
            from articles as a, ranked_views as v
            where a.slug = v.slug
            group by author
            order by sum desc;
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


def write_report(
            mostPop,popAuth):
    f = open("report.txt","w+")
    header = '''
                News Analytics Report
                --------------------------\n
                1. Most popular three articles of all time:\n
            '''
    f.write(textwrap.dedent(header))
    for article in mostPop:
        f.write('- "{0}" -- {1} views \n'.format(article[0],article[1]))
    auth_divider = '''
                --------------------------\n
                2. Most popular article authors of all time:\n
            '''
    f.write(textwrap.dedent(auth_divider))
    for author in popAuth:
        f.write('- "{0}" -- {1} views \n'.format(author[0],author[1]))
    f.close()

create_views()
write_report(most_popular(),pop_author())
