import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

#-------------------------------------------------------------------------------------------------
#-----------DATABASE DEFINITION------------------------------------------------------
#-------------------------------------------------------------------------------------------------

Base = declarative_base()

class Plants(Base): #parent - one type of plant can be in several pots
    __tablename__ = 'plants_tbl'
    id_number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    foto = db.Column(db.String, nullable=True)
    pypots = relationship('PyPots', backref=backref('plant'))

class PyPots(Base): #child - one pot has one plant
    __tablename__ = 'pots_tbl'
    id_number = db.Column(db.Integer, primary_key=True) 
    location = db.Column(db.String)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants_tbl.id_number'), nullable=True) #the pot can be empty
    status = relationship('Status', uselist=False, backref=backref('pot'), cascade='all, delete')

class Status(Base): #child - one pot has one status
    __tablename__ = 'status'
    id_number = db.Column(db.Integer, primary_key=True)
    pot_id = db.Column(db.Integer, db.ForeignKey('pots_tbl.id_number'))
    vwc = db.Column(db.Float)
    ph = db.Column(db.Float)
    sal = db.Column(db.Float)
    lux = db.Column(db.Float)

class DBHandler():
    def __init__(self):   
        self.db_engine = db.create_engine("sqlite:///PyFloraPots/pot_plant_database.db")
        Base.metadata.create_all(self.db_engine)
        Session = sessionmaker()
        Session.configure(bind=self.db_engine)
        self.session = Session()

#-------------------------------------------------------------------------------------------------
#------------SENSORS AND STATUS MANIPULATION--------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
    
    def plant_care_status(self, vwc, ph, sal, lux):
        if vwc < 20:
            status_vwc = 'Dry soil!'
        elif vwc < 50:
            status_vwc = 'Soil moisture ok!'
        elif vwc > 50:
            status_vwc = 'Moist soil!'
        if ph <= 5.5:
            status_ph = 'Soil is acidic!'
        elif ph <= 8:
            status_ph = 'Ok, soil is neutral!'
        elif ph > 8:
            status_ph = 'Soil is alkaline!'
        if sal < 4:
            status_sal = 'Ok, soil is very slightly salty!'
        elif sal < 8:
            status_sal = 'Ok, soil is slightly salty!'
        elif sal < 16:
            status_sal = 'Soil is moderately salty!'
        else:
            status_sal = 'Soil is highly salty!'
        if lux < 10:
            status_lux = 'Plant is in darkness!'
        elif lux < 200:
            status_lux = 'Plant is in shade!'
        elif lux < 500:
            status_lux = 'Plant is in low light!'
        elif lux < 800:
            status_lux = 'Ok, plant is in moderate light!'
        else:
            status_lux = 'Plant is in bright light!'
        return list((status_vwc, status_ph, status_sal, status_lux))
    
    def read_status_tbl(self):
        return self.session.query(Status).all()
    
    def read_status_values(self, pot_id): #read status by id number of a pot
        values = self.session.query(Status).filter(Status.pot_id == pot_id).one_or_none()
        if values is not None:
            return round(values.vwc), float(f'{values.ph:.2f}'), round(values.sal), round(values.lux) # type: ignore
    
    def read_status_row(self, pot_id): #read status by id number of a pot
        return self.session.query(Status).filter(Status.pot_id == pot_id).one_or_none()

    def update_sensor_data(self, pot_id):
        global pot_id_to_update
        self.pot_id_to_update = pot_id

    def store_sync_data(self, pot_id):
        from sensors import Sensor
        self.sns = Sensor()
        pot_status = self.read_status_row(pot_id)
        vwc,ph,sal,lux = self.sns.read_sensors(pot_id)
        if pot_status is not None:
            pot_status.vwc, pot_status.ph, pot_status.sal, pot_status.lux = vwc, ph, sal, lux # type: ignore
            self.session.add(pot_status)
        else:
            new_status = Status(pot_id=pot_id, vwc=vwc, ph=ph, sal=sal, lux=lux)
            self.session.add(new_status)
            self.update_sensor_data(pot_id)
        self.session.commit()
        print(f'PyPot ID {pot_id} successfuly updated!')
        return 

    def store_sync_data_all(self):
        pots_to_sync = self.session.query(PyPots)
        for pot in pots_to_sync:
            self.store_sync_data(pot.id_number)
        print(f'PyPots successfuly updated!')

    def fill_status_tbl(self):
        pots = self.session.query(PyPots)
        for pot in pots:
            vwc,ph,sal,lux = self.sns.read_sensors(pot.id_number)
            status = Status(vwc=vwc, ph=ph, sal=sal, lux=lux)
            pot.status = status
            self.session.add(status)
            self.session.commit()
        print('Status table filled')

