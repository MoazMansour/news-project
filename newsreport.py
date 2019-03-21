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

def create_views():
    db = psycopg2.connect("dbname = news")
    c = db.cursor()
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
    db.commit()
    db.close()


def most_popular():
    db = psycopg2.connect("dbname = news")
    c = db.cursor()
    c.execute('''
        select substring(path,position('e/' IN path)+2) as slug, count(*) as views
        from log
        where status = '200 OK'
        and path != '/'
        group by slug
        order by views desc
        limit 3''')
    results = c.fetchall()
    db.close()
    return results

create_views()
print(most_popular())
