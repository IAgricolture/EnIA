from src.dbConnection import schedule
from src.logic.model.Schedule import Schedule
from flask import jsonify
from datetime import date
from datetime import datetime
from bson.objectid import ObjectId

class ScheduleDAO():

    def findSchedule(id: str) -> Schedule:
        """
            Questo metodo trova un Schedule sul database, usando il suo ObjectId
            :return: Schedule
        """
        trovato = schedule.find_one({"_id": ObjectId(id)})
        
        id = str(trovato.get("_id"))
        inizio = trovato.get("inizio").time()
        fine = trovato.get("fine").time()
        modalita = str(trovato.get("modalita"))

        scheduleTrovato = Schedule(id, inizio, fine, modalita)
        
        return scheduleTrovato

    def creaSchedule(sched: Schedule) -> str:
        """
            Questo metodo instanzia un schedule sul database
        """
        data = date.min

        result = schedule.insert_one({
            "inizio": datetime.combine(data, sched.inizio),
            "fine": datetime.combine(data, sched.fine),
            "modalita": sched.modalita
        })

        return str(result.inserted_id)

        