#-------------------------------------------------------------------------------------------------
#------------PLANTS MANIPULATION--------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
    
    #   CRUD operacije 
    def create_plant(self, name, foto):
        plant_duplicate = self.session.query(Plants).filter(Plants.name == name).one_or_none()
        if plant_duplicate is not None:
            print(f'Plant {name} already exists!')
            return
        if plant_duplicate is None:           
            new_plant = Plants(name=name, foto=foto)
            self.session.add(new_plant)
            self.session.commit()
        print(f'Plant {name} created!')
    
    def read_plant(self, id_number):
        return self.session.query(Plants).filter(Plants.id_number == id_number).one_or_none()

    def read_plant_tbl(self):
        return self.session.query(Plants).all()

    def update_plant(self, id_number, name, foto):
        plant_to_update = self.session.query(Plants).filter(Plants.id_number == id_number).one_or_none()
        if plant_to_update is not None:
            plant_to_update.name = name
            plant_to_update.foto = foto
            self.session.add(plant_to_update)
            self.session.commit()
            print(f'Plant ID {id_number} successfuly updated!')
        else:
            return
        
    def update_foto_path(self, id_number, foto_path):
        pot_to_update = (
            self.session.query(PyPots)
            .filter(PyPots.id_number == id_number)
            .one_or_none()
            )
        if pot_to_update is not None:
            pot_to_update.plant.foto = foto_path
            self.session.add(pot_to_update)
            self.session.commit()
            print(f'Successfully changed photo for pot ID {id_number}!')
        else:
            return

    def delete_plant(self, id_number):
        plant_to_delete = self.session.query(Plants).filter(Plants.id_number == id_number).one_or_none()
        if plant_to_delete is None:
            print(f'Plant ID {id_number} does not exist!')
            return
        if plant_to_delete is not None:
            self.session.delete(plant_to_delete)
            self.session.commit()
            print(f'Plant ID {id_number} deleted!')       

    #   Manipulation with plant table
    
    def fill_plant_tbl(self):
        plants = [
            ['Aspidistra elatior'],
            ['Begonia maculata'],
            ['Chamaedorea elegans'],
            ['Chlorophytum'],
            ['Crassula ovata'],
            ['Ficus lyrata'],
            ['Monstera delicosa'],
            ['Philodendron scandens'],
            ['Spathiphyllum'],
            ['Microsorum diversifolum']
        ]
        for plant in plants:
            plant_image_path = f'PyFloraPots/foto/{plant[0]}.jpeg'
            self.create_plant(name=plant[0], foto=plant_image_path)
        print('Plant table populated!')

    def empty_plant_tbl(self):
        id_number = 0
        count = self.session.query(Plants).count()
        id_number = count
        while id_number != 0:    
            self.delete_plant(id_number)
            id_number -= 1
        print('Plant table emptied!')

