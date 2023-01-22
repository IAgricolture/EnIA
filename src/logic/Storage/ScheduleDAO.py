from src.dbConnection import schedule
from src.logic.model.Schedule import Schedule
from flask import jsonify
from datetime import date, timedelta
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

    def creaSettimanaScheduleNullo(id_terreno: str):
        """
            Questo metodo istanzia una settimana di schedule vuota sul database
        """
        #get today
        today = datetime.now()
        
        #Creo un dizionario con la settimana di schedule vuota
        settimanaSchedule = {
            
        }

        settimanaSchedule = []
        #crea un array di dizionari in cui in ogni dizionario avanzi di un giorno per tutta la settimana
        for i in range(0, 7):
            settimanaSchedule.append({
                "inizio": today,
                "fine": today,
                "modalita": "Nessuno",
                "terreno": ObjectId(id_terreno)
            })
            today = today + timedelta(days=1)
        
        #Inserisco la settimana di schedule vuota sul database
        result = schedule.insert_many(settimanaSchedule)

        return True

    def creaSchedule(sched: Schedule) -> str:
        """
            Questo metodo instanzia un schedule sul database
        """

        result = schedule.insert_one({
            "inizio": sched.inizio,
            "fine": sched.fine,
            "modalita": sched.modalita
        })

        return str(result.inserted_id)
    
    def getWeeklySchedule(id_terreno: str) -> list:
        """
            Questo metodo ritorna la settimana di schedule di un terreno
        """
        #get today
        today = datetime.now()
        #get isoformat of today
        print(today)
        #elimina gli schedule che sono passati
        schedule.delete_many({
            "terreno": ObjectId(id_terreno),
            "inizio": {"$lt": today},
        })
        
        #get schedules from db where date is greater or less than today
        schedules = list(schedule.find({
            "terreno": ObjectId(id_terreno),
            "inizio": {"$gte": today},
        }).sort("inizio", 1))
        
        if(len(schedules) == 0):
            ScheduleDAO.creaSettimanaScheduleNullo(id_terreno)
            schedules = list(schedule.find({
                "terreno": ObjectId(id_terreno),
                "inizio": {"$gte": today},
            }).sort("inizio", 1))
        
        #se ci sono meno di 7 schedule, istanzia i mancanti sul database
        if len(schedules) < 7:
            #prendi lo schedule più nuovo da schedules
            lastSchedule = schedules[len(schedules) - 1]
            #prendi la data di inizio dello schedule più nuovo
            lastDate = lastSchedule["inizio"]
            #istanzia 7 - len(schedules) schedule vuoti sul database
            for i in range(0, 7 - len(schedules)):
                lastDate = lastDate + timedelta(days=1)
                schedule.insert_one({
                    "inizio": lastDate,
                    "fine": lastDate,
                    "modalita": "nessuno",
                    "terreno": ObjectId(id_terreno)
                })
                
            schedules = list(schedule.find({
            "terreno": ObjectId(id_terreno),
            "inizio": {"$gte": today},
            }).sort("inizio", 1))
        
        
        #format every date in schedule to dd-mm-yyyy
        for sched in schedules:
            sched["inizio"] = sched["inizio"].strftime("%d-%m-%Y")
            sched["fine"] = sched["fine"].strftime("%d-%m-%Y")
        
        return schedules
    
    def modificaLivelloSchedule(id_terreno: str, date: str, modalita: str):
        """
            Questo metodo modifica la modalità di un schedule
        """
        #parse to datetime date
        date = datetime.strptime(date, "%d-%m-%Y")
        
        #get tomorrow
        tomorrow = date + timedelta(days=1)
        #modifica la modalita dello schedule nel database sulla entry che ha id_terreno e date uguali a quelle passate
        schedule.update_one({
            "terreno": ObjectId(id_terreno),
            "inizio": {"$gte": date, "$lt": tomorrow}
        }, { "$set": { "modalita": modalita } })
        
        print(schedule.find_one({
            "terreno": ObjectId(id_terreno),
            "inizio": {"$gte": date, "$lt": tomorrow}}
        ))
        
        return True
        


