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

def most_popular():
    db = psycopg2.connect("dbname = news")
    c = db.cursor()
    c.execute('''
        select path, count(*) as views
        from log
        where status = '200 OK'
        and path != '/'
        group by path
        order by views desc
        limit 3''')
    results = c.fetchall()
    db.close()
    return results


print(most_popular())
