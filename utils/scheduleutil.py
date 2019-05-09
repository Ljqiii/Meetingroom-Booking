from Model import Schedule, db


def remove(id,userid):
    try:
        s = Schedule.query.filter_by(id=id).filter_by(user_id=userid).first()
        db.session.delete(s)
        db.session.commit()
        return True
    except:
        return False