#-------------------------------------------------------------------------------------------------
#------------POT MANIPULATIONS--------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
    
    def create_pot(self, location=None):
        new_pot = PyPots(location=location) #default - pot is empty and does not contain plant
        self.session.add(new_pot)
        self.session.commit()
    
    def read_pot(self, id_number):
        return self.session.query(PyPots).filter(PyPots.id_number == id_number).one_or_none()
    
    def find_plant_id_by_name(self, name):
        return self.session.query(Plants.id_number).filter(Plants.name == name).one_or_none()
    
    def update_pot(self, id_number, plant_id, location):
        pot_to_update = self.session.query(PyPots).filter(PyPots.id_number == id_number).one_or_none()
        if pot_to_update is not None:
            pot_to_update.location = location
            pot_to_update.plant_id = plant_id
            self.session.add(pot_to_update)
            self.store_sync_data(id_number)
            self.session.commit()
            print(f'PyPot ID {id_number} successfuly updated!')
        else:
            return

    def delete_pot(self, id_number):
        pot_to_delete = self.session.query(PyPots).filter(PyPots.id_number == id_number).one_or_none()
        if pot_to_delete is None:
            print(f'PyPot ID {id_number} does not exist!')
            return
        if pot_to_delete is not None:
            self.session.delete(pot_to_delete)
            self.session.commit()
            print(f'PyPot ID {id_number} deleted!')

    def empty_pot(self, id_number):
        pot_to_empty = self.session.query(PyPots).filter(PyPots.id_number == id_number).one_or_none()
        if pot_to_empty is not None:
            pot_to_empty.plant_id = None # type: ignore
            self.session.delete(pot_to_empty.status)
            self.session.commit()
            print(f'PyPot ID {id_number} emptied!')
        else:
            print(f'PyPot ID {id_number} does not exist!')
            return
    
    def plant_pot(self, id_number, plant_id):
        pot_to_plant = self.session.query(PyPots).filter(PyPots.id_number == id_number).one_or_none()
        pot_to_plant.plant_id = plant_id # type: ignore
        self.store_sync_data(id_number)
        self.session.add(pot_to_plant)
        self.session.commit()

    #   Pot table manipulations
    def read_pot_tbl(self):
        return self.session.query(PyPots).all()
    
    def empty_pot_tbl(self):
        count = self.session.query(PyPots).count()
        id_number = count
        while id_number != 0:    
            self.delete_pot(id_number)
            id_number -= 1
        print('Tablica posude ispražnjena!')

    def fill_pot_tbl(self):
        locations = [
            'Kitchen - window outside',
            'Kitchen - window inside',
            'Sleeping room - desk',
            'Living room - window inside',
            'Living room - coffee table'
        ]
        for location_to_write in locations:
            self.create_pot(location_to_write)
        print('Pots table populated!')

    def plant_plants(self):
        plant_id_to_plant = [1,2,2,5,10]
        pot_tbl = self.session.query(PyPots)
        for pot_row in pot_tbl:
            i = pot_row.id_number
            pot_row.plant_id = plant_id_to_plant[i-1]
            self.session.add(pot_row)
        self.session.commit()
        print('Plants potted!')

#-------------------------------------------------------------------------------------------------
#----------------TESTING-----------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
    
pydb = DBHandler()

#   Sensor/status handling
#pydb.fill_status_tbl()
# vwc,ph,sal,lux = pydb.read_status_by_pot_id(6)
# status_list = pydb.plant_care_status(vwc,ph,sal,lux)
# print(status_list)
#pydb.store_sync_data(5)
#pydb.store_sync_data_all()
#print(pydb.read_status_by_pot_id(1))

#pydb.record_sensor_data()

#   Plant handling
#pydb.fill_plant_tbl()
#pydb.read_plant_tbl()
#pydb.create_plant(name='Spathiphyllum', foto='foto')
#pydb.empty_plant_tbl()
#pydb.create_plant(name='new_plant', foto='new_foto')
#pydb.update_plant(11, 'new_name_of_new_plant', 'new_foto')
#pydb.delete_plant(id_number=10)
#pydb.empty_plant_tbl()

#   Pot handling
#pydb.fill_pot_tbl()
#pydb.plant_plants()
#pydb.update_pot(id_number=9, plant_id=3, location='Garage')
#pydb.update_pot(id_number=6, plant_id=4)
#pydb.delete_pot(id_number=10)
#pydb.read_pot_tbl()
#pydb.empty_pot_tbl()
#print(pydb.find_foto_path(5))
#print(pydb.find_plant_name(5))
#pydb.update_foto_path(7,'PyFloraPots/foto/test_foto.jpeg')

#   Pot creating, planting and updating
#pydb.create_pot(location='Cellar')
#pydb.plant_pot(id_number=6, plant_id=4)
#pydb.empty_pot(6)
#pydb.delete_pot(6)

#   Populate table
#pydb.fill_plant_tbl()
#pydb.fill_pot_tbl()
#pydb.plant_plants()
#pydb.store_sync_data_all()