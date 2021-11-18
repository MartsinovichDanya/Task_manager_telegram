from Models import ReportModel
from DB import DB


def init_rep_db():
    db = DB('reports.db')

    rm = ReportModel(db.get_connection())
    rm.init_table()


init_rep_db()
